﻿<template>
  <div class="answer-box">
    <div class="result-message" :class="{ 'correct': quizStore.isCorrect }">
      {{ quizStore.isCorrect ? "정답입니다!" : "틀렸습니다." }}
    </div>
    <div v-if="quizStore.pointsEarned > 0" class="points-earned">
      +{{ quizStore.pointsEarned }}P
    </div>
    <div class="explanation">
      <h3>설명</h3>
      <p>{{ quizStore.explanation }}</p>
    </div>
    <button @click="nextQuiz" class="next-button">다음 문제</button>
  </div>
</template>


<script setup>
import { useQuizStore } from "@/stores/quizStore";

const quizStore = useQuizStore();

const nextQuiz = () => {
  quizStore.fetchRandomQuiz();
};
</script>


<style scoped>
.answer-box {
  background-color: white;
  border-radius: 15px;
  padding: 30px;
  margin: 20px auto;
  max-width: 600px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.result-message {
  font-size: 1.5em;
  font-weight: bold;
  margin-bottom: 15px;
  color: #dc3545;
}

.result-message.correct {
  color: #2E8B57;
}

.points-earned {
  font-size: 2em;
  color: #2E8B57;
  margin: 20px 0;
  font-weight: bold;
}

.explanation {
  background-color: #f0f8f4;
  padding: 20px;
  border-radius: 10px;
  margin: 20px 0;
  text-align: left;
}

.explanation h3 {
  color: #2E8B57;
  margin-bottom: 10px;
}

.next-button {
  background-color: #2E8B57;
  color: white;
  padding: 12px 30px;
  border: none;
  border-radius: 25px;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.next-button:hover {
  background-color: #1a5235;
  transform: translateY(-2px);
}
</style>
