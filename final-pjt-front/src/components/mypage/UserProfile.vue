﻿<template>
  <section class="profile-section">
    <h2>프로필 정보</h2>
    <form @submit.prevent="updateProfile">
      <div>
        <label for="username">아이디:</label>
        <input id="username" :value="accountStore.user?.username" disabled />
      </div>
      <div>
        <label for="profile_image">프로필 이미지:</label>
        <img
          v-if="profile.previewImage"
          :src="profile.previewImage"
          alt="프로필 이미지"
          style="max-width: 100px; max-height: 100px"
        />
        <input id="profile_image" type="file" @change="onFileChange" />
      </div>
      <div>
        <label for="nickname">닉네임:</label>
        <input id="nickname" v-model="profile.nickname" type="text" required />
      </div>
      <div>
        <label for="birth_date">생년월일:</label>
        <input id="birth_date" v-model="profile.birth_date" type="date" />
      </div>
      <div>
        <label for="income">월 수입:</label>
        <input id="income" v-model.number="profile.income" type="number" />
      </div>
      <div>
        <label for="assets">보유 자산:</label>
        <input
          id="assets"
          v-model.number="profile.assets"
          type="number"
          step="0.01"
        />
      </div>
      <div>
        <label for="point">포인트:</label>
        <input id="point" :value="accountStore.user?.point" disabled />
      </div>
      <button type="submit">프로필 업데이트</button>
    </form>
  </section>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useAccountStore } from "@/stores/accountStore";

const accountStore = useAccountStore();

const profile = ref({
  email: "",
  nickname: "",
  birth_date: "",
  income: 0,
  assets: 0.0,
  previewImage: null,
});

const loadUserProfile = async () => {
  try {
    const response = await accountStore.fetchUserProfile();
    profile.value.email = response.email;
    profile.value.nickname = response.nickname;
    profile.value.birth_date = response.birth_date;
    profile.value.income = response.income;
    profile.value.assets = response.assets;
    profile.value.previewImage = response.profile_image;
  } catch (error) {
    console.error("프로필 정보를 불러오지 못했습니다:", error);
  }
};

onMounted(() => {
  loadUserProfile();
});

const onFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    const reader = new FileReader();
    reader.onload = (e) => {
      profile.value.previewImage = e.target.result;
    };
    reader.readAsDataURL(file);
    // 파일 업로드 로직 추가 (예: 서버에 업로드)
    console.log("프로필 이미지 선택됨:", file);
  }
};

const updateProfile = async () => {
  try {
    await accountStore.updateUserInfo(profile.value);
    alert("프로필이 업데이트되었습니다.");
  } catch (error) {
    alert("프로필 업데이트에 실패했습니다.");
  }
};
</script>
