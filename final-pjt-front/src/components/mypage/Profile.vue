<template>
  <div class="profile-container">
    <div class="profile-card">
      <div class="profile-header">
        <h2>{{ profile.nickname }}님의 프로필</h2>
        <RouterLink :to="{ name: 'profile-update' }" class="edit-link">
      <i class="bi bi-pencil"></i> <!-- 연필 아이콘 -->
    </RouterLink>
      </div>

      <div class="profile-content">
        <div class="profile-image-section">
          <div class="profile-image-wrapper">
            <img
              :src="getImageUrl(profile.previewImage)"
              alt="프로필 이미지"
            />
          </div>
        </div>

        <div class="profile-info">
          <div class="info-item">
            <span class="label">아이디</span>
            <span class="value">{{ profile.username }}</span>
          </div>
          <div class="info-item">
            <span class="label">닉네임</span>
            <span class="value">{{ profile.nickname }}</span>
          </div>
          <div class="info-item">
            <span class="label">생년월일</span>
            <span class="value">{{ formatDate(profile.birth_date) }}</span>
          </div>
          <div class="info-item">
            <span class="label">월 수입</span>
            <span class="value">{{ formatCurrency(profile.income) }}원</span>
          </div>
          <div class="info-item">
            <span class="label">보유 자산</span>
            <span class="value">{{ formatCurrency(profile.assets) }}원</span>
          </div>
          <div class="info-item">
            <span class="label">보유 포인트</span>
            <span class="value point">{{ profile.point }}P</span>
          </div>
        </div>
      </div>

      <div class="profile-footer">
        <RouterLink :to="{ name: 'DeleteAccount' }" class="delete-account">
          회원 탈퇴
        </RouterLink>
      </div>
    </div>
  </div>
</template>

<script setup>
import { RouterLink } from "vue-router";
import { ref, onMounted } from "vue";
import { useAccountStore } from "@/stores/accountStore";

const accountStore = useAccountStore();

const profile = ref({
  username: "",
  email: "",
  nickname: "",
  birth_date: "",
  income: 0,
  assets: 0.0,
  point: 0,
  previewImage: null,
});

const loadUserProfile = async () => {
  try {
    const response = await accountStore.fetchUserProfile();
    // console.log(response);
    profile.value.username = response.username;
    profile.value.email = response.email;
    profile.value.nickname = response.nickname;
    profile.value.birth_date = response.birth_date;
    profile.value.income = response.income;
    profile.value.assets = response.assets;
    profile.value.point = response.point;
    profile.value.previewImage = response.profile_image || null;
  } catch (error) {
    console.error("프로필 정보를 불러오지 못했습니다:", error);
  }
};

const baseURL = "http://localhost:8000";
const defaultProfile = `${baseURL}/static/profile/default_profile_1.jpeg`;

const getImageUrl = (previewImage) => {
  // API 응답의 경로를 그대로 사용
  return previewImage ? `${baseURL}${previewImage}` : defaultProfile;
};

const formatDate = (date) => {
  return new Date(date).toLocaleDateString("ko-KR");
};

const formatCurrency = (amount) => {
  return new Intl.NumberFormat("ko-KR").format(amount);
};

onMounted(() => {
  loadUserProfile();
});
</script>

<style scoped>
.profile-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.profile-card {
  background: white;
  border-radius: 15px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  padding: 30px;
}

.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e0e0e0;
}

.profile-header h2 {
  color: #2E8B57;
  margin: 0;
}

.edit-link {
  color: #2E8B57;
  text-decoration: none;
  padding: 8px 15px;
  border: 2px solid #2E8B57;
  border-radius: 20px;
  transition: all 0.3s ease;
}

.edit-link:hover {
  background-color: #2E8B57;
  color: white;
}

.profile-image-wrapper {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  overflow: hidden;
  border: 3px solid #2E8B57;
  margin: 0 auto 20px;
}

.profile-image-wrapper img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.profile-info {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 20px;
}

.info-item {
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 10px;
}

.label {
  display: block;
  color: #666;
  margin-bottom: 5px;
  font-size: 0.9em;
}

.value {
  color: #2E8B57;
  font-weight: 500;
  font-size: 1.1em;
}

.value.point {
  color: #ff6b6b;
}

.profile-footer {
  margin-top: 30px;
  text-align: right;
}

.delete-account {
  color: #dc3545;
  text-decoration: none;
  font-size: 0.9em;
}

@media (max-width: 768px) {
  .profile-info {
    grid-template-columns: 1fr;
  }
}
</style>
