// 引入 Vue Router 以及 Vue 3 相关功能
import { createRouter, createWebHistory } from 'vue-router';

// 引入页面组件
import Home from '@/views/appHome.vue';
import Login from '@/views/userLogin.vue';
import Profile from '@/views/Profile/MyProfile.vue';
import OrderDetail from '@/views/OrderDetail.vue';
import UserPage from '@/views/UserPage.vue';
import PostProduct from '@/views/PostProduct.vue';
import Checkout from '@/views/OrderCheckout.vue';
import Register from '@/views/userRegister.vue';
import ProductDetail from '@/views/ProductDetail.vue';
import Admin from '@/views/AdminHome.vue';
// 个人中心页面的子页面组件
import MyProducts from '@/views/Profile/MyProducts.vue';
import SoldOrders from '@/views/Profile/SoldOrders.vue';
import BoughtOrders from '@/views/Profile/BoughtOrders.vue';
import Favorites from '@/views/Profile/MyFavorites.vue';
import Reviews from '@/views/Profile/MyReviews.vue';
// 创建路由实例
const router = createRouter({
  history: createWebHistory(process.env.VUE_APP_BASE_URL),  // 使用 createWebHistory 进行历史模式的设置
  routes: [
    { path: '/',},
    // 首页
    { path: '/', name: 'Home', component: Home },
    
    // 登录页面
    { path: '/login', name: 'Login', component: Login },

    { 
      path: '/profile', 
      name: 'Profile', 
      component: Profile,
      children: [
        { path: 'my-products', name: 'MyProducts', component: MyProducts },
        { path: 'sold-orders', name: 'SoldOrders', component: SoldOrders },
        { path: 'bought-orders', name: 'BoughtOrders', component: BoughtOrders },
        { path: 'favorites', name: 'Favorites', component: Favorites },
        { path: 'reviews', name: 'Reviews', component: Reviews },
      ]
    },

    // 商品详情页
    { path: '/product/:id', name: 'ProductDetail', component: ProductDetail },

    // 订单详情页
    { path: '/order/:id', name: 'OrderDetail', component: OrderDetail },

    // 用户主页
    { path: '/user/:id', name: 'UserPage', component: UserPage },

    // 发布商品页面
    { path: '/post-product', name: 'PostProduct', component: PostProduct },

    // 购买商品页面
    { path: '/checkout/:productId', name: 'Checkout', component: Checkout },

    // 注册页面
    { path: '/register', name: 'Register', component: Register },

    {
      path: '/order/:orderId', 
      name: 'orderDetail', 
      component: OrderDetail, 
      props: true,
    },
    { path: '/admin', name: 'Admin', component: Admin},
    
  ]
});

export default router;
