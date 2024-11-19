<template>
  <div>
    <h1>로그인</h1>
    <form action="">
      <label for="id">ID : </label>
      <input type="text" v-model="id" name="id" id="id">
  
      <label for="password">PW : </label>
      <input type="password" v-model="password" name="password" id="password">
      <input type="submit" value="로그인">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCalendarStore } from '@/stores/counter';
const id = ref('')
const password = ref('')



</script>

<style scoped>

</style>