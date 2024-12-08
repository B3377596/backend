<template>
  <div class="product-detail-container">
    <div>
    <div v-if="product" class="product-info-container">
      <div class="product-info">
        <h2 class="product-title">{{ product.name }}</h2>
        <p class="product-description">
          <strong>商品描述：</strong>{{ product.description }}
        </p>
        <p class="product-category">
          <strong>类别：</strong>{{ product.category }}
        </p>
        <p class="product-price">
          <strong>价格：</strong>¥{{ product.price }}
        </p>
      </div>
    </div>
    <div v-else class="loading-message">
      <p>加载商品信息...</p>
    </div>
  </div>
    <button 
      type="button" 
      @click="toggleFavorite" 
      class="favorite-button"
      :class="{ 'favorited': isFavorite }">
      {{ isFavorite ? '取消收藏' : '收藏商品' }}
    </button>
    

    <!-- 购买按钮 v-if="!isSeller" <p v-else>你不能购买自己发布的商品</p>-->
    <button type="button" @click="handlePurchase" class="purchase-button">立即购买</button>
    
    <!-- 购买表单弹出框 -->
    <div v-if="showPurchaseForm" class="purchase-form-overlay">
      <div class="purchase-form-container">
        <h3>购买商品</h3>
        <form @submit.prevent="submitPurchase">
          <button type="button" @click="goToCheckout">提交订单</button>
          <button type="button" @click="closePurchaseForm">取消</button>
        </form>
      </div>
    </div>
  </div>
</template>




<script>
import { getProductDetail } from '@/services/productService';
import axios from 'axios';

export default {
  data() {
    return {
      product: {},
      showPurchaseForm:false,
      isFavorite:false,
      isSeller: false,  
    };
  },
  async created() {
    const productId = this.$route.params.id; // 获取路由参数中的产品ID
      if (productId) {
        this.fetchProductDetail(productId); // 调用 fetchProductDetail 方法来获取商品信息
      }
      this.checkFavorite();
      
  },

  computed: {
      isLoggedIn() {
        return this.$store.state.user.isLoggedIn; // 检查是否登录
      },
      user() {
        return this.$store.getters.user;
      }
  },

  methods: {
    toggleFavorite() {
      this.isFavorite = !this.isFavorite;
      // 在这里你可以调用 API 将收藏状态保存到数据库
      if (this.isFavorite) {
        this.addToFavorites();
      } else {
        this.removeFromFavorites();
      }
    },
    async addToFavorites() {
      try {
        const accessToken = localStorage.getItem('access_token');
        await axios.post('/api/addfavorites', { productId: this.product.id }, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });
        console.log("商品已添加到收藏夹");
        this.isFavorite = true;
      } catch (error) {
        console.error("添加到收藏夹失败", error);
      }
    },
    async removeFromFavorites() {
      try {
        const accessToken = localStorage.getItem('access_token');
        await axios.post('/api/removefavorites', { productId: this.product.id }, {
          headers: {
            'Authorization': `Bearer ${accessToken}`,
          },
        });
        console.log("商品已从收藏夹移除");
        this.isFavorite = false;
      } catch (error) {
        console.error("从收藏夹移除失败", error);
      }
    },
    async checkFavorite() {
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.post('/api/checkfavorites', { productId: this.$route.params.id},{
            headers: {
              'Authorization': `Bearer ${accessToken}`,
            }
        });
        this.isFavorite = response.data.isFavorite; 
        console.log(response.data);  // 显示收藏状态
      } catch (error) {
        console.error('检查收藏失败', error.response);
      }
    },
    async fetchProductDetail(id) {
      try {
        const data = await getProductDetail(id);
        this.product = data; 
        const currentUserId = Number(localStorage.getItem('user_id'));
        if (this.product.owner === currentUserId) {
          this.isSeller = true;  
        }
      } catch (error) {
        console.error('获取商品详情失败:', error);
      }
    },

    goToCheckout() {
      // 跳转到结算页面，传递商品ID作为路由参数
      
        if (this.product && this.product.id) {
          this.$router.push(`/checkout/${this.product.id}`);
        }else {
          console.error("Product is not loaded properly");
        }
    },

    closePurchaseForm() {
    this.showPurchaseForm = false;  // 关闭弹出框
    },

    handlePurchase() {
      if (this.isLoggedIn) {    

        this.showPurchaseForm = true;
      }
      else{
        this.$router.push('/login')
      }
    },
   
  },
};
</script>

<style scoped>
.product-info-container {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 20px auto;
}

/* 商品标题样式 */
.product-title {
  font-size: 1.8rem;
  font-weight: bold;
  color: #333;
  margin-bottom: 15px;
}

/* 商品描述样式 */
.product-description,
.product-category,
.product-price {
  font-size: 1rem;
  margin-bottom: 10px;
  color: #555;
  line-height: 1.6;
}

.favorite-button {
  background-color: #ff6f61;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  margin-top: 10px;
}

.favorite-button.favorited {
  background-color: #5cb85c;
}
/* 强调内容 */
.product-description strong,
.product-category strong,
.product-price strong {
  color: #333;
}

/* 商品价格样式 */
.product-price {
  font-size: 1.2rem;
  font-weight: bold;
  color: #4caf50;
}

/* 加载信息样式 */
.loading-message {
  text-align: center;
  font-size: 1.2rem;
  color: #888;
  padding: 20px;
}

/* 全局容器居中显示 */
div {
  text-align: left;
}

.product-detail-container {
  display: flex;
  flex-direction: column;
  padding: 20px;
}

.product-info, .seller-info {
  margin-bottom: 20px;
}

.product-images {
  display: flex;
  gap: 10px;
}

.product-image {
  width: 100%;
  max-width: 300px;
  height: auto;
}

.seller-avatar {
  width: 50px;
  height: 50px;
  border-radius: 50%;
}

.seller-info {
  display: flex;
  align-items: center;
}

.seller-info img {
  margin-right: 10px;
}

.purchase-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  font-size: 16px;
  margin-top: 20px;
}

.purchase-button:hover {
  background-color: #45a049;
}

.purchase-form-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.purchase-form-container {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 300px;
  text-align: center;
}

.purchase-form-container form {
  display: flex;
  flex-direction: column;
}

.purchase-form-container input {
  margin-bottom: 10px;
  padding: 5px;
  font-size: 16px;
}

.purchase-form-container button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
  font-size: 16px;
  margin-bottom: 10px;
}

.purchase-form-container button:hover {
  background-color: #45a049;
}

</style>
