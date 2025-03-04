<template>
  <div class="main">
    <!-- 달력 -->
    <div class="calendar">
      <nav class="nav-container">
        <div class="budget-container">
          <form
            v-if="isBudgetFormVisible"
            @submit.prevent="submitBudget"
            class="budget-form"
          >
            <input type="number" v-model="amount" placeholder="예산 입력" />
            <input type="submit" value="저장" class="budget-form-btn" />
          </form>
          <span v-else>예산: {{ amount }}원</span>
          <button
            v-if="!isBudgetFormVisible"
            @click.prevent="showBudgetForm"
            class="budget-form-btn"
          >
            <i class="bi bi-pencil"></i>
          </button>
        </div>

        <div class="report">
          <button @click.prevent="goToReport">소비 분석 보기</button>
        </div>
      </nav>
      <div class="navs">
        <button
          @click="prevMonth"
          class="next-btn bi bi-caret-left-fill"
        ></button>
        <span class="date-span date-text"
          >{{ cal.yearText }}. {{ cal.monthText }}</span
        >
        <button
          @click="nextMonth"
          class="next-btn bi bi-caret-right-fill"
        ></button>
      </div>
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
              <img
                :src="getImageForDate(date)"
                alt="Post Image"
                @click.prevent="toggleDetailModal(date)"
              />
            </div>
          </div>
        </div>
      </section>
    </div>

    <!-- 물결 애니메이션 -->
    <Waterwave
      v-if="amount && total_price"
      class="waterwave-overlay"
      :amount="amount"
      :total_price="total_price"
    />

    <!-- 모달 컴포넌트 -->
    <Modal
      v-if="isModalOpen"
      :date="selectedDateTitle"
      @closeModal="toggleDetailModal()"
    />
  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from "vue";
import { useRouter } from "vue-router";
import { useRoute } from "vue-router";
import { Calendar } from "@/components/calendar/Calendar";
import Modal from "@/components/calendar/Modal.vue"; // 모달 컴포넌트 가져오기
import { useCalendarStore } from "@/stores/calendarStore";
import { useAccountStore } from "@/stores/accountStore";
import api from "@/stores/api";
import Waterwave from "@/components/calendar/Waterwave.vue";

const accountStore = useAccountStore();
const days = ["SUN", "MON", "TUE", "WED", "THU", "FRI", "SAT"];
const currentYear = new Date().getFullYear();
const currentMonth = String(new Date().getMonth() + 1).padStart(2, "0"); // 두 자리 형식으로 변환
const loginUser = accountStore.user.id;

let cal = ref(Calendar.fromYm(currentYear, currentMonth));

const router = useRouter();
const route = useRoute();

const dateStore = useCalendarStore();

const posts = ref([]); // 게시글 데이터
const calendarOwnerId = ref(0); // 캘린더 주인 pk
const amount = ref(0);
const total_price = ref(0);
const categorySumValue = ref([]);

// 쿼리에서 날짜 가져오기 (없으면 오늘 날짜 사용)
const selectedDate = ref(
  route.query.date || new Date().toISOString().split("T")[0]
);

const handlePostDeleted = (deletedId) => {
  posts.value = posts.value.filter((post) => post.id !== deletedId);
};

// 이전 달로 이동
const prevMonth = () => {
  cal.value = cal.value.prevMonth();
  const yearMonth = cal.value.yearText + "-" + cal.value.monthText;

  fetchPosts(`${cal.value.yearText}-${cal.value.monthText}`);
};

// 다음 달로 이동
const nextMonth = () => {
  cal.value = cal.value.nextMonth();
  const yearMonth = cal.value.yearText + "-" + cal.value.monthText;

  fetchPosts(`${cal.value.yearText}-${cal.value.monthText}`);
};

// 모달 상태 및 선택된 날짜 제목 관리
const isModalOpen = ref(false);
let selectedDateTitle = ref("");

// 모달 토글 (열기/닫기)
const toggleDetailModal = (date) => {
  if (date) {
    if (typeof date === "string") {
      const [year, month, day] = date.split("-");
      selectedDateTitle.value = `${year}-${month}-${day}`;
    } else if (date.year && date.month && date.date) {
      selectedDateTitle.value = `${date.year}-${String(date.month).padStart(2, "0")}-${String(date.date).padStart(2, "0")}`;
    }
  }

  // 모달 상태 토글
  isModalOpen.value = !isModalOpen.value;
};

// 날짜 클릭 시 게시글 작성 페이지로 이동
const goToNewPost = (date) => {
  const formattedDate = `${date.year}-${String(date.month).padStart(
    2,
    "0"
  )}-${String(date.date).padStart(2, "0")}`;

  // 선택한 날짜 저장
  dateStore.setSelectedDate(formattedDate);

  // 게시글 작성 페이지로 이동
  router.push({
    name: "PostPageView",
    params: { date: formattedDate },
  });
};

const fetchPosts = (yearMonth) => {
  api
    .get("/posts/post-list/", {
      params: { yearMonth },
    })
    .then((response) => {
      const categoryData = response.data.category_totals;
      const postsData = response.data.posts || [];

      posts.value = postsData;
      categorySumValue.value = categoryData;
      total_price.value = response.data.total_price || 0;
      amount.value = postsData[0].amount || 0;

      if (postsData.length > 0) {
        calendarOwnerId.value = postsData[0].owner || 0;
      } else {
        calendarOwnerId.value = 0;
        amount.value = 0;
      }
    })
    .catch((error) => {
      console.error("API 요청 실패:", error);
      posts.value = [];
      calendarOwnerId.value = 0;
      amount.value = 0;
      total_price.value = 0;
    });
};

const baseURL = "http://localhost:8000";

const getImageForDate = (date) => {
  const formattedDate = `${date.year}-${String(date.month).padStart(
    2,
    "0"
  )}-${String(date.date).padStart(2, "0")}`;

  const post = posts.value.find((post) => post.expenses_date === formattedDate);

  return post ? `${baseURL}${post.image}` : null;
};

const submitBudget = async () => {
  try {
    const data = {
      year: parseInt(cal.value.yearText),
      month: parseInt(cal.value.monthText),
      amount: amount.value,
    };
    const response = await api.post("/accounts/update-budget/", data);

    if (response.status === 201 || response.status === 200) {
      amount.value = response.data.amount;
      alert(amount.value + "원으로 예산을 설정했습니다.");
      isBudgetFormVisible.value = false;
    } else {
      alert("예산 저장을 실패했습니다.");
    }
  } catch (error) {
    console.error("오류 : ", error);
    alert("서버와 통신 중 문제가 발생했습니다.");
  }
};

const goToReport = () => {
  router.push({ name: "ReportView" });
};

const isBudgetFormVisible = ref(false);
const showBudgetForm = () => {
  isBudgetFormVisible.value = !isBudgetFormVisible.value;
};

onMounted(() => {
  const [year, month] = selectedDate.value.split("-");
  cal.value = Calendar.fromYm(parseInt(year), parseInt(month))
  fetchPosts(`${year}-${month}`)
  amount.value = 0, total_price, currentYear, currentMonth
  const query = route.query

  if (query.openModal && query.date) {
    selectedDateTitle.value = query.date
    toggleDetailModal(query.date)
    isModalOpen.value = true
  }
  // fetchPosts(`${cal.value.yearText}-${cal.value.monthText}`)
});
</script>

<style scoped>
.main {
  height: 100%;
  position: relative;
  width: 70%;
  margin: 40px auto;
}

.calendar {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  position: relative;
  /* box-shadow: 0 4px 12px rgba(45, 122, 49, 0.1); */
}

.navs {
  display: flex;
  width: 100%;
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
  background-color: #f8faf6;
  border-radius: 10px;
  padding-top: 8px;
  z-index: -1;
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
  position: relative;
  justify-content: center;
  align-items: center;
  height: 120px;
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

.cell .date {
  position: relative;
  z-index: 2;
}

.oob .date {
  color: #ccc;
}

.today .date {
  background-color: #c0d8a8;
}

.sunday .date {
  color: rgb(255, 96, 96);
}

.saturday .date {
  color: rgb(76, 76, 255);
}

/* 마우스 오버 시 날짜 셀 강조 */
.cell:hover .date {
  /* border: #2e8b57 2px solid; */
  background-color: rgba(255, 255, 255, 0.7); /* 0.5는 50% 투명도를 의미 */
  cursor: pointer;
}

.post-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
}

.post-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: 0;
}
.waterwave-overlay {
  left: 0;
  width: 100%;
  pointer-events: none;
  bottom: 0;
  left: 0;
  width: 100%;
  position: absolute;
  z-index: -1;
  opacity: 0.4; /* 0부터 1 사이의 값으로 불투명도 조절 */
  transition: opacity 0.3s ease; /* 부드러운 전환 효과 추가 */
}

.next-btn {
  margin: 20px;
  padding: 10px 20px;
  cursor: pointer;
  transition: all 0.3s ease;
  /* color: #2e8b57; */
  border: none;
  border-radius: 50%;
  background: none;
}

.option-btn {
  margin: 20px;
  padding: 10px 20px;
  border: 2px solid #2e8b57;
  background-color: white;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #2e8b57;
}

.submit-btn {
  text-align: center;
  background-color: #2e8b57;
  color: white;
  padding: 5px;
  margin: 10px;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  font-size: 1em;
  transition: all 0.3s ease;
}

input[type="number"] {
  width: 200px;
  padding: 3px;
  border: 2px solid #2e8b57;
  border-radius: 8px;
  font-size: 1em;
}

.nav-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
}

/* 총 소비 금액 스타일 */
.total-price-div {
  font-size: 1rem;
  /* font-weight: bold; */
}

form > span {
  /* font-weight: bold; */
  font-size: 1.1rem;
}

.date-span {
  font-size: 2rem;
  font-family: "Black Han Sans", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.report {
  margin-left: auto; /* 오른쪽으로 밀어내기 */
}

.report button {
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

.report button:hover {
  background-color: #2e8b57;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(46, 139, 87, 0.2);
}

.report button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(46, 139, 87, 0.1);
}

button:hover {
  color: white;
  background-color: #2e8b57;
}

.budget-container {
  display: flex;
  align-items: center;
  justify-content: flex-start; /* 왼쪽 정렬로 변경 */
  gap: 5px; /* 요소들 사이 간격 조정 */
}

.budget-form-btn {
  width: 28px; /* 버튼 크기 축소 */
  height: 28px; /* 버튼 크기 축소 */
  padding: 2px; /* 패딩 축소 */
  font-size: 0.8em; /* 폰트 크기 축소 */
  border: none;
  border-radius: 50%; /* 동그란 버튼 */
  background-color: white;
  color: #2e8b57;
  display: flex;
  align-items: center;
  justify-content: center;
}

.budget-form {
  display: flex;
  align-items: center;
  gap: 5px;
}

.submit-btn {
  padding: 3px 8px;
  font-size: 0.9em;
}
</style>
