<!-- components/UserProfile.vue -->
<template>
  <section class="profile-section">
    <h2>프로필 정보</h2>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="username">아이디:</label>
        <input id="username" :value="accountStore.user?.username" disabled />
      </div>
      <div>
        <label for="email">이메일:</label>
        <input id="email" v-model="profile.email" type="email" required />
      </div>
      <div>
        <label for="nickname">닉네임:</label>
        <input id="nickname" v-model="profile.nickname" type="text" required />
      </div>
      <button type="submit">프로필 업데이트</button>
    </form>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAccountStore } from "@/stores/accountStore";

const accountStore = useAccountStore();

const profile = ref({
  email: "",
  nickname: "",
});

onMounted(() => {
  if (accountStore.user) {
    profile.value.email = accountStore.user.email || "";
    profile.value.nickname = accountStore.user.nickname || "";
  }
});

const updateProfile = async () => {
  try {
    await accountStore.updateUserInfo(profile.value);
    alert("프로필이 업데이트되었습니다.");
  } catch (error) {
    alert("프로필 업데이트에 실패했습니다.");
  }
};
</script>
