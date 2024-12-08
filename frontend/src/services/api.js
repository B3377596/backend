import axios from 'axios';

const apiClient = axios.create({
  baseURL: '/api', // 设置后端基础路径
  timeout: 10000,
});

export default apiClient;

