<template>
  <div>
    <h2>我的已购买订单</h2>
    <ul v-if="orders.length">
      <li v-for="order in orders" :key="order.id" class="order-item">
        <div class="order-info">
          <span class="order-product-name">商品名称：{{ order.productname }}</span>
          <span class="order-status">订单状态：{{ order.status }}</span>
        </div>

        <!-- 查看订单详情按钮 -->
        <button @click="goToOrderDetail(order.id)" class="view-order-detail-button">
          查看详情
        </button>
      </li>
    </ul>
    <p v-else>没有已购买订单</p>
  </div>
</template>

<script>
import axios from 'axios';
import { mapState } from 'vuex';

export default {
  data() {
    return {
      orders: [],
    };
  },
  
  computed: {
    ...mapState({
      userId: state => state.user.id,  // 获取用户ID，假设通过 Vuex 管理用户信息
    }),
  },
  mounted() {
    this.fetchOrders();
  },
  methods: {
    async fetchOrders() {
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.get(`/api/user/bought-orders`, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.orders = response.data;
      } catch (error) {
        console.error('获取已购买订单失败', error);
      }
    },
    goToOrderDetail(orderId) {
      if (orderId) { 
        this.$router.push({ name: 'orderDetail', params: { orderId } });
      } else {
        console.error("orderId is missing");
      }
    },
  },
};
</script>

<style scoped>
/* 订单页面样式 */
.order-item {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 8px;
  background-color: #f9f9f9;
  display: flex;
  flex-direction: column;
}

.order-info {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.order-product-name {
  font-size: 16px;
  font-weight: bold;
  color: #333;
}

.order-status {
  font-size: 14px;
  color: #FF6347; /* 状态的颜色 */
}

.view-order-detail-button {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  border-radius: 4px;
  align-self: flex-start; /* 按钮左对齐 */
}

.view-order-detail-button:hover {
  background-color: #45a049;
}

/* 如果没有订单 */
p {
  font-size: 16px;
  color: #888;
}
</style>