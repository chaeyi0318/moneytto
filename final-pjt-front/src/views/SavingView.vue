<template>
  <div class="saving-container">
    <div class="header-section">
      <!-- <RouterLink :to="{ name: 'Recommend' }" class="recommend-link">
        <button class="btn btn-primary">적금 추천받기</button>
      </RouterLink> -->
      <!-- <h2 class="main-title text-center">적금 상품 검색</h2> -->
    </div>
    <Search @search="performSearch" />
    <div v-if="store.loading" class="loading-message">
      <span>잠시만 기다려주세요!</span>
    </div>
    <SavingList
      v-else
      :products="store.products"
      :error="store.error"
      :showPostTaxInterest="hasSearched"
    />
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted } from "vue";
import { useSavingStore } from "@/stores/savingStore";
import Search from "@/components/savings/Search.vue";
import SavingList from "@/components/savings/SavingList.vue";
import Recommend from "@/components/savings/Recommend.vue";

const store = useSavingStore();
const hasSearched = ref(false);

const performSearch = (searchParams) => {
  store.getSavings(searchParams);
  hasSearched.value = true;
};

onMounted(() => {
  store.getSavings();
});
</script>

<style scoped>
.saving-container {
  max-width: 1300px;
  margin: 0 auto;
  padding: 20px;
}

.header-section {
  margin-bottom: 30px;
}

.recommend-link {
  text-decoration: none;
  color: #2E8B57;
  transition: color 0.3s ease;
}

.recommend-link:hover {
  color: #1a5235;
}

.main-title {
  color: #2E8B57;
  font-size: 2em;
  margin: 20px 0;
}

.loading-message {
  text-align: center;
  padding: 20px;
  color: #2E8B57;
  font-size: 1.2em;
}
</style>
