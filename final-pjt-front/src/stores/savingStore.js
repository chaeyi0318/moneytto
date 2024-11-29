// src/stores/savingStore.js
import { ref, watch, computed } from "vue";
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
    pagination: { // 페이지네이션 상태 추가
      next: null,
      previous: null,
      count: 0,
    },
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
    
        // 페이지네이션 데이터 처리
        this.products = response.data.results; // 현재 페이지 데이터
        this.pagination = {
          next: response.data.next, // 다음 페이지 URL
          previous: response.data.previous, // 이전 페이지 URL
          count: response.data.count, // 전체 데이터 개수
        };
    
        this.currentSearchParams = searchParams; // 검색 상태 저장
      } catch (error) {
        console.error("Error fetching savings:", error);
        this.error = "적금 상품을 불러오는데 실패했습니다.";
      } finally {
        this.loading = false;
      }
    },
    async fetchNextPage() {
      if (!this.pagination.next) return; // 다음 페이지가 없으면 종료
      const nextPageUrl = new URL(this.pagination.next);
      const page = nextPageUrl.searchParams.get("page");
      
      await this.getSavings({ page });
    },

    async fetchPreviousPage() {
      if (!this.pagination.previous) return; // 이전 페이지가 없으면 종료
      const previousPageUrl = new URL(this.pagination.previous);
      const page = previousPageUrl.searchParams.get("page");

      await this.getSavings({ page });
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
  
      async fetchLikedSavings() {
        this.loading = true;
        this.error = null;
        try {
          const response = await api.get(`${this.API_URL}/liked-savings/`);
          return response.data; // 데이터를 반환합니다.
        } catch (error) {
          console.error("Error fetching liked savings:", error);
          this.error = "찜한 적금 상품을 불러오는데 실패했습니다.";
          return []; // 에러 시 빈 배열 반환
        } finally {
          this.loading = false;
        }
      },
    },
  })

