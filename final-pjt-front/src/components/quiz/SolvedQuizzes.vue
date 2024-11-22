<template>
  <div>
    <h1>풀었던 퀴즈</h1>
    <div v-if="totalQuizzes > 0" class="quiz-stats">
      <p>우와! 지금까지 {{ totalQuizzes }}문제를 풀었어요!</p>
      <p>
        {{ solvedQuizzes.length }}문제를 맞혔고 {{ failedQuizzes.length }}문제를
        틀렸네요!
      </p>
    </div>
    <div v-else class="no-quizzes-message">
      <p>아직 문제를 풀지 않았어요! 퀴즈를 풀러 가볼까요?</p>
    </div>
    <button @click="goToQuiz" class="quiz-btn">퀴즈 풀러 가기</button>
    <QuizList title="맞힌 퀴즈" :quizzes="quizStore.solvedQuizzes" />
    <QuizList title="틀린 퀴즈" :quizzes="quizStore.failedQuizzes" />
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
.quiz-stats {
  background-color: #f0f0f0;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.quiz-stats p {
  margin: 5px 0;
  font-weight: bold;
}

.quiz-btn {
  margin-top: 20px;
  padding: 10px 15px;
  background-color: #008cba;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

.quiz-btn:hover {
  background-color: #007b9a;
}
</style>
