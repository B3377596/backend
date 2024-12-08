<template>
  <div class="user-page-container">
    <div class="user-info">
      <img :src="seller.avatar" alt="Seller Avatar" class="user-avatar"/>
      <h2>{{ seller.username }}</h2>
      <p><strong>评分：</strong>{{ seller.rating }}/5</p>
    </div>

    <div class="reviews">
      <h3>评价列表</h3>
      <div v-if="seller.reviews.length">
        <h4>买家评价</h4>
        <ul>
          <li v-for="review in seller.reviews.buyers" :key="review.id">
            <p><strong>{{ review.username }}:</strong> {{ review.content }}</p>
            <p>评分: {{ review.rating }}/5</p>
          </li>
        </ul>
      </div>

      <div v-if="seller.reviews.length">
        <h4>卖家评价</h4>
        <ul>
          <li v-for="review in seller.reviews.sellers" :key="review.id">
            <p><strong>{{ review.username }}:</strong> {{ review.content }}</p>
            <p>评分: {{ review.rating }}/5</p>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
import { getSellerProfile } from "@/services/userService";

export default {
  data() {
    return {
      seller: {},
    };
  },
  async created() {
    const sellerId = this.$route.params.id; // 获取卖家ID
    try {
      this.seller = await getSellerProfile(sellerId); // 获取卖家信息
    } catch (error) {
      console.error("获取卖家信息失败", error);
    }
  },
};
</script>

<style scoped>
.user-page-container {
  padding: 20px;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.user-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  margin-right: 20px;
}

.reviews {
  margin-top: 20px;
}
</style>
