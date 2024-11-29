// src/stores/quizStore.js
import { defineStore } from "pinia";
import { ref } from "vue";
import api from "./api";

export const useQuizStore = defineStore("quiz", () => {
  const currentQuiz = ref(null);
  const solvedQuizzes = ref([]);
  const failedQuizzes = ref([]);
  const userAnswer = ref(null);
  const isCorrect = ref(null);
  const explanation = ref("");
  const pointsEarned = ref(0);
  const message = ref("");
  const answered = ref("false");

  async function fetchRandomQuiz() {
    try {
      const response = await api.get("/quizzes/random-quiz/");
      currentQuiz.value = response.data;
      userAnswer.value = null;
      isCorrect.value = null;
      explanation.value = "";
      pointsEarned.value = 0;
      answered.value = false;
    } catch (error) {
      console.error("퀴즈를 가져오는 중 오류 발생:", error);
      message.value = "퀴즈를 가져오는 중 오류가 발생했습니다.";
    }
  }

  async function submitAnswer(answer) {
    try {
      const response = await api.post(
        `/quizzes/answer-quiz/${currentQuiz.value.id}/`,
        { answer }
      );
      isCorrect.value = response.data.is_correct;
      explanation.value = response.data.explanation;
      pointsEarned.value = response.data.points_earned;
    } catch (error) {
      console.error("답변 제출 중 오류 발생:", error);
      message.value = "답변을 제출하는 중 오류가 발생했습니다.";
    }
  }

  async function fetchSolvedQuizzes() {
    try {
      const response = await api.get("/quizzes/solved-quizzes/");
      solvedQuizzes.value = response.data.solved_quizzes;
      failedQuizzes.value = response.data.failed_quizzes;
    } catch (error) {
      console.error("풀었던 퀴즈를 가져오는 중 오류 발생:", error);
      message.value = "풀었던 퀴즈를 가져오는 중 오류가 발생했습니다.";
    }
  }

  return {
    currentQuiz,
    solvedQuizzes,
    failedQuizzes,
    userAnswer,
    isCorrect,
    explanation,
    pointsEarned,
    message,
    fetchRandomQuiz,
    submitAnswer,
    fetchSolvedQuizzes,
  };
});
