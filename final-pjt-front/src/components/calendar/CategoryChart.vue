<template>
  <div class="outer-container">
    <div class="chart-container">
      <apexchart
        type="pie"
        :options="chartOptions"
        :series="series"
      ></apexchart>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import api from "@/stores/api";
import VueApexCharts from "vue3-apexcharts";

// props로 yearMonth를 전달받음
const props = defineProps({
  yearMonth: {
    type: String,
    required: true,
  },
});

// 반응형 변수 정의
const categorySumValue = ref([]); // 카테고리별 데이터 저장
const total_price = ref(0); // 총 소비 금액

// API 호출 함수
const fetchPosts = async (yearMonth) => {
  try {
    const response = await api.get("/posts/post-list/", {
      params: { yearMonth },
    });

    // 데이터 업데이트
    categorySumValue.value = response.data.category_totals || [];
    total_price.value = response.data.total_price || 0;
  } catch (error) {
    console.error("API 요청 실패:", error);
    categorySumValue.value = [];
    total_price.value = 0;
  }
};

// series 데이터 계산
const series = computed(() => {
  return categorySumValue.value.map((item) => item.total_price);
});

// 차트 라벨 계산
const chartLabels = computed(() => {
  return categorySumValue.value.map((item) => item.category_name);
});

// 차트 옵션 설정
const chartOptions = ref({
  chart: {
    type: "pie",
  },
  labels: chartLabels.value,
  // colors: [
  //   'rgba(46, 139, 87, 0.8)',  // 메인 녹색 (80% 불투명도)
  //   'rgba(192, 216, 168, 0.8)', // 연한 녹색
  //   'rgba(26, 82, 53, 0.8)',    // 진한 녹색
  //   'rgba(232, 245, 233, 0.8)', // 아주 연한 녹색
  //   'rgba(76, 175, 80, 0.8)',   // 밝은 녹색
  //   'rgba(129, 199, 132, 0.8)', // 중간 녹색
  //   'rgba(165, 214, 167, 0.8)', // 파스텔 녹색
  //   'rgba(200, 230, 201, 0.8)', // 연한 파스텔 녹색
  // ],
  colors: [
    "rgba(190, 220, 116, 0.8)", // #BEDC74 with 80% opacity
    "rgba(0, 2, 161, 0.8)", // #387F39 with 80% opacity
    "rgba(56, 127, 57, 0.8)", // #387F39 with 80% opacity
    "rgba(255, 138, 138, 0.8)", // #FF8A8A with 80% opacity
    "rgba(244, 222, 179, 0.8)", // #F4DEB3 with 80% opacity
    "rgba(255, 112, 171, 0.8)", // #FF70AB with 80% opacity
    "rgba(139, 93, 255, 0.8)", // #8B5DFF with 80% opacity
    "rgba(255, 219, 92, 0.8)", // #FFDB5C with 80% opacity
    "rgba(195, 255, 147, 0.8)", // #C3FF93 with 80% opacity
  ],
  legend: {
    position: "bottom",
    show: true,
    formatter: function (val, opts) {
      return chartLabels.value[opts.seriesIndex];
    },
  },
  dataLabels: {
    enabled: true,
    formatter: function (val, opts) {
      return chartLabels.value[opts.seriesIndex];
    },
  },
  tooltip: {
    y: {
      formatter: (value) => `₩${value.toLocaleString()}`,
    },
  },
  plotOptions: {
    pie: {
      dataLabels: {
        offset: -5,
      },
    },
  },
});

// watch를 사용해 props.yearMonth 변경 시 데이터 다시 가져오기
watch(
  () => props.yearMonth,
  (newYearMonth) => {
    fetchPosts(newYearMonth); // 새로운 yearMonth로 API 호출
  },
  { immediate: true } // 컴포넌트가 마운트될 때도 실행
);

// 컴포넌트가 처음 마운트될 때 초기 데이터 가져오기
onMounted(() => {
  fetchPosts(props.yearMonth); // 초기 yearMonth로 데이터 가져오기
});
</script>

<style scoped>
.outer-container {
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.chart-container {
  width: 400px; /* 원하는 너비 */
  height: 300px; /* 원하는 높이 */
}
</style>
