<template>
  <div class="login-container">
    <h1 class="form-title">로그인</h1>
    <form @submit.prevent="login" class="login-form">
      <div class="form-group">
        <label for="username">아이디</label>
        <input type="text" id="username" v-model.trim="username" required>
      </div>

      <div class="form-group">
        <label for="password">비밀번호</label>
        <input type="password" id="password" v-model.trim="password" required>
      </div>

      <button type="submit" class="submit-button">로그인</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/stores/accountStore";

const accountStore = useAccountStore();

const username = ref("");
const password = ref("");

// emit을 사용하여 부모 컴포넌트에 이벤트 전달 (모달 닫기)
const emit = defineEmits(["closeModal"]);

const login = async function () {
  const payload = {
    username: username.value,
    password: password.value,
  };

  // Pinia 스토어의 login 액션 호출
  await accountStore.login(payload);

  // 로그인 성공 시 모달 닫기
  if (accountStore.isLogin) {
    emit("closeModal"); // 부모에게 모달 닫기 이벤트 전달
  } else {
    alert('로그인에 실패하였습니다.')
  }
};
</script>

<style scoped>
/* .login-container {
  max-width: 400px;
  margin: 0 auto;
  padding: 20px;
} */

.form-title {
  color: #2E8B57;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2em;
}

/* .login-form {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
} */

.form-title {
  color: #2E8B57;
  text-align: center;
  margin-bottom: 30px;
  font-size: 2em;
}

.signup-form {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #2E8B57;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #2E8B57;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #2E8B57;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-button:hover {
  background-color: #1a5235;
  transform: translateY(-2px);
}
</style>
