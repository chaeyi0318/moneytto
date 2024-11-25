<template>
  <div class="main">
    <button class="back-btn" @click.prevent="goToCalendar">달력으로 돌아가기</button>
    <span>00월 레포트</span>
    <div class="chart-container">
      <CategoryChart class="category-chart"/>
      <BarGraph class="bar-graph"/>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from "vue-router";
import CategoryChart from '@/components/calendar/CategoryChart.vue';
import BarGraph from '@/components/calendar/BarGraph.vue';

const router = useRouter()

const goToCalendar = () => {
  router.push({ name: 'CalendarView'})
}
</script>

<style scoped>
* {
  font-family: 'Roboto', sans-serif;
  /* font-weight: bold; */
}

.main {
  width: 70%;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(45, 122, 49, 0.1);
  margin-top: 80px;
  margin-left: auto;
  margin-right: auto;
}

.back-btn {
  background-color: #2E8B57;
  color: white;
  border: none;
  padding: 5px 10px; /* 버튼 크기를 줄임 */
  font-size: 0.85rem; /* 글자 크기를 줄임 */
  border-radius: 15px; /* 둥근 모서리 유지 */
  cursor: pointer;
  transition: all 0.3s ease;
  margin-left: 30px;
  margin-top: 20px;
}

.back-btn:hover {
  background-color: #1a5235;
  transform: scale(1.05);
}

/* 두 그래프를 가로로 나란히 배치하는 컨테이너 */
.chart-container {
  display: flex; /* Flexbox로 자식 요소를 가로 배치 */
  justify-content: space-between; /* 두 그래프 사이에 여유 공간 추가 */
}

.bar-graph {
  flex: 2; /* 각 그래프가 동일한 비율로 공간을 차지 */
}

.category-chart {
  flex: 1;
  height: 100%;
  margin-right: 20px; /* 두 그래프 사이의 간격 조정 (선택 사항) */
}

span {
  display: block; /* span을 block 요소로 변경 */
  text-align: center; /* 텍스트를 가로 중앙 정렬 */
  font-size: 2rem;
  margin-top: 10px; /* 위쪽 여백 추가 (선택 사항) */
  color: #2E8B57;
  font-weight: bold;
}
</style>