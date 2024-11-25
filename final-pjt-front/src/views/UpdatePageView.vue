<template>
  <div class="post-container">
    <h1 class="title">게시글 수정</h1>

    <form @submit.prevent="updatePost" class="post-form">
      <div class="form-group top-info">
        <div class="info-row">
          <div class="date-wrapper">
            <span class="label-text">소비한 날짜:</span>
            <span class="date-text">{{ expenses_date }}</span>
          </div>
          <div class="privacy-wrapper">
            <select name="privacy_setting" v-model.trim="privacySetting" id="privacy_setting" class="privacy-select">
              <option value="public" selected>전체공개</option>
              <option value="subscriber">구독자공개</option>
              <option value="private">🔒</option>
            </select>
          </div>
        </div>
        <div class="info-row">
          <div class="category-wrapper">
            <span class="label-text">카테고리:</span>
            <select name="category_id" v-model.trim="category" id="category_id" class="compact-select">
              <option value="">선택바람</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.category_name }}
              </option>
            </select>
          </div>
          <div class="price-wrapper">
            <span class="label-text">가격:</span>
            <input type="number" v-model.trim="price" name="price" id="price" class="compact-input" />
          </div>
        </div>
      </div>

      <div class="form-group">
        <label for="image">파일 업로드 :</label>
        <input type="file" name="image" id="image" @change="onFileChange" class="file-input" />
      </div>

      <div v-if="imageUrl" class="image-preview">
        <img :src="imageUrl" alt="이미지 미리보기" />
      </div>

      <div class="form-group">
        <label for="content">내용 :</label>
        <input type="text" v-model.trim="content" name="content" id="content" class="content-input" />
      </div>

      <div class="button-group">
        <button type="button" @click.prevent="cancel" class="cancel-btn">취소</button>
        <button type="submit" class="submit-btn">수정</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRoute, useRouter } from "vue-router";
import api from "@/stores/api";

const route = useRoute(); // 현재 라우트 정보 가져오기
const router = useRouter(); // 라우터 객체

// 폼 데이터 상태 관리
const categories = ref([]);
const expenses_date = ref(""); // 소비 날짜
const privacySetting = ref("private"); // 공개 범위
const category = ref(""); // 카테고리 ID
const price = ref(""); // 가격
const content = ref(""); // 내용
const imageFile = ref(null); // 이미지 파일
const imageUrl = ref(""); // 이미지 미리보기 URL

// 파일 선택 시 처리
const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    imageFile.value = file;

    // 이미지 미리보기 URL 생성
    const reader = new FileReader();
    reader.onload = (e) => {
      imageUrl.value = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

// 라우트에서 전달된 데이터를 초기화
onMounted(async () => {
  const query = route.query;

  expenses_date.value = query.expenses_date || "";
  privacySetting.value = query.privacy_setting || "";
  category.value = query.category || "";
  price.value = query.price || "";
  content.value = query.content || "";
  imageUrl.value = query.image || "";

  try {
    const response = await api.get("/posts/categories/");
    if (response.status === 200) {
      categories.value = response.data;
    }
  } catch (error) {
    console.error("카테고리 데이터를 가져오는 중 오류 발생:", error);
  }
});

// 게시글 수정 요청 보내기
const updatePost = async () => {
  if (!expenses_date.value || !category.value || !price.value || !content.value) {
    alert("필수 항목을 모두 입력해주세요.");
    return;
  }

  const formData = new FormData();
  formData.append("expenses_date", expenses_date.value);
  formData.append("privacy_setting", privacySetting.value);
  formData.append("category", category.value);
  formData.append("price", price.value);
  formData.append("content", content.value);

  if (imageFile.value) {
    formData.append("image", imageFile.value); // 이미지 파일 추가
  }

  try {
    const postId = route.query.id; // 게시글 ID 가져오기
    const response = await api.put(`/posts/update-post/${postId}/`, formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    if (response.status === 200) {
      alert("게시글이 성공적으로 수정되었습니다.");
      router.push({ name: "CalendarView" }); // 수정 후 캘린더 화면으로 이동
    }
  } catch (error) {
    console.error("게시글 수정 중 오류 발생:", error);
    alert("게시글 수정에 실패했습니다. 다시 시도해주세요.");
  }
};

// 수정 취소 시 캘린더 화면으로 이동
const cancelUpdate = () => {
  router.push({ name: "CalendarView" });
};
</script>

<style scoped>
.post-container {
  background-color: #f8faf6;
  max-width: 800px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 16px;
  box-shadow: 0 4px 12px rgba(85, 136, 59, 0.1);
}

.title {
  color: #2D7A31;
  font-size: 1.8rem;
  text-align: center;
  margin-bottom: 2rem;
  font-weight: 700;
}

.form-group {
  background: white;
  padding: 1.2rem;
  border-radius: 12px;
  margin-bottom: 1.2rem;
  border: 1px solid #E8F3E9;
}

.top-info {
  padding: 1rem;
}

.info-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 0.8rem;
}

.info-row:last-child {
  margin-bottom: 0;
}

.date-wrapper, .category-wrapper, .price-wrapper {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  flex: 1 1 auto;
}

.label-text {
  color: #2D7A31;
  font-size: 0.9rem;
  font-weight: 600;
  white-space: nowrap;
}

.date-text {
  color: #333;
  font-weight: 500;
}

.privacy-wrapper {
  width: auto;
}

.privacy-select {
  width: auto;
  padding: 0.3rem 0.5rem;
  border: 1px solid #E8F3E9;
  border-radius: 6px;
  font-size: 0.9rem;
  cursor: pointer;
}

.compact-select, .compact-input {
  flex: 1;
  min-width: 0;
  padding: 0.3rem 0.5rem;
  border: 1px solid #E8F3E9;
  border-radius: 6px;
  font-size: 0.9rem;
}

label {
  color: #2D7A31;
  font-weight: 600;
  display: inline-block;
  width: 120px;
  margin-right: 1rem;
}

.file-input {
  background: white;
  padding: 0.6rem;
  width: calc(100% - 150px);
}

.content-input {
  width: calc(100% - 150px);
  min-height: 100px;
  padding: 0.8rem;
  border: 2px solid #E8F3E9;
  border-radius: 8px;
  transition: all 0.3s ease;
}

.image-preview {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100%;
  padding: 1rem;
}

.image-preview img {
  max-width: 80%;
  border-radius: 8px;
  margin-top: 1rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s ease;
}

.image-preview img:hover {
  transform: scale(1.02);
}

.button-group {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-top: 2rem;
}

.submit-btn, .cancel-btn {
  padding: 0.8rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
}

.submit-btn {
  background-color: #2D7A31;
  color: white;
}

.cancel-btn {
  background-color: #E8F3E9;
  color: #2D7A31;
}

.submit-btn:hover {
  background-color: #246627;
}

.cancel-btn:hover {
  background-color: #D1E6D3;
}

@media (max-width: 600px) {
  .post-container {
    margin: 1rem;
    padding: 1rem;
  }

  .info-row {
    flex-direction: column;
    gap: 0.8rem;
  }

  .date-wrapper, .category-wrapper, .price-wrapper {
    width: 100%;
  }

  .file-input, .content-input {
    width: 100%;
    margin-top: 0.5rem;
  }

  label {
    display: block;
    margin-bottom: 0.5rem;
  }

  .button-group {
    flex-direction: column;
  }

  .submit-btn, .cancel-btn {
    width: 100%;
    margin: 0.5rem 0;
  }

  .compact-select, .compact-input {
    max-width: none;
  }
}
</style>