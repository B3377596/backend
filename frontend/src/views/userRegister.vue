<template>
  <div class="register-container">
    <h2>用户注册</h2>

    <form @submit.prevent="submitForm">
      <!-- 用户名 -->
      <div class="form-group">
        <label for="username">用户名：</label>
        <input
          type="text"
          id="username"
          v-model="username"
          placeholder="请输入用户名"
          required
        />
      </div>

      <!-- 邮箱 -->
      <div class="form-group">
        <label for="email">邮箱：</label>
        <input
          type="email"
          id="email"
          v-model="email"
          placeholder="请输入邮箱"
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

      <!-- 确认密码 -->
      <div class="form-group">
        <label for="confirmPassword">确认密码：</label>
        <input
          type="password"
          id="confirmPassword"
          v-model="confirmPassword"
          placeholder="请再次输入密码"
          required
        />
      </div>

      <!-- 错误信息 -->
      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <!-- 注册按钮 -->
      <div class="form-group">
        <button type="submit">注册</button>
      </div>

      <div class="login-link">
        <p>已经有账号了？<router-link to="/login">登录</router-link></p>
      </div>
    </form>
  </div>
</template>

<script>
import { register } from "@/services/authService"; // 我们将在服务中定义注册函数

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
      errorMessage: "",
    };
  },
  methods: {
    async submitForm() {
      // 清除先前的错误信息
      this.errorMessage = "";

      // 校验输入字段
      if (!this.username || !this.email || !this.password || !this.confirmPassword) {
        this.errorMessage = "请填写所有字段";
        return;
      }

      // 检查密码是否匹配
      if (this.password !== this.confirmPassword) {
        this.errorMessage = "密码和确认密码不匹配";
        return;
      }

      try {
        const response = await register(this.username, this.email, this.password);

        // 注册成功后处理
        console.log("注册成功", response);
        this.$router.push("/login"); // 注册成功后跳转到登录页面
      } catch (error) {
        this.errorMessage = "注册失败，请重试";
      }
    },
  },
};
</script>

<style scoped>
/* 背景设计 */
body {
  background: linear-gradient(to right, #ff7e5f, #feb47b); /* 橙色到粉色渐变背景 */
  font-family: 'Arial', sans-serif;
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 注册容器 */
.register-container {
  max-width: 400px;
  margin: 100px auto;
  padding: 30px;
  border-radius: 10px;
  background-color: white;
  box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* 标题 */
h2 {
  font-size: 24px;
  color: #333;
  margin-bottom: 30px;
  font-weight: 600;
}

/* 表单组 */
.form-group {
  margin-bottom: 20px;
  text-align: left;
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
  border-color: #feb47b;
  box-shadow: 0 0 5px rgba(254, 180, 123, 0.5);
  outline: none;
}

/* 按钮样式 */
button {
  width: 100%;
  padding: 12px;
  font-size: 16px;
  background: linear-gradient(to right, #a7c5f3, #d6aaff);
  
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: all 0.3s ease;
}

/* 按钮悬停样式 */
button:hover {
  background: linear-gradient(to right,  #d6aaff,#a7c5f3, #ff7e5f);
  transform: translateY(-2px);
}

/* 错误提示信息 */
.error-message {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

/* 登录链接 */
.login-link {
  margin-top: 20px;
  font-size: 14px;
}

.login-link a {
  color: #2575fc;
  font-weight: 500;
  text-decoration: none;
}

.login-link a:hover {
  text-decoration: underline;
}

</style>
