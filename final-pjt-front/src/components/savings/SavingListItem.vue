<template>
  <tr>
    <td>{{ product.bank_name }}</td>
    <td>
      <a
        v-if="product.product_link"
        :href="product.product_link"
        target="_blank"
        class="product-link"
      >
        {{ product.product_name }}
      </a>
      <span v-else>{{ product.product_name }}</span>
    </td>
    <td>{{ product.saving_method }}</td>
    <td>{{ product.pre_tax_interest_rate }}%</td>
    <td>{{ product.post_tax_interest_rate }}%</td>
    <td>{{ product.max_preference_rate }}%</td>
    <td>{{ product.eligibility }}</td>
    <td>{{ product.interest_calculation_method }}</td>
    <td v-if="showPostTaxInterest">
      {{ formatNumber(product.post_tax_interest) }}
    </td>
    <td>
      <button
        @click="$emit('show-details', product)"
        class="details-button"
      >
        상세보기
      </button>
    </td>
  </tr>
</template>

<script setup>
defineProps({
  product: Object,
  showPostTaxInterest: Boolean,
});
defineEmits(["show-details"]);

const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};
</script>

<style scoped>
tr {
  transition: background-color 0.2s ease;
}

tr:hover {
  background-color: #f8faf6;
}

/* 첫 두 열을 제외한 모든 열 가운데 정렬 */
td:nth-child(n+3),
th:nth-child(n+3) {
  text-align: center;
}

td {
  padding: 12px;
  border-bottom: 1px solid #e9ecef;
  color: #333;
  font-size: 0.9rem;
}

.product-link {
  color: #2D7A31;
  text-decoration: none;
  font-weight: 500;
}

.product-link:hover {
  text-decoration: underline;
}

.details-button {
  background-color: #2E8B57;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 6px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.2s ease;
}

.details-button:hover {
  background-color: #1a5235;
}

.details-button:active {
  transform: translateY(1px);
}
</style>