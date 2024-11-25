<template>
  <div class="my-page-container">
    <nav class="sidebar">
      
      <h2 class="sidebar-title">My Page</h2>
      <ul class="sidebar-menu">
        <li>
          <RouterLink :to="{ name: 'profile' }" class="sidebar-link" active-class="active">
            <i class="fas fa-user"></i>
            내 프로필
          </RouterLink>
        </li>
        <li>
          <RouterLink :to="{ name: 'LikedSavings' }" class="sidebar-link" active-class="active">
            <i class="fas fa-heart"></i>
            찜한 적금 모아보기
          </RouterLink>
        </li>
        <li>
          <RouterLink :to="{ name: 'SolvedQuizzes' }" class="sidebar-link" active-class="active">
            <i class="fas fa-quiz"></i>
            지난 퀴즈 모아보기
          </RouterLink>
        </li>
        <!-- <li>
          <RouterLink :to="{ name: 'AdditionalInfo' }" class="sidebar-link" active-class="active">
            <i class="fas fa-info-circle"></i>
            추가 정보 입력
          </RouterLink>
        </li> -->
      </ul>
    </nav>

    <div class="main-content">
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useAccountStore } from "@/stores/accountStore";
import { onMounted } from "vue";
import { useRouter } from "vue-router";

const accountStore = useAccountStore();
const router = useRouter();

onMounted(() => {
  if (!accountStore.isLogin) {
    router.push({ name: "Login" });
  }
});
</script>

<style scoped>
.my-page-container {
  display: flex;
  min-height: 100vh;
  background-color: #f9f9f9;
}

.sidebar {
  width: 250px;
  background-color: #2e8b57;
  color: white;
  padding: 20px;
  box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
}

.logo-container {
  text-align: center;
  margin-bottom: 20px;
}

.sidebar-logo {
  width: 120px;
  height: auto;
}

.sidebar-title {
  font-size: 1.5rem;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(255, 255, 255, 0.1);
}

.sidebar-menu {
  list-style: none;
  padding: 0;
}

.sidebar-menu li {
  margin-bottom: 15px;
}

.sidebar-link {
  color: white;
  text-decoration: none;
  font-size: 1rem;
  display: block;
  padding: 10px 15px;
  border-radius: 5px;
  transition: all 0.3s ease;
}

.sidebar-link i {
  margin-right: 10px;
  width: 20px;
}

.sidebar-link:hover {
  background-color: #3e9b67;
  transform: translateX(5px);
}

.sidebar-link.active {
  background-color: #3e9b67;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  font-weight: bold;
}

.main-content {
  flex-grow: 1;
  padding: 30px;
  background-color: white;
  margin: 20px;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
}
</style>