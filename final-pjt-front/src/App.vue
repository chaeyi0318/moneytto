<template>
  <nav>
    <RouterLink :to="{ name: 'MainView' }">메인</RouterLink> |
    <RouterLink :to="{ name: 'CalendarView' }">가계부</RouterLink> |
    <RouterLink :to="{ name: 'SavingView' }">적금</RouterLink> |
    <RouterLink :to="{ name: 'FortuneView' }">운세</RouterLink> |
    <RouterLink :to="{ name: 'QuizView' }">금융퀴즈</RouterLink> |
    <RouterLink :to="{ name: 'MyPageView' }">마이페이지</RouterLink> |

    <!-- Pinia 스토어의 로그인 상태에 따른 조건부 렌더링 -->
    <div v-if="accountStore.isLogin">
      <LoginUsername />
      <!-- <span>{{ accountStore.user.nickname }}님 환영합니다!</span> -->
      <button @click="logOut">로그아웃</button>
    </div>
    <div v-else>
      <RouterLink :to="{ name: 'SignupView' }">회원가입</RouterLink> |
      <a href="#" @click.prevent="toggleLoginModal">로그인</a>
    </div>
  </nav>

  <!-- 페이지 라우터 뷰 -->
  <RouterView />

  <!-- 로그인 모달 -->
  <div v-if="isLoginModalOpen" class="modal-overlay" @click="toggleLoginModal">
    <div class="modal-content" @click.stop>
      <!-- Login 컴포넌트에서 로그인 성공 시 모달 닫기 -->
      <Login @closeModal="toggleLoginModal" />
      <!-- closeModal 이벤트 연결 -->
      <button @click="toggleLoginModal">닫기</button>
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

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
}
</style>
