﻿<template>
  <div class="solved-container">
    <h1 class="page-title">지난 퀴즈</h1>
    
    <div v-if="totalQuizzes > 0" class="stats-card">
      <p class="stats-total">지금까지 {{ totalQuizzes }}문제를 풀었어요!</p>
      <div class="stats-detail">
        <span class="correct">맞힌 문제: {{ solvedQuizzes.length }}</span>
        <span class="wrong">틀린 문제: {{ failedQuizzes.length }}</span>
      </div>
    </div>
    
    <div v-else class="empty-state">
      <p>아직 문제를 풀지 않았어요! 퀴즈를 풀러 가볼까요?</p>
    </div>
    
    <button @click="goToQuiz" class="quiz-button">퀴즈 풀러 가기</button>
    
    <div class="quiz-lists">
      <QuizList title="맞힌 퀴즈" :quizzes="quizStore.solvedQuizzes" />
      <QuizList title="틀린 퀴즈" :quizzes="quizStore.failedQuizzes" />
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from "vue";
import { useRouter } from "vue-router";
import { useQuizStore } from "@/stores/quizStore";
import QuizList from "./QuizList.vue";

const quizStore = useQuizStore();
const router = useRouter();

const goToQuiz = () => {
  router.push({ name: "Quiz" });
};

const solvedQuizzes = computed(() => quizStore.solvedQuizzes);
const failedQuizzes = computed(() => quizStore.failedQuizzes);

// 새로운 computed 속성 추가
const totalQuizzes = computed(
  () => solvedQuizzes.value.length + failedQuizzes.value.length
);

onMounted(() => {
  quizStore.fetchSolvedQuizzes();
});
</script>

<style scoped>
.solved-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  color: #2E8B57;
  text-align: center;
  margin-bottom: 30px;
}

.stats-card {
  background-color: white;
  border-radius: 15px;
  padding: 25px;
  margin-bottom: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.stats-total {
  font-size: 1.3em;
  color: #2E8B57;
  margin-bottom: 15px;
}

.stats-detail {
  display: flex;
  justify-content: center;
  gap: 30px;
}

.correct {
  color: #2E8B57;
  font-weight: bold;
}

.wrong {
  color: #dc3545;
  font-weight: bold;
}

.empty-state {
  text-align: center;
  color: #666;
  margin: 30px 0;
}

.quiz-button {
  display: block;
  margin: 30px auto;
  background-color: #2E8B57;
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 25px;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.quiz-button:hover {
  background-color: #1a5235;
  transform: translateY(-2px);
}

.quiz-lists {
  margin-top: 40px;
}
</style>
