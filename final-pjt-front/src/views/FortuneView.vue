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

<script>
export default {
  data() {
    return {
      itemName: "", // 물건 이름
      itemCost: null, // 물건 가격
      budget: null, // 총 예산
      result: null, // 결과 메시지
    };
  },
  methods: {
    handleFormSubmit() {
      // 남은 예산 계산
      const remainingBudget = this.budget - this.itemCost;

      // 응답 메시지 다양화
      if (remainingBudget < 0) {
        this.result = this.getRandomResponse("no");
      } else {
        this.result = this.getRandomResponse("yes");
      }
    },
    getRandomResponse(type) {
      const responses = {
        no: [
          `${this.itemName}는 사지마! 예산이 바닥났다고!`,
          `예산 대비 이만큼이나 썼는데 또 사고 싶어? 정신 차려!`,
          `지갑이 울고 있어요. ${this.itemName}를 사는 건 무리야.`,
          `너무 많이 썼어! 마법의 소라고동도 "${this.itemName}는 사지마"라고 하네.`,
          `아 지갑 너무 가볍다! 그래도 ${this.itemName}가 사고 싶니!?`
        ],
        yes: [
          `${this.itemName}는 사도 돼! 아직 여유가 있네.`,
          `이 정도는 괜찮아. ${this.itemName}를 사도 지갑이 고개를 끄덕이네.`,
          `오케이, ${this.itemName} 사자! 하지만 너무 들뜨진 말라고~`,
          `마법의 소라고동이 말하길… "${this.itemName}는 사도 된대!"`,
        ],
      };

      // 랜덤으로 응답 선택
      const randomIndex = Math.floor(Math.random() * responses[type].length);
      return responses[type][randomIndex];
    },
  },
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