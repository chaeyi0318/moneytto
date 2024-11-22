<template>
  <div class="quiz-box">
    <p class="text-end">
      획득 가능 포인트: {{ quizStore.currentQuiz.difficulty * 10 }}P
    </p>
    <h2>{{ quizStore.currentQuiz.question }}</h2>
    <button @click="submitAnswer('O')">O</button>
    <button @click="submitAnswer('X')">X</button>
  </div>
</template>

<script setup>
import { useQuizStore } from "@/stores/quizStore";

const quizStore = useQuizStore();

const submitAnswer = (answer) => {
  quizStore.submitAnswer(answer);
};
</script>

<style scoped>
.quiz-box {
  border: 1px solid black;
  display: flex;
  max-width: 1000px;
  text-align: center;
  flex-direction: column;
  justify-content: center;
  justify-items: center;
}
</style>
