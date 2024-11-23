<template>
    <div class="outer-container">
      <div class="chart-container">
        <apexchart type="pie" :options="chartOptions" :series="series"></apexchart>
      </div>
    </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { Calendar } from "@/components/calendar/Calendar";
import { useCalendarStore } from "@/stores/calendarStore";
import { useAccountStore } from "@/stores/accountStore";
import api from "@/stores/api";
import VueApexCharts from 'vue3-apexcharts'


const accountStore = useAccountStore()
const days = ["일", "월", "화", "수", "목", "금", "토"];
const currentYear = new Date().getFullYear();
const currentMonth = new Date().getMonth() + 1;
const loginUser = accountStore.user.id
// console.log(currentMonth, " 월입니다");
// console.log(currentYear, " 년 입니다.");

let cal = ref(Calendar.fromYm(currentYear, currentMonth));
const router = useRouter();
const dateStore = useCalendarStore();

const posts = ref([])   // 게시글 데이터
const calendarOwnerId = ref(0)    // 캘린더 주인 pk
const amount = ref(0)
const total_price = ref(0)
const categorySumValue = ref([])



// 이전 달로 이동
const prevMonth = () => {
    cal.value = cal.value.prevMonth();
    const yearMonth = cal.value.yearText + '-' + cal.value.monthText;
    // console.log(`${yearMonth}`);

    fetchPosts(yearMonth); // API 호출
};

// 다음 달로 이동
const nextMonth = () => {
    cal.value = cal.value.nextMonth();
    const yearMonth = cal.value.yearText + '-' + cal.value.monthText
    // console.log(`다음 달: ${yearMonth}`)

    fetchPosts(yearMonth)
}

// 모달 상태 및 선택된 날짜 제목 관리
const isModalOpen = ref(false)
let selectedDateTitle = ref("")

// 모달 토글 (열기/닫기)
const toggleDetailModal = (date) => {
  if (date) {
    selectedDateTitle.value = `${date.year}-${String(date.month).padStart(2, "0")}-${String(date.date).padStart(2, "0")}`
  }
  isModalOpen.value = !isModalOpen.value // 현재 상태에 따라 토글
}

// 날짜 클릭 시 게시글 작성 페이지로 이동
const goToNewPost = (date) => {
  const formattedDate = `${date.year}-${String(date.month).padStart(2, "0")}-${String(date.date).padStart(2, "0")}`

  // 선택한 날짜 저장
  dateStore.setSelectedDate(formattedDate)

  // 게시글 작성 페이지로 이동
  router.push({
    name: "PostPageView",
    params: { date: formattedDate },
  })
}

const fetchPosts = (yearMonth) => {
    api.get('/posts/post-list/', {
        params: { yearMonth }
    })
    .then((response) => {
        // console.log(response.data)
        const categoryData = response.data.category_totals
        const postsData = response.data.posts || []
        // console.log(response.data.category_totals)

        posts.value = postsData
        categorySumValue.value = categoryData

        // console.log(categorySumValue.value)

        if (postsData.length > 0) {
        calendarOwnerId.value = postsData[0].owner || 0
        amount.value = postsData[0].amount || 0
      } else {
        calendarOwnerId.value = 0
        amount.value = 0
      }

      total_price.value = response.data.total_price || 0
    })
    .catch((error) => {
      console.error('API 요청 실패:', error)
      posts.value = []
      calendarOwnerId.value = 0
      amount.value = 0
      total_price.value = 0
    })
}

const baseURL = "http://localhost:8000"

const getImageForDate = (date) => {
  const formattedDate = `${date.year}-${String(date.month).padStart(2, "0")}-${String(date.date).padStart(2, "0")}`

  // posts 데이터에서 해당 날짜의 게시글 찾기
  const post = posts.value.find(post => post.expenses_date === formattedDate);

  // API 응답의 경로를 그대로 사용
  return post ? `${baseURL}${post.image}` : null;
}




const submitBudget = async () => {
  try {
    // console.log("현재 연도:", cal.value.yearText);
    // console.log("현재 월:", cal.value.monthText);
    const data= {
      year: parseInt(cal.value.yearText),
      month: parseInt(cal.value.monthText),
      amount: amount.value,
    }
    const response = await api.post('/accounts/update-budget/', data)
    
    if (response.status === 201 || response.status === 200) {
      alert("예산 저장 성공")
      amount.value = response.data.amount
      // console.log(response.data)
    } else {
      alert("예산 저장 실패")
    }
  } catch (error) {
    console.error("오류 : ", error)
    alert("서버와 통신 중 문제가 발생했습니다.")
  }
}

// series 데이터 계산
const series = computed(() => {
  return categorySumValue.value.map(item => item.total_price)
})
const chartLabels = computed(() => categorySumValue.value.map(item => item.category_name))

// 차트 옵션 설정
const chartOptions = ref({
  chart: {
    type: 'pie',
  },
  labels: chartLabels.value, // computed 값을 직접 할당
  colors: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF', 
          '#FF9F40', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0',
          '#9966FF', '#FF9F40', '#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0'],
  legend: {
    position: 'bottom',
    show: true,
    formatter: function(val, opts) {
      return chartLabels.value[opts.seriesIndex].toLocaleString()
      // return chartLabels.value[opts.seriesIndex] + ": ₩" + opts.w.globals.series[opts.seriesIndex].toLocaleString()
    }
  },
  dataLabels: {
    enabled: true,
    formatter: function (val, opts) {
      return chartLabels.value[opts.seriesIndex]
    }
  },
  tooltip: {
    y: {
      formatter: (value) => `₩${value.toLocaleString()}`
    }
  },
  plotOptions: {
    pie: {
      dataLabels: {
        offset: -5
      }
    }
  }
})

// fetchPosts 함수 내에서 데이터가 업데이트될 때마다 차트 옵션도 업데이트
watch(categorySumValue, (newValue) => {
  chartOptions.value.labels = newValue.map(item => item.category_name)
}, { deep: true })


onMounted(() => {
    const yearMonth = `${cal.value.yearText}-${cal.value.monthText}`
    fetchPosts(yearMonth)
    amount
})
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
  width: 400px;      /* 원하는 너비 */
  height: 300px;     /* 원하는 높이 */
}
</style>