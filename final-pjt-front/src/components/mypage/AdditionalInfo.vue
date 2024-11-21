﻿<template>
  <div class="modal-backdrop">
    <div class="modal">
      <section class="additional-info-section">
        <h2>추가 정보</h2>
        <form @submit.prevent="updateAdditionalInfo">
          <div>
            <label for="birthDate">생년월일:</label>
            <input
              id="birthDate"
              v-model="additionalInfo.birth_date"
              type="date"
              required
            />
          </div>
          <div>
            <label for="assets">보유자산:</label>
            <input
              id="assets"
              v-model.number="additionalInfo.assets"
              type="number"
              required
            />
          </div>
          <div>
            <label for="income">월 수입:</label>
            <input
              id="income"
              v-model.number="additionalInfo.income"
              type="number"
              required
            />
          </div>
          <button type="submit">추가 정보 업데이트</button>
          <button type="button" @click="$emit('skip')">건너뛰기</button>
        </form>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAccountStore } from "@/stores/accountStore";
import { useRouter } from "vue-router";

const accountStore = useAccountStore();
const router = useRouter();
const emit = defineEmits(["close", "skip"]);

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
    emit("close");
    router.push({ name: "MainView" }); // 메인 페이지로 이동
  } catch (error) {
    alert("추가 정보 업데이트에 실패했습니다.");
  }
};
</script>

<style scoped>
/* 기존 스타일 유지 */
</style>
