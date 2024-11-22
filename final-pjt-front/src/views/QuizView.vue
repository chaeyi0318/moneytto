<template>
  <div>
    <h1>금융 퀴즈</h1>
    <p>퀴즈 풀고 포인트 겟 겟!</p>
    <button @click="goToSolvedQuizzes" class="solved-quizzes-btn">
      풀었던 퀴즈 보기
    </button>
    <hr />
    <QuizQuestion v-if="quizStore.currentQuiz" />
    <QuizAnswer v-if="quizStore.isCorrect !== null" />
    <p v-if="!quizStore.currentQuiz">
      {{ quizStore.message || "퀴즈를 불러오는 중..." }}
    </p>
  </div>
</template>

<script setup>
import { onMounted } from "vue";
import { useRouter } from "vue-router";
import { useQuizStore } from "@/stores/quizStore";
import QuizQuestion from "@/components/quiz/QuizQuestion.vue";
import QuizAnswer from "@/components/quiz/QuizAnswer.vue";

const quizStore = useQuizStore();
const router = useRouter();

const goToSolvedQuizzes = () => {
  router.push({ name: "SolvedQuizzes" });
};

onMounted(() => {
  quizStore.fetchRandomQuiz();
});
</script>

<style scoped>
.solved-quizzes-btn {
  margin-top: 20px;
  padding: 10px 15px;
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.solved-quizzes-btn:hover {
  background-color: #45a049;
}
</style>
