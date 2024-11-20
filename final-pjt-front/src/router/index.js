import CalendarView from "@/views/CalendarView.vue";
import FortuneView from "@/views/FortuneView.vue";
import MainView from "@/views/MainView.vue";
import MyPageView from "@/views/MyPageView.vue";
import PostPageView from "@/views/PostPageView.vue";
import QuizView from "@/views/QuizView.vue";
import SavingView from "@/views/SavingView.vue";
import SignupView from "@/views/SignupView.vue";
import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "MainView",
      component: MainView,
    },
    {
      path: "/signup",
      name: "SignupView",
      component: SignupView,
    },
    {
      path: "/money-calendar",
      name: "CalendarView",
      component: CalendarView,
    },
    {
      path: "/saving",
      name: "SavingView",
      component: SavingView,
    },
    {
      path: "/fortune",
      name: "FortuneView",
      component: FortuneView,
    },
    {
      path: "/quiz",
      name: "QuizView",
      component: QuizView,
    },
    {
      path: "/mypage",
      name: "MyPageView",
      component: MyPageView,
    },
    {
      path: "/post-page",
      name: "PostPageView",
      component: PostPageView,
    },
  ],
});

export default router;
