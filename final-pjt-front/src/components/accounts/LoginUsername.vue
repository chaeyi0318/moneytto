<template>
  <div v-if="user">
    {{ user.nickname }}님, 안녕하세요!
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: null, // 사용자 정보를 저장할 변수
    };
  },
  created() {
    // 컴포넌트가 생성될 때 localStorage에서 사용자 정보를 가져옴
    const storedUser = localStorage.getItem('user');
    if (storedUser) {
      this.user = JSON.parse(storedUser); // JSON 문자열을 객체로 변환
    }
  },
};
</script>

<style scoped>

</style>