<template>
  <div class="quiz-list-container">
    <h2 class="list-title">{{ title }}</h2>
    <div class="quiz-list">
      <div v-for="quiz in quizzes" :key="quiz.id" class="quiz-item">
        <div class="quiz-content">
          <div class="quiz-header">
            <span class="difficulty-badge">난이도: {{ quiz.difficulty }}</span>
          </div>
          
          <div class="quiz-body">
            <p class="question">
              <span class="label">문제</span>
              {{ quiz.question }}
            </p>
            
            <p class="answer">
              <span class="label">정답</span>
              {{ quiz.answer }}
            </p>
            
            <p class="explanation">
              <span class="label">설명</span>
              {{ quiz.explanation }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>


<script setup>
defineProps({
  title: String,
  quizzes: Array,
});
</script>

<style scoped>
.quiz-list-container {
  margin: 30px 0;
}

.list-title {
  color: #2E8B57;
  font-size: 1.5em;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #e0e0e0;
}

.quiz-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.quiz-item {
  background-color: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.quiz-item:hover {
  transform: translateY(-2px);
}

.quiz-content {
  padding: 20px;
}

.quiz-header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 15px;
}

.difficulty-badge {
  background-color: #f0f8f4;
  color: #2E8B57;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.9em;
  font-weight: 500;
}

.quiz-body p {
  margin-bottom: 12px;
  line-height: 1.5;
}

.label {
  display: inline-block;
  background-color: #2E8B57;
  color: white;
  padding: 4px 12px;
  border-radius: 15px;
  font-size: 0.9em;
  margin-right: 10px;
  min-width: 60px;
  text-align: center;
}

.question {
  font-size: 1.1em;
  margin-bottom: 15px;
}

.answer {
  color: #2E8B57;
  font-weight: 500;
}

.explanation {
  background-color: #f0f8f4;
  padding: 15px;
  border-radius: 8px;
  margin-top: 15px;
}

@media (max-width: 768px) {
  .quiz-content {
    padding: 15px;
  }
  
  .label {
    margin-bottom: 5px;
    display: block;
  }
}
</style>
