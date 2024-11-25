<template>
  <div class="main-container">
    <div class="background-animation"></div>
    
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
  background-color: rgb(213, 222, 221);
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
}

.background-animation {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-image: url("@/assets/logo.jpg");
  background-size: contain;
  background-position: center;
  background-repeat: no-repeat;
  animation: bounceBackground 1.2s cubic-bezier(0.36, 0, 0.66, 1.5);
}

@keyframes bounceBackground {
  0% {
    opacity: 0;
    transform: translateY(100px) scale(0.8);
  }
  50% {
    opacity: 1;
    transform: translateY(-30px) scale(1.1);
  }
  75% {
    transform: translateY(15px) scale(0.95);
  }
  90% {
    transform: translateY(-5px) scale(1.02);
  }
  100% {
    transform: translateY(0) scale(1);
  }
}

.btn-container {
  position: absolute;
  bottom: 28%;
  left: 50%;
  transform: translateX(-50%);
  /* z-index: 2; */
  opacity: 0; /* 처음에는 투명하게 */
  animation: fadeIn 0.8s ease-out forwards; /* forwards로 마지막 상태 유지 */
  animation-delay: 1s; /* 배경 애니메이션(1초) 후에 시작 */
}

@keyframes fadeIn {
  0% {
    opacity: 0;
    transform: translate(-50%, 20px); /* X축은 중앙 정렬 유지하면서 Y축으로만 이동 */
  }
  100% {
    opacity: 1;
    transform: translate(-50%, 0);
  }
}

.signup-btn {
  background-color: transparent;
  color: #369456;
  border: 3px solid #369456;
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
