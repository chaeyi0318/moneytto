import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";
import { useRouter } from "vue-router";

export const useCalendarStore = defineStore("dateStore", {
  state: () => ({
    selectedDate: ref(""),
  }),
  actions: {
    setSelectedDate(date) {
      this.selectedDate = date;
    },
  },
});

export const useSavingStore = defineStore("saving", {
  state: () => ({
    API_URL: "http://127.0.0.1:8000/savings",
    products: [],
    recommendedSavings: [],
    loading: false,
    error: null,
    currentSearchParams: {},
    sortField: "max_preference_rate",
    sortOrder: "desc",
    ageBasedRecommendations: [],
    incomeBasedRecommendations: [],
  }),

  actions: {
    async getSavings(params = {}) {
      this.loading = true;
      this.error = null;
      try {
        const searchParams = {
          ...this.currentSearchParams,
          ...params,
          sort_by: params.sort_by || this.sortField,
          sort_order: params.sort_order || this.sortOrder,
        };

        const response = await axios.get(`${this.API_URL}/search/`, {
          params: searchParams,
        });
        this.products = response.data;
        this.currentSearchParams = searchParams;
      } catch (error) {
        console.error("Error fetching savings:", error);
        this.error = "적금 상품을 불러오는데 실패했습니다.";
      } finally {
        this.loading = false;
      }
    },

    updateSort(field) {
      if (this.sortField === field) {
        this.sortOrder = this.sortOrder === "asc" ? "desc" : "asc";
      } else {
        this.sortField = field;
        this.sortOrder = "desc";
      }

      this.getSavings({
        ...this.currentSearchParams,
        sort_by: this.sortField,
        sort_order: this.sortOrder,
      });
    },

    async toggleLike(savingPk) {
      try {
        const token = localStorage.getItem("token");
        if (!token) {
          throw new Error("로그인이 필요합니다.");
        }

        const response = await axios.post(
          `${this.API_URL}/likes/${savingPk}/`,
          {},
          {
            headers: {
              Authorization: `Token ${token}`,
            },
          }
        );
        const productIndex = this.products.findIndex((p) => p.id === savingPk);
        if (productIndex !== -1) {
          this.products[productIndex].is_liked = response.data.is_liked;
        }
      } catch (error) {
        console.error("Error toggling like:", error);
        this.error = "찜하기 처리 중 오류가 발생했습니다.";
        if (error.response && error.response.status === 401) {
          // 401 Unauthorized 에러 처리
          console.log("인증 오류: 로그인이 필요합니다.");
          // 여기에 로그인 페이지로 리다이렉트하는 로직을 추가할 수 있습니다.
        }
      }
    },

    getCsrfToken() {
      return (
        document.cookie
          .split(";")
          .find((cookie) => cookie.trim().startsWith("csrftoken="))
          ?.split("=")[1] || ""
      );
    },

    async fetchRecommendedSavings() {
      this.loading = true;
      this.error = null;
      try {
        const token = localStorage.getItem("token");
        const response = await axios.get(`${this.API_URL}/recommend/`, {
          headers: {
            Authorization: `Token ${token}`,
          },
        });
        this.ageBasedRecommendations = response.data.age_based;
        this.incomeBasedRecommendations = response.data.income_based;
      } catch (error) {
        console.error("Error fetching recommended savings:", error);
        this.error = "추천 적금 상품을 불러오는데 실패했습니다.";
      } finally {
        this.loading = false;
      }
    },
  },
});

export const useAccountStore = defineStore("accountStore", () => {
  const router = useRouter();
  const API_URL = "http://127.0.0.1:8000";
  const token = ref(null);
  const user = ref(null);

  
  // 로그인 여부를 computed로 계산
  const isLogin = computed(() => {
    if (token.value === null) {
      return false;
    } else {
      return true;
    }
  });

  const signup = function (payload) {
    const { username, password1, password2, nickname, email } = payload;

    axios({
      method: "post",
      url: `${API_URL}/accounts/signup/`,
      data: {
        username,
        password1,
        password2,
        nickname,
        email,
      },
    })
      .then((response) => {
        console.log("회원가입 완");
        router.push({ name: "MainView" });
      })
      .catch((error) => {
        console.log(error);
      });
  };

  // 로그인 함수
  const login = async function (payload) {
    const { username, password } = payload;

    try {
      const response = await axios.post(`${API_URL}/accounts/login/`, {
        username,
        password,
      });

      console.log(response.data.token);

      token.value = response.data.token;
      user.value = {
        id: response.data.user.id,
        username: response.data.user.username,
        nickname: response.data.user.nickname,
      };

      // localStorage.setItem('token', token.value)
      localStorage.setItem("token", token.value);
      localStorage.setItem("user", JSON.stringify(user.value));
      console.log("로그인 성공");
    } catch (error) {
      console.error("로그인 실패:", error.message);
    }
  };

  const checkLoginStatus = () => {
    const storedToken = localStorage.getItem("token"); // localStorage에서 토큰 가져오기
    if (storedToken) {
      console.log("로그인 상태 유지 중");
      token.value = storedToken; // Vue 상태에 토큰 반영
    } else {
      console.log("로그인 필요");
    }
  };

  // 페이지 로드 시 로그인 상태 확인
  window.onload = checkLoginStatus;

  const logOut = function () {
    axios({
      method: "post",
      url: `${API_URL}/accounts/logout/`,
      headers: {
        Authorization: `Token ${token.value}`, // 헤더에 토큰 포함
      },
    })
      .then((res) => {
        console.log(res.data);

        // Vue 상태 및 localStorage에서 토큰과 사용자 정보 제거
        token.value = null;
        user.value = null;
        localStorage.removeItem("token");
        localStorage.removeItem("user");

        // 로그아웃 후 메인 페이지로 리다이렉트
        router.push({ name: "MainView" });
      })
      .catch((err) => {
        console.log(err);
      });
  };

  return { token, isLogin, login, signup, checkLoginStatus, logOut };
});
