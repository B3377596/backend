<template>
  <div class="category-list">
    <!-- 添加 "全部" 类别按钮 -->
    <button
      :key="'all'"
      :class="{ active: selectedCategoryId === null }"
      @click="selectCategory(null)"
    >
      全部
    </button>
    
    <!-- 循环显示其他类别按钮 -->
    <button
      v-for="category in categories"
      :key="category.id"
      :class="{ active: category.id === selectedCategoryId }"
      @click="selectCategory(category.id)"
    >
      {{ category.name }}
    </button>
  </div>
</template>

<script>
export default {
  data() {
    return {
      categories: [],  // 存储类别
      selectedCategoryId: null,  // 当前选中的类别ID，null 表示全部
    };
  },
  async created() {
    try {
      const response = await fetch("/api/categories");
      const data = await response.json();
      // 在 categories 数组中添加一个 "全部" 类别
      this.categories = data;
    } catch (error) {
      console.error("Failed to fetch categories:", error);
    }
  },
  methods: {
    // 选择类别，向父组件发送选中的类别ID
    selectCategory(categoryId) {
      this.selectedCategoryId = categoryId;  
      this.$emit("category-selected", categoryId);  // 发送类别ID到父组件
    },
  },
};
</script>

<style scoped>
.category-list {
  display: flex;
  gap: 1rem;
  margin-bottom: 1rem;
  flex-wrap: wrap;  /* 防止按钮溢出，允许换行 */
}

button {
  background: #f0f0f0;
  border: 1px solid #ccc;
  padding: 0.5rem 1rem;
  cursor: pointer;
  border-radius: 5px;
  transition: background 0.3s ease;
}

button:hover {
  background: #e0e0e0;
}

/* 激活的按钮样式 */
button.active {
  background: #4caf50;
  color: white;
  border: 1px solid #4caf50;
}

</style>