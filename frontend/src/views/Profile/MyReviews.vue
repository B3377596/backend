<template>
  <div>
    <ul v-if="reviews.length">
      <li v-for="review in reviews" :key="review.id" class="review-item">
        <div class="review-product">商品：{{ review.product_name }}</div>
        <div class="review-comment">评价：{{ review.comment }}</div>
        <div class="review-rating">评分：{{ review.rating }} 星</div>
        <div class="review-time">时间：{{ formatDate(review.created_at) }}</div>
      </li>
    </ul>
    <p v-else>您还没有评论。</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      reviews: [],
    };
  },
  mounted() {
    this.fetchReviews();
  },
  methods: {
    async fetchReviews() {
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.get('/api/user/reviews', {
          headers: {
            Authorization: `Bearer ${accessToken}`,
          },
        });
        this.reviews = response.data;
      } catch (error) {
        console.error('获取评价失败', error);
      }
    },
    formatDate(dateString) {
      const date = new Date(dateString);
      return `${date.getFullYear()}-${(date.getMonth() + 1).toString().padStart(2, '0')}-${date.getDate().toString().padStart(2, '0')}`;
    }
  },
};
</script>

<style scoped>
.reviews-container {
  padding: 20px;
}

.review-item {
  border: 1px solid #ddd;
  padding: 15px;
  margin-bottom: 20px;
  border-radius: 8px;
  background-color: #f9f9f9;
}

.review-item .review-product {
  font-weight: bold;
  margin-bottom: 5px;
}

.review-item .review-comment {
  margin-bottom: 5px;
  font-style: italic;
}

.review-item .review-rating {
  color: #ffcc00;
  margin-bottom: 5px;
}

.review-item .review-time {
  font-size: 0.9em;
  color: #888;
}
</style>