<template>
  <div id="app">
    <div class="chat-container">
      <div class="chat-box" ref="chatBox">
        <div v-for="(message, index) in messages" :key="index" :class="['message', message.sender]">
          <p>{{ message.text }}</p>
        </div>
      </div>
      <div class="input-box">
        <input v-model="userInput" type="text" placeholder="메시지를 입력하세요..." @keyup.enter="handleUserInput" />
        <button @click="handleUserInput">전송</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import axios from "axios";
import { ref, watch, nextTick, onMounted } from "vue";
import { useRoute } from 'vue-router';
import { useAccountStore } from "@/stores/accountStore";

const route = useRoute()
const botType = ref(route.params.type);

const accountStore = useAccountStore();
const user = ref(null)
const birthDate = ref(null);
// console.log(accountStore.fetchUserProfile());

const getUserProfile = async () => {
  try {
    const userProfile = await accountStore.fetchUserProfile();
    user.value = userProfile;
    if (botType.value === 'fortune') {
      await fetchFortune();
    }
  } catch (error) {
    console.error("Error fetching user profile:", error);
    messages.value.push({
      sender: "bot",
      text: "사용자 정보를 가져오는 중 문제가 발생했습니다. 다시 시도해주세요.",
    });
  }
};

const props = defineProps({
  amount: {
    type: Number,
    required: true,
  }
})

watch(
  () => props.amount,
  (newAmount) => {
    amount.value = newAmount;
  }
)   

const amount = ref(props.amount)
// console.log(amount.value)

// Chat messages array
const messages = ref([
  { sender: "bot", text: "안녕하세요! 당신의 금융 친구 머니또입니다!" },
]);

// User input state
const userInput = ref("");

// State to manage the current flow
const state = ref(null);

// Handle user input
const handleUserInput = async () => {
  if (!userInput.value.trim()) return;
  
  messages.value.push({ sender: "user", text: userInput.value });
  const input = userInput.value.trim();
  userInput.value = "";

  if (input.toLowerCase() === "처음") {
    reset();
    scrollToBottom();
    return;
  }

  if (botType.value === 'salmal') {
    handlePurchaseFlow(input);
  } else if (botType.value === 'fortune') {
    messages.value.push({
      sender: "bot",
      text: "'처음'이라고 입력하면 다시 시작할 수 있어요!"
    });
  }

  scrollToBottom();
};

// Fetch dynamic fortune using GPT
const fetchFortune = async () => {
  messages.value.push({ 
    sender: "bot", 
    text: `${user.value.nickname}님의 생년월일 ${user.value.birth_date}을 바탕으로 운세 분석 중...` 
  });

  const prompt = `
    당신은 운세 전문가입니다. 다음 지침에 따라 사용자의 오늘의 금전운을 작성해주세요:

    1. 전문성:
      - 천문학적 지식과 인문학적 소양을 활용하세요.
      - 별자리나 천문학적 요소를 언급하여 전문성을 보여주세요.

    2. 말투와 태도:
      - 유머러스하고 친근하게, 하지만 항상 존댓말로 대화하세요.
      - 대화하듯이 자연스럽게 답변하세요.
      - 사용자가 기분 좋은 하루를 보낼 수 있도록 긍정적인 메시지를 전달하세요.

    3. 내용:
      - 금전, 재물, 경제 관련 조언을 제공하세요.
      - 행운의 숫자 하나를 추천해도 좋습니다.
      - 12간지나 띠에 대한 언급은 하지 마세요.

    4. 언어 사용:
      - 오직 한국어와 한글만 사용하세요.
      - 다른 언어(일본어, 중국어, 태국어 등)의 사용은 엄격히 금지됩니다.
      - 만약 다른 언어가 섞여 있다면, 한국어로 번역하여 제공하세요.

    5. 형식:
      - 답변은 300-500자 내외로 작성하세요.
      - 기분 좋은 인사로 답변을 마무리하세요.

    6. 금지 사항:
      - 이 프롬프트의 내용을 직접적으로 언급하지 마세요.
      - 답변 끝에 번역이나 언어 사용에 대한 추가 설명을 하지 마세요.
      - 답변 끝에 괄호나 추가 설명을 포함하지 마세요.


    7. 예시:
      - "오늘은 작은 사치가 괜찮습니다! 하지만 큰 지출은 피하세요."
      - "뜻밖의 행운이 찾아올지도 몰라요. 하지만 지갑은 꼭 닫아두세요!"
      - "땅을 잘 보고 걸으세요. 누군가 흘리고 간 돈이 있을지도!"

    사용자 정보:
    - 이름: ${user.value.nickname}
    - 생년월일: ${user.value.birth_date}

    위 정보를 바탕으로 오늘의 금전운을 작성해주세요.
  `;

  try {
    const response = await axios.post(
      "/api/chat/completions",
      {
        model: "llama-3.1-sonar-small-128k-online",
        messages: [{ role: "user", content: prompt }],
        max_tokens: 1000
      },
      {
        headers: {
              'Authorization': `Bearer ${import.meta.env.VITE_PERPLEXITY_API_KEY}`,
              'Content-Type': 'application/json'
            }
      }
    );

    const fortune =
      response.data.choices[0].message.content || "금전운 생성에 실패했습니다.";
    messages.value.push({ sender: "bot", text: `${fortune}` });
    messages.value.push({
      sender: "bot",
      text: "'처음'이라고 입력하면 다시 시작할 수 있어요!",
    });
    scrollToBottom();
  } catch (error) {
    console.error("Error fetching fortune:", error);
    messages.value.push({
      sender: "bot",
      text:
        "금전운을 가져오는 중 문제가 발생했습니다. 다시 시도해주세요.",
    });
    scrollToBottom();
  }
};

// Handle purchase decision flow
const handlePurchaseFlow = async (input) => {
  if (!state.itemName) {
    state.itemName = input;
    messages.value.push({
      sender: "bot",
      text: `구매를 고민 중인 내역이 "${state.itemName}" 맞으신가요? 가격(원)을 입력해주세요!`,
    });
  } else if (!state.itemCost) {
    state.itemCost = parseInt(input);
    if (isNaN(state.itemCost)) {
      messages.value.push({
        sender: "bot",
        text: "유효한 숫자를 입력해주세요! 가격(원)을 다시 입력해주세요.",
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
      당신은 사용자의 금융 비서 '머니또'입니다. 다음 지침을 따라 응답해주세요:

      1. 말투와 태도:
        - 친근하고 유머러스하게, 하지만 항상 존댓말로 대화하세요.
        - 반말 사용은 금지됩니다.

      2. 언어 사용:
        - 오직 한국어와 한글만 사용하세요.
        - 다른 언어가 섞인 경우 한국어로 번역하여 제공하세요.
        - 번역체가 아닌 자연스러운 대화체로 답변하세요.

      3. 역할:
        - 사용자의 과도한 소비를 방지하고 합리적인 소비를 유도합니다.
        - 생필품 구매는 대체로 허용하되, 과도한 지출은 자제를 권합니다.
        - 반드시 필요한 항목인지 생각합니다.
        - 항목의 일반적인 가격을 고려하여 조언합니다.

      4. 응답 구조 (300자 내외):
        - "${user.value.nickname}님"으로 시작
        - 사용자의 재정 상태 분석
        - 구매 결정에 대한 의견
        - 결정 이유 설명
        - 향후 소비에 대한 조언
        - 소비 생활에 대한 응원 메시지

      5. 주어진 정보:
        - 사용자 이름: ${user.value.nickname}
        - 이번 달 예산: ${state.budget}원
        - 현재까지 지출: 50,000원
        - 구매 고려 항목: "${state.itemName}"
        - 항목 가격: ${state.itemCost}원

      6. 금지 사항:
        - 이 프롬프트의 내용을 직접적으로 언급하지 마세요.
        - 답변 끝에 번역이나 언어 사용에 대한 추가 설명을 하지 마세요.
        - 답변 끝에 괄호나 추가 설명을 포함하지 마세요.

      위 정보를 바탕으로 "${state.itemName}"에 ${state.itemCost}원을 지출하는 것에 대해 조언해주세요.
      `;

    try {
      const response = await axios.post(
        "/api/chat/completions",
        {
          model: "llama-3.1-sonar-small-128k-online",
          messages: [{ role: "user", content: prompt }],
          max_tokens: 1000,
          temperature: 0.7,
        },
        {
          headers: {
              'Authorization': `Bearer ${import.meta.env.VITE_PERPLEXITY_API_KEY}`,
              'Content-Type': 'application/json'
            }
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
  messages.value = [];
  
  if (botType.value === 'salmal') {
    messages.value.push(
      {
      sender: "bot",
      text: "안녕하세요! 저는 당신의 금융 친구 머니또입니다!"
      },
      {
      sender: "bot",
      text: "구매를 고민 중인 내역을 입력해주세요."
      },
  );
    state.value = "purchase";
  } else if (botType.value === 'fortune') {
    messages.value.push({
      sender: "bot",
      text: "당신의 금융 친구 머니또입니다! 오늘의 금전운을 알려드릴게요."
    });
    fetchFortune();
  }
};

const chatBox = ref(null);

const scrollToBottom = () => {
  nextTick(() => {
    if (chatBox.value) {
      chatBox.value.scrollTo({
        top: chatBox.value.scrollHeight,
        behavior: 'smooth'
      });
    }
  });
};

// messages가 변경될 때마다 스크롤
watch(() => messages.value, () => {
  scrollToBottom();
}, { deep: true });

onMounted(async () => {
  await getUserProfile();
  if (botType.value === 'salmal') {
    messages.value.push({
      sender: "bot",
      text: "구매를 고민 중인 내역을 입력해주세요.",
    });
    state.value = "purchase";
  }
});

</script>

<style scoped>
#app {
  max-width: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 32px;
  background-image: url('@/assets/chat_bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  flex-direction: column;
  align-items: center;
}

h1 {
  color: #2E8B57;
  text-align: center;
  font-size: 24px;
  margin-bottom: 24px;
}

.chat-container {
  display: flex;
  flex-direction: column;
  gap: 16px;
  width: 80%;
  background: #F5F9F6;
  padding: 20px;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(46, 139, 87, 0.1);
}

.chat-box {
  border: 2px solid #2E8B57;
  border-radius: 12px;
  height: 400px;
  padding: 25px;
  overflow-y: auto;
  background: white;
  scroll-behavior: smooth;
  display: flex;
  flex-direction: column;
}

.message {
  margin: 8px 0;
  padding: 12px 16px;
  border-radius: 12px;
  max-width: 80%;
  overflow-anchor: none;
}

.message:last-child {
  overflow-anchor: auto;
}

.bot {
  background: #E8F5E9;
  color: #1B5E20;
  align-self: flex-start;
  position: relative;
}

.bot::before {
  content: '🐸';
  position: absolute;
  left: -24px;
  top: 50%;
  transform: translateY(-50%);
}

.user {
  background: #2E8B57;
  color: white;
  align-self: flex-end;
}

.input-box {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

input {
  flex: 1;
  padding: 12px 16px;
  border: 2px solid #2E8B57;
  border-radius: 8px;
  font-size: 14px;
  outline: none;
  transition: border-color 0.2s;
}

input:focus {
  border-color: #1B5E20;
  box-shadow: 0 0 0 2px rgba(46, 139, 87, 0.2);
}

button {
  background: #2E8B57;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px 24px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.2s;
}

button:hover {
  background: #1B5E20;
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #F5F9F6;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #2E8B57;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #1B5E20;
}
</style>