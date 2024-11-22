﻿<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">프로필 정보</h2>
            <form @submit.prevent="updateProfile">
              <div class="mb-3">
                <label for="profile_image" class="form-label"
                  >프로필 사진:</label
                >
                <input
                  id="profile_image"
                  type="file"
                  @change="onFileChange"
                  accept="image/*"
                  class="form-control"
                />
                <div v-if="profile.previewImage" class="mb-3">
                  <img
                    :src="profile.previewImage"
                    alt="프로필 미리보기"
                    class="img-thumbnail"
                    style="max-width: 200px"
                  />
                </div>
              </div>
              <div class="mb-3">
                <label for="username" class="form-label">아이디:</label>
                <input
                  id="username"
                  :value="accountStore.user?.username"
                  class="form-control"
                  disabled
                />
              </div>
              <div class="mb-3">
                <label for="nickname" class="form-label">닉네임:</label>
                <input
                  id="nickname"
                  v-model="profile.nickname"
                  type="text"
                  class="form-control"
                  required
                />
              </div>
              <div class="mb-3">
                <label for="birth_date" class="form-label">생년월일:</label>
                <input
                  id="birth_date"
                  v-model="profile.birth_date"
                  type="date"
                  class="form-control"
                />
              </div>
              <div class="mb-3">
                <label for="income" class="form-label">월 수입:</label>
                <input
                  id="income"
                  v-model.number="profile.income"
                  type="number"
                  class="form-control"
                />
              </div>
              <div class="mb-3">
                <label for="assets" class="form-label">보유 자산:</label>
                <input
                  id="assets"
                  v-model.number="profile.assets"
                  type="number"
                  step="0.01"
                  class="form-control"
                />
              </div>
              <div class="d-grid gap-2">
                <button type="submit" class="btn btn-primary">
                  프로필 업데이트
                </button>
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

<style scoped></style>
