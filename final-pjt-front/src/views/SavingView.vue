<template>
  <div class="saving-view">
    <h2>적금 상품 검색</h2>
    <Search @search="performSearch" />
    <div v-if="store.loading">검색 중...</div>
    <SavingList
      v-else
      :products="store.products"
      :error="store.error"
      :showPostTaxInterest="hasSearched"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useSavingStore } from "@/stores/counter";
import Search from "@/components/savings/Search.vue";
import SavingList from "@/components/savings/SavingList.vue";

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

<style scoped></style>
