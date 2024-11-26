<template>
  <div>
    <!-- <span>막대그래프</span> -->
    <BarChart :barGraphData="barGraphData" />
  </div>
</template>

<script setup>
import api from '@/stores/api'
import { onMounted, watch, ref } from 'vue'
import { useAccountStore } from '@/stores/accountStore'
import BarChart from "@/components/calendar/BarChart.vue";

const accountStore = useAccountStore()
const loginUser = accountStore.user.id    // 로그인한 유저id

const props = defineProps({
  yearMonth: {
    type: String,
    required: true,
  },
});

// console.log(props.yearMonth)

const date = ref(`${props.yearMonth}`);

const barGraphData = ref([])
console.log(barGraphData)

const graphData = async (date, loginUser) => {
  try {
    const response = await api.get('/posts/graph-data/', {
      params: { date, loginUser }
    })
    barGraphData.value = response.data
    console.log(response.data)
  } catch (error) {
    if (error.response) {
      console.error('Error response:', error.response.data)
      console.error('Status code:', error.response.status)
    } else if (error.request) {
      console.error('No response received:', error.request)
    } else {
      console.error('Error setting up request:', error.message)
    }
  }
}

watch(
  () => props.yearMonth,
  (newYearMonth) => {
    if (loginUser) {
      graphData(newYearMonth, loginUser); // 변경된 yearMonth와 loginUser를 전달
    }
  },
  { immediate: true } // 컴포넌트가 마운트될 때도 즉시 실행
);

// 컴포넌트가 처음 마운트될 때 초기 데이터 가져오기
onMounted(() => {
  if (loginUser) {
    graphData(props.yearMonth, loginUser); // 초기 yearMonth와 loginUser를 전달
  }
});

</script>

<style scoped>

</style>