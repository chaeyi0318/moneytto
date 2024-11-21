<template>
  <div>
    <div v-if="error">{{ error }}</div>
    <div v-else-if="products.length > 0">
      <table>
        <thead>
          <tr>
            <th @click="sort('bank_name')" class="sortable-header">
              금융회사
              <div
                class="sort-indicator"
                v-if="store.sortField === 'bank_name'"
              >
                <div
                  class="triangle"
                  :class="{
                    'triangle-down': store.sortOrder === 'desc',
                    'triangle-up': store.sortOrder === 'asc',
                  }"
                ></div>
              </div>
            </th>
            <th @click="sort('product_name')" class="sortable-header">
              상품명
              <div
                class="sort-indicator"
                v-if="store.sortField === 'product_name'"
              >
                <div
                  class="triangle"
                  :class="{
                    'triangle-down': store.sortOrder === 'desc',
                    'triangle-up': store.sortOrder === 'asc',
                  }"
                ></div>
              </div>
            </th>
            <th @click="sort('saving_method')" class="sortable-header">
              적립방식
              <div
                class="sort-indicator"
                v-if="store.sortField === 'saving_method'"
              >
                <div
                  class="triangle"
                  :class="{
                    'triangle-down': store.sortOrder === 'desc',
                    'triangle-up': store.sortOrder === 'asc',
                  }"
                ></div>
              </div>
            </th>
            <th @click="sort('pre_tax_interest_rate')" class="sortable-header">
              세전이자율
              <div
                class="sort-indicator"
                v-if="store.sortField === 'pre_tax_interest_rate'"
              >
                <div
                  class="triangle"
                  :class="{
                    'triangle-down': store.sortOrder === 'desc',
                    'triangle-up': store.sortOrder === 'asc',
                  }"
                ></div>
              </div>
            </th>
            <th @click="sort('post_tax_interest_rate')" class="sortable-header">
              세후이자율
              <div
                class="sort-indicator"
                v-if="store.sortField === 'post_tax_interest_rate'"
              >
                <div
                  class="triangle"
                  :class="{
                    'triangle-down': store.sortOrder === 'desc',
                    'triangle-up': store.sortOrder === 'asc',
                  }"
                ></div>
              </div>
            </th>
            <th @click="sort('max_preference_rate')" class="sortable-header">
              최고우대금리
              <div
                class="sort-indicator"
                v-if="store.sortField === 'max_preference_rate'"
              >
                <div
                  class="triangle"
                  :class="{
                    'triangle-down': store.sortOrder === 'desc',
                    'triangle-up': store.sortOrder === 'asc',
                  }"
                ></div>
              </div>
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
    <div v-else>검색 결과가 없습니다.</div>

    <SavingListItemDetail
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="closeDetails"
    />
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useSavingStore } from "@/stores/savingStore";
import SavingListItem from "./SavingListItem.vue";
import SavingListItemDetail from "./SavingListItemDetail.vue";

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
table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th,
td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
  background-color: #fff;
}

th {
  background-color: #f8f9fa;
  font-weight: normal;
}

.check-column {
  width: 80px;
  text-align: center;
}

.sortable-header {
  cursor: pointer;
  position: relative;
  padding-right: 20px;
  user-select: none;
}

.sortable-header:hover {
  background-color: #e9ecef;
}

.sort-indicator {
  position: absolute;
  right: 5px;
  top: 50%;
  transform: translateY(-50%);
}

.triangle {
  width: 0;
  height: 0;
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
}

.triangle-up {
  border-bottom: 4px solid #666;
}

.triangle-down {
  border-top: 4px solid #666;
}

tbody tr:hover {
  background-color: #f5f5f5;
}

/* 반응형 테이블 스타일 */
@media screen and (max-width: 768px) {
  table {
    display: block;
    overflow-x: auto;
    white-space: nowrap;
  }
}
</style>
