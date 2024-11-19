<template>
  <div>
    <h1>회원가입</h1>
    <form @submit.prevent="signup">
        <label for="username">Username:</label>
        <input type="text" id="username" name="username" v-model.trim="username" required><br><br>

        <label for="password1">Password:</label>
        <input type="password" id="password1" name="password1" v-model.trim="password1" required><br><br>

        <label for="password2">Confirm Password:</label>
        <input type="password" id="password2" name="password2" v-model.trim="password2" required><br><br>

        <label for="nickname">Nickname:</label>
        <input type="text" id="nickname" name="nickname" v-model.trim="nickname" required><br><br>

        <label for="email">Email:</label>
        <input type="email" id="email" name="email" v-model.trim="email" required><br><br>

        <input type="submit" value="회원가입"></input>
    </form>
</div>
</template>

<script setup>
import { ref } from 'vue'
import { RouterView, RouterLink } from 'vue-router'
import { useAccountStore } from '@/stores/counter'

const accountStore = useAccountStore()

const username = ref(null)
const password1 = ref(null)
const password2 = ref(null)
const nickname = ref(null)
const email = ref(null)

const signup = function () {
  const payload = {
    username: username.value,
    password1: password1.value,
    password2: password2.value,
    nickname: nickname.value,
    email: email.value
  }

  accountStore.signup(payload)
}
</script>

<style scoped>

</style>