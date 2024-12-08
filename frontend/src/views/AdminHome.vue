<template>
    <div class="admin-dashboard">
      <!-- 侧边栏 -->
      <aside class="sidebar">
        <ul>
          <li :class="{ active: selectedTab === 'orders' }" @click="selectTab('orders')">
            订单管理
          </li>
          <li :class="{ active: selectedTab === 'products' }" @click="selectTab('products')">
            商品管理
          </li>
          <li :class="{ active: selectedTab === 'users' }" @click="selectTab('users')">
            用户管理
          </li>
        </ul>
      </aside>
  
      <!-- 主内容 -->
      <main class="content">
        <h1>{{ getTitle }}</h1>
  
        <!-- 搜索表单 -->
        <div class="search-bar">
          <input
            v-model="searchQuery"
            :placeholder="getPlaceholder"
            @keydown.enter="search"
          />
          <button @click="search">搜索</button>
        </div>
  
        <!-- 搜索结果 -->
        <div class="search-results">
          <component
            :is="currentComponent"
            :data="currentData"
            v-if="currentData.length"
          ></component>
          <p v-else>暂无结果</p>
        </div>
      </main>
    </div>
  </template>
  
  
  <script>
  import OrderCard from "@/components/OrderCard.vue";
  import ProductCard from "@/components/ProductCard.vue";
  import UserCard from "@/components/UserCard.vue";
  
  export default {
    created(){
      window.location.href = 'http://localhost:8000/admin';
    },
    mounted() {
      window.location.href = 'http://localhost:8000/admin';
    },
    data() {
      return {
        selectedTab: "orders", // 当前选中的管理模块
        searchQuery: "", // 用户输入的搜索内容
        currentData: [], // 搜索结果数据
        components: {
          orders: OrderCard,
          products: ProductCard,
          users: UserCard,
        },
      };
    },
    computed: {
      // 动态获取页面标题
      getTitle() {
        switch (this.selectedTab) {
          case "orders":
            return "订单管理";
          case "products":
            return "商品管理";
          case "users":
            return "用户管理";
          default:
            return "管理面板";
        }
      },
      // 动态获取搜索框的占位符
      getPlaceholder() {
        switch (this.selectedTab) {
          case "orders":
            return "请输入订单编号";
          case "products":
            return "请输入商品ID或商品名称";
          case "users":
            return "请输入用户名";
          default:
            return "请输入搜索内容";
        }
      },
      // 动态获取要加载的组件
      currentComponent() {
        return this.components[this.selectedTab];
      },
    },

    methods: {
      handleUserDetails(userId) {
        console.log("查看用户详情:", userId);
        // 可以跳转到用户详情页面
        this.$router.push(`/user/${userId}`);
      },
      handleDeleteUser(userId) {
        try {
          const response = axios.delete(`/api/user/favorites/${favoriteId}`);
          if (response.status === 200) {
            this.favorites = this.favorites.filter(fav => fav.id !== favoriteId);
          }
        } catch (error) {
          console.error('移除收藏失败', error);
        }
      },
  
      handleOrderDetails(orderId) {
        console.log("查看订单详情:", orderId);
        // 可以跳转到订单详情页面
        this.$router.push(`/order/${orderId}`);
      },
      handleDeleteOrder(orderId) {
        console.log("删除订单:", orderId);
        // 调用删除订单的 API
        this.deleteOrderAPI(orderId);
      },
      handleProductDetails(productId) {
        console.log("查看商品详情:", productId);
        // 可以跳转到商品详情页面
        this.$router.push(`/product/${productId}`);
      },
      handleDeleteProduct(productId) {
        console.log("删除商品:", productId);
        // 调用删除商品的 API
        this.deleteProductAPI(productId);
      },
  
      // 切换选项卡
      selectTab(tab) {
        this.selectedTab = tab;
        this.searchQuery = ""; // 切换时清空搜索框
        this.currentData = []; // 切换时清空数据
      },
      // 搜索功能
      async search() {
        if (!this.searchQuery) {
          alert("请输入搜索内容！");
          return;
        }
  
        try {
          const endpointMap = {
            orders: "/api/orders",
            products: "/api/products",
            users: "/api/user",
          };
  
          const response = await fetch(endpointMap[this.selectedTab], {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: this.searchQuery }),
          });
  
          this.currentData = await response.data;
        } catch (error) {
          console.error("搜索失败:", error);
          this.currentData = [];
        }
      },
    },
  };
  </script>
  
  
  <style scoped>
  .admin-dashboard {
    display: flex;
    min-height: 100vh;
  }
  
  .sidebar {
    width: 200px;
    background-color: #2c3e50;
    color: white;
    padding: 1rem;
  }
  
  .sidebar ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }
  
  .sidebar li {
    padding: 10px 15px;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .sidebar li:hover {
    background-color: #34495e;
  }
  
  .sidebar li.active {
    background-color: #1abc9c;
  }
  
  .content {
    flex-grow: 1;
    padding: 2rem;
  }
  
  h1 {
    font-size: 1.5rem;
    color: #2c3e50;
    margin-bottom: 1rem;
  }
  
  .search-bar {
    display: flex;
    gap: 1rem;
    margin-bottom: 2rem;
  }
  
  .search-bar input {
    flex-grow: 1;
    padding: 0.5rem;
    font-size: 1rem;
  }
  
  .search-bar button {
    padding: 0.5rem 1rem;
    font-size: 1rem;
    background-color: #4caf50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .search-results {
    background: #f8f9fa;
    padding: 1rem;
    border-radius: 8px;
    border: 1px solid #ddd;
  }
  
  .search-results p {
    text-align: center;
    color: #888;
  }
  </style>