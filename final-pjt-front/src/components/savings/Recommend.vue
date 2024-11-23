<!-- Recommend.vue -->
<template>
  <div class="recommended-savings">
    <h2>추천 적금 상품</h2>
    <div v-if="savingStore.loading">로딩 중...</div>
    <div v-else-if="savingStore.error">{{ savingStore.error }}</div>
    <div v-else>
      <div class="age-based">
        <h3>
          {{ userNickname }}님과 비슷한 연령대의 고객님들이 많이 가입한 상품
        </h3>
        <div class="card-container">
          <RecommendItem
            v-for="saving in savingStore.ageBasedRecommendations.slice(0, 5)"
            :key="saving.id"
            :saving="saving"
          />
        </div>
      </div>
      <div class="income-based">
        <h3>수입 기반 추천 상품</h3>
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

<script>
import { ref, onMounted, computed } from "vue";
import { useSavingStore } from "@/stores/savingStore";
import { useAccountStore } from "@/stores/accountStore";
import RecommendItem from "./RecommendItem.vue";

export default {
  name: "RecommendedSavings",
  components: {
    RecommendItem,
  },
  setup() {
    const savingStore = useSavingStore();
    const accountStore = useAccountStore();

    const userNickname = computed(() => accountStore.user?.nickname || "고객");

    onMounted(() => {
      savingStore.fetchRecommendedSavings();
    });

    return {
      savingStore,
      userNickname,
    };
  },
};
</script>

<style scoped>
.recommended-savings {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

h2 {
  color: #2E8B57;
  font-size: 2em;
  margin-bottom: 30px;
}

h3 {
  color: #2E8B57;
  font-size: 1.5em;
  margin: 20px 0;
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin: 20px 0;
}

.age-based,
.income-based {
  margin-bottom: 40px;
}
</style>