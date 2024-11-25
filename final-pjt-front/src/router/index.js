import Login from "@/components/accounts/Login.vue";
import Bot from "@/components/bot/Bot.vue";
import AdditionalInfo from "@/components/mypage/AdditionalInfo.vue";
import DeleteAccount from "@/components/mypage/DeleteAccount.vue";
import LikedSavings from "@/components/mypage/LikedSavings.vue";
import Profile from "@/components/mypage/Profile.vue";
import ProfileUpdate from "@/components/mypage/ProfileUpdate.vue";
import SolvedQuizzes from "@/components/quiz/SolvedQuizzes.vue";
import Recommend from "@/components/savings/Recommend.vue";
import { useAccountStore } from "@/stores/accountStore";
import CalendarView from "@/views/CalendarView.vue";
import FortuneView from "@/views/FortuneView.vue";
import MainView from "@/views/MainView.vue";
import MyPageView from "@/views/MyPageView.vue";
import PostPageView from "@/views/PostPageView.vue";
import QuizView from "@/views/QuizView.vue";
import ReportView from "@/views/ReportView.vue";
import SavingView from "@/views/SavingView.vue";
import SignupView from "@/views/SignupView.vue";
import UpdatePageView from "@/views/UpdatePageView.vue";
import { createRouter, createWebHistory } from "vue-router";

const routes = [
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
    path: "/login",
    name: "Login",
    component: Login,
  },
  {
    path: '/bot/:type',
    name: 'Bot',
    component: Bot,
    props: true
  },
  {
    path: "/mypage",
    name: "MyPageView",
    component: MyPageView,
    meta: { requiresAuth: true },
    children: [
      {
        path: "/profile",
        name: "profile",
        component: Profile,
      },
      {
        path: "/profile-update",
        name: "profile-update",
        component: ProfileUpdate,
      },
      {
        path: "/liked-savings",
        name: "LikedSavings",
        component: LikedSavings,
      },
      {
        path: "/delete-account",
        name: "DeleteAccount",
        component: DeleteAccount,
      },
      {
        path: "/solved-quizzes",
        name: "SolvedQuizzes",
        component: SolvedQuizzes,
      },
    ]
  },
  {
    path: "/post-page",
    name: "PostPageView",
    component: PostPageView,
  },
  
  {
    path: "/additional-info",
    name: "AdditionalInfo",
    component: AdditionalInfo,
  },
  
  {
    path: "/recommend",
    name: "Recommend",
    component: Recommend,
  },
  {
    path: "/quiz",
    name: "Quiz",
    component: QuizView,
  },
  {
    path: "/update-post",
    name: "UpdatePageView",
    component: UpdatePageView,
  },
  {
    path: '/report',
    name: 'ReportView',
    component: ReportView,
  }
];

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
  const accountStore = useAccountStore();

  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!accountStore.isLogin) {
      next({ name: "Login", query: { redirect: to.fullPath } });
    } else {
      next();
    }
  } else {
    next();
  }
});
export default router;
