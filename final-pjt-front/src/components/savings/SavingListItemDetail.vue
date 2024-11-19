<!-- SavingListItemDetail.vue -->
<template>
  <div class="modal">
    <div class="modal-content">
      <h3>{{ product.product_name }} 상세 정보</h3>
      <div class="detail-info">
        <p>
          <strong>비교공시일:</strong> {{ product.comparison_disclosure_date }}
        </p>
        <p>
          <strong>담당부서 및 연락처:</strong> {{ product.department_contact }}
        </p>
        <p><strong>우대조건:</strong> {{ product.preferential_conditions }}</p>
        <p>
          <strong>상세 가입대상:</strong> {{ product.detailed_eligibility }}
        </p>
        <p><strong>가입방법:</strong> {{ product.application_method }}</p>
        <p>
          <strong>만기 후 이자율:</strong>
          {{ product.post_maturity_interest_rate }}
        </p>
        <p>
          <strong>기타 유의사항:</strong> {{ product.other_considerations }}
        </p>
      </div>
      <button @click="$emit('close')" class="close-button">닫기</button>
    </div>
  </div>
</template>

<script setup>
defineProps(["product"]);
defineEmits(["close"]);
</script>

<style scoped>
.modal {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  overflow: auto;
  background-color: rgba(0, 0, 0, 0.4);
}

.modal-content {
  background-color: #fefefe;
  margin: 15% auto;
  padding: 20px;
  border: 1px solid #888;
  width: 80%;
  max-width: 600px;
  border-radius: 5px;
}

h3 {
  color: #333;
  border-bottom: 1px solid #ddd;
  padding-bottom: 10px;
}

.detail-info p {
  margin: 10px 0;
}

.close-button {
  background-color: #f44336;
  color: white;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  float: right;
}

.close-button:hover {
  background-color: #d32f2f;
}
</style>
