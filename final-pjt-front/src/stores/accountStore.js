// src/stores/accountStore.js
import { ref, computed } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import api from "./api"; // API 인스턴스 import

export const useAccountStore = defineStore("accountStore", () => {
  const router = useRouter();
  const token = ref(null);
  const user = ref(null);

  const isLogin = computed(() => token.value !== null);

  const signup = async (payload) => {
    try {
      await api.post("/accounts/signup/", payload);
      console.log("회원가입 완료");
      router.push({ name: "MainView" });
    } catch (error) {
      console.error("회원가입 실패:", error.response?.data || error.message);
    }
  };

  const login = async (payload) => {
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

  const logOut = async () => {
    try {
      await api.post("/accounts/logout/");

      token.value = null;
      user.value = null;

      localStorage.removeItem("token");
      localStorage.removeItem("user");

      router.push({ name: "MainView" });

      console.log("로그아웃 성공");
    } catch (error) {
      console.error("로그아웃 실패:", error.response?.data || error.message);
    }
  };

  // 스토어 초기화 시 로그인 상태 확인
  checkLoginStatus();

  return { token, user, isLogin, login, signup, logOut };
});
