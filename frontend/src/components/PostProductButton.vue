<template>
  <div class="post-product-button">
    <button @click="$emit('click')" class="post-button">
      发布商品
    </button>
  </div>
</template>

<script>
export default {
  name: 'PostProductButton',
};
</script>

<style scoped>
.post-product-button {
  display: flex;
  justify-content: center;  /* 水平居中 */
  align-items: center;  /* 垂直居中 */
  margin: 20px 0;
}

.post-button {
  width: 120px; /* 设置按钮宽度 */
  height: 120px; /* 设置按钮高度 */
  background-color: #1e90ff; 
  color: white;
  border: none;
  border-radius: 50%; /* 使按钮变为圆形 */
  font-size: 24px; /* 设置文字大小 */
  display: flex;
  justify-content: center;
  align-items: center;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s ease;
}

.post-button:hover {
  background-color: #87CEEB; /* 悬停时改为稍微深一点的蓝色 */
  transform: scale(1.1); /* 鼠标悬停时按钮放大 */
}

.post-button span {
  display: block;
  transition: opacity 0.3s ease;
}

.post-button:hover span {
  opacity: 0; /* 鼠标悬停时文字消失 */
}

.post-button:hover::before {
  content: '+';
  font-size: 50px;
  color: white;
}

</style>
