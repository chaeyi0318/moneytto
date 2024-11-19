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
    recommendedSavings: [],
    loading: false,
    error: null,
    currentSearchParams: {},
    sortField: 'max_preference_rate',
    sortOrder: 'desc'
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
          sort_order: params.sort_order || this.sortOrder
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
        this.sortOrder = this.sortOrder === 'asc' ? 'desc' : 'asc';
      } else {
        this.sortField = field;
        this.sortOrder = 'desc';
      }

      this.getSavings({
        ...this.currentSearchParams,
        sort_by: this.sortField,
        sort_order: this.sortOrder
      });
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
        ?.split("=")[1] || '';
    },

    async fetchRecommendedSavings() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.get(`${this.API_URL}/recommend/`);
        this.recommendedSavings = response.data;
      } catch (error) {
        console.error("Error fetching recommended savings:", error);
        this.error = "추천 적금 상품을 불러오는데 실패했습니다.";
      } finally {
        this.loading = false;
      }
    }
  }
});

export const useAccountStore = defineStore('account', {
  state: () => ({
    API_URL: 'http://127.0.0.1:8000/'
  })
})

