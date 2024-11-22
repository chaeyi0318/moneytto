<!-- SavingListItemDetail.vue -->
<template>
  <div
    class="modal fade show"
    tabindex="-1"
    role="dialog"
    style="display: block"
  >
    <div class="modal-dialog modal-dialog-centered" role="document">
      <div class="modal-content">
        <div class="modal-header d-flex justify-content-between">
          <h3 class="modal-title">{{ product.product_name }}</h3>
          <h6 class="mb-0">{{ product.bank_name }}</h6>
        </div>
        <div class="modal-body">
          <div class="d-flex justify-content-end align-items-center mb-3">
            <!-- <button class="btn btn-light">이미 보유하고 있어요!</button> -->
            <button
              @click="toggleLike"
              class="btn btn-light star-button"
              :class="{ 'btn-warning': product.is_liked }"
            >
              <i :class="product.is_liked ? 'bi-star-fill' : 'bi-star'"></i>
            </button>
            <!-- <button>
              <i
                :class="
                  product.is_owned ? 'plus-square-fill' : 'plus-square-dotted'
                "
              ></i>
            </button> -->
          </div>
          <hr />
          <div class="detail-info">
            <p>
              <strong>적립방식:</strong>
              {{ product.saving_method }}
            </p>
            <p>
              <strong>세전이자율:</strong>
              {{ product.pre_tax_interest_rate }}%
            </p>
            <p>
              <strong>세후이자율:</strong>
              {{ product.post_tax_interest_rate }}%
            </p>
            <p>
              <strong>최고우대금리:</strong>
              {{ product.max_preference_rate }}%
            </p>
            <p>
              <strong>이자계산방식:</strong>
              {{ product.interest_calculation_method }}
            </p>
            <!-- <p v-if="showPostTaxInterest">
              <strong>세후이자: 예시</strong>
              {{ formatNumber(product.post_tax_interest) }}
            </p> -->
            <p>
              <strong>비교공시일:</strong>
              {{ product.comparison_disclosure_date }}
            </p>
            <p>
              <strong>담당부서 및 연락처:</strong>
              {{ product.department_contact }}
            </p>
            <p>
              <strong>우대조건:</strong> {{ product.preferential_conditions }}
            </p>
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
        </div>
        <div class="modal-footer">
          <button class="btn btn-light">이미 보유하고 있어요!</button>
          <a
            v-if="product.product_link"
            :href="product.product_link"
            target="_blank"
          >
            <button class="btn btn-success">가입하러 가기</button>
          </a>
          <button
            type="button"
            class="btn btn-secondary"
            @click="$emit('close')"
          >
            닫기
          </button>
        </div>
      </div>
    </div>
  </div>
  <div class="modal-backdrop fade show"></div>
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
.modal {
  background-color: rgba(0, 0, 0, 0.5);
}

.star-button {
  font-size: 1.5rem;
  padding: 0.25rem 0.5rem;
  line-height: 1;
  color: green;
}

.detail-info p {
  margin-bottom: 0.5rem;
}
</style>
