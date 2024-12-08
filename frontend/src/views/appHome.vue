<template>
  <div class="home-page">
    <!-- Header -->
    <AppHeader />

    <!-- Main Content -->
    <main class="content">
      <!-- Page Title -->
      <div class="title-bar">
        <h1>校园二手交易平台</h1>
      </div>
    </main>

    <!-- 搜索框 -->
    <SearchBar  @search="handleSearch"/>

    <!-- 发布商品按钮 -->
    <PostProductButton @click="handlePostProductClick" />

    <!-- 商品分类列表 -->
    <CategoryList @category-selected="selectCategory" />

    
    <div>
    <!-- 商品列表 -->
      <div class="product-list">
        <div 
          v-for="product in products" 
          :key="product.id" 
          class="product-item"
        >
          <router-link :to="'/product/' + product.id" class="product-link">
            <img :src="product.imageUrl" alt="Product Image" class="product-image" />
            <div class="product-details">
              <h3 class="product-name">{{ product.name }}</h3>
              <p class="product-price">¥{{ product.price }}</p>
            </div>
          </router-link>
        </div>
      </div>
    
    <!-- 分页 -->
      <div class="pagination">
        <button @click="changePage(page - 1)" :disabled="page <= 1">上一页</button>
        <span>页数: {{ page }} / {{ totalPages }}</span>
        <button @click="changePage(page + 1)" :disabled="page >= totalPages">下一页</button>
      </div>
    </div>
    

    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue";
import AppFooter from "@/components/AppFooter.vue";
import SearchBar from "@/components/SearchBar.vue";
import CategoryList from "@/components/CategoryList.vue";
import PostProductButton from "@/components/PostProductButton.vue";
import axios from 'axios';
import { fetchProducts } from '@/services/productService';

export default {
  name: "appHome",
  components: {
    AppHeader,
    AppFooter,
    SearchBar,
    CategoryList,
    PostProductButton
  },
  data() {
    return {
      products: [],
      categories: [],            // 商品分类
      searchQuery: "",           // 搜索关键词
      selectedCategory: null ,    // 当前选中的商品分类
      page:1,
      total:0
    };
  },
  async created() {
    // 获取商品分类和产品
    this.fetchProducts();
    const isLoggedIn = localStorage.getItem('islog') === 'true'; 
    const userInfo = localStorage.getItem('user');
    if (isLoggedIn && userInfo) {
      const user = JSON.parse(userInfo);
      this.$store.dispatch('user/login', user);
    } 
  },
  methods: {
    async fetchProducts(){
      try{
        const data=await fetchProducts();
        this.products = data.products;
        this.total = data.total;
      }catch(error){
        console.error("获取商品失败");
      }
    },

    async loadProducts() {
      try {
        const response = await axios.get("/api/searchproducts", {
          headers: {
            'Content-Type': 'application/json'
          },
          params: {
            query: this.searchQuery,
            category: this.selectedCategory,
            page: this.page,
          },
        });
        this.products = response.data.products;
        this.total = response.data.total;
      } catch (error) {
        console.error("Error loading products:", error);
        this.products = [];
      }
    },

    handleSearch(query) {
      this.searchQuery = query;
      this.page = 1;
      this.loadProducts(); 
    },

    selectCategory(categoryId) {
      this.selectedCategory = categoryId;
      this.page = 1;
      this.loadProducts();
    },

    changePage(newPage) {
      if (newPage > 0 && newPage <= this.totalPages) {
        this.page = newPage;  // 更新当前页码
        this.fetchProducts(); // 刷新商品列表
      }
    },
    
    handlePostProductClick() {
      if (this.isLoggedIn) {
        // 已登录状态，跳转到发布商品页面
        this.$router.push("/post-product");
      } else {
        // 未登录状态，跳转到登录页面
        this.$router.push("/login");
      }
    },
  },
  computed: {
    isLoggedIn() {
      return this.$store.state.user.isLoggedIn ; 

    },
    username() {
      return this.$store.state.user.username; 
    },
    totalPages() {
      return Math.ceil(this.total / 10);  // 每页10个商品
    }
  },
};
</script>

<style scoped>
/* 样式可以根据需要进行自定义 */
.user-info {
  padding: 20px;
  background-color: #f8f8f8;
  border-radius: 8px;
  margin-bottom: 20px;
}

.user-info p {
  margin: 5px 0;
  font-size: 16px;
}
</style>


<style scoped>
.product-list {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  justify-content: space-between;
  margin-top: 20px;
}

.product-item {
  width: 220px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.product-item:hover {
  transform: translateY(-5px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.product-link {
  display: block;
  text-decoration: none;
  color: inherit;
}

.product-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-bottom: 1px solid #eee;
}

.product-details {
  padding: 15px;
}

.product-name {
  font-size: 1.1rem;
  font-weight: bold;
  margin-bottom: 10px;
  color: #333;
  text-overflow: ellipsis;
  white-space: nowrap;
  overflow: hidden;
}

.product-price {
  font-size: 1rem;
  color: #4caf50;
  font-weight: 600;
}
.home-page {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.title-bar {
  text-align: center;
  margin: 20px 0;
  font-size: 1.5em;
  font-weight: bold;
  color: #333;
}

.search-container {
  margin: 20px auto;
  width: 80%;
}

.category-container,
.product-container {
  margin: 20px auto;
  width: 90%;
}

.category-container {
  margin-bottom: 20px;
}

.product-container {
  display: flex;
  flex-wrap: wrap;
  justify-content: space-around;
  gap: 20px;
}

/* Footer spacing */
footer {
  margin-top: auto;
}
</style>