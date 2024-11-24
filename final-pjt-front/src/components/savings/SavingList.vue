<template>
  <div class="savings-table-container">
    <div v-if="error" class="error-message">{{ error }}</div>
    <div v-else-if="products.length > 0">
      <table>
        <thead>
          <tr>
            <th @click="sort('bank_name')" class="sortable-header">
              금융회사
              <SortIndicator :active="store.sortField === 'bank_name'" :order="store.sortOrder" />
            </th>
            <th @click="sort('product_name')" class="sortable-header">
              상품명
              <SortIndicator :active="store.sortField === 'product_name'" :order="store.sortOrder" />
            </th>
            <th @click="sort('saving_method')" class="sortable-header">
              적립방식
              <SortIndicator :active="store.sortField === 'saving_method'" :order="store.sortOrder" />
            </th>
            <th @click="sort('pre_tax_interest_rate')" class="sortable-header">
              세전이자율
              <SortIndicator :active="store.sortField === 'pre_tax_interest_rate'" :order="store.sortOrder" />
            </th>
            <th @click="sort('post_tax_interest_rate')" class="sortable-header">
              세후이자율
              <SortIndicator :active="store.sortField === 'post_tax_interest_rate'" :order="store.sortOrder" />
            </th>
            <th @click="sort('max_preference_rate')" class="sortable-header">
              최고우대금리
              <SortIndicator :active="store.sortField === 'max_preference_rate'" :order="store.sortOrder" />
            </th>
            <th>가입대상</th>
            <th>이자계산방식</th>
            <th v-if="showPostTaxInterest">세후이자(예시)</th>
            <th>상세정보</th>
          </tr>
        </thead>
        <tbody>
          <SavingListItem
            v-for="product in products"
            :key="product.id"
            :product="product"
            :showPostTaxInterest="showPostTaxInterest"
            @show-details="showDetails"
          />
        </tbody>
      </table>
    </div>
    <div v-else class="no-results">검색 결과가 없습니다.</div>

    <SavingListItemDetail
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="closeDetails"
    />
  </div>
</template>

<script setup>
import { ref, defineComponent } from "vue";
import { useSavingStore } from "@/stores/savingStore";
import SavingListItem from "./SavingListItem.vue";
import SavingListItemDetail from "./SavingListItemDetail.vue";
import SortIndicator from "./SortIndicator.vue";

const store = useSavingStore();
const props = defineProps({
  products: Array,
  error: String,
  showPostTaxInterest: Boolean,
});

const selectedProduct = ref(null);

const sort = (field) => {
  store.updateSort(field);
};

const showDetails = (product) => {
  selectedProduct.value = product;
};

const closeDetails = () => {
  selectedProduct.value = null;
};
</script>

<style scoped>
.savings-table-container {
  background-color: #f8faf6;
  padding: 20px;
  border-radius: 20px;
  box-shadow: 0 4px 12px rgba(45, 122, 49, 0.1);
}

table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  background: white;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 2px 8px rgba(45, 122, 49, 0.08);
}

th {
  background-color: #2E8B57;
  color: white;
  padding: 16px;
  font-weight: 600;
  font-size: 0.95rem;
  text-align: left;
  position: relative;
}

th:first-child {
  border-top-left-radius: 12px;
}

th:last-child {
  border-top-right-radius: 12px;
}

td {
  padding: 14px 16px;
  border-bottom: 1px solid #E8F3E9;
  color: #333;
  font-size: 0.9rem;
}

.sortable-header {
  cursor: pointer;
  user-select: none;
  transition: background-color 0.2s ease;
}

.sortable-header:hover {
  background-color: #1a5235;
}

.sort-indicator {
  display: inline-block;
  margin-left: 4px;
  vertical-align: middle;
}

.sort-arrow {
  font-size: 0.8em;
  color: white;
  opacity: 0.8;
  transition: transform 0.2s ease;
}

.sort-arrow-down {
  transform: rotate(180deg);
}

tbody tr {
  transition: background-color 0.2s ease;
}

tbody tr:hover {
  background-color: #f8faf6;
}

.error-message {
  color: #e74c3c;
  text-align: center;
  padding: 20px;
  background: #fdf0ed;
  border-radius: 12px;
  margin: 20px 0;
}

.no-results {
  text-align: center;
  padding: 40px;
  color: #666;
  font-size: 1.1em;
}

button {
  background-color: #2D7A31;
  color: white;
  border: none;
  padding: 8px 16px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

button:hover {
  background-color: #246627;
  transform: translateY(-1px);
  box-shadow: 0 2px 4px rgba(45, 122, 49, 0.2);
}

button:active {
  transform: translateY(0);
}

@media (max-width: 768px) {
  .savings-table-container {
    padding: 10px;
    border-radius: 12px;
  }

  table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }

  th, td {
    padding: 12px;
    font-size: 0.85rem;
  }
}
</style>