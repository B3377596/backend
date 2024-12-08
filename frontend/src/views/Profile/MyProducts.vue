<template>
  <div>
    <h2>我的商品</h2>
    <ul v-if="products.length">
      <li v-for="product in products" :key="product.id" class="product-item">
        <div class="product-info">
          <span class="product-name">{{ product.name }}</span>
          <span class="product-price">¥{{ product.price }}</span>
        </div>
        <div class="product-description">{{ product.description }}</div>

        <!-- 跳转到商品详情页按钮 -->
        <router-link :to="`/product/${product.id}`">
          <button class="view-detail-button">查看详情</button>
        </router-link>
      </li>
    </ul>
    <p v-else>没有发布商品</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      products: [],
    };
  },
  mounted() {
    this.fetchProducts();
  },
  methods: {
    async fetchProducts() {
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.get('/api/user/products',{headers: {
          'Authorization': `Bearer ${accessToken}`,  // 将 token 添加到请求头
        }
        })

        this.products = response.data;
      } catch (error) {
        console.error('获取商品失败', error);
      }
    },
  },
};
</script>

<style scoped>
.product-item {
  border: 1px solid #ddd;
  padding: 10px;
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
}

.product-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.product-name {
  font-size: 18px;
  font-weight: bold;
}

.product-price {
  font-size: 18px;
  color: #FF6347; /* 橙红色 */
}

.product-description {
  margin-bottom: 10px;
  font-size: 14px;
  color: #666;
}

.view-detail-button {
  background-color: #4CAF50;
  color: white;
  padding: 8px 16px;
  border: none;
  cursor: pointer;
  font-size: 14px;
  border-radius: 4px;
}

.view-detail-button:hover {
  background-color: #45a049;
}
</style>