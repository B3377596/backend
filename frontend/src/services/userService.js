import api from './api';

export const login = credentials => api.post('/auth/login', credentials);
export const fetchUserById = id => api.get(`/users/${id}`);


  // src/services/userService.js
  export async function getSellerProfile(sellerId) {
    try {
      const response = await fetch(`/api/users/${sellerId}`);
      if (!response.ok) {
        throw new Error("卖家信息获取失败");
      }
      return await response.json();
    } catch (error) {
      console.error("获取卖家信息失败", error);
      throw error;
    }
  }
  