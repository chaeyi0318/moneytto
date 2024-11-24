<template>
  <div class="recommended-savings">
    <h2 class="main-title">추천 적금 상품</h2>
    <div v-if="savingStore.loading" class="loading">로딩 중...</div>
    <div v-else-if="savingStore.error" class="error-message">{{ savingStore.error }}</div>
    <div v-else class="recommendations-container">
      <div class="recommendation-section age-based">
        <h3 class="section-title">
          <span class="user-nickname">{{ userNickname }}</span>님과 비슷한 연령대의 고객님들이 많이 가입한 상품
        </h3>
        <div class="card-container">
          <RecommendItem
            v-for="saving in savingStore.ageBasedRecommendations.slice(0, 5)"
            :key="saving.id"
            :saving="saving"
          />
        </div>
      </div>
      <div class="recommendation-section income-based">
        <h3 class="section-title">수입 기반 추천 상품</h3>
        <div class="card-container">
          <RecommendItem
            v-for="saving in savingStore.incomeBasedRecommendations.slice(0, 5)"
            :key="saving.id"
            :saving="saving"
          />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted } from "vue";
import { useSavingStore } from "@/stores/savingStore";
import { useAccountStore } from "@/stores/accountStore";
import RecommendItem from "./RecommendItem.vue";

const savingStore = useSavingStore();
const accountStore = useAccountStore();

const userNickname = computed(() => accountStore.user?.nickname || "고객");

onMounted(() => {
  savingStore.fetchRecommendedSavings();
});
</script>

<style scoped>
.recommended-savings {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem;
  background-color: #f8faf6;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(45, 122, 49, 0.1);
}

.main-title {
  color: #2D7A31;
  font-size: 2.2rem;
  font-weight: 700;
  text-align: center;
  margin-bottom: 2rem;
  position: relative;
  padding-bottom: 1rem;
}

.main-title::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100px;
  height: 3px;
  background-color: #2D7A31;
  border-radius: 2px;
}

.recommendation-section {
  background: white;
  border-radius: 16px;
  padding: 2rem;
  margin-bottom: 2rem;
  border: 1px solid #E8F3E9;
  transition: transform 0.3s ease;
}

.recommendation-section:hover {
  transform: translateY(-5px);
}

.section-title {
  color: #2D7A31;
  font-size: 1.5rem;
  margin-bottom: 1.5rem;
  font-weight: 600;
}

.user-nickname {
  color: #246627;
  font-weight: 700;
}

.card-container {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  gap: 1.5rem;
  padding: 0.5rem;
}

.card-container::-webkit-scrollbar {
  height: 8px;
}

.card-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 4px;
}

.card-container::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

.card-container::-webkit-scrollbar-thumb:hover {
  background: #555;
}

.card-container > * {
  flex: 0 0 calc(33.33% - 1rem);
  scroll-snap-align: start;
  min-width: 280px;
}

.loading {
  text-align: center;
  padding: 2rem;
  color: #2D7A31;
  font-size: 1.2rem;
}

.error-message {
  color: #e74c3c;
  text-align: center;
  padding: 2rem;
  background: #fdf0ed;
  border-radius: 12px;
  margin: 1rem 0;
}

@media (max-width: 768px) {
  .recommended-savings {
    padding: 1rem;
  }

  .main-title {
    font-size: 1.8rem;
  }

  .section-title {
    font-size: 1.3rem;
  }

  .recommendation-section {
    padding: 1.5rem;
  }

  .card-container > * {
    flex: 0 0 calc(100% - 1rem);
  }
}
</style>