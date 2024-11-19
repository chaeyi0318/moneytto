<template>
    <div class="recommended-savings">
      <h2>추천 적금 상품</h2>
      <div v-if="savingStore.loading">로딩 중...</div>
      <div v-else-if="savingStore.error">{{ savingStore.error }}</div>
      <div v-else-if="savingStore.recommendedSavings.length" class="savings-grid">
        <RecommendItem 
          v-for="saving in savingStore.recommendedSavings" 
          :key="saving.id" 
          :saving="saving"
        />
      </div>
      <p v-else>추천할 적금 상품이 없습니다.</p>
    </div>
  </template>
  
  <script>
  import { useSavingStore } from '@/stores/counter';
  import RecommendItem from './RecommendItem.vue';
  
  export default {
    name: 'RecommendedSavings',
    components: {
      RecommendItem,
    },
    setup() {
      const savingStore = useSavingStore();
  
      savingStore.fetchRecommendedSavings();
  
      return {
        savingStore,
      };
    },
  };
  </script>
  
  <style scoped>
  .savings-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
  }
  </style>