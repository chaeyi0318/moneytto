<template>
  <div class="fortune-view">
    <div class="button-container">
      <div class="tarot-card" @click="navigateTo('salmal')">
        <span>살말마스터</span>
      </div>
      <div class="tarot-card" @click="navigateTo('fortune')">
        <span>금전운</span>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue';
import { useRouter } from 'vue-router';
import { useAccountStore } from '@/stores/accountStore';

const router = useRouter();
const accountStore = useAccountStore();

onMounted(async () => {
  await accountStore.fetchUserProfile(); // 페이지 로드 시 사용자 프로필 가져오기
});

const navigateTo = async (type) => {
  if (confirm('머니또와 상담 시 10P가 소요됩니다. 계속하시겠습니까?')) {
    await accountStore.fetchUserProfile(); // 최신 사용자 프로필 정보 가져오기
    
    if (accountStore.user.point >= 10) { // 포인트 확인
      const success = await accountStore.deductPoints(10); // 포인트 차감 시도
      if (success) {
        router.push({ name: 'Bot', params: { type } }); // 성공적으로 차감되면 이동
      } else {
        alert('포인트 차감에 실패했습니다. 다시 시도해주세요.');
      }
    } else {
      alert('포인트가 부족합니다.');
    }
  }
};
</script>


<style scoped>
.fortune-view {
  width: 100%;
  height: 100vh;
  background-image: url('@/assets/chat_bg.jpg');
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}

.button-container {
  display: flex;
  gap: 40px;
  z-index: 1;
  position: absolute;
  top: 25%;
  transform: translateY(-50%);
}

.tarot-card {
  width: 300px;
  height: 100px;
  position: relative;
  cursor: pointer;
  padding: 4px;
  transition: all 0.3s ease;
}

.tarot-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(45deg, #4a1f7f, #8250c8);
  border-radius: 10px;
  z-index: -1;
}

.tarot-card::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  right: 2px;
  bottom: 2px;
  background: #2f1155;
  border-radius: 8px;
  z-index: -1;
}

.tarot-card span {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 100%;
  height: 100%;
  color: #fff;
  font-size: 20px;
  font-weight: bold;
  text-shadow: 0 0 10px rgba(255, 255, 255, 0.5);
  position: relative;
  z-index: 1;
}

.tarot-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 5px 20px rgba(74, 31, 127, 0.4);
}

.tarot-card:hover span {
  text-shadow: 0 0 15px rgba(255, 255, 255, 0.8);
}
</style>