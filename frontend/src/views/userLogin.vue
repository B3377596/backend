<template>
  <div class="login-container">
    <h2>用户登录</h2>

    <form @submit.prevent="submitForm">
      <!-- 用户名/邮箱 -->
      <div class="form-group">
        <label for="username">用户名/邮箱：</label>
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="请输入用户名或邮箱"
          required
        />
      </div>

      <!-- 密码 -->
      <div class="form-group">
        <label for="password">密码：</label>
        <input
          type="password"
          id="password"
          v-model="password"
          placeholder="请输入密码"
          required
        />
      </div>

      <!-- 错误信息 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 登录按钮 -->
      <div class="form-group">
        <button type="submit">登录</button>
      </div>

      <div class="register-link">
        <p>还没有账号？<router-link to="/register">注册</router-link></p>
      </div>
    </form>
  </div>
</template>

<script>
import { login } from "@/services/authService"; // 我们将在服务中定义登录函数

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async submitForm() {
      // 清除先前的错误信息
      this.errorMessage = "";

      // 校验输入字段
      if (!this.username || !this.password) {
        this.errorMessage = "请输入用户名和密码";
        return;
      }

      try {
        const response = await login(this.username, this.password);
        // 登录成功后处理
        console.log("登录成功", response);
        const user = response.user;
        const accessToken = response.access_token;
        const refresh_token=response.refresh_token
        // 存储在 localStorage 中
        localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refresh_token);
        localStorage.setItem('user_id',user.id);
        localStorage.setItem('user', JSON.stringify(user));
        localStorage.setItem('islog', true); 
        this.$store.dispatch('user/login', user) ;
        if(user.role=='admin'){
          this.$router.push('/admin');
        }
        else if (user.role=='user'){
          this.$router.push('/');
        }
      } catch (error) {
        console.log("登陆失败,无法获取数据")
        this.errorMessage = "登录失败，请检查用户名和密码";
      }
    },
  },
};
</script>

<style scoped>
/* 背景设计 */
body {
  background: linear-gradient(to right, #6a11cb, #2575fc); /* 漸變背景 */
  font-family: 'Arial', sans-serif;
}

/* 登录容器 */
.login-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 30px;
  border-radius: 10px;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  background-color: white;
  text-align: center;
}

/* 标题 */
h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 30px;
  font-weight: 600;
}

/* 输入框容器 */
.form-group {
  margin-bottom: 20px;
}

label {
  font-size: 14px;
  color: #555;
  margin-bottom: 8px;
  display: block;
  font-weight: 500;
}

/* 输入框样式 */
input {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
  margin-top: 5px;
  box-sizing: border-box;
  transition: all 0.3s ease;
}

/* 输入框聚焦样式 */
input:focus {
  border-color: #2575fc;
  box-shadow: 0 0 5px rgba(37, 117, 252, 0.5);
  outline: none;
}

/* 按钮样式 */
button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background-color: #2575fc;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

button:hover {
  background-color: #1d61d6;
  transform: translateY(-2px);
}

/* 错误提示信息 */
.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

/* 注册链接 */
.register-link {
  margin-top: 20px;
}

.register-link a {
  color: #2575fc;
  font-size: 14px;
  text-decoration: none;
  font-weight: 500;
}

.register-link a:hover {
  text-decoration: underline;
}

</style>
