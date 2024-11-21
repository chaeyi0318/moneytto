<!-- views/MyPageView.vue -->
<template>
  <div class="my-page">
    <h1>마이 페이지</h1>
    <RouterLink :to="{ name: 'LikedSavings' }"><p>찜한 적금 보여줘</p></RouterLink></br>
    <RouterLink :to="{ name: 'AdditionalInfo' }"><p>추가 정보 입력</p></RouterLink></br>
    <Profile />
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

<style scoped></style>
