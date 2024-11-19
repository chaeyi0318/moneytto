<template>
  <div>
    <div v-if="error">{{ error }}</div>
    <div v-else-if="products.length > 0">
      <table>
        <thead>
          <tr>
            <th>금융회사</th>
            <th>상품명</th>
            <th>적립방식</th>
            <th>세전이자율</th>
            <th>세후이자율</th>
            <th>최고우대금리</th>
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
    <div v-else>
      검색 결과가 없습니다.
    </div>

    <SavingListItemDetail 
      v-if="selectedProduct"
      :product="selectedProduct"
      @close="closeDetails"
    />
  </div>
</template>

<script setup>
import { ref } from 'vue';
import SavingListItem from './SavingListItem.vue';
import SavingListItemDetail from './SavingListItemDetail.vue';

const props = defineProps({
  products: Array,
  error: String,
  showPostTaxInterest: Boolean
});

const selectedProduct = ref(null);

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
}

th {
  background-color: #f2f2f2;
}
</style>
