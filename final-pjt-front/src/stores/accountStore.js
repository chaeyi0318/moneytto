// src/stores/accountStore.js
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import api from "./api"; // API 인스턴스 import
import { useCalendarStore } from "./calendarStore";

export const useAccountStore = defineStore("accountStore", () => {
  const router = useRouter();
  const token = ref(null);
  const user = ref(null);

  const isLogin = computed(() => token.value !== null);

  const isLoginModalOpen = ref(false)
  const redirectAfterLogin = ref(null)

  const signup = async function (payload) {
    try {
      const response = await api.post("/accounts/signup/", payload);
      console.log("회원가입 완료");
      await login({
        username: payload.username,
        password: payload.password1,
      });
      // router.push({ name: "MainView" });
      router.push({ name: "AdditionalInfo" });
    } catch (error) {
      console.error("회원가입 실패:", error.response?.data || error.message);
    }
  };

  const login = async function (payload) {
    try {
      const response = await api.post("/accounts/login/", payload);
      token.value = response.data.token;
      user.value = {
        id: response.data.user.id,
        username: response.data.user.username,
        nickname: response.data.user.nickname,
      };
      localStorage.setItem("token", token.value);
      localStorage.setItem("user", JSON.stringify(user.value));
      console.log("로그인 성공");
      isLoginModalOpen.value = false;

      if (redirectAfterLogin.value) {
        router.push(redirectAfterLogin.value);
        redirectAfterLogin.value = null; // 리다이렉트 후 초기화
      } else {
        router.push({ name: "MainView" }); // 기본적으로 MainView로 이동
      }
      
    } catch (error) {
      console.error("로그인 실패:", error.response?.data || error.message);
    }
  };

  const checkLoginStatus = () => {
    const storedToken = localStorage.getItem("token");
    const storedUser = localStorage.getItem("user");
    if (storedToken && storedUser) {
      token.value = storedToken;
      user.value = JSON.parse(storedUser);
      console.log("로그인 상태 유지 중");
    } else {
      console.log("로그인 필요");
    }
  };

  const logOut = async function () {
    try {
      await api.post("/accounts/logout/");
      const calendarStore = useCalendarStore(); // 여기서 스토어를 초기화합니다
      calendarStore.clearState(); // clearState 메서드 호출
      token.value = null;
      user.value = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      router.push({ name: "MainView" });
    } catch (error) {
      console.error("로그아웃 실패:", error.response?.data || error.message);
    }
  };

  const fetchUserProfile = async () => {
    try {
      const response = await api.get("/accounts/update/");
      user.value = response.data;
      return response.data;
    } catch (error) {
      console.error(
        "프로필 정보 불러오기 실패:",
        error.response?.data || error.message
      );
      throw error;
    }
  };

  const updateUserInfo = async (payload) => {
    try {
      const response = await api.put("/accounts/update/", payload, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      user.value = { ...user.value, ...response.data };
      localStorage.setItem("user", JSON.stringify(user.value)); // 로컬 스토리지 업데이트
      console.log("사용자 정보 업데이트 성공");
    } catch (error) {
      console.error(
        "사용자 정보 업데이트 실패:",
        error.response?.data || error.message
      );
      throw error; // 에러를 다시 던져서 컴포넌트에서 처리할 수 있게 함
    }
  };

  const updateAdditionalInfo = async (payload) => {
    try {
      const response = await api.put("/accounts/additional-info/", payload);
      user.value = { ...user.value, ...response.data };
      console.log("추가 정보 업데이트 성공");
    } catch (error) {
      console.error(
        "추가 정보 업데이트 실패:",
        error.response?.data || error.message
      );
    }
  };

  const deleteAccount = async (password) => {
    try {
      await api.delete("/accounts/delete/", { data: { password } });
      token.value = null;
      user.value = null;
      localStorage.removeItem("token");
      localStorage.removeItem("user");
      router.push({ name: "MainView" });
      console.log("계정 삭제 성공");
    } catch (error) {
      console.error("계정 삭제 실패:", error.response?.data || error.message);
    }
  };

  const deductPoints = async (amount) => {
    try {
      const response = await api.post("/accounts/deduct-points/", { amount });
      user.value.point = response.data.point; // 차감 후 남은 포인트 업데이트
      return true;
    } catch (error) {
      console.error("포인트 차감 오류:", error.response?.data || error.message);
      return false;
    }
  };

  const setLoginModalOpen = (status) => {
    isLoginModalOpen.value = status
  }

  // 스토어 초기화 시 로그인 상태 확인
  checkLoginStatus();

  return {
    token,
    user,
    isLogin,
    login,
    signup,
    logOut,
    updateUserInfo,
    updateAdditionalInfo,
    deleteAccount,
    fetchUserProfile,
    deductPoints,
    isLoginModalOpen,
    setLoginModalOpen
  };
});
