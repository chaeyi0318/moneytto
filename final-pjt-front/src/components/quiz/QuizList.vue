<template>
  <div>
    <h2>{{ title }}</h2>
    <ul>
      <li v-for="quiz in quizzes" :key="quiz.id">
        <strong>문제:</strong> {{ quiz.question }} <br />
        <strong>정답:</strong> {{ quiz.answer }} <br />
        <strong>설명:</strong> {{ quiz.explanation }} <br />
        <strong>난이도:</strong> {{ quiz.difficulty }}
      </li>
    </ul>
  </div>
</template>

<script setup>
defineProps({
  title: String,
  quizzes: Array,
});
</script>
