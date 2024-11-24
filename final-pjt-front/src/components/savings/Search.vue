<template>
  <form @submit.prevent="search" class="search-form">
    <div class="header-row">
      <h2 class="search-title">적금 상품 검색</h2>
      <button @click.prevent="goToRecommend" class="recommend-button">
        ✨ {{ accountStore.user.nickname}}님에게 맞는 상품 추천받기
      </button>
    </div>

    <div class="search-content">
      <!-- 첫 번째 열: 월 저축 금액, 저축 예정 기간, 총 저축 금액 -->
      <div class="search-col">
        <div class="amount-input">
          <label>월 저축 금액<span class="hint">(최소: 1만원)</span></label>
          <!-- <span class="hint">(최소: 1만원)</span> -->
          <div class="input-wrapper">
            <input v-model="amount" type="number" placeholder="금액 입력" />
            <span class="unit">원</span>
          </div>
        </div>

        <div class="period-input">
          <label>저축 예정 기간</label>
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

        <div class="total-amount">
          <label>총 저축 금액</label>
          <div v-if="totalAmount > 0" class="amount-display">{{ formatNumber(totalAmount) }}원</div>
        </div>
      </div>

      <!-- 두 번째 열: 적립 방식, 금융 권역, 이자 계산 방식 -->
      <div class="search-col">
        <div class="saving-method">
          <label>적립 방식</label>
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

        <div class="cal-method">
          <label>이자 계산 방식</label>
          <div class="option-buttons">
            <button
              v-for="method in interestMethods"
              :key="method.value"
              type="button"
              :class="['option-btn', { active: interestCalculationMethod === method.value }]"
              @click="interestCalculationMethod = method.value"
            >
              {{ method.label }}
            </button>
          </div>
        </div>

        <div class="institution-type">
          <label>금융 권역</label>
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
      </div>
    </div>

    <!-- 검색 버튼 -->
    <div class="footer-row">
      <button type="submit" class="search-button">검색하기</button>
    </div>
  </form>
</template>

<script setup>
import { ref, computed } from "vue";
import { useRouter } from "vue-router";
import { useAccountStore } from "@/stores/accountStore";

const accountStore = useAccountStore()
const router = useRouter()

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
  { label: "신협조합", value: "신용협동조합" },
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

const goToRecommend = function() {
  router.push({name:'Recommend'})
}
</script>

<style scoped>
.search-form {
  display: flex;
  flex-direction: column;
  background-color: #f8f9fa;
  padding: 30px;
  border-radius: 20px;
  margin-bottom: 30px;
  box-shadow: 0 4px 12px rgba(45, 122, 49, 0.1);
}

.header-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.search-title {
  color: #2E8B57;
  font-size: 1.8rem;
  font-weight: 700;
  margin: 0;
}

.recommend-button {
  background-color: white;
  color: #2E8B57;
  border: 2px solid #2E8B57;
  padding: 12px 24px;
  border-radius: 10px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
}

.recommend-button:hover {
  background-color: #1a5235;
  color: white;
  transform: translateY(-2px);
}

.search-content {
  display: flex;
  gap: 40px;
  margin-bottom: 30px;
}

.search-col {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.input-wrapper {
  position: relative;
  display: flex;
  align-items: center;
}

input[type="number"] {
  width: 100%;
  padding: 12px;
  border: 2px solid #2E8B57;
  border-radius: 10px;
  font-size: 1em;
  transition: all 0.3s ease;
}

input[type="number"]:focus {
  outline: none;
  border-color: #2E8B57;
  box-shadow: 0 0 0 3px rgba(45, 122, 49, 0.1);
}

.unit {
  position: absolute;
  right: 12px;
  color: #2E8B57;
  font-weight: 500;
}

.hint {
  color: #666;
  font-size: 0.9em;
  margin-left: 8px;
}

.period-buttons,
.option-buttons {
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
}

.period-btn,
.option-btn {
  padding: 10px 20px;
  border: 2px solid #2E8B57;
  background-color: white;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  color: #2E8B57;
  flex: 1;
  min-width: 80px;
  font-weight: 500;
}

.period-btn:hover,
.option-btn:hover {
  background-color: rgba(45, 122, 49, 0.05);
}

.period-btn.active,
.option-btn.active {
  background-color: #2E8B57;
  color: white;
}

.footer-row {
  display: flex;
  justify-content: center;
}

.search-button {
  background-color: #2E8B57;
  color: white;
  padding: 16px 40px;
  border: none;
  border-radius: 12px;
  font-size: 1.1em;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 4px 6px rgba(45, 122, 49, 0.2);
  width: 200px;
}

.search-button:hover {
  background-color: #1a5235;
  transform: translateY(-2px);
  box-shadow: 0 6px 8px rgba(45, 122, 49, 0.25);
}

.search-button:active {
  transform: translateY(0);
  box-shadow: 0 2px 4px rgba(45, 122, 49, 0.2);
}

label {
  color: #2E8B57;
  font-weight: 600;
  margin-bottom: 8px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.total-amount {
  background-color: white;
  padding: 15px;
  border-radius: 10px;
  border: 2px solid #E8F3E9;
}

.amount-display {
  color: #2E8B57;
  font-size: 1.2em;
  font-weight: 700;
  margin-top: 5px;
}

@media (max-width: 768px) {
  .search-content {
    flex-direction: column;
    gap: 20px;
  }

  .header-row {
    flex-direction: column;
    gap: 15px;
    align-items: stretch;
  }

  .recommend-button {
    width: 100%;
  }

  .search-button {
    width: 100%;
  }

  .search-title {
    text-align: center;
  }
}
</style>
