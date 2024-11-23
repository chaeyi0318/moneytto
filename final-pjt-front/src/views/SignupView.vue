<template>
  <div class="signup-container">
    <h1 class="title">회원가입</h1>
    <form @submit.prevent="signup" class="signup-form">
      <label for="username">아이디:</label>
      <input type="text" id="username" v-model.trim="username" required />

      <label for="password1">비밀번호:</label>
      <input type="password" id="password1" v-model.trim="password1" required />

      <label for="password2">비밀번호 확인:</label>
      <input type="password" id="password2" v-model.trim="password2" required />

      <label for="nickname">닉네임:</label>
      <input type="text" id="nickname" v-model.trim="nickname" required />

      <label for="email">이메일:</label>
      <input type="email" id="email" v-model.trim="email" required />

      <button type="submit" class="submit-btn">회원가입</button>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/stores/accountStore";

const accountStore = useAccountStore();

const username = ref("");
const password1 = ref("");
const password2 = ref("");
const nickname = ref("");
const email = ref("");

const signup = () => {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    email: email.value,
  };
  accountStore.signup(payload);
};
</script>

<style scoped>
.signup-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border-radius: 10px;
  background-color: #f9f9f9;
  box-shadow: 0px 4px 6px rgba(0, 0, 0, 0.1);
}

.title {
  font-size: 24px;
  color: #2e8b57;
  text-align: center;
}

.signup-form {
  display: flex;
  flex-direction: column;
}

.signup-form label {
  margin-bottom: 5px;
  font-weight: bold;
}

.signup-form input {
  margin-bottom: 15px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
}

.submit-btn {
  background-color: #2e8b57;
  color: white;
  padding: 10px;
  border-radius: 5px;
  border: none;
}

.submit-btn:hover {
  background-color: #1a5235;
}
</style>