<template>
  <div class="card">
    <h3>{{ saving.product_name }}</h3>
    <h5>{{ saving.bank_name }}</h5>
    <p>{{ saving.saving_method }}</p>
    <p>최고우대금리: {{ saving.max_preference_rate }}%</p>
    <button
      @click="$emit('show-details', saving)"
      class="btn btn-sm btn-success"
    >
      상세보기
    </button>
  </div>
</template>

<script setup>
defineProps({
  saving: Object,
});

defineEmits(["show-details"]);
</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  width: calc(20% - 16px); /* Five cards per row */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.card p {
  margin-bottom: 10px;
  font-size: 0.9em;
}
</style>