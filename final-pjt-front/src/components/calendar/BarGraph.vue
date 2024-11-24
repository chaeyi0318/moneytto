<template>
  <div>
    <h1>막대그래프</h1>
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

const currentYear = new Date().getFullYear()
const currentMonth = String(new Date().getMonth() + 1).padStart(2, '0')
const date = `${currentYear}-${currentMonth}`

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

onMounted(() => {
  const loginUser = ref(accountStore.user?.id)

  watch(
    loginUser,
    (newVal) => {
      if (newVal) {
        graphData(date, newVal)
      }
    },
    { immediate: true }
  )
})

</script>

<style scoped>

</style>