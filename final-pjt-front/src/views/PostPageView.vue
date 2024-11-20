<template>
  <div>
    <h1>게시글 작성</h1>

    <!-- 소비한 날짜 -->
    <form @submit.prevent="createPost">
      <div style="margin-bottom: 10px;">
        <p id="expenses_date">소비한 날짜 : {{ selectedDate }}</p>
        <label for="privacy_setting">공개범위 : </label>
        <select name="privacy_setting" v-model.trim="privacy_setting" id="privacy_setting">
          <option value="public">전체공개</option>
          <option value="subscriber">구독자공개</option>
          <option value="private">비공개</option>
        </select>
      </div>
  
      <!-- 카테고리 선택 -->
      <div style="margin-bottom: 10px;">
        <label for="category_id">카테고리 :</label>
        <select name="category_id" v-model.trim="category_id" id="category_id">
          <option value="">선택바람</option>
          <option value="1">식비</option>
          <option value="2">문화</option>
          <option value="3">생활비</option>
        </select>
      </div>
  
      <!-- 파일 업로드 -->
      <div style="margin-bottom: 10px;">
        <label for="image">파일 업로드 :</label>
        <input 
          type="file" 
          name="image" 
          id="image" 
          @change="onFileChange"
        >
      </div>

      <!-- 이미지 미리보기 -->
      <div v-if="imageUrl">
        <img :src="imageUrl" alt="이미지 미리보기" style="max-width: 200px; margin-top: 10px;">
      </div>
  
      <!-- 가격 입력 -->
      <div style="margin-bottom: 10px;">
        <label for="price">가격 :</label>
        <input type="number" v-model.trim="price" name="price" id="price">
      </div>
  
      <!-- 내용 입력 -->

          <label for="content">내용 :</label>
          <input type="text" v-model.trim="content" name="content" id="content">
  
        <!-- 버튼 -->
        <input type="button" @click.prevent="cancel" value="취소">
        <input type="submit" value="저장">

    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCalendarStore } from '@/stores/counter'
import { useRouter } from 'vue-router'
import CalendarView from './CalendarView.vue';

const router = useRouter()
const dateStore = useCalendarStore()

const selectedDate = ref(dateStore.selectedDate)   // expenses_date
const privacy_setting = ref('')
const category_id = ref('')
const price = ref('')
const content = ref('')
const imageFile = ref(null)
const imageUrl = ref('')

// 파일 선택 시 처리
const onFileChange = (event) => {
  const file = event.target.files[0]
  if (file) {
    imageFile.value = file

    // 이미지 미리보기 URL 생성
    const reader = new FileReader()
    reader.onload = (e) => {
      imageUrl.value = e.target.result
    }
    reader.readAsDataURL(file)
  }
}

const createPost = async function () {
  const payload = {
    selectedDate: selectedDate.value,
    privacy_setting: privacy_setting.value,
    category_id: category_id.value,
    price: price.value,
    content: content.value,
    image: imageFile.value
  }

  try {
    console.log('작성된 게시글 데이터: ', payload)
    dateStore.submitPost(payload)
    router.push({name: 'CalendarView'})
  } catch (error) {
    console.log('게시글 작성 중 오류 발생: ', error)
  }

  const cancel = () => {
  router.push({name: 'CalendarView'})
}
}

</script>

<style scoped>
  div {
    margin-bottom: 15px;
  }

  label {
    display: inline-block;
    width: 100px;
  }

  input, select {
    padding: 5px;
    margin-left: 10px;
  }

  input[type='submit'] {
    margin-right: 10px;
  }
</style>