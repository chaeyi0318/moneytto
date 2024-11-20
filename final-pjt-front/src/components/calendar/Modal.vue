<template>
  <!-- 오버레이 클릭 시 closeModal 호출 -->
  <div class="modal-overlay" @click.self="closeModal">
    <div class="modal-content">
      <header>
        <p>{{ date }}</p>
        <button @click="closeModal">X</button> 
      </header>
      <slot></slot> 
    </div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits } from "vue";

const props = defineProps({
  date : String,
});

const emit = defineEmits(["closeModal"]); // closeModal 이벤트 정의

const closeModal = () => {
  emit("closeModal"); // 부모 컴포넌트에 closeModal 이벤트 전달
};
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
</style>