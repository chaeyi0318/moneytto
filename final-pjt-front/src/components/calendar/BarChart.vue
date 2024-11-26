<template>
  <div>
    <Bar :data="chartData" :options="chartOptions" />
  </div>
</template>
<script setup>
import { Bar } from "vue-chartjs";
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale,
} from "chart.js";
import { computed } from "vue";

// Chart.js 구성 등록
ChartJS.register(
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
);

// Props 정의
const props = defineProps({
  barGraphData: {
    type: Array,
    required: true,
  },
});

// Chart 데이터 계산
const chartData = computed(() => ({
  labels: props.barGraphData.map((item) => item.date), // x축 라벨 (날짜)
  datasets: [
    {
      label: "예산", // 첫 번째 데이터셋 (budget)
      data: props.barGraphData.map((item) => item.budget),
      backgroundColor: "rgba(66, 165, 245, 0.7)", // 파란색
    },
    {
      label: "총 소비 금액",
      data: props.barGraphData.map((item) => item.total_value),
      backgroundColor: "rgba(255, 99, 132, 0.7)",
    },
  ],
}));

const chartOptions = computed(() => ({
  responsive: true,
  plugins: {
    legend: { display: true }, // 범례 표시
    title: { display: true, text: "예산 대비 소비 금액" },
  },
  scales: {
    x: { title: { display: true, text: "기간" } },
    y: { title: { display: true, text: "금액" } },
  },
}));
</script>

<style scoped>
/* 스타일을 필요에 따라 추가 */
</style>
