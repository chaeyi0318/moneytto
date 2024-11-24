﻿<template>
  <div class="quiz-box">
    <div class="points-badge">
      획득 가능 포인트: {{ quizStore.currentQuiz.difficulty * 10 }}P
    </div>
    <h2 class="question-text">{{ quizStore.currentQuiz.question }}</h2>
    <div class="answer-buttons">
      <button @click="submitAnswer('O')" class="answer-btn o-btn" :disabled="answered">O</button>
      <button @click="submitAnswer('X')" class="answer-btn x-btn" :disabled="answered">X</button>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import { useQuizStore } from "@/stores/quizStore";

const answered = ref(false);
const quizStore = useQuizStore();

const submitAnswer = (answer) => {
  answered.value = true;
  quizStore.submitAnswer(answer);
};
</script>

<style scoped>
.quiz-box {
  background-color: white;
  border-radius: 15px;
  padding: 30px;
  margin: 20px auto;
  max-width: 600px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.points-badge {
  background-color: #f0f8f4;
  color: #2E8B57;
  padding: 8px 15px;
  border-radius: 20px;
  display: inline-block;
  margin-bottom: 20px;
  font-weight: 500;
}

.question-text {
  color: #333;
  font-size: 1.3em;
  margin-bottom: 30px;
  line-height: 1.5;
}

.answer-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.answer-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  box-shadow: none;
}

.answer-btn {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  border: none;
  font-size: 2em;
  font-weight: bold;
  cursor: pointer;
  transition: all 0.3s ease;
}

.o-btn {
  background-color: #2E8B57;
  color: white;
}

.x-btn {
  background-color: #dc3545;
  color: white;
}

.answer-btn:hover {
  transform: scale(1.1);
}
</style>
