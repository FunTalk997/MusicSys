import router from "@/router/index";
import Cookies from "js-cookie";

router.beforeEach((to, from, next) => {
  const adminToken = Cookies.get("adminToken");
  const userToken = Cookies.get("userToken");

  if (to.path.includes("admin")) {
    if (!adminToken && to.path !== "/admin/login") {
      next({
        path: "/admin/login",
      });
    } else if (adminToken && to.path === "/admin/login") {
      next({
        path: "/admin/login",
      });
    } else {
      next();
    }
  } else {
    if (!userToken && to.path !== "/login") {
      next({
        path: "/login",
      });
    } else if (userToken && to.path === "/login") {
      next({
        path: "/",
      });
    } else {
      next();
    }
  }
});
