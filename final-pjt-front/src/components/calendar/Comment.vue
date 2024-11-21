<template>
  <div>
    <h4>댓글</h4>
    <form @submit.prevent="addComment">
      <input type="text" name="content" id="content" placeholder="댓글을 입력하세요" v-model.trim="content">
      <input type="submit" value="작성">
    </form>
    <div>
      <p>댓글 목록</p>
      <ul>
        <li v-for="comment in commentList" :key="comment.id">
          <!-- 수정 상태가 아닐 때 -->
          <div v-if="!comment.isEditing">
            {{ comment.content }} (작성일: {{ comment.created_at_formatted }}) | 작성자 {{ comment.user.username }}
            <span @click.prevent="enableEdit(comment)">수정</span>
            <span> | </span>
            <span @click.prevent="deleteComment(comment.id)">삭제</span>
          </div>

          <!-- 수정 상태일 때 -->
          <div v-else>
            <input type="text" v-model.trim="comment.newContent" />
            <button @click.prevent="updateComment(comment.id, comment.newContent)">저장</button>
            <button @click.prevent="cancelEdit(comment)">취소</button>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>
<script setup>
import { ref, defineProps, onMounted } from 'vue'
import api from "@/stores/api"

const props = defineProps({
  date: String,
  author_user_pk: Number
})

const currentDate = props.date
const content = ref('')
const commentList = ref([])
const author_user_pk = props.author_user_pk

// 댓글 목록 가져오기
const fetchComments = async () => {
  try {
    const response = await api.get('/posts/comment-list/', {
      params: {
        expenses_date: currentDate,
        author_user_pk: author_user_pk,
      },
    })

    // 댓글 데이터에 isEditing과 newContent 추가
    commentList.value = response.data.map(comment => ({
      ...comment,
      isEditing: false, // 수정 상태 여부
      newContent: comment.content, // 기존 내용을 기본값으로 설정
    }))
  } catch (error) {
    console.error("댓글 목록 가져오기 중 오류 발생:", error);
  }
}

onMounted(() => {
  fetchComments()
})

// 댓글 추가
const addComment = async () => {
  if (content.value.trim() === "") {
    alert("댓글을 입력해주세요.");
    return
  }

  try {
    const response = await api.post('/posts/create-comment/', {
      expenses_date: currentDate,
      content: content.value,
      author_user_pk: author_user_pk,
    })

    // 새로 작성된 댓글 추가
    commentList.value.push({
      ...response.data,
      isEditing: false,
      newContent: response.data.content, // 새 댓글의 기본값 설정
    })

    content.value = "" // 입력 필드 초기화
  } catch (error) {
    console.error("댓글 작성 중 오류 발생:", error)
  }
}

// 수정 상태 활성화
const enableEdit = (comment) => {
  comment.isEditing = true // 수정 상태로 전환
}

// 수정 상태 취소
const cancelEdit = (comment) => {
  comment.isEditing = false; // 수정 상태 해제
  comment.newContent = comment.content; // 원래 내용 복원
}

// 댓글 수정
const updateComment = async (commentId, newContent) => {
  if (!newContent.trim()) {
    alert("수정할 내용을 입력해주세요.");
    return
  }

  try {
    const response = await api.put(`/posts/update-comment/${commentId}/`, {
      content: newContent,
    })

    const index = commentList.value.findIndex(comment => comment.id === commentId)
    if (index !== -1) {
      // 서버에서 반환된 데이터로 업데이트
      commentList.value[index].content = response.data.content
      commentList.value[index].isEditing = false
    }
  } catch (error) {
    console.error("댓글 수정 중 오류 발생:", error)
  }
}


const deleteComment = async (commentId) => {
  if (!confirm("정말로 이 댓글을 삭제하시겠습니까?")) return

  try {
    await api.delete(`/posts/delete-comment/${commentId}/`)

    commentList.value = commentList.value.filter(comment => comment.id !== commentId)
  } catch (error) {
    console.error("댓글 삭제 중 오류 발생:", error)
  }
}
</script>
