<!-- RecommendItem.vue -->
<template>
  <div class="saving-card">
    <div class="card-header">
      <h3 class="product-name">{{ saving.product_name }}</h3>
      <h5 class="bank-name">{{ saving.bank_name }}</h5>
    </div>
    <div class="card-body">
      <div class="saving-info">
        <p class="saving-method">{{ saving.saving_method }}</p>
        <p class="interest-rate">
          <span class="label">최고우대금리</span>
          <span class="rate">{{ saving.max_preference_rate }}%</span>
        </p>
      </div>
    </div>
    <button
      class="btn btn-sm btn-success"
    >
      상세보기
    </button>
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
.saving-card {
  background: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 2px solid transparent;
}

.saving-card:hover {
  transform: translateY(-5px);
  border-color: #2E8B57;
}

.product-name {
  color: #2E8B57;
  font-size: 1.2em;
  margin: 0 0 8px 0;
  line-height: 1.3;
}

.bank-name {
  color: #666;
  font-size: 1em;
  margin: 0;
  font-weight: 500;
}

.saving-info {
  padding-top: 15px;
  border-top: 1px solid #e0e0e0;
}

.saving-method {
  color: #666;
  margin-bottom: 10px;
  font-size: 0.9em;
}

.interest-rate {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #f0f8f4;
  padding: 10px;
  border-radius: 8px;
  margin: 0;
}

.label {
  color: #666;
  font-size: 0.9em;
}

.rate {
  color: #2E8B57;
  font-weight: 600;
  font-size: 2em;
}

@media (max-width: 768px) {
  .saving-card {
    padding: 15px;
  }
}
</style>