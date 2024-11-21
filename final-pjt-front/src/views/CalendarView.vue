<template>
  <div class="calendar">
    <!-- 달력 네비게이션 -->
    <nav>
      <h3>{{ cal.yearText }} - {{ cal.monthText }}</h3>
      <div class="navs">
        <button @click="prevMonth">이전</button>
        <button @click="nextMonth">다음</button>
      </div>
    </nav>

    <!-- 요일 표시 -->
    <section class="dow">
      <div v-for="day in days" :key="day" class="day">{{ day }}</div>
    </section>

    <!-- 달력 본문 -->
    <section class="body">
      <div v-for="week in cal.getWeeks()" :key="week" class="week">
        <div
          v-for="date in week.days()"
          :key="date.ymdText"
          class="cell"
          :class="{
            oob: !cal.containsDate(date),
            today: cal.isToday(date),
            sunday: date.weekOffset === 0,
            saturday: date.weekOffset === 6,
          }"
        >
          <!-- 날짜 표시 -->
          <span class="date" @click.stop="goToNewPost(date)">
            {{ date.date }}
          </span>
          <div v-if="getImageForDate(date)" class="post-image">
            <img :src="getImageForDate(date)" alt="Post Image" @click.prevent="toggleDetailModal(date)"/>
          </div>
        </div>
      </div>
    </section>

    <!-- 모달 컴포넌트 -->
    <Modal
      v-if="isModalOpen"
      :date="selectedDateTitle"
      @closeModal="toggleDetailModal()"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { Calendar } from "@/components/calendar/Calendar";
import Modal from "@/components/calendar/Modal.vue"; // 모달 컴포넌트 가져오기
import { useCalendarStore } from "@/stores/calendarStore";
import api from "@/stores/api";

const days = ["일", "월", "화", "수", "목", "금", "토"];
const currentYear = new Date().getFullYear();
const currentMonth = new Date().getMonth() + 1;

// console.log(currentMonth, " 월입니다");
// console.log(currentYear, " 년 입니다.");

let cal = ref(Calendar.fromYm(currentYear, currentMonth));
const router = useRouter();
const dateStore = useCalendarStore();

const posts = ref([])   // 게시글 데이터

// 이전 달로 이동
const prevMonth = () => {
    cal.value = cal.value.prevMonth();
    const yearMonth = cal.value.yearText + '-' + cal.value.monthText;
    console.log(`${yearMonth}`);

    fetchPosts(yearMonth); // API 호출
};


// 다음 달로 이동
const nextMonth = () => {
    cal.value = cal.value.nextMonth();
    const yearMonth = cal.value.yearText + '-' + cal.value.monthText
    console.log(`다음 달: ${yearMonth}`)

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
        console.log('게시글 데이터:', response.data)
        posts.value = response.data // 게시글 데이터를 상태에 저장
    })
    .catch((error) => {
        console.error('API 요청 실패:', error)
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

onMounted(() => {
    const yearMonth = `${cal.value.yearText}-${cal.value.monthText}`
    fetchPosts(yearMonth)
})
</script>

<style scoped>
.calendar {
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
</style>
