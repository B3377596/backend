<template>
  <header class="app-header">
    <h1 class="title">校园二手交易平台</h1>
    <div class="nav-right">
      <div v-if="isLoggedIn">
        <span>欢迎，{{ username }}</span>
        <button @click="goToProfile">个人中心</button>
      </div>
      <div v-else>
        <button @click="goToLogin">登录</button>
      </div>
    </div>
  </header>
</template>

<script>
export default {
  computed: {
    isLoggedIn() {
      return this.$store.state.user.isLoggedIn;
    },
    username() {
      return this.$store.state.user.userInfo?.username || "Guest";
    },
  },
  methods: {
    goToLogin() {
      this.$router.push("/login");
    },
    goToProfile() {
      this.$router.push("/profile");
    },
  },
};
</script>

<style scoped>

.app-header {
  display: flex;
  justify-content: space-between;
  padding: 0.2rem;
  background: #1e90ff; /* 亮蓝色 */
  color: white;
  border-bottom: 2px solid #1c86ee; /* 更深的蓝色作为底边框 */
}

.title {
  font-size: 1.5rem;
  font-weight: bold;
  margin-left: 20px;  /* 增加左边距 */
  margin-right: 20px; /* 增加右边距 */
  margin-top: 10px;   /* 增加顶部边距 */
  margin-bottom: 10px; /* 增加底部边距 */
}

.nav-right {
  display: flex;
  justify-content: flex-end; /* 将按钮靠右对齐 */
  align-items: center; /* 垂直居中 */
  padding-right: 50px; /* 增加右侧间距，避免按钮贴近右边 */
}

.nav-right button {
  background: #a7c5f3; /* 淡蓝 */
  border: none;
  padding: 0.5rem 1.2rem;
  margin-left: 1rem;
  cursor: pointer;
  color: white;
  font-size: 1rem;
  font-weight: 600;
  border-radius: 10px;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.nav-right button:hover {
  background: linear-gradient(135deg, #a7c5f3, #d6aaff); /* 悬停时反转渐变 */
  transform: translateY(-3px);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}


/* 点击时按钮收缩 */
.nav-right button:active {
  transform: translateY(0); /* 恢复原位 */
  box-shadow: none; /* 移除阴影 */
}
</style>
