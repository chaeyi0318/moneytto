<template>
  <div class="quiz-container">
    <h1 class="quiz-title">퀴즈 풀고 포인트 겟 겟!</h1>
    <!-- <p class="quiz-subtitle">퀴즈 풀고 포인트 겟 겟!</p> -->
    <!-- <button @click="goToSolvedQuizzes" class="history-button">
      지난 퀴즈
    </button> -->
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
  padding: 20px;
  text-align: center;
}

.quiz-title {
  color: #2E8B57;
  font-size: 2.5em;
  margin-bottom: 10px;
}

.quiz-subtitle {
  color: #666;
  font-size: 1.2em;
  margin-bottom: 20px;
}

.history-button {
  background-color: #2E8B57;
  color: white;
  padding: 12px 24px;
  border: none;
  border-radius: 25px;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.history-button:hover {
  background-color: #1a5235;
  transform: translateY(-2px);
}

.divider {
  border: none;
  height: 2px;
  background-color: #e0e0e0;
  margin: 30px 0;
}

.loading-message {
  color: #666;
  font-size: 1.1em;
  margin: 20px 0;
}
</style>
