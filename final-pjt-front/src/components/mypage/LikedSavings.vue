<template>
   <div class="liked-savings-container">
    <div class="page-header">
      <h1>찜한 적금 모아보기</h1>
      <div class="savings-count">
        <span class="user-name">{{ userNickname }}</span>님이 찜한 상품의 개수: 
        <span class="count">총 {{ likedSavingsCount }}개</span>
      </div>
    </div>

    <div class="savings-content">
      <div v-if="likedSavingsCount > 0" class="savings-grid">
        <LikedSavingsItem
          v-for="saving in likedSavings"
          :key="saving.id"
          :saving="saving"
          @show-details="showDetails"
        />
      </div>
      <div v-else class="empty-state">
        <p>찜한 상품이 없습니다. 마음에 드는 적금 상품을 찜해보세요!</p>
      </div>
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
.liked-savings-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.page-header {
  margin-bottom: 30px;
}

.page-header h1 {
  color: #2E8B57;
  font-size: 2em;
  margin-bottom: 15px;
}

.savings-count {
  background-color: #f0f8f4;
  padding: 15px;
  border-radius: 10px;
  color: #666;
}

.user-name {
  color: #2E8B57;
  font-weight: 600;
}

.count {
  color: #2E8B57;
  font-weight: 600;
}

.savings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  background-color: #f8f9fa;
  border-radius: 10px;
  color: #666;
}

.error-message {
  color: #dc3545;
  padding: 15px;
  background-color: #f8d7da;
  border-radius: 8px;
  margin-top: 20px;
}

@media (max-width: 768px) {
  .savings-grid {
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  }
}
</style>
