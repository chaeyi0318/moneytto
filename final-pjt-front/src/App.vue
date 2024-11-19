<template>
  <nav>
    <RouterLink :to="{ name: 'MainView' }">메인</RouterLink> | 
    <RouterLink :to="{ name: 'CalendarView' }">가계부</RouterLink> | 
    <RouterLink :to="{ name: 'SavingView' }">적금</RouterLink> | 
    <RouterLink :to="{ name: 'FortuneView' }">운세</RouterLink> | 
    <RouterLink :to="{ name: 'QuizView' }">금융퀴즈</RouterLink> |
    <RouterLink :to="{ name: 'MyPageView' }">마이페이지</RouterLink> | 
    <RouterLink :to="{ name: 'SignupView' }">회원가입</RouterLink> | 
    <a href="#" @click.prevent="toggleLoginModal">로그인</a>
  </nav>
  <RouterView/>

  <div v-show="isLoginModalOpen" class="modal-overlay" @click="toggleLoginModal">
    <div class="modal-content" @click.stop>
      <!-- Login.vue 컴포넌트를 여기서 불러옴 -->
      <Login />
      <!-- 닫기 버튼 -->
      <button @click="toggleLoginModal">닫기</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { RouterLink, RouterView } from "vue-router"
import Login from "./components/accounts/Login.vue"

// 모달 상태 관리
const isLoginModalOpen = ref(false)

const toggleLoginModal = () => {
  isLoginModalOpen.value = !isLoginModalOpen.value;
}
</script>

<style scoped>
/* 모달 오버레이 (배경 어둡게 처리) */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

/* 모달 콘텐츠 */
.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
}
</style>