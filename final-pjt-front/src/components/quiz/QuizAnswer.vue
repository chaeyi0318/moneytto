<template>
  <div>
    <p>{{ quizStore.isCorrect ? "정답입니다!" : "틀렸습니다." }}</p>
    <p v-if="quizStore.pointsEarned > 0">
      {{ quizStore.pointsEarned }}포인트 획득!
    </p>
    <p>설명: {{ quizStore.explanation }}</p>
    <button @click="nextQuiz">다음 문제</button>
  </div>
</template>

<script setup>
import { useQuizStore } from "@/stores/quizStore";

const quizStore = useQuizStore();

const nextQuiz = () => {
  quizStore.fetchRandomQuiz();
};
</script>
