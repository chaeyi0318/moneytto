<template>
  <div>
    <h1>찜한 적금 모아보기</h1>

    <div class="liked">
      <h4>
        {{ userNickname }}님이 찜한 상품의 개수: 총 {{ likedSavingsCount }}개
      </h4>
      <div v-if="likedSavingsCount > 0" class="card-container">
        <LikedSavingsItem
          v-for="saving in likedSavings"
          :key="saving.id"
          :saving="saving"
          @show-details="showDetails"
        />
      </div>
      <p v-else>찜한 상품이 없습니다. 마음에 드는 적금 상품을 찜해보세요!</p>
    </div>

    <!-- 상세보기 모달 -->
    <LikedSavingsItemDetail
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="closeDetails"
    />

    <div v-if="savingStore.error" class="error">
      <p>{{ savingStore.error }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import { useSavingStore } from "@/stores/savingStore";
import { useAccountStore } from "@/stores/accountStore";
import LikedSavingsItem from "./LikedSavingsItem.vue";
import LikedSavingsItemDetail from "./LikedSavingsItemDetail.vue";

const accountStore = useAccountStore();
const savingStore = useSavingStore();
const likedSavings = ref([]);
const selectedProduct = ref(null);

const userNickname = computed(() => accountStore.user?.nickname || "고객");
const likedSavingsCount = computed(() => likedSavings.value.length);

const fetchLikedSavings = async () => {
  const data = await savingStore.fetchLikedSavings();
  likedSavings.value = data;
};

const showDetails = (product) => {
  selectedProduct.value = product; // 선택된 상품 저장
};

const closeDetails = () => {
  selectedProduct.value = null; // 상세보기 닫기
};

onMounted(() => {
  fetchLikedSavings();
});
</script>

<style scoped>
.card-container {
  display: flex;
  justify-content: left;
  flex-wrap: wrap;
  gap: 20px;
}
</style>