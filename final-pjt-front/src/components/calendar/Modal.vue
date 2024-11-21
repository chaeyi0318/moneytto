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
        <ul v-if="posts.length > 0">
          <li v-for="(post, index) in posts" :key="index">
            <img v-if="post.image" :src="post.image" alt="">
            <p>카테고리 : {{ post.category_name }}</p>
            <p>가격 : {{ post.price }}</p>
            <p>소비내용 : {{ post.content }}</p>
            <button>수정</button>
            <button>삭제</button>
          </li>
        </ul>
      </main>
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, ref, onMounted } from "vue";
import api from "@/stores/api";
// import { Comment } from "@/Comment"

const props = defineProps({
  date: String
})

const emit = defineEmits(["closeModal"]); // closeModal 이벤트 정의

const closeModal = () => {
  emit("closeModal"); // 부모 컴포넌트에 closeModal 이벤트 전달
}

const posts = ref([])
const isLoading = ref(false)
const error = ref(null)

const fetchPosts = async () => {
  isLoading.value = true
  error.value = null

  try {
    const response = await api.get(`/posts/detail-post/`, {
      params: { date: props.date }
    })
    posts.value = response.data;

    // console.log(posts.value)
  } catch (err) {
    error.value = "게시글을 불러오는 데 실패했습니다. 다시 시도해주세요."
  } finally {
    isLoading.value = false; // 로딩 종료
  }
};

// 컴포넌트가 마운트될 때 데이터 가져오기
onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.modal-overlay {
  position :fixed; 
  top :0; 
  left :0; 
  width :100vw; 
  height :100vh; 
  background-color :rgba(0,0,0,.5); /* 배경 어둡게 처리 */
  display:flex; 
  justify-content:center; 
  align-items:center; 
  z-index :1000; /* 화면 위에 고정 */
}

.modal-content{
  background-color:white; 
  padding :20px; 
  border-radius :8px; 
  max-width :500px; 
  width :100%; 
}

header{
  display:flex ; 
  justify-content :space-between ; 
  align-items:center ;
}
/* main ul {
  list-style-type: none;
} */

main li {
  margin-bottom: 16px;
}

img {
  width: 50%;
}
</style>