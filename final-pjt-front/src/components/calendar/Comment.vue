<template>
  <div class="comments-section">
    <h4 class="comments-title">댓글</h4>
    <form @submit.prevent="addComment" class="comment-form">
      <div class="input-group">
        <input 
          type="text" 
          name="content" 
          id="content" 
          placeholder="댓글을 입력하세요" 
          v-model.trim="content"
          class="comment-input"
        >
        <button type="submit" class="submit-button">작성</button>
      </div>
    </form>
    
    <div class="comments-container">
      <p class="comments-subtitle">댓글 목록</p>
      <ul class="comments-list">
        <li v-for="comment in commentList" :key="comment.id" class="comment-item">
          <div v-if="!comment.isEditing" class="comment-content">
            <div class="comment-main">
              <span class="comment-text">{{ comment.content }}</span>
              <div class="comment-info">
                <span class="comment-date">{{ comment.created_at_formatted }}</span>
                <span class="comment-author">{{ comment.user.username }}</span>
              </div>
            </div>
            <div class="comment-actions">
              <button @click.prevent="enableEdit(comment)" class="action-button edit">
                수정
              </button>
              <button @click.prevent="deleteComment(comment.id)" class="action-button delete">
                삭제
              </button>
            </div>
          </div>

          <div v-else class="edit-mode">
            <input 
              type="text" 
              v-model.trim="comment.newContent" 
              class="edit-input"
            >
            <div class="edit-actions">
              <button @click.prevent="updateComment(comment.id, comment.newContent)" class="action-button save">
                저장
              </button>
              <button @click.prevent="cancelEdit(comment)" class="action-button cancel">
                취소
              </button>
            </div>
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

<style scoped>
.comments-section {
  padding: 1.5rem;
  background-color: #fff;
  border-radius: 12px;
  margin-top: 1rem;
}

.comments-title {
  color: #2D8B57;
  font-size: 1.2rem;
  margin-bottom: 1rem;
  font-weight: 600;
}

.comment-form {
  margin-bottom: 1.5rem;
}

.input-group {
  display: flex;
  gap: 0.5rem;
}

.comment-input {
  flex: 1;
  padding: 0.8rem;
  border: 1px solid #E8E8E8;
  border-radius: 8px;
  font-size: 0.9rem;
}

.submit-button {
  padding: 0.8rem 1.5rem;
  background-color: #2D8B57;
  color: white;
  border: none;
  border-radius: 8px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover {
  background-color: #1B5E20;
}

.comments-container {
  background-color: #F5F5F5;
  border-radius: 8px;
  padding: 1rem;
}

.comments-subtitle {
  color: #666;
  font-weight: 500;
  margin-bottom: 1rem;
}

.comments-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.comment-item {
  background-color: white;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 0.5rem;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.comment-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.comment-main {
  flex: 1;
}

.comment-text {
  display: block;
  margin-bottom: 0.5rem;
}

.comment-info {
  font-size: 0.8rem;
  color: #666;
}

.comment-date, .comment-author {
  margin-right: 1rem;
}

.comment-actions {
  display: flex;
  gap: 0.5rem;
}

.action-button {
  padding: 0.4rem 0.8rem;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.8rem;
  transition: all 0.3s;
}

.action-button.edit {
  background-color: #E8F5E9;
  color: #2D8B57;
}

.action-button.delete {
  background-color: #FFEBEE;
  color: #FF5252;
}

.action-button.save {
  background-color: #2D8B57;
  color: white;
}

.action-button.cancel {
  background-color: #E0E0E0;
  color: #333;
}

.edit-mode {
  display: flex;
  gap: 0.5rem;
}

.edit-input {
  flex: 1;
  padding: 0.5rem;
  border: 1px solid #E8E8E8;
  border-radius: 4px;
}

.edit-actions {
  display: flex;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .comment-content {
    flex-direction: column;
    align-items: flex-start;
  }
  
  .comment-actions {
    margin-top: 0.5rem;
  }
  
  .edit-mode {
    flex-direction: column;
  }
  
  .edit-actions {
    margin-top: 0.5rem;
  }
}
</style>