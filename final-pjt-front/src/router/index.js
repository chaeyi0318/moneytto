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

// router.beforeEach((to, from, next) => {
//   const accountStore = useAccountStore();

//   if (to.matched.some((record) => record.meta.requiresAuth)) {
//     if (!accountStore.isLogin) {
//       next({ name: "Login", query: { redirect: to.fullPath } });
//     } else {
//       next();
//     }
//   } else {
//     next();
//   }
// });
router.beforeEach((to, from, next) => {
  const accountStore = useAccountStore();
  const isLogin = accountStore.isLogin;

  // 로그인 상태가 아닐 때 허용된 경로
  const publicPages = ["SignupView", "MainView"];

  if (!isLogin) {
    // 로그인 상태가 아니고, 접근하려는 페이지가 공개 페이지가 아닌 경우
    if (!publicPages.includes(to.name)) {
      accountStore.setLoginModalOpen(true); // 로그인 모달 열기
      accountStore.redirectAfterLogin = to.fullPath; // 로그인 후 리다이렉트할 경로 저장
      return;
    }
  }

  // 인증이 필요한 페이지 접근 시 로그인 상태 확인
  if (to.matched.some((record) => record.meta.requiresAuth)) {
    if (!isLogin) {
      next({ name: "Login", query: { redirect: to.fullPath } }); // 로그인 페이지로 리다이렉트
    } else {
      next(); // 로그인 상태라면 이동 허용
    }
  } else {
    next(); // 인증이 필요 없는 페이지는 그대로 이동
  }
});
export default router;
