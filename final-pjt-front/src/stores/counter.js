import { ref, computed } from "vue";
import { defineStore } from "pinia";
import axios from "axios";

export const useCalendarStore = defineStore(
  "calendar",
  () => {}
  // return {}
);

export const useSavingStore = defineStore("saving", () => {
  const API_URL = "http://127.0.0.1:8000";
  const products = ref([]);
  const loading = ref(false);
  const error = ref(null);

  const getSavings = async function (amount, period) {
    loading.value = true;
    error.value = null;
    try {
      const response = await axios.get(`${API_URL}/savings/search/`, {
        params: { amount, period },
      });
      products.value = response.data;
    } catch (err) {
      console.error(err);
      error.value = "적금 상품을 불러오는데 실패했습니다.";
    } finally {
      loading.value = false;
    }
  };

  return { API_URL, products, loading, error, getSavings };
});
