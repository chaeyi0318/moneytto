import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useCalendarStore = defineStore(
  "calendar",
  () => {}
  // return {}
);

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
  },
});
