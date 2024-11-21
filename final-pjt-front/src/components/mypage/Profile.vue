<template>
    <div class="container mt-5">
      <div class="row justify-content-center">
        <div class="col-md-6">
            <div class="card">
                <div class="card-body">
                    <h2 class="card-title text-center mb-4">내 정보</h2>
                    <RouterLink class="text-end" :to="{ name: 'profile-update' }"><p>프로필 수정</p></RouterLink>
                    <div class="mb-3">
                    <div>
                        <img
                            v-if="profile.previewImage"
                            :src="profile.previewImage"
                            alt="프로필 이미지"
                            style="max-width: 100px; max-height: 100px"
                        />
                    </div>
                  <!-- <p>프로필: {{ profile.previewImage }}</p> -->
                  <div>
                      <p>아이디: {{ profile.username }}</p>
                      <p>닉네임: {{ profile.nickname }}</p>
                      <p>생년월일: {{ profile.birth_date }}</p>
                      <p>월 수입: {{ profile.income }}원</p>
                      <p>보유 자산: {{ profile.assets }}원</p>
                      <p>보유 포인트: {{ profile.point }}P</p>
                  </div>
                  <RouterLink class="text-end" :to="{ name: 'DeleteAccount' }"><p>탈퇴</p></RouterLink>
                </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>

<script setup>
import { RouterLink } from 'vue-router';
import { ref, onMounted } from 'vue';
import { useAccountStore } from '@/stores/accountStore';

const accountStore = useAccountStore()

const profile = ref({
  username: "",
  email: "",
  nickname: "",
  birth_date: "",
  income: 0,
  assets: 0.0,
  point: "",
  previewImage: null,
});

const loadUserProfile = async () => {
  try {
    const response = await accountStore.fetchUserProfile();
    profile.value.username = response.username;
    profile.value.email = response.email;
    profile.value.nickname = response.nickname;
    profile.value.birth_date = response.birth_date;
    profile.value.income = response.income;
    profile.value.assets = response.assets;
    profile.value.point = response.point;
    profile.value.previewImage = response.profile_image;
  } catch (error) {
    console.error("프로필 정보를 불러오지 못했습니다:", error);
  }
};

onMounted(() => {
  loadUserProfile();
});
</script>

<style scoped>

</style>