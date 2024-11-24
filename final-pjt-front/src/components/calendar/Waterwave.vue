<template>
  <div class="wave-container">
    <canvas ref="waveCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";

const waveCanvas = ref(null); // 캔버스 참조
let animationFrameId = null; // 애니메이션 프레임 ID

// 물결 애니메이션 설정
const initWaveAnimation = () => {
  const canvas = waveCanvas.value;
  const ctx = canvas.getContext("2d");

  // 캔버스 크기 설정
  canvas.width = canvas.parentElement.offsetWidth;
  canvas.height = canvas.parentElement.offsetHeight;

  let waveHeight = 12; // 물결 높이
  let waveLength = 0.04; // 물결 길이
  let waveSpeed = 0.03; // 물결 속도
  let offset = 0; // 물결 이동 오프셋

  const drawWave = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height); // 캔버스 초기화

    ctx.beginPath();
    ctx.moveTo(0, canvas.height / 2);

    for (let x = 0; x < canvas.width; x++) {
      const y =
        waveHeight * Math.sin(x * waveLength + offset) +
        canvas.height / 2;
      ctx.lineTo(x, y);
    }

    ctx.lineTo(canvas.width, canvas.height);
    ctx.lineTo(0, canvas.height);
    ctx.closePath();

    ctx.fillStyle = "rgba(0, 150, 255, 0.5)"; // 물 색상
    ctx.fill();

    offset += waveSpeed; // 물결 이동
    animationFrameId = requestAnimationFrame(drawWave); // 다음 프레임 요청
  };

  drawWave(); // 애니메이션 시작
};

// 컴포넌트 마운트 시 애니메이션 초기화
onMounted(() => {
  initWaveAnimation();
});

// 컴포넌트 언마운트 시 애니메이션 정지
onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId);
  }
});
</script>

<style scoped>
.wave-container {
  position: relative;
  width: 100%;
  height: 300px;
}

canvas {
  width: 100%;
  height: 100%;
  display: block;
}
</style>