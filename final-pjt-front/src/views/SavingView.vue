<template>
  <div class="saving-container">
    <div class="header-section">
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
    <!-- 페이지네이션 버튼 -->
    <div class="pagination" v-if="store.pagination.count > 0">
      <button type="button" @click.prevent="fetchPreviousPage" :disabled="!store.pagination.previous"><</button>
      <span>{{ currentPage }} / {{ totalPages }}</span>
      <button type="button" @click.prevent="fetchNextPage" :disabled="!store.pagination.next">></button>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted, computed } from "vue";
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

const currentPage = computed(() => {
  const nextUrl = store.pagination.next ? new URL(store.pagination.next) : null;
  const nextPage = nextUrl ? parseInt(nextUrl.searchParams.get("page")) : null;
  return nextPage ? nextPage - 1 : 1;
});

const totalPages = computed(() => {
  return Math.ceil(store.pagination.count / 10);
});

const fetchNextPage = () => {
  store.fetchNextPage();
};

const fetchPreviousPage = () => {
  store.fetchPreviousPage();
};

onMounted(() => {
  store.getSavings();
});
</script>

<style scoped>
.saving-container {
  max-width: 1400px;
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

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  margin-top: 20px;
}

.pagination button {
  background-color: #2E8B57;
  color: #fff;
  border: none;
  padding: 10px 20px;
  margin: 0 10px;
  cursor: pointer;
  transition: background-color 0.3s ease;
  border-radius: 50%;
  outline: none;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: default;
}

.pagination button:hover:not(:disabled) {
  background-color: #1a5235;
}

.pagination span {
  font-size: 1.2em;
  color: #2E8B57;
}
</style>
