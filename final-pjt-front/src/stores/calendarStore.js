// src/stores/calendarStore.js
import { ref, watch } from "vue";
import { defineStore } from "pinia";
import api from "./api"; // API 인스턴스 import

export const useCalendarStore = defineStore("dateStore", () => {
  const expenses_date = ref(localStorage.getItem("expenses_date") || "");

  const setSelectedDate = (date) => {
    expenses_date.value = date;
  };

  watch(expenses_date, (newDate) => {
    localStorage.setItem("expenses_date", newDate);
  });

  const clearState = () => {
    localStorage.removeItem("expenses_date");
    expenses_date.value = "";
  };

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
      formData.append("expenses_date", expenses_date);
      formData.append("privacy_setting", privacy_setting);
      formData.append("category", parseInt(category));
      formData.append("price", parseInt(price));
      formData.append("content", content);

      if (image) {
        formData.append("image", image);
      }

      const response = await api.post("/posts/create-post/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
    } catch (error) {
      console.error("게시글 작성 실패:", error);
    }
  };

  return {
    expenses_date,
    setSelectedDate,
    submitPost,
    clearState,
  };
});
