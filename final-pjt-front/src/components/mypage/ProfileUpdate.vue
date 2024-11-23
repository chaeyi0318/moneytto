﻿<template>
  <div class="profile-update-container">
    <div class="update-card">
      <h2 class="card-title">프로필 수정</h2>
      
      <form @submit.prevent="updateProfile" class="update-form">
        <div class="form-group">
          <label for="profile_image">프로필 사진</label>
          <div class="image-upload">
            <input
              id="profile_image"
              type="file"
              @change="onFileChange"
              accept="image/*"
              class="file-input"
            />
            <div v-if="profile.previewImage" class="preview-container">
              <img
                :src="profile.previewImage"
                alt="프로필 미리보기"
                class="preview-image"
              />
            </div>
          </div>
        </div>

        <div class="form-group">
          <label for="username">아이디</label>
          <input
            id="username"
            :value="accountStore.user?.username"
            disabled
            class="disabled-input"
          />
        </div>

        <div class="form-group">
          <label for="nickname">닉네임</label>
          <input
            id="nickname"
            v-model="profile.nickname"
            type="text"
            required
          />
        </div>

        <div class="form-group">
          <label for="birth_date">생년월일</label>
          <input
            id="birth_date"
            v-model="profile.birth_date"
            type="date"
          />
        </div>

        <div class="form-group">
          <label for="income">월 수입</label>
          <input
            id="income"
            v-model.number="profile.income"
            type="number"
          />
        </div>

        <div class="form-group">
          <label for="assets">보유 자산</label>
          <input
            id="assets"
            v-model.number="profile.assets"
            type="number"
            step="0.01"
          />
        </div>

        <button type="submit" class="update-button">프로필 업데이트</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAccountStore } from "@/stores/accountStore";

const accountStore = useAccountStore();
const router = useRouter();

const profile = ref({
  email: "",
  nickname: "",
  birth_date: "",
  income: 0,
  assets: 0.0,
  imageFile: null,
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
    profile.value.imageFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      profile.value.previewImage = e.target.result;
    };
    reader.readAsDataURL(file);
  }
};

const updateProfile = async () => {
  try {
    const formData = new FormData();
    formData.append("email", profile.value.email);
    formData.append("nickname", profile.value.nickname);
    formData.append("birth_date", profile.value.birth_date);
    formData.append("income", profile.value.income);
    formData.append("assets", profile.value.assets);
    if (profile.value.imageFile) {
      formData.append("profile_image", profile.value.imageFile);
    }

    await accountStore.updateUserInfo(formData);
    alert("프로필이 업데이트되었습니다.");
    router.push({ name: "MyPageView" });
  } catch (error) {
    alert("프로필 업데이트에 실패했습니다.");
  }
};
</script>

<style scoped>
.profile-update-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
}

.update-card {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-title {
  color: #2E8B57;
  text-align: center;
  margin-bottom: 30px;
  font-size: 1.8em;
}

.form-group {
  margin-bottom: 20px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #2E8B57;
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
  border-color: #2E8B57;
}

.disabled-input {
  background-color: #f8f9fa;
  cursor: not-allowed;
}

.image-upload {
  margin-bottom: 15px;
}

.preview-container {
  margin-top: 15px;
  text-align: center;
}

.preview-image {
  max-width: 200px;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.update-button {
  width: 100%;
  padding: 12px;
  background-color: #2E8B57;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.3s ease;
  margin-top: 20px;
}

.update-button:hover {
  background-color: #1a5235;
  transform: translateY(-2px);
}

@media (max-width: 768px) {
  .update-card {
    padding: 20px;
  }
}
</style>
