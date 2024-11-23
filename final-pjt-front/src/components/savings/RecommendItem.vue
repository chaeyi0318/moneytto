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
  background-color: white;
  border: 2px solid #2E8B57;
  border-radius: 12px;
  padding: 20px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.card:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
}

.card h3 {
  color: #2E8B57;
  font-size: 1.2em;
  margin-bottom: 10px;
}

.card h5 {
  color: #666;
  font-size: 1em;
  margin-bottom: 15px;
}

.card p {
  color: #444;
  margin: 8px 0;
  font-size: 0.9em;
}
</style>