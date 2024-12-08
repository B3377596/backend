<template>
    <div class="order-card">
      <!-- 订单图片 -->
      <img :src="order.productImage" alt="订单商品图片" class="order-image" />
      <div class="order-details">
        <!-- 订单商品名称 -->
        <h3 class="order-name">{{ order.productName }}</h3>
        <!-- 订单状态 -->
        <p class="order-status">{{ order.status }}</p>
        <!-- 订单价格 -->
        <p class="order-price">￥{{ order.price.toFixed(2) }}</p>
  
        <!-- 操作按钮 -->
        <div class="order-actions">
          <button @click.stop="goToOrderDetail" class="view-detail-btn">查看详情</button>
          <button @click.stop="deleteOrder" class="delete-order-btn">删除订单</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: {
      order: Object, // 接收订单对象
    },
    methods: {
      // 点击订单卡片，跳转到订单详情页
      goToOrderDetail() {
        this.$router.push({ name: 'OrderDetail', params: { id: this.order.id } });
      },
  
      // 删除订单
      async deleteOrder() {
        try {
          // 发送 DELETE 请求删除订单
          await axios.delete(`/api/order/${this.order.id}`);
          // 提示删除成功
          alert('订单删除成功');
          
          this.$parent.orders = this.$parent.orders.filter(order => order.id !== this.order.id);
        } catch (error) {
          console.error('删除订单失败:', error);
          alert('删除订单失败，请重试');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* 样式可以根据你的设计需求调整 */
  .order-card {
    display: flex;
    align-items: center;
    padding: 16px;
    border: 1px solid #ddd;
    border-radius: 8px;
    cursor: pointer;
    transition: box-shadow 0.3s ease;
  }
  
  .order-image {
    max-width: 100px;
    margin-right: 16px;
    border-radius: 8px;
  }
  
  .order-details {
    flex-grow: 1;
  }
  
  .order-actions {
    display: flex;
    gap: 8px;
    margin-top: 8px;
  }
  
  .view-detail-btn,
  .delete-order-btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .view-detail-btn {
    background-color: #007bff;
    color: white;
  }
  
  .delete-order-btn {
    background-color: #dc3545;
    color: white;
  }
  
  /* 阻止点击按钮时触发整个卡片的点击事件 */
  .view-detail-btn:hover,
  .delete-order-btn:hover {
    opacity: 0.9;
  }
  </style>