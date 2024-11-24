<template>
  <div class="quiz-container">
    <h1 class="quiz-title">퀴즈 풀고 포인트 겟 겟!</h1>
    <hr class="divider" />
    <QuizQuestion v-if="quizStore.currentQuiz" />
    <QuizAnswer v-if="quizStore.isCorrect !== null" />
    <p v-if="!quizStore.currentQuiz" class="loading-message">
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
.quiz-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 30px;
  text-align: center;
  background-color: #f8faf6;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(45, 122, 49, 0.1);
}

.quiz-title {
  color: #2D7A31;
  font-size: 2.0em;
  margin-bottom: 20px;
  font-weight: 700;
  text-shadow: 1px 1px 2px rgba(45, 122, 49, 0.1);
}

.divider {
  border: none;
  height: 3px;
  background: linear-gradient(to right, transparent, #2D7A31, transparent);
  margin: 30px 0;
  opacity: 0.3;
}

.loading-message {
  color: #2D7A31;
  font-size: 1.2em;
  margin: 30px 0;
  font-weight: 500;
}
</style>