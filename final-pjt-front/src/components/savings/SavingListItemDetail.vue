<!-- SavingListItemDetail.vue -->
<template>
  <div class="modal">
    <div class="modal-content">
      <div class="modal-top">
        <button
          @click="toggleLike"
          class="star-button"
          :class="{ starred: product.is_liked }"
        >
          {{ product.is_liked ? "★" : "☆" }}
        </button>
        <h2>{{ product.product_name }}</h2>
        <h4>{{ product.bank_name }}</h4>
        <hr />
      </div>
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
import { useSavingStore } from "@/stores/counter";

const props = defineProps(["product"]);
const emit = defineEmits(["close"]);

const savingStore = useSavingStore();

const toggleLike = () => {
  savingStore.toggleLike(props.product.id);
};
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
  position: relative;
}

.star-button {
  position: absolute;
  top: 10px;
  right: 10px;
  background: none;
  border: none;
  font-size: 50px;
  cursor: pointer;
  color: #ccc;
  transition: color 0.3s ease;
}

.star-button.starred {
  color: gold;
}

.modal-top {
  color: #333;
  margin-top: 0;
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
