<template>
  <tr>
    <td>{{ product.bank_name }}</td>
    <td>
      <a v-if="product.product_link" :href="product.product_link" target="_blank">
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
    <td v-if="showPostTaxInterest">{{ product.post_tax_interest }}</td>
    <td>
      <button @click="$emit('show-details', product)">상세보기</button>
    </td>
  </tr>
</template>

<script setup>
defineProps({
  product: Object,
  showPostTaxInterest: Boolean
});
defineEmits(['show-details']);
</script>

<style scoped></style>
