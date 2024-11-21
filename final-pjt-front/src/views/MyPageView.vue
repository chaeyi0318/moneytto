<!-- views/MyPageView.vue -->
<template>
  <div class="my-page">
    <h1>마이 페이지</h1>
    <UserProfile />
    <AdditionalInfoModal />
    <DeleteAccount />
  </div>
</template>

<script setup>
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
