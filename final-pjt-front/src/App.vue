<template>
  <nav class="nav-container">
    <div class="nav-links">
      <RouterLink class="nav-link" :to="{ name: 'MainView' }">홈</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'CalendarView' }">머니캘린더</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'SavingView' }">적금</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'FortuneView' }">운세</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'QuizView' }">퀴즈</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'profile' }">마이페이지</RouterLink>
    </div>

    <div class="auth-section">
      <div v-if="accountStore.isLogin" class="user-info">
        <LoginUsername />
        <button class="logout-btn" @click="logOut">로그아웃</button>
      </div>
      <div v-else class="login-links">
        <RouterLink class="nav-link" :to="{ name: 'SignupView' }">회원가입</RouterLink>
        <a href="#" class="nav-link" @click.prevent="toggleLoginModal">로그인</a>
      </div>
    </div>
  </nav>

  <RouterView />

  <div v-if="isLoginModalOpen" class="modal-overlay" @click="toggleLoginModal">
    <div class="modal-content" @click.stop>
      <button class="close-icon" @click="toggleLoginModal">×</button> <!-- X 아이콘 추가 -->
      <Login @closeModal="toggleLoginModal" />
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink, RouterView } from "vue-router";
import { useAccountStore } from "@/stores/accountStore";
import Login from "@/components/accounts/Login.vue";
import LoginUsername from "@/components/accounts/LoginUsername.vue";

// Pinia 스토어 인스턴스 가져오기
const accountStore = useAccountStore();

// 로그인 모달 상태 관리
const isLoginModalOpen = ref(false);

// 로그인 모달 열기/닫기 함수
const toggleLoginModal = () => {
  isLoginModalOpen.value = !isLoginModalOpen.value; // 모달 상태 토글
};

const logOut = () => {
  accountStore.logOut(); // Pinia 스토어의 logOut 함수 호출
};
</script>

<style scoped>
body {
  font-family: 'Roboto', sans-serif;
}

.nav-container {
  padding: 20px;
  background-color: #ffffff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  display: flex;
  align-items: center;
  justify-content: center; /* 중앙 정렬 */
  flex-wrap: wrap;
  gap: 10px;
}

.nav-links {
  display: flex;
  gap: 15px;
  align-items: center;
}

.nav-link {
  color: #2E8B57;
  text-decoration: none;
  padding: 8px 12px;
  border-radius: 20px;
  transition: all 0.3s ease;
  font-weight: 500;
}

.nav-link:hover {
  background-color: #2E8B57;
  color: white;
}

.auth-section {
  display: flex;
  align-items: center;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
}

.login-links {
  display: flex;
  gap: 15px;
  align-items: center;
}

.logout-btn {
  background-color: #2E8B57;
  color: white;
  border: none;
  padding: 5px 10px; /* 버튼 크기를 줄임 */
  font-size: 0.85rem; /* 글자 크기를 줄임 */
  border-radius: 15px; /* 둥근 모서리 유지 */
  cursor: pointer;
  transition: all 0.3s ease;
}

.logout-btn:hover {
  background-color: #1a5235;
  transform: scale(1.05);
}

.close-btn {
  background-color: #2E8B57;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-btn:hover {
  background-color: #1a5235;
  transform: scale(1.05);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.6); /* 어두운 배경 */
  display: flex;
  justify-content: center;
  align-items: center; /* 중앙 정렬 */
}

/* X 아이콘 스타일 */
.close-icon {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 1.5rem;
  font-weight: bold;
  color: #2e8b57; /* 로고 색상과 통일 */
  cursor: pointer;
}

.close-icon:hover {
  color: #1a5235; /* 호버 시 색상 변경 */
}

.modal-content {
  position: relative; /* 닫기 버튼 위치를 위해 필요 */
  width: min(90%, 400px); /* 화면 크기에 따라 최대 너비 제한 */
  background-color: white;
  padding: 30px;
  border-radius: 15px;
}

.router-link-active {
 background-color: #2E8B57; 
 color:white; 
}

@media (max-width:768px) { 
 .nav-container { 
   flex-direction:column; 
   text-align:center; 
 } 
 
 .nav-links { 
   flex-wrap:wrap; 
   justify-content:center; 
 } 
 
 .auth-section { 
   margin-top :15px; 
   width :100%; 
   justify-content:center; 
 } 
 
 .user-info, .login-links { 
   flex-direction :column; 
   gap :10px; 
 } 
}
</style>
