import { createRouter, createWebHistory } from "vue-router";

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: "/",
      name: "home",
      component: () => import("@/views/frontground/HomeView.vue"),
      redirect: "/index",
      children: [
        {
          path: "index",
          component: () => import("@/views/frontground/index/Index.vue"),
        },
        {
          path: "musicList",
          component: () =>
            import("@/views/frontground/musicList/MusicList.vue"),
        },
        {
          path: "collect",
          component: () => import("@/views/frontground/collect/Collect.vue"),
        },
        {
          path: "profile",
          component: () => import("@/views/frontground/profile/Profile.vue"),
        },
        {
          path: "detail/:id",
          component: () => import("@/views/frontground/detail/Detail.vue"),
        },
      ],
    },
    {
      path: "/login",
      component: () => import("@/views/frontground/Login.vue"),
    },
    {
      path: "/admin",
      name: "admin",
      component: () => import("@/views/background/HomeView.vue"),
      redirect: "/admin/index",
      children: [
        {
          path: "index",
          component: () => import("@/views/background/index/Index.vue"),
        },
        {
          path: "musicList",
          component: () => import("@/views/background/musicList/MusicList.vue"),
        },
        {
          path: "collect",
          component: () => import("@/views/background/collect/Collect.vue"),
        },
        {
          path: "comment",
          component: () => import("@/views/background/comment/Comment.vue"),
        },
        {
          path: "userList",
          component: () => import("@/views/background/userList/UserList.vue"),
        },
      ],
    },
    {
      path: "/admin/login",
      component: () => import("@/views/background/Login.vue"),
    },
  ],
});

export default router;
