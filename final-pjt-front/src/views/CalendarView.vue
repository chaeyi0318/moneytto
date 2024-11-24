<template>
  <nav>
    <form @submit.prevent="submitBudget">
      <span>{{ cal.yearText }} - {{ cal.monthText }} 예산 </span>
      <input type="number" v-model="amount" placeholder="예산 입력" />
      <input type="submit" value="설정">
    </form>
    <span>{{ cal.monthText }}월 총 소비 금액 : {{ total_price }}</span>

    <h3>{{ cal.yearText }} - {{ cal.monthText }}</h3>
    <div class="navs">
      <button @click="prevMonth">이전</button>
      <button @click="nextMonth">다음</button>
    </div>
  </nav>
  <div class="main">
    <div class="calendar">
      <!-- 달력 네비게이션 -->
      <!-- 요일 표시 -->
      <section class="dow">
        <div v-for="day in days" :key="day" class="day">{{ day }}</div>
      </section>

      <!-- 달력 본문 -->
      <section class="body">
        <div v-for="week in cal.getWeeks()" :key="week" class="week">
          <div v-for="date in week.days()" :key="date.ymdText" class="cell" :class="{
            oob: !cal.containsDate(date),
            today: cal.isToday(date),
            sunday: date.weekOffset === 0,
            saturday: date.weekOffset === 6,
          }">
            <!-- 날짜 표시 -->
            <span class="date" @click.stop="goToNewPost(date)">
              {{ date.date }}
            </span>
            <div v-if="getImageForDate(date)" class="post-image">
              <img :src="getImageForDate(date)" alt="Post Image" @click.prevent="toggleDetailModal(date)" />
            </div>
          </div>
        </div>
      </section>
    </div>

    <div class="container">
      <!-- 항아리 -->
      <div class="jar">
        <div class="water" :style="{ height: fillLevel + '%', backgroundColor: overflow ? 'red' : 'lightblue' }"></div>
      </div>
    </div>
  </div>
  <Waterwave />
  <!-- 모달 컴포넌트 -->
  <Modal v-if="isModalOpen" :date="selectedDateTitle" @closeModal="toggleDetailModal()" />
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { Calendar } from "@/components/calendar/Calendar";
import Modal from "@/components/calendar/Modal.vue"; // 모달 컴포넌트 가져오기
import { useCalendarStore } from "@/stores/calendarStore";
import { useAccountStore } from "@/stores/accountStore";
import api from "@/stores/api";
import Bot from "@/components/bot/Bot.vue";
import Waterwave from "@/components/calendar/Waterwave.vue";

const accountStore = useAccountStore()
const days = ["일", "월", "화", "수", "목", "금", "토"];
const currentYear = new Date().getFullYear();
const currentMonth = new Date().getMonth() + 1;
const loginUser = accountStore.user.id

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
  cal.value = cal.value.prevMonth()
  const yearMonth = cal.value.yearText + '-' + cal.value.monthText

  fetchPosts(yearMonth)
};

// 다음 달로 이동
const nextMonth = () => {
  cal.value = cal.value.nextMonth()
  const yearMonth = cal.value.yearText + '-' + cal.value.monthText

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
      const categoryData = response.data.category_totals
      const postsData = response.data.posts || []

      posts.value = postsData
      categorySumValue.value = categoryData

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

  const post = posts.value.find(post => post.expenses_date === formattedDate);

  return post ? `${baseURL}${post.image}` : null;
}

const submitBudget = async () => {
  try {
    const data = {
      year: parseInt(cal.value.yearText),
      month: parseInt(cal.value.monthText),
      amount: amount.value,
    }
    const response = await api.post('/accounts/update-budget/', data)

    if (response.status === 201 || response.status === 200) {
      alert("예산 저장 성공")
      amount.value = response.data.amount
    } else {
      alert("예산 저장 실패")
    }
  } catch (error) {
    console.error("오류 : ", error)
    alert("서버와 통신 중 문제가 발생했습니다.")
  }
}

onMounted(() => {
  const yearMonth = `${cal.value.yearText}-${cal.value.monthText}`
  fetchPosts(yearMonth)
  amount
})

const fillLevel = computed(() => {
  if (amount.value === 0) return 0; // 예산이 0이면 물 높이를 0으로 설정
  return Math.min((total_price.value / amount.value) * 100, 100); // 최대 100%
});

// 물이 넘치는지 여부
const overflow = computed(() => {
  return total_price.value > amount.value; // 소비 금액이 예산을 초과하면 true
});

</script>

<style scoped>
.main {
  border: yellow 5px solid;
  display: flex;
  /* Flexbox 사용 */
  justify-content: space-between;
  /* 두 요소 간 간격 조정 */
  align-items: flex-start;
  /* 세로 정렬 */
  gap: 20px;
  /* 달력과 항아리 간격 */
}

.calendar {
  width: 75%;
  display: flex;
  flex-direction: column;
}

.navs {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.navs button {
  padding: 5px 10px;
}

.dow {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
  text-align: center;
}

.dow .day {
  font-weight: bold;
  padding-bottom: 10px;
}

.body {
  display: grid;
  grid-template-columns: repeat(7, 1fr);
}

.week {
  display: contents;
}

.cell {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 80px;
  border-bottom: 1px solid #e0e0e0;
}

.date {
  display: inline-block;
  width: 40px;
  height: 40px;
  line-height: 40px;
  text-align: center;
  border-radius: 50%;
}

.oob .date {
  color: #ccc;
}

.today .date {
  background-color: lightblue;
}

.sunday .date {
  color: red;
}

.saturday .date {
  color: blue;
}

/* 마우스 오버 시 날짜 셀 강조 */
.cell:hover .date {
  background-color: rgba(0, 0, 255, 0.1);
}

.post-image img {
  width: 40px;
  height: 40px;
  border-radius: 50%;
}

.container {
  width: 25%;
  height: 100%;
  border: #000 solid 1px;
}

.jar {
  position: relative;
  width: 200px;
  height: 300px;
  border: 2px solid #000;
  margin: auto;
  overflow: hidden;
  /* 물 넘침 방지 */
}

.water {
  position: absolute;
  bottom: 0;
  width: 100%;
  transition: height 0.5s ease, background-color 0.5s ease;
  /* 부드러운 애니메이션 */
}

.controls {
  margin-top: 20px;
}

.warning {
  color: red;
}
</style>
