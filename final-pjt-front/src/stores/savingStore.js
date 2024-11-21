﻿// src/stores/savingStore.js
import { defineStore } from "pinia";
import api from "./api"; // API 인스턴스 import

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