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
    </div>

    <div class="profile-main">
      <!-- 个人信息展示 -->
      <div class="profile-header">
        <img :src="user.avatar" alt="用户头像" class="avatar" />
        <h3>{{ user.username }}</h3>
        <p>评分: {{ user.rating }}</p>
      </div>

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
.profile-container {
  display: flex;
  padding: 20px;
}

.sidebar {
  width: 250px;
  height: 100vh;
  position: fixed;
  top: 0;
  left: 0;
  padding: 20px;
  background-color: #f4f4f4;
}

.profile-main {
  margin-left: 250px;
  padding: 20px;
  width: calc(100% - 250px);
}

.sidebar h3 {
  margin-top: 0;
}

.sidebar ul {
  list-style-type: none;
  padding-left: 0;
}

.sidebar ul li {
  margin-bottom: 10px;
}

.sidebar ul li a {
  text-decoration: none;
  color: #333;
}

.sidebar ul li a:hover {
  color: #007BFF;
}

.profile-header {
  margin-bottom: 20px;
}

.avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}

.profile-header h3 {
  margin: 0;
  font-size: 24px;
}

.profile-header p {
  margin: 5px 0;
}
</style>