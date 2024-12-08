<template>
  <div class="profile-container">
    <div class="sidebar">
      <!-- 侧边栏导航 -->
      <h3>个人中心</h3>
      <ul>
        <li><router-link to="/profile/my-products" @click="handleReplace('/profile/my-products')">我的商品</router-link></li>
        <li><router-link to="/profile/sold-orders" @click="handleReplace('/profile/sold-orders')">出售的订单</router-link></li>
        <li><router-link to="/profile/bought-orders" @click="handleReplace('/profile/bought-orders')">购买的订单</router-link></li>
        <li><router-link to="/profile/favorites" @click="handleReplace('/profile/favorites')">收藏夹</router-link></li>
        <li><router-link to="/profile/reviews" @click="handleReplace('/profile/reviews')">评价</router-link></li>
      </ul>
      <div class="logout-button">
        <button @click="logout">登出</button>
      </div>
    </div>

    <div class="profile-main">
      <!-- 个人信息展示 -->
      <div class="profile-header">
        <img :src="user.avatar" alt="用户头像" class="avatar" />
        <h3>{{ user.username }}</h3>
        <p>评分: {{ user.rating }}</p>
      </div>
      <!-- 登出按钮 -->
     

      <!-- 显示当前子页面内容 -->
      <router-view></router-view>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      user: {
        username: "张三",  // 示例用户名
        defaultAvatar: '/path/to/default-avatar.png',
        rating: 4.5, // 示例评分
      },
    };
  },
  mounted() {
    this.fetchUserProfile();  // 在组件挂载后获取用户信息
  },
  methods: {
    logout() {
      // 清除本地存储的用户数据
      localStorage.removeItem('access_token');
      localStorage.removeItem('refresh_token');
      localStorage.removeItem('user');
      localStorage.removeItem('user_id')
      // 清空 Vuex 状态中的用户数据
      this.$store.dispatch('user/logout');

      // 跳转到登录页面
      this.$router.push('/');
    },
    handleReplace(path) {
    // 使用 router.replace 来替代默认的跳转
    this.$router.replace(path);
    },
    // 获取用户信息
    async fetchUserProfile() {
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.get('/api/profile', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.user = response.data;  // 保存用户信息
      } catch (error) {
        console.error('获取用户信息失败:', error);
        // 在此处理错误，可以展示错误提示
        this.$router.push('/');  
      }
    },
  },
};
</script>

<style scoped>
/* 主容器 */
.profile-container {
display: flex;
min-height: 100vh;
background-color: #f9f9f9;
}

/* 侧边栏 */
.sidebar {
   width: 200px;
 height: 100vh;
 position: fixed;
 top: 0;
 left: 0;
 padding: 20px;
 background-color: #ffffff;
 box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
 transition: transform 0.3s ease-in-out;
}

.sidebar.hidden {
 transform: translateX(-100%);
}

/* 侧边栏标题 */
.sidebar h3 {
 margin-top: 0;
 font-size: 1.5rem;
 color: #333;
}

/* 侧边栏菜单 */
.sidebar ul {
 list-style-type: none;
 padding-left: 0;
 margin-top: 20px;
}

.sidebar ul li {
 margin-bottom: 10px;
}

.sidebar ul li a {
 text-decoration: none;
 color: #333;
 font-size: 1rem;
 display: block;
 padding: 10px 15px;
 border-radius: 4px;
 transition: background-color 0.3s, color 0.3s;
}

.sidebar ul li a:hover,
.sidebar ul li a.active {
 background-color: #e8f5ff;
 color: #007bff;
}

/* 主内容区 */
.profile-main {
 margin-left: 250px;
 padding: 20px;
 width: calc(100% - 250px);
 transition: margin-left 0.3s ease-in-out;
}

.sidebar.hidden + .profile-main {
 margin-left: 0;
}

/* 用户头像和信息 */
.profile-header {
 display: flex;
 align-items: center;
 margin-bottom: 20px;
}

.avatar {
 width: 100px;
 height: 100px;
 border-radius: 50%;
 margin-right: 20px;
 object-fit: cover; /* 确保图像不会变形 */
 box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
}

.profile-header h3 {
 margin: 0;
 font-size: 24px;
 color: #333;
}

.profile-header p {
 margin: 5px 0 0;
 color: #666;
}
.logout-button {
  margin-top: auto;  /* 使按钮始终靠底部 */
}

.logout-button button {
  padding: 10px 20px;
  background-color: #ff4444;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.logout-button button:hover {
  background-color: #ff0000;
}
</style>