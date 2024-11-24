<template>
  <div class="wave-container" :style="dynamicStyles">
    <canvas ref="waveCanvas"></canvas>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from "vue"

const waveCanvas = ref(null)
let animationFrameId = null

const props = defineProps({
  amount: Number,
  total_price: Number,
})

// props 추출
const amount = ref(0)
const totalPrice = ref(0)

// 퍼센트 계산 및 높이 설정
const dynamicStyles = computed(() => {
  const percentage = props.total_price > 0 ? (props.total_price / props.amount) * 100 : 0 // 퍼센트 계산
  let height

  if (percentage <= 10) {
    height = 100;
  } else if (percentage <= 20) {
    height = 200;
  } else if (percentage <= 30) {
    height = 300;
  } else if (percentage <= 40) {
    height = 400;
  } else if (percentage <= 50) {
    height = 500;
  } else if (percentage <= 60) {
    height = 600;
  } else if (percentage <= 70) {
    height = 700;
  } else if (percentage <= 80) {
    height = 800;
  } else if (percentage <= 90) {
    height = 900;
  } else if (percentage <= 100) {
    height = 1000;
  } else {
    height = 1200; // 초과 사용 시
  }

  return {
    height: `${height}px`,
  }
})

const initWaveAnimation = () => {
  const canvas = waveCanvas.value
  const ctx = canvas.getContext("2d")

  canvas.width = canvas.parentElement.offsetWidth
  canvas.height = canvas.parentElement.offsetHeight

  let waveHeight = 15           // 물결 높이
  let waveLength = 0.04         // 물결 길이
  let waveSpeed = 0.04          // 물결 속도
  let offset = 0                // 물결 이동 오프셋

  const drawWave = () => {
    ctx.clearRect(0, 0, canvas.width, canvas.height)

    ctx.beginPath()
    ctx.moveTo(0, canvas.height / 2)
    
    for (let x = 0; x < canvas.width; x++) {
      const y =
        waveHeight * Math.sin(x * waveLength + offset) +
        canvas.height / 2;
      ctx.lineTo(x, y)
    }

    ctx.lineTo(canvas.width, canvas.height)
    ctx.lineTo(0, canvas.height)
    ctx.closePath()

    ctx.fillStyle = "rgba(0,150,255,0.5)"
    ctx.fill()

    offset += waveSpeed; // 물결 이동
    animationFrameId = requestAnimationFrame(drawWave) // 다음 프레임 요청
  }

  drawWave() // 애니메이션 시작
}

// 컴포넌트 마운트 시 애니메이션 초기화
onMounted(() => {
  initWaveAnimation()
})

// 컴포넌트 언마운트 시 애니메이션 정지
onUnmounted(() => {
  if (animationFrameId) {
    cancelAnimationFrame(animationFrameId)
  }
})

watch(
  () => [amount, totalPrice],
  ([newAmount, newTotalPrice]) => {
    console.log("amount changed:", newAmount)
    console.log("totalPrice changed:", newTotalPrice)
  }
)
</script>

<style scoped>
.wave-container {
  position: relative;
  width: 100%;
  height: 100px;
  max-height: 1000px;
}

canvas {
  width: 100%;
  height: 100%;
  display: block;
}
</style>