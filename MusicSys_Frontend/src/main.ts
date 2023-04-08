import { createApp } from "vue";
import App from "./App.vue";
import router from "./router";
import "./assets/global.css";
import "element-plus/dist/index.css";
import "@/router/permission";

const app = createApp(App);

app.use(router);

app.mount("#app");
