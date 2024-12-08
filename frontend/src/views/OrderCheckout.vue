<template>
  <div class="checkout-container">
    <h2 class="checkout-title">购买商品</h2>
    
    <div class="product-info">
      <h3 class="product-name">{{ product.name }}</h3>

      <div class="product-images">
        <img
          v-for="(image, index) in product.images"
          :key="index"
          :src="image"
          alt="Product Image"
          class="product-image"
        />
      </div>

      <p class="product-description"><strong>商品描述：</strong>{{ product.description }}</p>
      <p class="product-category"><strong>类别：</strong>{{ product.category }}</p>
      <p class="product-price"><strong>价格：</strong>¥{{ product.price }}</p>
    </div>

    <form @submit.prevent="submitPurchase" class="purchase-form">
      <!-- 交付信息备注 -->
      <div class="form-group">
        <label for="delivery-note">交付信息备注</label>
        <textarea
          id="delivery-note"
          v-model="deliveryNote"
          placeholder="填写您的备注信息（如配送要求、收货人信息等）"
          class="form-control"
        ></textarea>
      </div>

      <div class="button-container">
        <button type="submit" class="submit-btn">提交订单</button>
        <button type="button" @click="cancelPurchase" class="cancel-btn">取消</button>
      </div>
    </form>
  </div>
</template>

<script>
import { getProductDetail } from "@/services/productService";
import { submitPurchase } from "@/services/orderService";

export default {
  data() {
    return {
      product: {},
      deliveryNote:''
    };
  },
  async created() {
    const productId = this.$route.params.productId; // 从路由参数中获取商品ID
    try {
      this.product = await getProductDetail(productId); // 获取商品详细信息
    } catch (error) {
      console.error("获取商品详情失败", error);
    }
  },
  methods: {
    async submitPurchase() {
      const orderData = {
        productId: this.product.id,
        deliveryNote:this.deliveryNote
      };
      try {
        await submitPurchase(orderData); // 提交购买请求
        alert("购买成功！");
        this.$router.push("/"); // 购买成功后跳转到首页
      } catch (error) {
        console.error("购买失败", error);
        
        alert("购买失败，请重试！");
      }
    },
    cancelPurchase() {
      this.$router.push("/"); // 用户取消购买后跳转到首页
    },
    
  },
};
</script>

<style scoped>
.checkout-container {
  background-color: #f8f8f8;
  padding: 40px;
  border-radius: 12px;
  box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
  max-width: 800px;
  margin: 40px auto;
  font-family: 'Arial', sans-serif;
  background: linear-gradient(145deg, #ffffff, #f1f1f1);
}

.checkout-title {
  text-align: center;
  font-size: 2.2rem;
  margin-bottom: 30px;
  color: #333;
}

.product-info {
  background-color: #fff;
  padding: 25px;
  border-radius: 10px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  margin-bottom: 35px;
}

.product-name {
  font-size: 1.8rem;
  font-weight: bold;
  color: #444;
  margin-bottom: 15px;
  text-align: center;
}

.product-images {
  display: flex;
  gap: 15px;
  justify-content: center;
  margin-bottom: 20px;
}

.product-image {
  max-width: 150px;
  max-height: 150px;
  object-fit: cover;
  border-radius: 8px;
  transition: transform 0.3s ease;
}

.product-image:hover {
  transform: scale(1.05);
}

.product-description,
.product-category,
.product-price {
  font-size: 1.1rem;
  margin-bottom: 10px;
  color: #555;
  line-height: 1.8;
}

.purchase-form {
  display: flex;
  flex-direction: column;
  gap: 25px;
}

.form-group {
  display: flex;
  flex-direction: column;
}

.form-group label {
  font-size: 1.1rem;
  margin-bottom: 8px;
  color: #444;
  font-weight: 500;
}

.form-control {
  padding: 12px;
  font-size: 1.1rem;
  border-radius: 8px;
  border: 1px solid #ddd;
  outline: none;
  box-sizing: border-box;
  transition: border 0.3s ease, box-shadow 0.3s ease;
  resize: vertical;
  min-height: 120px;
}

.form-control:focus {
  border-color: #4caf50;
  box-shadow: 0 0 8px rgba(76, 175, 80, 0.2);
}

.button-container {
  display: flex;
  gap: 20px;
  justify-content: space-between;
  align-items: center;
}

.submit-btn,
.cancel-btn {
  padding: 14px 30px;
  font-size: 1.2rem;
  border-radius: 30px;
  cursor: pointer;
  transition: transform 0.3s ease;
  border: none;
  font-weight: 600;
  width: 45%;
}

.submit-btn {
  background: #4caf50;
  color: white;
  box-shadow: 0 4px 12px rgba(76, 175, 80, 0.15);
}

.submit-btn:hover {
  background: #45a049;
  transform: scale(1.05);
}

.cancel-btn {
  background: #f44336;
  color: white;
  box-shadow: 0 4px 12px rgba(244, 67, 54, 0.15);
}

.cancel-btn:hover {
  background: #e53935;
  transform: scale(1.05);
}

</style>