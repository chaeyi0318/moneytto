<template>
  <nav class="nav-container">
    <div class="logo-section">
      <a class="logo-text" @click="goToMain">moneytto</a>
      <!-- <img src="@/assets/logo.jpg" alt="Moneyto Logo" class="logo-img" /> -->
    </div>

    <div class="nav-links">
      <RouterLink class="nav-link" :to="{ name: 'MainView' }">Home</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'CalendarView' }"
        >Money Calendar</RouterLink
      >
      <RouterLink class="nav-link" :to="{ name: 'SavingView' }"
        >Savings</RouterLink
      >
      <RouterLink class="nav-link" :to="{ name: 'FortuneView' }"
        >Fortune</RouterLink
      >
      <RouterLink class="nav-link" :to="{ name: 'QuizView' }">Quiz</RouterLink>
      <RouterLink class="nav-link" :to="{ name: 'profile' }"
        >My Page</RouterLink
      >
    </div>

    <div class="auth-section">
      <div v-if="accountStore.isLogin" class="user-info">
        <LoginUsername class="user-name"/>
        <button class="logout-btn" @click="logOut">로그아웃</button>
      </div>
      <div v-else class="login-links">
        <!-- <RouterLink class="nav-link signup-btn" :to="{ name: 'SignupView' }"
          >회원가입</RouterLink
        > -->
        <a href="#" class="nav-link login-btn" @click.prevent="toggleLoginModal"
          >로그인</a
        >
      </div>
    </div>
  </nav>

  <RouterView />

  <div v-if="accountStore.isLoginModalOpen" class="modal-overlay" @click="toggleLoginModal">
    <div class="modal-content" @click.stop>
      <button class="close-icon" @click="toggleLoginModal">×</button>
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
import { useRouter } from "vue-router";

// Pinia 스토어 인스턴스 가져오기
const accountStore = useAccountStore();
const router = useRouter();

// 로그인 모달 상태 관리
const isLoginModalOpen = ref(false);

// 로그인 모달 열기/닫기 함수
const toggleLoginModal = () => {
  accountStore.setLoginModalOpen(!accountStore.isLoginModalOpen) // 모달 상태 토글
};
// const toggleLoginModal = () => {
//   isLoginModalOpen.value = !isLoginModalOpen.value; // 모달 상태 토글
// };

const logOut = () => {
  accountStore.logOut(); // Pinia 스토어의 logOut 함수 호출
};

const goToMain = function () {
  router.push({ name: "MainView" });
};
</script>

<style scoped>
.nav-container {
  padding: 15px 30px;
  background-color: #f5f9f7;
  box-shadow: 0 2px 12px rgba(46, 139, 87, 0.1);
  display: flex;
  align-items: center;
  justify-content: space-between;
  position: sticky;
  top: 0;
  z-index: 1000;
}

.logo-section {
  flex: 0 0 auto;
}

.logo-img {
  height: 40px;
  transition: transform 0.3s ease;
}

.logo-img:hover {
  transform: scale(1.05);
}

.logo-text {
  font-family: "Baloo Tamma 2", system-ui;
  text-decoration: none;
  cursor: pointer;
  /* font-family: "Noto Sans", system-ui; */
  font-optical-sizing: auto;
  font-weight: 600;
  font-size: 30px; /* Add this line to set the font size */
  font-style: normal;
  color: #1a5235;
}

.nav-links {
  display: flex;
  gap: 20px;
  align-items: center;
  margin: 0 30px;
}

.nav-link {
  color: #2e8b57;
  text-decoration: none;
  padding: 10px 20px;
  border-radius: 25px;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.95rem;
  position: relative;
  overflow: hidden;
}

.nav-link::before {
  content: "";
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 0;
  height: 2px;
  background-color: #2e8b57;
  transition: width 0.3s ease;
}

.nav-link:hover::before {
  width: 80%;
}

.nav-link:hover {
  background-color: #e8f5e9;
  color: #1a5235;
}

.router-link-active {
  background-color: #2e8b57;
  color: white;
}

.router-link-active::before {
  display: none;
}

.auth-section {
  display: flex;
  align-items: center;
  gap: 15px;
}

.logout-btn {
  /* background-color: #2e8b57; */
  color: #2e8b57;
  border: 2px solid #2e8b57;
  padding: 3px;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: inline-block;
}

.logout-btn:hover {
  background-color: white;
}

.user-name {
  display: inline-block;
  margin-right: 30px;
}

.login-btn,
.signup-btn {
  background-color: #2e8b57;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-btn:hover,
.signup-btn:hover {
  background-color: #1a5235;
  transform: translateY(-2px);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(3px);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 40px;
  border-radius: 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  position: relative;
  width: min(90%, 400px);
  animation: modalFadeIn 0.3s ease;
}

@keyframes modalFadeIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.close-icon {
  position: absolute;
  top: 15px;
  right: 15px;
  background: none;
  border: none;
  font-size: 24px;
  color: #2e8b57;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.close-icon:hover {
  transform: rotate(90deg);
}

@media (max-width: 768px) {
  .nav-container {
    flex-direction: column;
    padding: 15px;
  }

  .nav-links {
    flex-wrap: wrap;
    justify-content: center;
    margin: 15px 0;
  }

  .nav-link {
    padding: 8px 15px;
    font-size: 0.9rem;
  }

  .auth-section {
    width: 100%;
    justify-content: center;
  }
}
</style>
