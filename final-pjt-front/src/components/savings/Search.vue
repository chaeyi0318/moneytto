<template>
  <div>
    <h3>적금 상품 검색하기</h3>
    <form @submit.prevent="savingSearch">
      <div>
        <label for="amount">월 저축 금액</label>
        <input v-model="amount" id="amount" type="number" />
      </div>
      <div>
        <label for="period">저축 예정기간(개월)</label>
        <input v-model="period" id="period" type="number" />
      </div>
      <input type="submit" value="검색" :disabled="store.loading" />
    </form>

    <div v-if="store.loading">검색 중...</div>
    <div v-else-if="store.error">{{ store.error }}</div>
    <div v-else-if="store.products && store.products.length > 0">
      <h4>검색 결과</h4>
      <table>
        <thead>
          <tr>
            <th>은행명</th>
            <th>상품명</th>
            <th>적립방식</th>
            <th>세전이자율</th>
            <th>세후이자율</th>
            <th>최고우대금리</th>
            <th>가입대상</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="product in store.products" :key="product.id">
            <td>{{ product.bank_name }}</td>
            <td>{{ product.product_name }}</td>
            <td>{{ product.saving_method }}</td>
            <td>{{ product.pre_tax_interest_rate }}%</td>
            <td>{{ product.post_tax_interest_rate }}%</td>
            <td>{{ product.max_preference_rate }}%</td>
            <td>{{ product.eligibility }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else-if="store.products && store.products.length === 0">
      검색 결과가 없습니다.
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useSavingStore } from "@/stores/counter";

const store = useSavingStore();

const amount = ref(null);
const period = ref(null);

const savingSearch = () => {
  if (amount.value && period.value) {
    store.getSavings(amount.value, period.value);
  }
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
