﻿<template>
  <div class="additional-info-container">
    <div class="info-card">
      <h2 class="card-title">Welcome to moneytto!</h2>
      <p class="card-subtitle">
        {{ accountStore.user.nickname }}님, 머니또에 오신 것을 환영합니다!<br />
        맞춤형 금융 서비스 제공을 위해 아래 정보를 입력해주세요.
      </p>

      <form @submit.prevent="updateAdditionalInfo" class="info-form">
        <div class="form-group">
          <label for="birthDate">생년월일</label>
          <input
            id="birthDate"
            v-model="additionalInfo.birth_date"
            type="date"
            required
          />
        </div>

        <div class="form-group">
          <label for="assets">보유자산</label>
          <input
            id="assets"
            v-model.number="additionalInfo.assets"
            type="number"
            required
          />
        </div>

        <div class="form-group">
          <label for="income">월 수입</label>
          <input
            id="income"
            v-model.number="additionalInfo.income"
            type="number"
            required
          />
        </div>

        <button type="submit" class="submit-button">저장</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAccountStore } from "@/stores/accountStore";
import { useRouter } from "vue-router";

const accountStore = useAccountStore();
const router = useRouter();

const additionalInfo = ref({
  birth_date: "",
  assets: 0,
  income: 0,
});

onMounted(() => {
  if (accountStore.user) {
    additionalInfo.value.birth_date = accountStore.user.birthDate || "";
    additionalInfo.value.assets = accountStore.user.assets || 0;
    additionalInfo.value.income = accountStore.user.income || 0;
  }
});

const updateAdditionalInfo = async () => {
  try {
    await accountStore.updateAdditionalInfo(additionalInfo.value);
    alert("추가 정보가 업데이트되었습니다.");
    router.push({ name: "MainView" }); // 메인 페이지로 이동
  } catch (error) {
    alert("추가 정보 업데이트에 실패했습니다.");
  }
};

const skipUpdate = () => {
  router.push({ name: "MainView" }); // 메인 페이지로 이동
};
</script>

<style scoped>
.additional-info-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
}

.info-card {
  background: white;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-title {
  font-family: "Baloo Tamma 2", system-ui;
  /* font-family: "Noto Sans", system-ui; */
  font-optical-sizing: auto;
  font-weight: 600;
  font-style: normal;
  color: #2e8b57;
  text-align: center;
  margin-bottom: 10px;
  font-size: 2.5em;
}

.card-subtitle {
  text-align: center;
  color: #666;
  margin-bottom: 30px;
}

.info-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #2e8b57;
  font-weight: 500;
}

input {
  width: 100%;
  padding: 12px;
  border: 2px solid #e0e0e0;
  border-radius: 8px;
  font-size: 1em;
  transition: border-color 0.3s ease;
}

input:focus {
  outline: none;
  border-color: #2e8b57;
}

.submit-button {
  width: 100%;
  padding: 12px;
  background-color: #2e8b57;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.submit-button:hover {
  background-color: #1a5235;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .additional-info-container {
    margin: 20px auto;
  }

  .info-card {
    padding: 20px;
  }
}
</style>
