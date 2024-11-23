<template>
  <div id="app">
    <h1>살말 개구리봇</h1>
    <form @submit.prevent="handleFormSubmit">
      <label for="itemName">물건 이름:</label>
      <input id="itemName" v-model="itemName" type="text" placeholder="물건 이름을 입력하세요" required />

      <label for="itemCost">물건 가격 (원):</label>
      <input id="itemCost" v-model.number="itemCost" type="number" placeholder="가격을 입력하세요" required />

      <label for="budget">총 예산 (원):</label>
      <input id="budget" v-model.number="budget" type="number" placeholder="예산을 입력하세요" required />

      <button type="submit">결정 요청</button>
    </form>

    <div v-if="result">
      <h2>결과:</h2>
      <p>{{ result }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";

// Props 선언
const props = defineProps({
  amount: {
    type: Number,
    required: true, // amount는 필수 prop
  },
});

// 상태 변수
const itemName = ref(""); // 물건 이름
const itemCost = ref(null); // 물건 가격
const budget = ref(props.amount); // 총 예산
const result = ref(null); // 결과 메시지

watch(
  () => props.amount,
  (newAmount) => {
    budget.value = newAmount;
  }
);

// 폼 제출 핸들러
const handleFormSubmit = async () => {
  const prompt = `
    당신은 "머니또"입니다. 사용자가 물건 구매 여부를 묻습니다.  
    물건 이름은 "${itemName.value}"이고, 가격은 ${itemCost.value}원입니다.  
    사용자의 총 예산은 ${budget.value}원입니다.

    사용자는 당신에게 물건을 사야 할지 말아야 할지 조언을 구하고 있습니다. 당신의 역할은 다음과 같습니다:  
    - 사용자의 재정 상태와 예산 상황을 분석합니다.  
    - 물건의 가격이 예산 내인지 초과인지 판단합니다.  
    - 유머러스하고 재치 있는 말투로, 마치 친한 친구처럼 답변하되, 존댓말을 사용합니다.  
    - 사용자가 웃으면서도 합리적인 결정을 내릴 수 있도록 돕습니다.

    다음 규칙을 따르세요:

    ### **1. 분석 시작**  
    먼저 사용자의 재정 상태를 간단히 요약하며 대화를 시작하세요.
    인삿말 예시
    - 안녕하세요! 당신의 금융 친구 머니또입니다!

    ### **2. 예산 초과일 경우**  
    - 물건이 생필품(생활용품)이라면 약간의 타박과 함께 긍정적인 조언을 섞어서 답변하세요

    - 생필품이 아니더라도 상황에 따라 허락할 수 있습니다. 단, 허락할 때는 유머러스한 이유를 덧붙이세요:  

    ### **3. 예산 내일 경우**  
    - 기본적으로 "사셔도 돼요!"라고 긍정적으로 말하세요.  
    - 하지만 가끔은 "그런데 꼭 사야 할까요?"라고 질문하며, 물건에 대한 필요성을 고민하게 만드세요.  

    ### **4. 추가 요소**  
    - 항상 친근하고 장난기 있는 말투로 대화하세요. 그러나 존댓말을 유지합니다.  
    - 필요하다면 물건에 대한 엉뚱한 상상이나 농담을 섞어 대화를 재미있게 만들어주세요.  

    ### **5. 답변 길이**  
    답변은 간단하지 않게 길고 자세하게 작성하세요. 사용자가 마치 친구와 수다 떠는 기분이 들도록 만들어주세요.

    ### **6. 이모지 사용 최소화**  
    - 이모지는 최소한으로 사용하며, 꼭 필요한 경우에만 활용하세요.

    이제 아래 정보를 바탕으로 답변을 생성하세요:  
    - 물건 이름: "${itemName.value}"  
    - 물건 가격: ${itemCost.value}원  
    - 사용자 총 예산: ${budget.value}원
  `;

  try {
    const response = await axios.post(
      "https://api.openai.com/v1/chat/completions",
      {
        model: "gpt-4o-mini", // 모델 설정
        messages: [{ role: "user", content: prompt }],
        max_tokens: 1000,
        temperature: 0.7,
      },
      {
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${import.meta.env.VITE_OPENAI_API_KEY}`,
        }
      }
    );
    
    // 결과 저장
    result.value = response.data.choices[0].message.content;
  } catch (error) {
    console.error("Error fetching data from OpenAI:", error);
    result.value = "OpenAI와 통신 중 문제가 발생했습니다. 다시 시도해주세요.";
  }
};
</script>

<style scoped>
#app {
  text-align: center;
  margin-top: 50px;
}
h1 {
  color: #4caf50;
}
form {
  margin-bottom: 20px;
}
label {
  display: block;
  margin-bottom: 5px;
}
input {
  margin-bottom: 15px;
}
button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 15px;
}
</style>