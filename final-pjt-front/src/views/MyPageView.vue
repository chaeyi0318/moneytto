<!-- views/MyPageView.vue -->
<template>
  <div class="my-page">
    <h1>마이 페이지</h1>
    <RouterLink :to="{ name: 'profile' }"><p>프로필 수정</p></RouterLink>
    <RouterLink :to="{ name: 'AdditionalInfo' }"><p>추가 정보 입력</p></RouterLink></br>
    <RouterLink :to="{ name: 'LikedSavings' }"><p>찜한 적금 보여줘</p></RouterLink></br>
    <RouterLink :to="{ name: 'DeleteAccount' }"><p>탈퇴</p></RouterLink>

    <!-- <RouterView /> -->
    <!-- <UserProfile /> -->
    <!-- <AdditionalInfoModal /> -->
    <!-- <DeleteAccount /> -->
  </div>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
import UserProfile from "@/components/mypage/UserProfile.vue";
import AdditionalInfoModal from "@/components/mypage/AdditionalInfo.vue";
import DeleteAccount from "@/components/mypage/DeleteAccount.vue";
import { useAccountStore } from "@/stores/accountStore";
import { onMounted } from "vue";
import { useRouter } from "vue-router";

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
