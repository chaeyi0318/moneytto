<template>
  <div class="main-container">
    <!-- 텍스트 섹션 -->
    <!-- <div class="content">
      <h1 class="line" :class="{ visible: currentLine >= 0 }">소비의 시각화부터 맞춤형 재정 조언까지</h1>
      <h2 class="line" :class="{ visible: currentLine >= 1 }">당신의 금융 친구, 머니또!</h2>
    </div> -->
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";

// 현재 보이는 라인을 관리하는 상태
const currentLine = ref(-1);

onMounted(() => {
  // 각 줄이 순서대로 나타나도록 설정
  let delay = 0;
  const lines = document.querySelectorAll(".line");
  lines.forEach((_, index) => {
    setTimeout(() => {
      currentLine.value = index;
    }, delay);
    delay += 1000; // 각 줄마다 1초의 간격
  });
});
</script>

<style scoped>
/* 화면 전체를 로고 이미지로 채우기 */
.main-container {
  height: 100vh;
  width: 100vw;
  background-image: url("@/assets/logo.jpg"); /* 로고 경로 */
  background-size: cover; /* 화면에 꽉 차도록 설정 */
  background-position: center; /* 중앙 정렬 */
  display: flex;
  justify-content: center;
  align-items: stretch /* 텍스트를 화면 중앙에 정렬 */
}

.content {
  text-align: center;
}

.line {
  opacity: 0; /* 초기 상태에서 보이지 않음 */
  transform: translateY(20px); /* 아래에서 올라오는 효과 */
  transition: opacity 0.8s ease, transform 0.8s ease; /* 서서히 나타나는 애니메이션 */
}

.line.visible {
  opacity: 1; /* 보이도록 설정 */
  transform: translateY(0); /* 원래 위치로 이동 */
}

h1, h2 {
  font-family: 'Arial', sans-serif;
  color: #4caf50; /* 로고 색상과 통일 */
}

h1 {
  font-size: 2rem;
}

h2 {
  font-size: 1.8rem;
}
</style>