<template>
  <div class="favorites-container">
    <h2>我的收藏夹</h2>
    
    <!-- 显示收藏夹商品 -->
    <div v-if="favorites.length" class="favorites-list">
      <div 
        v-for="favorite in favorites" 
        :key="favorite.id" 
        class="favorite-item"
      >
        <div class="product-info">
          <div class="product-details">
            <div class="product-name">{{ favorite.productName }}</div>
            <div class="product-price">¥{{ favorite.productPrice }}</div>
            <div class="product-category">{{ favorite.productCategory }}</div>
            <button @click="goToProductDetail(favorite.productId)" class="view-detail-button">查看详情</button>
          </div>
        </div>
      </div>
    </div>
    
    <!-- 如果收藏夹为空 -->
    <p v-else class="empty-message">您的收藏夹为空</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      favorites: [],
    };
  },
  mounted() {
    this.fetchFavorites();
  },
  methods: {
    // 获取用户的收藏夹数据
    async fetchFavorites() {
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.get('/api/user/favorites', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.favorites = response.data; // 假设返回的数据中有商品信息
      } catch (error) {
        console.error('获取收藏夹失败', error);
      }
    },
    
    // 跳转到商品详情页
    goToProductDetail(productId) {
      this.$router.push(`/product/${productId}`);
    },
  },
};
</script>

<style scoped>
.favorites-container {
  margin: 20px;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 10px;
}

.favorites-list {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
}

.favorite-item {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease;
}

.favorite-item:hover {
  transform: translateY(-5px);
}

.product-info {
  display: flex;
  padding: 15px;
}

.product-image {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 5px;
  margin-right: 15px;
}

.product-details {
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.product-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 10px;
}

.product-price {
  font-size: 14px;
  color: #ff5722;
  margin-bottom: 10px;
}

.product-category {
  font-size: 12px;
  color: #777;
  margin-bottom: 15px;
}

.view-detail-button {
  background-color: #4caf50;
  color: white;
  padding: 10px 20px;
  font-size: 14px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.view-detail-button:hover {
  background-color: #45a049;
}

.empty-message {
  text-align: center;
  font-size: 16px;
  color: #777;
}
</style>
