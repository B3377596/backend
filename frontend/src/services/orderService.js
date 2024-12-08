import api from './api';

export const fetchOrderById = id => api.get(`/orders/${id}`);
export const updateOrderStatus = (id, status) => api.put(`/orders/${id}`, { status });


// src/services/orderService.js
export async function submitPurchase(orderData) {
    try {
      const accessToken = localStorage.getItem('access_token');
      const response = await fetch('/api/createorders', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(orderData),
      });
      if (!response.ok) {
        throw new Error('购买失败');
      }
      return await response.json();
    } catch (error) {
      console.error('提交购买订单失败', error);
      throw error;
    }
  }
  