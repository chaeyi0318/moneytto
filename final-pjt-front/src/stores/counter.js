import { ref, computed, watch } from "vue";
import { defineStore } from "pinia";
import { useRouter } from "vue-router";
import axios from "axios";
import api from "./api"; // 새로 만든 api 인스턴스 import

export const useCalendarStore = defineStore("dateStore", () => {
  const expenses_date = ref(localStorage.getItem('expenses_date') || '')

  const setSelectedDate = (date) => {
    expenses_date.value = date;
  };

  watch(expenses_date, (newDate) => {
    localStorage.setItem('expenses_date', newDate)
  })

  const clearState = () => {
    localStorage.removeItem('expenses_date')
    expenses_date.value = ''
  }

  const submitPost = async ({
    expenses_date,
    privacy_setting,
    category,
    price,
    content,
    image,
  }) => {
    try { 
      const formData = new FormData();
      
      formData.append('expenses_date', expenses_date); // 소비한 날짜
      formData.append('privacy_setting', privacy_setting); // 공개 범위
      formData.append('category', parseInt(category)); // 카테고리 ID를 정수로 변환
      formData.append('price', parseInt(price)); // 가격을 정수로 변환
      formData.append('content', content);

      if (image) {
        formData.append('image', image); // 이미지 파일 추가
      }

      // API 요청 전송
      const response = await api.post("/posts/create-post/", formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });

      if (response.status === 200) {
        console.log("게시글 작성 완료");
      }
    } catch (error) {
      console.error("게시글 작성 실패:", error);
    }
  };

  return {
    expenses_date,
    setSelectedDate,
    submitPost,
    clearState
  };
});

export const useSavingStore = defineStore("saving", {
  state: () => ({
    API_URL: "/savings",
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

        const response = await api.get(`${this.API_URL}/search/`, {
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

    async toggleLike(savingPk) {
      try {
        const response = await api.post(`${this.API_URL}/likes/${savingPk}/`);
        const productIndex = this.products.findIndex((p) => p.id === savingPk);
        if (productIndex !== -1) {
          this.products[productIndex].is_liked = response.data.is_liked;
        }
      } catch (error) {
        console.error("Error toggling like:", error);
        this.error = "찜하기 처리 중 오류가 발생했습니다.";
        if (error.response && error.response.status === 401) {
          console.log("인증 오류: 로그인이 필요합니다.");
          // 로그인 페이지로 리다이렉트 로직
        }
      }
    },

    async fetchRecommendedSavings() {
      this.loading = true;
      this.error = null;
      try {
        const response = await api.get(`${this.API_URL}/recommend/`);
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
  const token = ref(null);
  const user = ref(null);

  const isLogin = computed(() => token.value !== null);

  const signup = async function (payload) {
    try {
      const response = await api.post("/accounts/signup/", payload);
      console.log("회원가입 완료");
      router.push({ name: "MainView" });
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

  const updateUserInfo = async (payload) => {
    try {
      const response = await api.put("/accounts/update/", payload);
      user.value = { ...user.value, ...response.data };
      console.log("사용자 정보 업데이트 성공");
    } catch (error) {
      console.error(
        "사용자 정보 업데이트 실패:",
        error.response?.data || error.message
      );
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
  };
});
