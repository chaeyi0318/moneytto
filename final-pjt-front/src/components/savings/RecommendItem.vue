<!-- RecommendItem.vue -->
<template>
  <div class="card">
    <h3>{{ saving.product_name }}</h3>
    <h5>{{ saving.bank_name }}</h5>
    <p>적립방식: {{ saving.saving_method }}</p>
    <p>최고우대금리: {{ saving.max_preference_rate }}%</p>
  </div>
</template>

<script>
export default {
  name: "RecommendItem",
  props: {
    saving: {
      type: Object,
      required: true,
    },
  },
};
</script>

<style scoped>
.card {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 15px;
  width: calc(20% - 16px); /* Five cards per row */
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  box-sizing: border-box;
}

/* .card h3 {
  margin-top: 0;
  font-size: 1em;
} */

.card p {
  margin-bottom: 10px;
  font-size: 0.9em;
}
</style>
