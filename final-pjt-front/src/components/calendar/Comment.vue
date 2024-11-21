<template>
  <div>
    <h4>댓글</h4>
    <form @submit.prevent="addComment">
      <p>{{ currentDate }}</p>
      <input type="text" name="content" id="content" placeholder="댓글을 입력하세요" v-model.trim="content">
      <input type="submit" value="작성">
    </form>
    <div>
      <p>댓글 목록</p>
    </div>
  </div>
</template>

<script setup>
import { ref, defineProps } from 'vue'
import api from "@/stores/api"

const props = defineProps({
  date: String
})

const currentDate = props.date
const content = ref('')
const commentList = ref([])

const addComment = async () => {
  if (content.value.trim() === "") {
    alert("댓글을 입력해주세요."); // 빈 댓글 방지
    return;
  }

  try {
    // 서버에 댓글 생성 요청
    const response = await api.post('/posts/create-comment/', {
      expenses_date: currentDate, // 날짜 정보
      content: content.value // 댓글 내용
    });

    // 응답 데이터 콘솔 출력 (디버깅용)
    console.log(response.data);

    // 새로 작성된 댓글을 목록에 추가
    commentList.value.push(response.data);

    // 입력 필드 초기화
    content.value = "";
  } catch (error) {
    console.error("댓글 작성 중 오류 발생:", error);
  }
};
</script>

<style scoped>

</style>