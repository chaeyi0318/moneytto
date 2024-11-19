<template>
  <div>
    <h1>로그인</h1>
    <form @submit.prevent="login">
      <label for="username">ID : </label>
      <input type="text" v-model.trim="username" id="username">
  
      <label for="password">PW : </label>
      <input type="password" v-model.trim="password" id="password">
      <input type="submit" value="로그인">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useAccountStore } from '@/stores/counter'

const accountStore = useAccountStore()

const username = ref('')
const password = ref('')

// emit을 사용하여 부모 컴포넌트에 이벤트 전달 (모달 닫기)
const emit = defineEmits(['closeModal'])

const login = async function() {
  const payload = {
    username: username.value,
    password: password.value
  }
  
  // Pinia 스토어의 login 액션 호출
  await accountStore.login(payload)

  // 로그인 성공 시 모달 닫기
  if (accountStore.isLogin) {
    emit('closeModal') // 부모에게 모달 닫기 이벤트 전달
  }
}
</script>

<style scoped>

</style>