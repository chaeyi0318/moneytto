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
  import { ref, watch, nextTick, onMounted } from "vue";
  import axios from "axios";
  import { useAccountStore } from "@/stores/accountStore";
  
  const accountStore = useAccountStore();
  const user = ref(null)
  const birthDate = ref(null);
  // console.log(accountStore.fetchUserProfile());
  
  async function getUserProfile() {
    const userProfile = await accountStore.fetchUserProfile();
    user.value = userProfile
    // console.log(user.value);
  }
  
  getUserProfile();
  
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
      scrollToBottom();
      return;
    }
  
    // Reset logic for starting over
    if (input.toLowerCase() === "처음") {
      reset();
      scrollToBottom();
      return;
    }
  
    // Handle purchase decision flow
    if (state.value === "purchase") {
      handlePurchaseFlow(input);
      scrollToBottom();
      return;
    }
    scrollToBottom();
  };
  
  // Fetch dynamic fortune using GPT
  const fetchFortune = async () => {
    const prompt = `
      당신은 역학적 지식이 풍부하고 인문학적 소양을 갖추고 있으며 의사소통 능력이 뛰어난 운세 전문가입니다.
      사용자의 생년월일 정보를 바탕으로 오늘의 금전운을 작성해주세요.
      - 유머러스하고 친근한 말투를 사용하지만 늘 정중한 자세로 존댓말로 소통하세요.
      - 사용자가 기분 좋은 하루를 보낼 수 있도록 도와주세요.
      - 금전, 재물 관련 조언과 함께 재미있게 운세를 작성해주세요.
      - 천문학이나 역학적인 요소를 섞어 전문적인 답변을 해주세요.
      
      예시:
      - 오늘은 작은 사치가 괜찮습니다! 하지만 큰 지출은 피하세요.
      - 뜻밖의 행운이 찾아올지도 몰라요. 하지만 지갑은 꼭 닫아두세요!
      
      사용자의 이름은 ${user.value.nickname}, 생년월일은 ${user.value.birth_date}입니다.
      이제 답변을 작성해주세요. 답변은 기분 좋은 인사와 함께 마무리합니다.
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
      messages.value.push({ sender: "bot", text: `오늘의 금전운: ${fortune}` });
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
        당신은 내 손 안의 금융 비서 '머니또'입니다.
        친구처럼 친근하면서도 친절하고 농담도 잘 하며 유머러스하죠.
        하지만 존댓말로 정중한 자세를 유지해야 합니다. 반말은 절대 안돼요.
        한국어를 제외한 일본어, 중국어, 태국어, 한자 등 다른 모든 언어의 사용은 금지합니다.
        
        당신의 역할은 사용자의 지갑에서 새는 돈을 막아주는 것입니다.   
        너무 과한 소비가 아닌지 브레이크를 걸어주는 역할도 잘 해야해요. 
        기분 나쁘지 않게 조언도 잘 할 수 있는 능력이 있습니다.
        하지만 무조건 소비를 반대해서도 안됩니다.
        적절한 소비인지 내역과 비용을 잘 비교해 보고 조언해 주세요.
        해당 항목에 너무 과도한 비용을 지출하는 것은 아닌지 생각해 주시고요.
        너무 과한 지출이라면 정신 차릴 수 있게 호된 채찍도 줄 수 있죠.
        사용자의 이번 달 예산과 소비 내역을 바탕으로 구매 결정을 도와주세요.
  
        사용자의 이름은 ${user.value.nickname}, 이번 달 예산은 ${state.budget}원이며 지금까지 50000원 지출했습니다.
  
        "${state.itemName}"에 ${state.itemCost}원을 지출해도 괜찮을까요?
  
        답변은 ${user.value.nickname}님으로 시작하며 500자 내외로 사용자의 상태 분석, 구매 결정 여부, 결정 이유, 조언의 순서대로 자연스럽게 해주세요.
        사용자의 소비 생활에 대한 응원도 잊지 마세요!
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
    messages.value.push({
      sender: "bot",
      text:
        "안녕하세요! 저는 당신의 금융 친구 머니또입니다! 오늘의 금전운 보기를 원하시면 1번, 물건 구매 결정에 대한 도움이 필요하시면 2번을 입력해주세요!",
    });
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