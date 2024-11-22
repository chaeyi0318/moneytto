<template>
  <div>
    <h1>게시글 작성</h1>

    <!-- 소비한 날짜 -->
    <form @submit.prevent="createPost">
      <div style="margin-bottom: 10px">
        <p id="expenses_date">소비한 날짜 : {{ expenses_date }}</p>
        <label for="privacy_setting">공개범위 : </label>
        <select
          name="privacy_setting"
          v-model.trim="privacySetting"
          id="privacy_setting">
          <option value="">공개범위설정</option>
          <option value="public">전체공개</option>
          <option value="subscriber">구독자공개</option>
          <option value="private">비공개</option>
        </select>
      </div>

      <!-- 카테고리 선택 -->
      <div style="margin-bottom: 10px">
        <label for="category_id">카테고리 :</label>
        <select name="category_id" v-model.trim="category" id="category_id">
          <option value="">선택바람</option>
          <option v-for="cat in categories" :key="cat.id" :value="cat.id">
            {{ cat.category_name }}
          </option>
        </select>
      </div>

      <!-- 파일 업로드 -->
      <div style="margin-bottom: 10px">
        <label for="image">파일 업로드 :</label>
        <input type="file" name="image" id="image" @change="onFileChange" />
      </div>

      <!-- 이미지 미리보기 -->
      <div v-if="imageUrl">
        <img
          :src="imageUrl"
          alt="이미지 미리보기"
          style="max-width: 200px; margin-top: 10px"
        />
      </div>

      <!-- 가격 입력 -->
      <div style="margin-bottom: 10px">
        <label for="price">가격 :</label>
        <input type="number" v-model.trim="price" name="price" id="price" />
      </div>

      <!-- 내용 입력 -->
      <label for="content">내용 :</label>
      <input type="text" v-model.trim="content" name="content" id="content" />

      <!-- 버튼 -->
      <input type="button" @click.prevent="cancel" value="취소" />
      <input type="submit" value="저장" />
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
div {
  margin-bottom: 15px;
}

label {
  display: inline-block;
  width: 100px;
}

input,
select {
  padding: 5px;
  margin-left: 10px;
}

input[type="submit"] {
  margin-right: 10px;
}
</style>
