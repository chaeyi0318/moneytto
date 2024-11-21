<!-- components/DeleteAccount.vue -->
<template>
  <section class="delete-account-section">
    <h2>계정 삭제</h2>
    <form @submit.prevent="deleteAccount">
      <div>
        <label for="password">비밀번호 확인:</label>
        <input id="password" v-model="password" type="password" required />
      </div>
      <button type="submit">계정 삭제</button>
    </form>
  </section>
</template>

<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/stores/accountStore";

const accountStore = useAccountStore();
const password = ref("");

const deleteAccount = async () => {
  if (
    confirm("정말로 계정을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.")
  ) {
    try {
      await accountStore.deleteAccount(password.value);
      alert("계정이 성공적으로 삭제되었습니다.");
      // 로그아웃 처리는 deleteAccount 함수 내에서 이미 처리되므로 여기서는 추가 작업 불필요
    } catch (error) {
      alert("계정 삭제에 실패했습니다.");
    }
  }
};
</script>
