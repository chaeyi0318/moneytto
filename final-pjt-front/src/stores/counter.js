import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useCalendarStore = defineStore("dateStore", {
  state: () => ({
    selectedDate: ref('')
  }),
  actions: {
    setSelectedDate(date) {
      this.selectedDate = date
    }
  }
});

export const useSavingStore = defineStore("saving", {
  state: () => ({
    API_URL: "http://127.0.0.1:8000/savings",
    products: [],
    loading: false,
    error: null,
  }),
  actions: {
    async getSavings(searchParams = {}) {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(`${this.API_URL}/search/`, {
          params: searchParams,
        });
        this.products = response.data;
      } catch (error) {
        console.error("Error fetching savings:", error);
        this.error = "적금 상품을 불러오는데 실패했습니다.";
      } finally {
        this.loading = false;
      }
    },
    async toggleLike(savingPk) {
      try {
        const response = await axios.post(
          `${this.API_URL}/likes/${savingPk}/`,
          {},
          {
            headers: {
              "X-CSRFToken": this.getCsrfToken(),
            },
          }
        );
        // 찜하기 상태 업데이트
        const productIndex = this.products.findIndex((p) => p.id === savingPk);
        if (productIndex !== -1) {
          this.products[productIndex].is_liked = response.data.is_liked;
        }
      } catch (error) {
        console.error("Error toggling like:", error);
        this.error = "찜하기 처리 중 오류가 발생했습니다.";
      }
    },
    getCsrfToken() {
      return document.cookie
        .split(";")
        .find((cookie) => cookie.trim().startsWith("csrftoken="))
        .split("=")[1];
    },
  },
});

export const useAccountStore = defineStore('account', {
  state: () => ({
    API_URL: 'http://127.0.0.1:8000/'
  })
})

