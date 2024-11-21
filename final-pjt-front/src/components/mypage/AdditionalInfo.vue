﻿<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">가입을 환영합니다!</h2>
            <p class="text-center">맞춤형 금융 서비스 제공을 위해 아래 정보를 입력해주세요.</p>
            <form @submit.prevent="updateAdditionalInfo">
              <div class="mb-3">
                <label for="birthDate" class="form-label">생년월일:</label>
                <input
                  id="birthDate"
                  v-model="additionalInfo.birth_date"
                  type="date"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="assets" class="form-label">보유자산:</label>
                <input
                  id="assets"
                  v-model.number="additionalInfo.assets"
                  type="number"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="income" class="form-label">월 수입:</label>
                <input
                  id="income"
                  v-model.number="additionalInfo.income"
                  type="number"
                  class="form-control"
                  required
                />
              </div>
              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">
                  추가 정보 업데이트
                </button>
                <!-- <button
                  type="button"
                  @click="skipUpdate"
                  class="btn btn-secondary"
                >
                  건너뛰기
                </button> -->
              </div>
            </form>
          </div>
        </div>
      </div>
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
