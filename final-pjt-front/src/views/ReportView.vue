<template>
  <div class="main">
    <button class="back-btn" @click.prevent="goToCalendar">
      달력으로 돌아가기
    </button>
    <div class="navigation">
      <i
        class="prev-btn option-btn bi bi-caret-left-fill"
        @click.prevent="goToPreviousMonth"
      ></i>
      <span class="month-txt">{{ yearMonth }} 소비 분석</span>
      <i
        class="next-btn option-btn bi bi-caret-right-fill"
        @click.prevent="goToNextMonth"
      ></i>
    </div>
    <div class="chart-container">
      <CategoryChart :yearMonth="yearMonth" class="category-chart" />
      <BarGraph :yearMonth="yearMonth" class="bar-graph" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import CategoryChart from "@/components/calendar/CategoryChart.vue";
import BarGraph from "@/components/calendar/BarGraph.vue";

const router = useRouter();

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
  router.push({ name: "CalendarView" });
};
</script>

<style scoped>
.main {
  width: 70%;
  border-radius: 15px;
  box-shadow: 0 4px 12px rgba(45, 122, 49, 0.1);
  margin-top: 50px;
  margin-left: auto;
  margin-right: auto;
  padding: 10px;
}

.navigation {
  display: flex; /* Flexbox로 자식 요소를 가로 배치 */
  align-items: center; /* 세로 중앙 정렬 */
  justify-content: center; /* 가로 중앙 정렬 */
  max-height: 80px;
  /* gap: 20px; 버튼 간 간격 추가 */
}

.back-btn {
  margin: 10px;
  padding: 8px 16px;
  border: 1.5px solid #2e8b57;
  border-radius: 20px;
  font-size: 0.9em;
  font-weight: 500;
  color: #2e8b57;
  background-color: white;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 4px rgba(46, 139, 87, 0.1);
}

.back-btn:hover {
  background-color: #2e8b57;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(46, 139, 87, 0.2);
}

.back-btn:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(46, 139, 87, 0.1);
}

/* 두 그래프를 가로로 나란히 배치하는 컨테이너 */
.chart-container {
  display: flex; /* Flexbox로 자식 요소를 가로 배치 */
  justify-content: space-between; /* 두 그래프 사이에 여유 공간 추가 */
  align-items: center;
  margin-top: 50px;
  margin-bottom: 100px;
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

.month-txt {
  display: block; /* span을 block 요소로 변경 */
  text-align: center; /* 텍스트를 가로 중앙 정렬 */
  font-weight: bold;
  font-size: 2rem;
  font-family: "Black Han Sans", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.option-btn {
  margin-top: 50px;
  margin: 50px;
  padding: 3px;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: bold;
  /* font-size: 50px; */
  /* color: #2e8b57; */
}
</style>
