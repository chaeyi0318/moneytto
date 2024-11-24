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

  let waveHeight = 20; // 물결 높이
  let waveLength = 0.02; // 물결 길이
  let waveSpeed = 0.05; // 물결 속도
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
  display: block;
}
</style>

<!-- <template>
  <div class=cup></div>
</template>

<script setup>

</script>

<style scoped>
.cup{
	display: block;
    position: relative;
    width: 150px;
    height: 180px;
    border: 6px solid #000;
    border-radius: 15px;
    border-top-left-radius: 5px;
    border-top-right-radius: 5px;
    box-shadow: 0 0 0 6px, 0 20px 35px rgba(0,0,0,1);
}

.cup::before{
    content: '';
    position: absolute;
    top: 30px;
    right: -75px;
    width: 50px;
    height: 80px;
    border: 12px solid #000;
    border-top-right-radius: 35px;
    border-bottom-right-radius: 35px;
}

.cup{
  background: url(https://image.ibb.co/fmHm66/wave.png);
  background-position: 0 350px;
  background-repeat: repeat-x;
}

.cup{
    transition: ease-in-out;
    animation: filling 10s infinite;
}

@keyframes filling {
    50% {background-position: 3000px 0;}
    100% {background-position: 6000px 350px;}
}

@keyframes test_circle{
    0%{transform: translateX(-500%) scale(0.3) rotate(0deg);}
    40%{transform: translateX(0) scale(1) rotate(0deg);}
    100%{transform: translateX(0) scale(1) rotate(720deg);}
}
</style> -->