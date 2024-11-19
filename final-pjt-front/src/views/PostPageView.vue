<template>
  <div>
    <h1>게시글 작성</h1>

    <!-- 소비한 날짜 -->
    <div style="margin-bottom: 10px;">
      <p id="expenses_date">소비한 날짜 : {{ selectedDate }}</p>
      <label for="privacy_setting">공개범위 : </label>
      <select name="privacy_setting" id="privacy_setting">
        <option value="public">전체공개</option>
        <option value="subscriber">구독자공개</option>
        <option value="private">비공개</option>
      </select>
    </div>

    <!-- 카테고리 선택 -->
    <div style="margin-bottom: 10px;">
      <label for="category_id">카테고리 :</label>
      <select name="category_id" id="category_id">
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

    <!-- 가격 입력 -->
    <div style="margin-bottom: 10px;">
      <label for="price">가격 :</label>
      <input type="number" name="price" id="price">
    </div>

    <!-- 내용 입력 -->
    <form style="margin-bottom: 10px;">
      <div style="margin-bottom: 10px;">
        <label for="content">내용 :</label>
        <input type="text" name="content" id="content">
      </div>

      <!-- 버튼 -->
      <input type="submit" value="취소">
      <input type="submit" value="저장">
    </form>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useCalendarStore } from '@/stores/counter'

const dateStore = useCalendarStore()
const selectedDate = dateStore.selectedDate


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