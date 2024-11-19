<template>
  <form @submit.prevent="search" class="search-form">
    <div class="search-row">
      <div class="amount-input">
        <label>월 저축 금액</label>
        <div class="input-wrapper">
          <input v-model="amount" type="number" placeholder="금액 입력" />
          <span class="unit">원</span>
        </div>
        <span class="hint">(최소: 1만원)</span>
      </div>
    </div>

    <div class="search-row">
      <label>저축 예정기간을 선택하세요</label>
      <div class="period-buttons">
        <button
          v-for="p in periods"
          :key="p.value"
          type="button"
          :class="['period-btn', { active: period === p.value }]"
          @click="period = p.value"
        >
          {{ p.label }}
        </button>
      </div>
    </div>

    <!-- 총 저축 금액 표시 -->
    <div v-if="totalAmount > 0" class="total-amount">
      <label>총 저축 금액</label>
      <div class="amount-display">{{ formatNumber(totalAmount) }}원</div>
    </div>

    <div class="search-row">
      <label>적립방식</label>
      <div class="option-buttons">
        <button
          v-for="method in savingMethods"
          :key="method.value"
          type="button"
          :class="['option-btn', { active: savingMethod === method.value }]"
          @click="savingMethod = method.value"
        >
          {{ method.label }}
        </button>
      </div>
    </div>

    <div class="search-row">
      <label>금융권역</label>
      <div class="option-buttons">
        <button
          v-for="type in institutionTypes"
          :key="type.value"
          type="button"
          :class="['option-btn', { active: institutionType === type.value }]"
          @click="institutionType = type.value"
        >
          {{ type.label }}
        </button>
      </div>
    </div>

    <div class="search-row">
      <label>이자계산방식</label>
      <div class="option-buttons">
        <button
          v-for="method in interestMethods"
          :key="method.value"
          type="button"
          :class="[
            'option-btn',
            { active: interestCalculationMethod === method.value },
          ]"
          @click="interestCalculationMethod = method.value"
        >
          {{ method.label }}
        </button>
      </div>
    </div>

    <button type="submit" class="search-button">검색</button>
  </form>
</template>

<script setup>
import { ref, computed } from "vue";

const amount = ref("");
const period = ref("");
const savingMethod = ref("");
const institutionType = ref("");
const interestCalculationMethod = ref("");

// 총 저축 금액 계산
const totalAmount = computed(() => {
  if (amount.value && period.value) {
    return Number(amount.value) * Number(period.value);
  }
  return 0;
});

// 숫자 포맷팅 함수 (1000단위 콤마)
const formatNumber = (num) => {
  return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
};

const periods = [
  { label: "6개월", value: "6" },
  { label: "12개월", value: "12" },
  { label: "24개월", value: "24" },
  { label: "36개월", value: "36" },
];

// 적립방식 옵션
const savingMethods = [
  { label: "전체", value: "" },
  { label: "정액적립식", value: "정액적립식" },
  { label: "자유적립식", value: "자유적립식" },
];

// 금융권역 옵션
const institutionTypes = [
  { label: "전체", value: "" },
  { label: "은행", value: "은행" },
  { label: "저축은행", value: "저축은행" },
  { label: "신용협동조합", value: "신용협동조합" },
];

// 이자계산방식 옵션
const interestMethods = [
  { label: "전체", value: "" },
  { label: "단리", value: "단리" },
  { label: "복리", value: "복리" },
];

const emit = defineEmits(["search"]);

const search = () => {
  if (!amount.value || !period.value) {
    let message = "";
    if (!amount.value) message += "저축 금액을 입력해주세요.\n";
    if (!period.value) message += "저축 예정 기간을 선택하세요.";
    alert(message);
    return;
  }

  const searchParams = {};
  if (amount.value) searchParams.amount = amount.value;
  if (period.value) searchParams.period = period.value;
  if (savingMethod.value) searchParams.saving_method = savingMethod.value;
  if (institutionType.value)
    searchParams.institution_type = institutionType.value;
  if (interestCalculationMethod.value)
    searchParams.interest_calculation_method = interestCalculationMethod.value;

  emit("search", searchParams);
};
</script>

<style scoped>
.search-form {
  background-color: #f8f9fa;
  padding: 20px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.search-row {
  margin-bottom: 20px;
}

.amount-input {
  position: relative;
}

.input-wrapper {
  display: flex;
  align-items: center;
  gap: 5px;
}

input[type="number"] {
  width: 200px;
  padding: 8px;
  border: 1px solid #ddd;
  border-radius: 4px;
}

.unit {
  color: #666;
}

.hint {
  font-size: 0.8em;
  color: #666;
  margin-left: 5px;
}

.period-buttons,
.option-buttons {
  display: flex;
  gap: 10px;
  margin-top: 8px;
}

.period-btn,
.option-btn {
  padding: 8px 16px;
  border: 1px solid #ddd;
  background-color: white;
  border-radius: 4px;
  cursor: pointer;
  transition: all 0.2s;
}

.period-btn.active,
.option-btn.active {
  background-color: #bedc74;
  color: white;
  border-color: #bedc74;
}

.period-btn:hover,
.option-btn:hover {
  background-color: #e9ecef;
}

.period-btn.active:hover,
.option-btn.active:hover {
  background-color: #bedc74;
}

.total-amount {
  margin: 20px 0;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 4px;
  border: 1px solid #ddd;
}

.amount-display {
  font-size: 1.2em;
  font-weight: bold;
  color: #333;
  margin-top: 5px;
}

.search-button {
  background-color: #bedc74;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  width: 100%;
  font-size: 1.1em;
}

.search-button:hover {
  background-color: #bedc74;
}

label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}
</style>
