<template>
  <div class="post-container">
    <h1 class="title">게시글 작성</h1>

    <form @submit.prevent="createPost" class="post-form">
      <div class="form-group top-info">
        <div class="info-row">
          <div class="date-wrapper">
            <span class="label-text">소비한 날짜:</span>
            <span class="date-text">{{ expenses_date }}</span>
          </div>
          <div class="privacy-wrapper">
            <select name="privacy_setting" v-model.trim="privacySetting" id="privacy_setting" class="privacy-select">
              <option value="">🔒</option>
              <option value="public" selected>전체공개</option>
              <option value="subscriber">구독자공개</option>
              <option value="private">비공개</option>
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
        <button type="submit" class="submit-btn">저장</button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useCalendarStore } from "@/stores/calendarStore";
import { useRouter } from "vue-router";
import api from "@/stores/api";

const router = useRouter();
const dateStore = useCalendarStore();

const categories = ref([])
const expenses_date = ref(dateStore.expenses_date); // expenses_date
const privacySetting = ref("");
const category = ref("");
const price = ref("");
const content = ref("");
const imageFile = ref(null);
const imageUrl = ref("");

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

const createPost = async function () {
  // 필수 값 체크
  if (
    !expenses_date.value ||
    !category.value ||
    !price.value ||
    !content.value
  ) {
    console.log("필수 항목이 누락되었습니다.");
    return;
  }

  const payload = {
    expenses_date: expenses_date.value, // 소비한 날짜
    privacy_setting: privacySetting.value, // 공개 범위
    category: parseInt(category.value), // 카테고리 ID를 정수로 변환
    price: parseInt(price.value), // 가격을 정수로 변환
    content: content.value,
    image: imageFile.value, // 이미지 파일
  };

  try {
    console.log("작성된 게시글 데이터: ", payload);
    await dateStore.submitPost(payload); // 비동기 함수 호출 시 await 추가
    router.push({ name: "CalendarView" });
  } catch (error) {
    console.log("게시글 작성 중 오류 발생: ", error);
  }
};

const cancel = () => {
  dateStore.clearState();
  router.push({ name: "CalendarView" });
};

onMounted(async () => {
  try {
    const response = await api.get("/posts/categories/"); // Django API 호출
    if (response.status === 200) { // 상태 코드가 200인지 확인
      console.log("Fetched categories:", response.data); // 응답 데이터 출력
      categories.value = response.data; // JSON 데이터를 Vue 데이터에 저장
    } else {
      console.error(`Failed to fetch categories: ${response.status}`); // 상태 코드 출력
    }
  } catch (error) {
    console.error("Error fetching categories:", error); // 네트워크 오류 출력
  }
});
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