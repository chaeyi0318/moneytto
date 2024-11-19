<template>
  <div class="calendar">
     <nav>
        <h3>{{ cal.yearText }} - {{ cal.monthText }}</h3>
        <div class="navs">
           <button @click="prevMonth">prev</button>
           <button @click="nextMonth">next</button>
        </div>
     </nav>
  
     <section class="dow">
        <div v-for="day in days" :key="day" class="day">{{ day }}</div>
     </section>
  
     <section class="body">
        <div v-for="week in cal.getWeeks()" :key="week" class="week">
           <div v-for="date in week.days()" :key="date.ymdText" class="cell" :class="{ oob: !cal.containsDate(date), today: cal.isToday(date), sunday: date.weekOffset === 0, saturday: date.weekOffset === 6 }">
              <span class="date">{{ date.date }}</span>
           </div>
        </div>
     </section>
  </div>
  </template>
  
  <script setup>
  import { ref } from 'vue';
  import { Calendar } from './Calendar'; // 경로 수정됨
  
  const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
  const currentYear = new Date().getFullYear();
  const currentMonth = new Date().getMonth() + 1;
  
  let cal = ref(Calendar.fromYm(currentYear, currentMonth));
  
  const prevMonth = () => {
     cal.value = cal.value.prevMonth();
  };
  
  const nextMonth = () => {
     cal.value = cal.value.nextMonth();
  };
  </script>
  
  <style scoped>
  .calendar { 
     display: flex; 
     flex-direction: column; 
     height: auto; 
  }
  
  .navs {
     display: flex;
     justify-content: space-between;
     margin-bottom: 10px;
  }
  
  .navs button { 
     padding: 5px 10px; 
  }
  
  .dow {
     display: grid;
     grid-template-columns: repeat(7, 1fr);
     text-align: center;
  }
  
  .dow .day {
     font-weight: bold;
     padding-bottom: 10px;
  }
  
  .body {
     display: grid;
     grid-template-columns: repeat(7, 1fr);
  }
  
  .week {
     display: contents; /* 각 주의 날짜를 그리드 내에서 개별적으로 배치 */
  }
  
  .cell {
     display: flex;
     justify-content: center;
     align-items: center;
     height: 80px;
     border-bottom: 1px solid #e0e0e0;
  }
  
  .date {
     display: inline-block;
     width: 40px;
     height: 40px;
     line-height: 40px;
     text-align: center;
     border-radius: 50%;
  }
  
  .oob .date { 
     color: #ccc; /* 현재 달에 속하지 않는 날짜 흐리게 */
  }
  
  .today .date { 
     background-color: lightblue; /* 오늘 날짜 강조 */
  }
  
  .sunday .date {
     color: red; /* 일요일 빨간색 */
  }
  
  .saturday .date {
     color: blue; /* 토요일 파란색 */
  }
  
  /* 마우스 오버 시 날짜 셀 강조 */
  .cell:hover .date {
      background-color: rgba(0, 0, 255, 0.1);
  }
  </style>
  