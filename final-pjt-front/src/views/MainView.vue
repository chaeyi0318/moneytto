<template>
  <div class="main-container">
    <!-- 텍스트 섹션 -->
    <!-- <div class="content">
      <h1 class="line" :class="{ visible: currentLine >= 0 }">
        소비의 시각화부터 맞춤형 재정 조언까지
      </h1>
      <h2 class="line" :class="{ visible: currentLine >= 1 }">
        당신의 금융 친구, 머니또!
      </h2>
    </div> -->

    <div v-if="!accountStore.isLogin" class="btn-container">
      <button @click="goToSignup" class="signup-btn">Sign up</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { RouterLink, useRouter } from "vue-router";
import { useAccountStore } from "@/stores/accountStore";

const router = useRouter();
const accountStore = useAccountStore();

const goToSignup = function () {
  router.push({ name: "SignupView" });
};
// 현재 보이는 라인을 관리하는 상태
// const currentLine = ref(-1);

// onMounted(() => {
//   // 각 줄이 순서대로 나타나도록 설정
//   let delay = 0;
//   const lines = document.querySelectorAll(".line");
//   lines.forEach((_, index) => {
//     setTimeout(() => {
//       currentLine.value = index;
//     }, delay);
//     delay += 1000; // 각 줄마다 1초의 간격
//   });
// });
</script>

<style scoped>
.main-container {
  height: 100vh;
  width: 100vw;
  background-image: url("@/assets/logo.jpg");
  background-size: cover;
  background-position: center;
  display: flex;
  justify-content: center;
  align-items: center;
}

.btn-container {
  display: flex;
  justify-content: center;
  width: 100%;
  padding-top: 20%; /* 화면 높이의 1/4 지점으로 이동 */
}

.signup-btn {
  background-color: transparent;
  color: #2e8b57;
  border: 3px solid #2e8b57;
  padding: 20px 50px;
  border-radius: 25px;
  font-size: 22px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.signup-btn:hover {
  background-color: #2e8b57;
  color: white;
  transform: translateY(-2px);
}
</style>
