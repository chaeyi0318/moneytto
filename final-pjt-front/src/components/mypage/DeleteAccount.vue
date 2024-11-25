<template>
  <div class="delete-account-container">
    <div class="delete-card">
      <h2 class="card-title">계정 삭제</h2>
      <div class="warning-message">
        <i class="bi bi-exclamation-triangle"></i>
        <p>계정을 삭제하면 모든 데이터가 영구적으로 삭제됩니다.</p>
      </div>
      
      <form @submit.prevent="deleteAccount" class="delete-form">
        <div class="form-group">
          <label for="password">비밀번호 확인</label>
          <input 
            id="password" 
            v-model="password" 
            type="password" 
            required 
            placeholder="비밀번호를 입력해주세요"
          />
        </div>
        
        <button type="submit" class="delete-button">계정 삭제</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useAccountStore } from "@/stores/accountStore";

const accountStore = useAccountStore();
const password = ref("");

const deleteAccount = async () => {
  if (
    confirm("정말로 계정을 삭제하시겠습니까? 이 작업은 되돌릴 수 없습니다.")
  ) {
    try {
      await accountStore.deleteAccount(password.value);
      alert("계정이 성공적으로 삭제되었습니다.");
      router.push({ name: "MainView" })
      // 로그아웃 처리는 deleteAccount 함수 내에서 이미 처리되므로 여기서는 추가 작업 불필요
    } catch (error) {
      alert("계정 삭제에 실패했습니다.");
    }
  }
};
</script>


<style scoped>
.delete-account-container {
  max-width: 600px;
  margin: 40px auto;
  padding: 20px;
}

.delete-card {
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}

.card-title {
  color: #dc3545;
  text-align: center;
  margin-bottom: 25px;
  font-size: 1.8em;
}

.warning-message {
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
  border-radius: 8px;
  padding: 15px;
  margin-bottom: 25px;
  display: flex;
  align-items: center;
  gap: 10px;
}

.warning-message i {
  color: #dc3545;
  font-size: 1.5em;
}

.warning-message p {
  margin: 0;
  color: #856404;
}

.form-group {
  margin-bottom: 25px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #666;
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
  border-color: #dc3545;
}

.delete-button {
  width: 100%;
  padding: 12px;
  background-color: #dc3545;
  color: white;
  border: none;
  border-radius: 8px;
  font-size: 1.1em;
  cursor: pointer;
  transition: all 0.3s ease;
}

.delete-button:hover {
  background-color: #c82333;
  transform: translateY(-2px);
}
</style>