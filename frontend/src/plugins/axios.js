import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/',  // 替换为你的后端 API 地址
  timeout: 10000,
});


api.interceptors.request.use(
    (config) => {
      // 获取存储在 localStorage 或 Vuex 中的 token
      const accessToken = localStorage.getItem('access_token');
      if (accessToken) {
        config.headers['Authorization'] = `Bearer ${accessToken}`;
      }
      return config;
    },
    (error) => {
      return Promise.reject(error);
    }
  );
  
  // 响应拦截器 - 用于处理 401 错误并刷新 token
  api.interceptors.response.use(
    (response) => response,
    async (error) => {
      if (error.response && error.response.status === 401) {
        // 如果是 401 Unauthorized 错误，说明 token 过期
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          try {
            // 刷新 token
            const { data } = await api.post('api/token/refresh/', { refresh: refreshToken });
            const newAccessToken = data.access;
  
            // 保存新的 access token
            localStorage.setItem('access_token', newAccessToken);
  
            // 重试原请求
            error.config.headers['Authorization'] = `Bearer ${newAccessToken}`;
            return api(error.config);
          } catch (refreshError) {
            console.error('Token refresh failed', refreshError);
            // 处理刷新失败，例如跳转到登录页面
          }
        } else {
          console.error('No refresh token available');
        }
      }
  
      return Promise.reject(error);
    }
  );

  export default api;