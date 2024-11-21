<template>
  <!-- 오버레이 클릭 시 closeModal 호출 -->
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <header>
        <p>{{ date }}</p>
        <button @click="closeModal">X</button> 
      </header>
      <main v-if="isLoading">
        <p>로딩 중...</p>
      </main>
      <main v-else-if="error">
        <p>{{ error }}</p>
      </main>
      <main v-else>
        <!-- 게시글 슬라이드 -->
        <div class="image-container" v-if="posts.length > 0">
          <!-- 이전 버튼 -->
          <button class="nav-button left" @click="showPreviousPost" :disabled="currentIndex === 0">이전</button>

          <!-- 현재 게시글 이미지 -->
          <img v-if="currentPost.image" :src="currentPost.image" alt="게시글 이미지" />

          <!-- 다음 버튼 -->
          <button class="nav-button right" @click="showNextPost" :disabled="currentIndex === posts.length - 1">다음</button>
        </div>

        <!-- 현재 게시글 정보 -->
        <div v-if="currentPost">
          <p>카테고리 : {{ currentPost.category_name }}</p>
          <p>가격 : {{ currentPost.price }}원</p>
          <p>소비내용 : {{ currentPost.content }}</p>
          <button @click.prevent="updatePost">수정</button>
          <button @click.prevent="deletePost">삭제</button> <!-- 삭제 버튼 -->
        </div>
      </main>

      <!-- 댓글 컴포넌트 -->
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
.modal-overlay {
  position: fixed; 
  top: 0; 
  left: 0; 
  width: 100vw; 
  height: 100vh; 
  background-color: rgba(0,0,0,.5); /* 배경 어둡게 처리 */
  display: flex; 
  justify-content: center; 
  align-items: center; 
  z-index: 1000; /* 화면 위에 고정 */
}

.modal-content {
  background-color: white; 
  padding: 20px; 
  border-radius: 8px; 
  max-width: 650px; 
}

header {
  display: flex ; 
  justify-content: space-between ; 
  align-items: center ;
}

.image-container {
  position: relative;
}

img {
  width: auto;
  max-width: calc(100% - 120px); /* 양쪽 버튼 공간 확보 */
}

/* 이전/다음 버튼 스타일 */
.nav-button {
  position: absolute;
  top: calc(50% - 20px); /* 중앙 정렬 */
  transform: translateY(-50%);
  background-color: rgba(0,0,0,0.5);
  color: white;
  border: none;
  padding: 10px;
}

.nav-button.left {
   left: -60px;
}

.nav-button.right {
   right: -60px;
}

.nav-button:hover {
   background-color: rgba(0,0,0,0.8);
}

button[disabled] {
   opacity: .5;
}
</style>