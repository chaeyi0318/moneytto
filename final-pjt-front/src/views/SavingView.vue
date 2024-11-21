<template>
  <div class="saving-view">
    <RouterLink :to="{ name: 'Recommend' }"><h3>추천 적금 상품</h3></RouterLink>
    <h2>적금 상품 검색</h2>
    <Search @search="performSearch" />
    <div v-if="store.loading">잠시만 기다려주세요!</div>
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

<style scoped></style>
