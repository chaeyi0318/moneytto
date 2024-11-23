<template>
  <div class="my-page-container">
    <!-- 왼쪽 네비게이션 바 -->
    <nav class="sidebar">
      <h2 class="sidebar-title">마이페이지</h2>
      <ul class="sidebar-menu">
        <li>
          <RouterLink :to="{ name: 'profile' }" class="sidebar-link">
            내 프로필
          </RouterLink>
        </li>
        <!-- <li>
          <RouterLink :to="{ name: 'profile-update' }" class="sidebar-link">
            회원정보 수정
          </RouterLink>
        </li> -->
        <li>
          <RouterLink :to="{ name: 'LikedSavings' }" class="sidebar-link">
            찜한 적금 모아보기
          </RouterLink>
        </li>
        <li>
          <RouterLink :to="{ name: 'SolvedQuizzes' }" class="sidebar-link">
            지난 퀴즈 모아보기
          </RouterLink>
        </li>
        <li>
          <RouterLink :to="{ name: 'AdditionalInfo' }" class="sidebar-link">
            추가 정보 입력(추후 삭제)
          </RouterLink>
        </li>
      </ul>
    </nav>

    <!-- 오른쪽 콘텐츠 영역 -->
    <div class="main-content">
    <!-- <Profile /> -->
      <RouterView />
    </div>
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import { useAccountStore } from "@/stores/accountStore";
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import Profile from "@/components/mypage/Profile.vue";

const accountStore = useAccountStore();
const router = useRouter();

onMounted(() => {
  if (!accountStore.isLogin) {
    // 로그인되지 않은 경우 로그인 페이지로 리다이렉트
    router.push({ name: "Login" });
  }
});
</script>

<style scoped>
/* 전체 컨테이너 */
.my-page-container {
  display: flex;
  min-height: 100vh;
  background-color: #f9f9f9;
}

/* 사이드바 스타일 */
.sidebar {
  width: 250px;
  background-color: #2e8b57;
  color: white;
  padding: 20px;
  box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.1);
}

.sidebar-title {
  font-size: 1.5rem;
  margin-bottom: 20px;
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
}

.sidebar-link:hover {
  text-decoration: underline;
}

/* 메인 콘텐츠 스타일 */
.main-content {
  flex-grow: 1;
  padding: 30px;
}
</style>