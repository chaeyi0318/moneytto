<template>
  <div class="main">
    <button class="back-btn" @click.prevent="goToCalendar">달력으로 돌아가기</button>
    <div class="navigation">
      <button class="prev-btn option-btn" @click.prevent="goToPreviousMonth">이전 달</button>
      <span class="current-month">{{ yearMonth }}월 레포트</span>
      <button class="next-btn option-btn" @click.prevent="goToNextMonth">다음 달</button>
    </div>
    <div class="chart-container">
      <CategoryChart :yearMonth="yearMonth" class="category-chart"/>
      <BarGraph :yearMonth="yearMonth" class="bar-graph"/>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import CategoryChart from '@/components/calendar/CategoryChart.vue';
import BarGraph from '@/components/calendar/BarGraph.vue';

const router = useRouter()

const currentYear = new Date().getFullYear();
const currentMonth = String(new Date().getMonth() + 1).padStart(2, "0"); // 두 자리 형식으로 변환
const yearMonth = ref(`${currentYear}-${currentMonth}`);

// 이전 달로 이동하는 함수
const goToPreviousMonth = () => {
  const [year, month] = yearMonth.value.split("-").map(Number); // 현재 년도와 월 분리
  const newDate = new Date(year, month - 2); // 이전 달 계산 (JavaScript는 월이 0부터 시작)
  const newYear = newDate.getFullYear();
  const newMonth = String(newDate.getMonth() + 1).padStart(2, "0"); // 두 자리 형식으로 변환
  yearMonth.value = `${newYear}-${newMonth}`; // yearMonth 값 업데이트
};

// 다음 달로 이동하는 함수
const goToNextMonth = () => {
  const [year, month] = yearMonth.value.split("-").map(Number); // 현재 년도와 월 분리
  const newDate = new Date(year, month); // 다음 달 계산 (JavaScript는 월이 0부터 시작)
  const newYear = newDate.getFullYear();
  const newMonth = String(newDate.getMonth() + 1).padStart(2, "0"); // 두 자리 형식으로 변환
  yearMonth.value = `${newYear}-${newMonth}`; // yearMonth 값 업데이트
};

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
  padding-bottom: 50px;
}

.navigation {
  display: flex; /* Flexbox로 자식 요소를 가로 배치 */
  align-items: center; /* 세로 중앙 정렬 */
  justify-content: center; /* 가로 중앙 정렬 */
  gap: 20px; /* 버튼 간 간격 추가 */
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
  height: 100%;
  margin-right: 20px;
}

.category-chart {
  flex: 1;
  height: 100%;
  margin-right: 20px; /* 두 그래프 사이의 간격 조정 (선택 사항) */
  margin-top: 65px;
}

span {
  display: block; /* span을 block 요소로 변경 */
  text-align: center; /* 텍스트를 가로 중앙 정렬 */
  font-size: 2rem;
  /* margin-top: 10px; 위쪽 여백 추가 (선택 사항) */
  color: #2E8B57;
  font-weight: bold;
}

.option-btn {
  margin-top: 50px;
  margin: 50px;
  /* margin-right: 50px; */
  padding: 3px;
  border: 2px solid #2E8B57;
  background-color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  /* color: #2E8B57; */
}
</style>