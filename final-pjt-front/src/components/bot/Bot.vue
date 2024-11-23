<template>
  <div id="app">
    <h1>살말 개구리봇</h1>
    <div class="chat-container">
      <!-- Chat messages -->
      <div class="chat-box">
        <div
          v-for="(message, index) in messages"
          :key="index"
          :class="['message', message.sender]"
        >
          <p>{{ message.text }}</p>
        </div>
      </div>

      <!-- User input -->
      <div class="input-box">
        <input
          v-model="userInput"
          type="text"
          placeholder="메시지를 입력하세요..."
          @keyup.enter="handleUserInput"
        />
        <button @click="handleUserInput">전송</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

// Chat messages array
const messages = ref([
  { sender: "bot", text: "안녕하세요! 당신의 금융 친구 머니또입니다!" },
  {
    sender: "bot",
    text: "오늘의 금전운 보기를 원하시면 1번, 물건 구매 결정에 대한 도움이 필요하시면 2번을 입력해주세요!",
  },
]);

// User input state
const userInput = ref("");

// State to manage the current flow
const state = ref(null);

// Handle user input
const handleUserInput = async () => {
  if (!userInput.value.trim()) return;

  // Add user's message to the chat
  messages.value.push({ sender: "user", text: userInput.value });

  const input = userInput.value.trim();
  userInput.value = ""; // Clear input field

  // Initial selection logic
  if (!state.value) {
    if (input === "1") {
      state.value = "fortune";
      messages.value.push({
        sender: "bot",
        text: "잠시만 기다려 주세요! 오늘의 금전운을 확인 중입니다...",
      });
      await fetchFortune();
    } else if (input === "2") {
      state.value = "purchase";
      messages.value.push({
        sender: "bot",
        text: "구매하려는 물건 이름을 입력해주세요!",
      });
    } else {
      messages.value.push({
        sender: "bot",
        text: "잘못된 입력입니다. 1번 또는 2번을 입력해주세요!",
      });
    }
    return;
  }

  // Reset logic for starting over
  if (input.toLowerCase() === "처음") {
    reset();
    return;
  }

  // Handle purchase decision flow
  if (state.value === "purchase") {
    handlePurchaseFlow(input);
    return;
  }
};

// Fetch dynamic fortune using GPT
const fetchFortune = async () => {
  const prompt = `
    당신은 금전운 전문가입니다. 사용자를 위해 오늘의 금전운을 작성해주세요.
    - 유머러스하고 친근한 말투를 사용하세요.
    - 사용자가 웃으면서도 오늘 하루를 긍정적으로 시작할 수 있도록 도와주세요.
    - 금전 관련 조언과 함께 운세를 재미있게 작성해주세요.
    
    예시:
    - 오늘은 작은 사치가 괜찮습니다! 하지만 큰 지출은 피하세요.
    - 뜻밖의 행운이 찾아올지도 몰라요. 하지만 지갑은 꼭 닫아두세요!
    
    이제 오늘의 금전운을 작성해주세요.
  `;

  try {
    const response = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4o-mini",
        messages: [{ role: "user", content: prompt }],
        max_tokens: 16384,
        temperature: 0.7,
      },
      {
        headers: {
          Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
          "Content-Type": "application/json",
        },
      }
    );

    const fortune =
      response.data.choices[0].message.content || "금전운 생성에 실패했습니다.";
    messages.value.push({ sender: "bot", text: `오늘의 금전운: ${fortune}` });
    messages.value.push({
      sender: "bot",
      text: "'처음'이라고 입력하면 다시 시작할 수 있어요!",
    });
  } catch (error) {
    console.error("Error fetching fortune:", error);
    messages.value.push({
      sender: "bot",
      text:
        "금전운을 가져오는 중 문제가 발생했습니다. 다시 시도해주세요.",
    });
  }
};

// Handle purchase decision flow
const handlePurchaseFlow = async (input) => {
  if (!state.itemName) {
    state.itemName = input;
    messages.value.push({
      sender: "bot",
      text: `물건 이름이 "${state.itemName}" 맞으신가요? 가격(원)을 입력해주세요!`,
    });
  } else if (!state.itemCost) {
    state.itemCost = parseInt(input);
    if (isNaN(state.itemCost)) {
      messages.value.push({
        sender: "bot",
        text: "유효한 숫자를 입력해주세요! 물건 가격(원)을 다시 입력해주세요.",
      });
      return;
    }
    messages.value.push({
      sender: "bot",
      text: `가격이 ${state.itemCost}원이라고 하셨네요. 총 예산(원)을 알려주세요!`,
    });
  } else if (!state.budget) {
    state.budget = parseInt(input);
    if (isNaN(state.budget)) {
      messages.value.push({
        sender: "bot",
        text: "유효한 숫자를 입력해주세요! 총 예산(원)을 다시 입력해주세요.",
      });
      return;
    }

    // Call GPT for purchase advice
    const prompt = `
      당신은 '머니또'입니다. 사용자가 물건 구매 여부를 묻습니다.
      물건 이름은 "${state.itemName}"이고, 가격은 ${state.itemCost}원입니다.
      사용자의 총 예산은 ${state.budget}원입니다.

      사용자의 재정 상태와 예산 상황을 분석해 유머러스하고 재치 있는 말투로 답변하세요.
    `;

    try {
      const response = await axios.post(
        "https://api.openai.com/v1/chat/completions",
        {
          model: "gpt-4o-mini",
          messages: [{ role: "user", content: prompt }],
          max_tokens: 1000,
          temperature: 0.7,
        },
        {
          headers: {
            Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
            "Content-Type": "application/json",
          },
        }
      );

      const advice =
        response.data.choices[0].message.content || "결정 생성 실패!";
      messages.value.push({ sender: "bot", text: advice });
      messages.value.push({
        sender: "bot",
        text:
          "'처음'이라고 입력하면 다시 시작할 수 있어요!",
      });
    } catch (error) {
      console.error("Error fetching purchase advice:", error);
      messages.value.push({
        sender: "bot",
        text:
          "구매 결정을 가져오는 중 문제가 발생했습니다. 다시 시도해주세요.",
      });
    }
  }
};

// Reset the chat flow
const reset = () => {
  state.value = null;
  state.itemName = null;
  state.itemCost = null;
  state.budget = null;
  messages.value.push({
    sender: "bot",
    text:
      "안녕하세요! 저는 당신의 금융 친구 머니또입니다! 오늘의 금전운 보기를 원하시면 1번, 물건 구매 결정에 대한 도움이 필요하시면 2번을 입력해주세요!",
  });
};
</script>

<style scoped>
#app {
  max-width: 500px;
  margin: auto;
}
.chat-container {
  display: flex;
  flex-direction: column;
}
.chat-box {
  border: solid #ddd;
  height: 400px;
}
/* .message {}
.input-box {} */
</style>