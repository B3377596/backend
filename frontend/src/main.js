import { createApp } from 'vue'
import App from './App.vue'
import './assets/styles/base/_global.scss'
import router from "./router/index"; // 引入路由
import store from "./store";   // 引入 Vuex

createApp(App)
  .use(router)
  .use(store)
  .mount("#app");