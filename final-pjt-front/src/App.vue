<template>
  <nav>
    <RouterLink :to="{ name: 'MainView' }">메인</RouterLink> | 
    <RouterLink :to="{ name: 'CalendarView' }">가계부</RouterLink> | 
    <RouterLink :to="{ name: 'SavingView' }">적금</RouterLink> | 
    <RouterLink :to="{ name: 'FortuneView' }">운세</RouterLink> | 
    <RouterLink :to="{ name: 'QuizView' }">금융퀴즈</RouterLink> |
    <RouterLink :to="{ name: 'MyPageView' }">마이페이지</RouterLink> | 
    <RouterLink :to="{ name: 'SignupView' }">회원가입</RouterLink> | 
    <RouterLink :to="{ name: 'LoginView' }">로그인</RouterLink>
  </nav>
  <RouterView/>
</template>

<script setup>
import { RouterLink, RouterView } from "vue-router";
</script>

<style scoped>

</style>
