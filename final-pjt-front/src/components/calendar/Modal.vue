<template>
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <header class="modal-header">
        <p class="date-text">{{ formattedDate }}의 소비기록</p>
        <button class="close-button" @click="closeModal">×</button>
      </header>
      
      <main class="modal-main">
        <div v-if="isLoading" class="loading-state">
          <p>로딩 중...</p>
        </div>
        
        <div v-else-if="error" class="error-state">
          <p>{{ error }}</p>
        </div>
        
        <div v-else class="content-container">
          <div class="image-slider" v-if="posts.length > 0">
            <button class="slider-button left" @click="showPreviousPost" :disabled="currentIndex === 0">
              <span class="arrow">←</span>
            </button>
            <div class="image-wrapper">
              <img v-if="currentPost.image" :src="currentPost.image" alt="게시글 이미지" class="post-image" />
            </div>
            <button class="slider-button right" @click="showNextPost" :disabled="currentIndex === posts.length - 1">
              <span class="arrow">→</span>
            </button>
          </div>

          <div v-if="currentPost" class="post-details">
            <div class="info-row">
              <span class="label">카테고리:</span>
              <span class="value">{{ currentPost.category_name }}</span>
            </div>
            <div class="info-row">
              <span class="label">가격:</span>
              <span class="value">{{ currentPost.price }}원</span>
            </div>
            <div class="info-row">
              <span class="label">소비내용:</span>
              <span class="value">{{ currentPost.content }}</span>
            </div>
            <div class="button-group">
              <button class="action-button update" @click.prevent="updatePost">
                <i class="fas fa-edit"></i> 수정
              </button>
              <button class="action-button delete" @click.prevent="deletePost">
                <i class="fas fa-trash"></i> 삭제
              </button>
            </div>
          </div>
        </div>
      </main>

      <Comment v-if="posts.length > 0" :date="props.date" :author_user_pk="posts[0]?.user_pk"/>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, onMounted, computed } from "vue";
import router from "@/router";
import api from "@/stores/api";
import Comment from "@/components/calendar/Comment.vue";

const props = defineProps({
  date: String
});

const emit = defineEmits(["closeModal"]); // closeModal 이벤트 정의

const closeModal = () => {
  emit("closeModal"); // 부모 컴포넌트에 closeModal 이벤트 전달
};

const posts = ref([]);
const isLoading = ref(false);
const error = ref(null);
const currentIndex = ref(0); // 현재 표시 중인 게시글의 인덱스

// 현재 표시 중인 게시글 계산
const currentPost = computed(() => posts.value[currentIndex.value]);

// 이전 게시글로 이동
const showPreviousPost = () => {
  if (currentIndex.value > 0) {
    currentIndex.value -= 1;
  }
};

// 다음 게시글로 이동
const showNextPost = () => {
  if (currentIndex.value < posts.value.length - 1) {
    currentIndex.value += 1;
  }
};

// API에서 게시글 가져오기
const fetchPosts = async () => {
  isLoading.value = true;
  error.value = null;

  try {
    const response = await api.get(`/posts/detail-post/`, {
      params: { 
        date: props.date,
      }
    });
    posts.value = response.data;
  } catch (err) {
    error.value = "게시글을 불러오는 데 실패했습니다. 다시 시도해주세요.";
  } finally {
    isLoading.value = false; // 로딩 종료
  }
};

const formattedDate = computed(() => {
  if (!props.date) return '';
  const [year, month, day] = props.date.split('-');
  return `${year}년 ${parseInt(month)}월 ${parseInt(day)}일`;
});

// 게시글 삭제
const deletePost = async () => {
  if (!currentPost.value) return;

  const confirmDelete = confirm("정말로 이 게시글을 삭제하시겠습니까?");
  if (!confirmDelete) return;

  try {
    await api.delete(`/posts/delete-post/${currentPost.value.id}`); // API 호출
    alert("게시글이 삭제되었습니다.");

    // 삭제 후 리스트에서 제거
    posts.value.splice(currentIndex.value, 1);

    // 인덱스 조정 (삭제 후 마지막 게시글일 경우)
    if (currentIndex.value >= posts.value.length && posts.value.length > 0) {
      currentIndex.value -= 1;
    }
    
    // 모든 게시글이 삭제된 경우 모달 닫기
    if (posts.value.length === 0) {
      closeModal();
    }
    
  } catch (err) {
    console.error(err);
    alert("게시글 삭제에 실패했습니다. 다시 시도해주세요.");
  }
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(() => {
  fetchPosts();
});

const updatePost = () => {
  if (!currentPost.value) return;

  // PostPageView로 이동하면서 게시글 데이터를 전달
  router.push({
    name: "PostPageView", // 라우트 이름
    query: {
      id: currentPost.value.id, // 게시글 ID
      expenses_date: props.date, // 소비 날짜
      privacy_setting: currentPost.value.privacy_setting, // 공개 범위
      category: currentPost.value.category_id, // 카테고리 ID
      price: currentPost.value.price, // 가격
      content: currentPost.value.content, // 내용
      image: currentPost.value.image, // 이미지 URL (수정 시 미리보기)
    },
  });
};
</script>

<style scoped>
:root {
  --primary-green: #2D8B57;
  --secondary-green: #3CB371;
  --light-green: #E8F5E9;
  --hover-green: #1B5E20;
  --error-red: #FF5252;
  --text-dark: #333333;
  --text-light: #666666;
  --white: #FFFFFF;
  --shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(4px);
}

.modal-content {
  background-color: #FFFFFF;
  width: 100%;
  max-height: 90vh; /* 뷰포트 높이의 90%로 제한 */
  max-width: 650px;
  border-radius: 20px;
  box-shadow: var(--shadow);
  overflow: auto;
  display: flex;
  flex-direction: column;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 2px solid var(--primary-green);
}

.date-text {
  font-size: 1.2rem;
  font-weight: 600;
  color: var(--primary-green);
}

.close-button {
  background: none;
  border: none;
  font-size: 1.8rem;
  color: var(--primary-green);
  cursor: pointer;
  transition: color 0.3s ease;
}

.close-button:hover {
  color: var(--hover-green);
}

.modal-main {
  padding: 2rem;
  flex: 1;
}

.loading-state, .error-state {
  text-align: center;
  padding: 2rem;
}

.error-state {
  color: var(--error-red);
}

.image-slider {
  position: relative;
  margin: 2rem 0;
  padding: 0 3rem;
}

.slider-button {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  background-color: var(--primary-green);
  color: var(--white);
  border: none;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.slider-button:hover:not([disabled]) {
  background-color: var(--hover-green);
}

.slider-button.left { left: 0; }
.slider-button.right { right: 0; }

.slider-button[disabled] {
  opacity: 0.5;
  cursor: not-allowed;
}

.image-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

.post-image {
  max-width: 100%;
  max-height: 400px;
  object-fit: contain;
  border-radius: 8px;
}

.post-details {
  padding: 1.5rem;
  background-color: var(--light-green);
  border-radius: 12px;
}

.info-row {
  margin-bottom: 1rem;
  display: flex;
  align-items: baseline;
}

.label {
  font-weight: 600;
  color: var(--text-dark);
  min-width: 100px;
}

.value {
  color: var(--text-light);
  flex: 1;
}

.button-group {
  display: flex;
  gap: 1rem;
  margin-top: 1.5rem;
}

.action-button {
  padding: 0.8rem 1.5rem;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.action-button.update {
  background-color: var(--primary-green);
  color: var(--white);
}

.action-button.delete {
  background-color: var(--error-red);
  color: var(--white);
}

.action-button:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow);
}

::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #F5F9F6;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb {
  background: #2E8B57;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #1B5E20;
}

@media (max-width: 768px) {
  .modal-content {
    width: 95%;
    margin: 1rem;
  }
  
  .post-details {
    padding: 1rem;
  }
  
  .info-row {
    flex-direction: column;
  }
  
  .label {
    margin-bottom: 0.5rem;
  }
}
</style>