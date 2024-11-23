<template>
  <div class="modal-overlay">
    <div class="modal-container">
      <div class="modal-content">
        <div class="modal-header">
          <div class="title-section">
            <h3 class="product-title">{{ product.product_name }}</h3>
            <h6 class="bank-name">{{ product.bank_name }}</h6>
          </div>
          <div class="action-buttons">
            <button
              @click="toggleLike"
              class="like-button"
              :class="{ 'is-liked': product.is_liked }"
            >
              <i :class="product.is_liked ? 'bi-star-fill' : 'bi-star'"></i>
            </button>
          </div>
        </div>

        <div class="modal-body">
          <div class="detail-info">
            <p><strong>적립방식:</strong> {{ product.saving_method }}</p>
            <p><strong>세전이자율:</strong> {{ product.pre_tax_interest_rate }}%</p>
            <p><strong>세후이자율:</strong> {{ product.post_tax_interest_rate }}%</p>
            <p><strong>최고우대금리:</strong> {{ product.max_preference_rate }}%</p>
            <p><strong>이자계산방식:</strong> {{ product.interest_calculation_method }}</p>
            <p><strong>비교공시일:</strong> {{ product.comparison_disclosure_date }}</p>
            <p><strong>담당부서 및 연락처:</strong> {{ product.department_contact }}</p>
            <p><strong>우대조건:</strong> {{ product.preferential_conditions }}</p>
            <p><strong>상세 가입대상:</strong> {{ product.detailed_eligibility }}</p>
            <p><strong>가입방법:</strong> {{ product.application_method }}</p>
            <p><strong>만기 후 이자율:</strong> {{ product.post_maturity_interest_rate }}</p>
            <p><strong>기타 유의사항:</strong> {{ product.other_considerations }}</p>
          </div>
        </div>

        <div class="modal-footer">
          <button class="owned-button">이미 보유하고 있어요!</button>
          <a
            v-if="product.product_link"
            :href="product.product_link"
            target="_blank"
            class="join-link"
          >
            <button class="join-button">가입하러 가기</button>
          </a>
          <button class="close-button" @click="$emit('close')">닫기</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useSavingStore } from "@/stores/savingStore";

const props = defineProps({
  product: Object,
  showPostTaxInterest: Boolean,
});
const emit = defineEmits(["close"]);

const savingStore = useSavingStore();

const toggleLike = () => {
  savingStore.toggleLike(props.product.id);
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-container {
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.modal-content {
  padding: 20px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  padding-bottom: 15px;
  border-bottom: 2px solid #e9ecef;
}

.product-title {
  color: #2E8B57;
  margin: 0;
  font-size: 1.5em;
}

.bank-name {
  color: #666;
  margin: 5px 0 0 0;
}

.like-button {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #2E8B57;
  cursor: pointer;
  padding: 5px;
  transition: transform 0.2s ease;
}

.like-button:hover {
  transform: scale(1.1);
}

.like-button.is-liked {
  color: #FFD700;
}

.modal-body {
  padding: 20px 0;
}

.detail-info p {
  margin-bottom: 12px;
  line-height: 1.6;
}

.detail-info strong {
  color: #2E8B57;
  margin-right: 8px;
}

.modal-footer {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  padding-top: 15px;
  border-top: 2px solid #e9ecef;
}

.owned-button, .join-button, .close-button {
  padding: 10px 20px;
  border-radius: 8px;
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.owned-button {
  background-color: #f8f9fa;
  color: #2E8B57;
  border: 2px solid #2E8B57;
}

.join-button {
  background-color: #2E8B57;
  color: white;
}

.close-button {
  background-color: #6c757d;
  color: white;
}

.owned-button:hover, .join-button:hover, .close-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.join-link {
  text-decoration: none;
}

@media (max-width: 768px) {
  .modal-container {
    width: 95%;
    margin: 10px;
  }

  .modal-footer {
    flex-direction: column;
  }

  .modal-footer button {
    width: 100%;
  }
}
</style>
