<template>
  <div class="search-bar">
    <input
      v-model="searchQuery"
      type="text"
      placeholder="搜索商品"
      @keydown.enter="search"
    />
    <button @click="search">搜索</button>
    <button @click="resetSearch">重置搜索</button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      searchQuery: "",
    };
  },
  methods: {
    // 搜索商品
    search() {
      this.$emit("search", this.searchQuery); // 触发搜索事件，传递关键词到主页面
    },
    // 重置搜索
    resetSearch() {
      this.searchQuery = "";
      this.$emit("search", ""); // 重置搜索结果
    },
  },
};
</script>

<style scoped>
.search-bar {
  display: flex;
  gap: 0.5rem;
  margin: 1rem 0;
  justify-content: center;
  align-items: center;
}

.search-bar input {
  flex: 1;
  padding: 0.8rem 1rem;
  font-size: 1rem;
  border-radius: 25px;
  border: 2px solid #ccc;
  outline: none;
  transition: border-color 0.3s ease, box-shadow 0.3s ease;
  max-width: 600px; 
}

.search-bar input:focus {
  border-color: #4caf50;
  box-shadow: 0 0 8px rgba(76, 175, 80, 0.3);
}

.search-bar button {
  background: linear-gradient(135deg, #4e9ad1, #4caf50);
  color: white;
  border: none;
  padding: 0.8rem 1.5rem;
  cursor: pointer;
  border-radius: 25px;
  font-size: 1rem;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.search-bar button:hover {
  background: linear-gradient(135deg, #4caf50, #4e9ad1);
  transform: scale(1.05);
}

.search-bar button:focus {
  outline: none;
}
</style>
