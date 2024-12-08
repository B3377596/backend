<template>
  <div class="product-form-container">
    <h2>发布商品</h2>
    <form @submit.prevent="submitForm" class="product-form">
      
      <!-- 商品名称 -->
      <div class="form-row">
        <label for="name" class="form-label">商品名称：</label>
        <input type="text" id="name" v-model="product.name" class="form-input" placeholder="请输入商品名称" required />
      </div>
      
      <!-- 商品价格 -->
      <div class="form-row">
        <label for="price" class="form-label">价格：</label>
        <input type="number" id="price" v-model="product.price" class="form-input" placeholder="请输入价格" required />
      </div>

      <!-- 商品分类 -->
      <div class="form-row">
        <label for="category" class="form-label">商品分类：</label>
        <select v-model="product.category" id="category" class="form-input" required>
          <option value="" disabled>请选择分类</option>
          <option v-for="category in categories" :key="category.id" :value="category.id">{{ category.name }}</option>
        </select>
      </div>

      <!-- 商品描述 -->
      <div class="form-row">
        <label for="description" class="form-label">商品描述：</label>
        <textarea id="description" v-model="product.description" class="form-input" placeholder="请输入商品描述" required></textarea>
      </div>

      <!-- 提交按钮 -->
      <div class="form-row">
        <button type="submit" class="submit-btn">发布商品</button>
      </div>
    </form>
  </div>
</template>

<script>
import { submitProduct, fetchCategories } from '@/services/postProductService';

export default {
  data() {
    return {
      product: {
        name: '',
        price: '',
        category: '',
        description: ''
      },
      categories: [] // 商品分类
    };
  },
  async created() {
    // 获取商品分类
    await this.fetchCategories();
  },
  methods: {
    // 获取商品分类
    async fetchCategories() {
      try {
        this.categories = await fetchCategories();
      } catch (error) {
        console.error('Error fetching categories:', error);
      }
    },

    // 提交商品表单
    async submitForm() {
      try {
        const productData = {
          name: this.product.name,
          price: this.product.price,
          category: this.product.category,
          description: this.product.description
        };

        const result = await submitProduct(productData);

        // 提交成功后的逻辑
        console.log('商品发布成功', result);
        this.$router.push('/'); // 发布成功后跳转到首页
      } catch (error) {
        console.error('发布商品失败', error);
        alert('发布商品失败，请稍后再试');
      }
    }
  }
};
</script>


<style scoped>
.product-form-container {
  width: 100%;
  max-width: 600px;
  margin: 0 auto;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  text-align: center;
  color: #333;
  margin-bottom: 20px;
}

.product-form {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.form-row {
  display: flex;
  flex-direction: column;
}

.form-label {
  font-weight: 600;
  margin-bottom: 8px;
  color: #555;
}

.form-input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ddd;
  border-radius: 4px;
  outline: none;
  transition: border-color 0.3s;
}

.form-input:focus {
  border-color: #4CAF50;
}

textarea.form-input {
  height: 150px;
  resize: vertical;
}

.submit-btn {
  padding: 12px 20px;
  background-color: #4CAF50;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background-color 0.3s;
  align-self: center;
}

.submit-btn:hover {
  background-color: #45a049;
}

.submit-btn:active {
  background-color: #388e3c;
}
</style>