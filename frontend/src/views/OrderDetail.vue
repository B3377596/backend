<template>
  <div class="order-detail-container">
    <h2 class="order-title">订单详情</h2>
    
    <div v-if="orderDetail" class="order-info">
      <div class="order-item">
        <strong>订单号：</strong>
        <span>{{ orderDetail.order_id }}</span>
      </div>
      <div class="order-item">
        <strong>商品名称：</strong>
        <span>{{ orderDetail.product_name }}</span>
      </div>
      <div class="order-item">
        <strong>商品描述：</strong>
        <p>{{ orderDetail.product_description }}</p>
      </div>
      <div class="order-item">
        <strong>价格：</strong>
        <span>¥{{ orderDetail.product_price }}</span>
      </div>
      <div class="order-item">
        <strong>发货备注：</strong>
        <p>{{ orderDetail.shipping_requirement }}</p>
      </div>
      <div class="order-item">
        <strong>订单状态：</strong>
        <span>{{ orderDetail.order_status }}</span>
      </div>
      
      <div class="order-item">
        <strong>支付状态：</strong>
        <span>{{ orderDetail.payment_status }}</span>
      </div>
      <div class="order-item">
        <strong>货运状态：</strong>
        <span>{{ orderDetail.shipping_status }}</span>
      </div>
      <div class="order-item">
        <strong>货运信息：</strong>
        <span>{{ orderDetail.shipping_info }}</span>
      </div>
      <div class="order-item">
        <strong>下单时间：</strong>
        <span>{{ orderDetail.order_date }}</span>
      </div>
    </div>
    
    <div v-else class="loading-message">
      <p>加载订单详情失败，请稍后再试。</p>
    </div>
    
    <div class="action-buttons">
      <!-- 支付按钮 -->
      <button 
        v-if="orderDetail.order_status === '未完成' && orderDetail.buy_user_id === userid && orderDetail.payment_status=== '待支付'"
        @click="completePayment" 
        class="btn btn-pay">
        完成支付
      </button>

      <button v-if="orderDetail.order_status === '未完成' && orderDetail.sell_user_id === userid && orderDetail.shipping_status==='待发货'" 
      @click="openTransportationForm" 
      class="transportation-button">
        填写发货信息
      </button>

      <!-- 发货信息表单 -->
      <div v-if="showTransportationForm " class="transportation-form">
        <h3>填写发货信息</h3>
        <textarea v-model="shippingInfo" placeholder="请输入发货信息" rows="4" required></textarea>
        <button @click="submitTransportation">提交发货信息</button>
        <button @click="closeTransportationForm">取消</button>
      </div>

      <button v-if="orderDetail.order_status === '未完成' && orderDetail.buy_user_id === userid 
                  &&orderDetail.payment_status=== '已支付' && orderDetail.shipping_status==='已发货'" 
      @click="completeOrder" 
      class="complete-order-button">
        完成交易
      </button>
      <!-- 评价按钮 -->
      <button 
        v-if="orderDetail.order_status === '已完成' && orderDetail.buy_user_id === userid && orderDetail.review_content===null" 
        @click="openReviewModal" 
        class="btn btn-review">
        进行评价
      </button>

      <!-- 评价浮窗 -->
      <div v-if="showReviewModal " class="review-modal-overlay">
        <div class="review-modal">
          <label for="rating">评分：</label>
            <select v-model="rating" id="rating">
              <option v-for="n in 5" :key="n" :value="n">{{ n }} 星</option>
            </select>
          <h3>填写评价</h3>
          <textarea v-model="reviewContent" placeholder="请输入您的评价..." rows="4" required></textarea>
          <button @click="submitReview" class="btn btn-submit">提交</button>
          <button @click="closeReviewModal" class="btn btn-cancel">取消</button>
        </div>
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';

export default {
  data() {
    return {
      orderDetail:{},
      orderId: null, 
      userid:localStorage.getItem('user_id'), 
      showTransportationForm:false,
      showReviewModal: false, 
      rating: 5, 
      reviewContent: "",  
    };
  },
  created() {
    this.getOrderId(); 
    this.userid=Number(localStorage.getItem('user_id'));
  },
  mounted() {
    this.getOrderId();
    if (this.orderId) {
      this.fetchOrderDetail();  
    }
  },
  methods: {
    getOrderId() {
      this.orderId = this.$route.params.orderId;
      console.log('Initial orderId:', this.orderId);  
    },
    async fetchOrderDetail() {
      if (!this.orderId) {
        console.error('Order ID is undefined');
        return;
      }
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.get(`/api/orderdetail/${this.orderId}`,{
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        });
        this.orderDetail = response.data;
        
      } catch (error) {
        console.error('获取订单详情失败', error);
      }
    },
    async completePayment() {
      try {
        const accessToken = localStorage.getItem('access_token');
        const orderId = this.$route.params.orderId;
        const response = await axios.post('/api/payment', { orderId }, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json'
          }
        });

        if (response.status === 200) {
          alert('支付成功！');
          this.orderDetail.payment_status="已支付"
        } else {
          alert('支付失败，请重试！');
        }
      } catch (error) {
        console.error('支付失败', error);
        alert('支付过程中出现错误，请稍后再试！');
      }
    },

    openTransportationForm() {
      this.showTransportationForm = true;
    },

    // 关闭发货信息表单
    closeTransportationForm() {
      this.showTransportationForm = false;
    },
    openReviewModal() {
      this.showReviewModal = true;
    },

    // 关闭评价浮窗
    closeReviewModal() {
      this.showReviewModal = false;
      this.reviewContent = "";  // 清空输入框
    },
    // 提交发货信息
    async submitTransportation() {
      const orderId = this.$route.params.orderId;  // 获取订单 ID
      try {
        const response = await axios.post('/api/transportation',
          {
            order_id: orderId,
            shipping_info: this.shippingInfo, 
          },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('access_token')}`,
              'Content-Type': 'application/json',
            },
          }
        );
        if(response.ok)
          alert('发货信息提交成功');
        this.showTransportationForm = false;  
        this.fetchOrderDetail(); 
        this.orderDetail.shipping_status='已发货' 
      } catch (error) {
        console.error('提交发货信息失败', error);
        alert('提交发货信息失败，请重试');
      }
    },

    async completeOrder() {
      const orderId = this.$route.params.orderId;
      try {
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.post(`/api/completeorder`,
        { order_id: orderId },
          {
            headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
            },
          }
        );
        if (response.status===200) {
          this.orderDetail.order_status = '已完成'; // 更新订单状态
          alert('交易完成！');
        } else {
          alert('交易失败，请重试！');
        }
      } catch (error) {
        console.error('完成交易失败', error);
        alert('完成交易失败，请重试！');
      }
    },
    // 进行评价
    async submitReview() {
      try {
        // 提交评价的 API 请求
        const accessToken = localStorage.getItem('access_token');
        const response = await axios.post('/api/review', {
          order_id: this.orderDetail.order_id,
          rating: this.rating,     
          content: this.reviewContent,
          },
          {
          headers: {
              Authorization: `Bearer ${accessToken}`,
              'Content-Type': 'application/json',
            },
          }
        );
        if (response.ok) {
          this.showReviewModal = false;
          this.reviewContent = "";  
          this.rating = 5; 
          this.orderDetail.review_content=this.reviewContent
          alert('评价成功！');
        }
      } catch (error) {
        console.error('评价提交失败', error);
        alert('评价失败，请稍后再试！');
      }
        
    }
  },
};
</script>

<style scoped>

.review-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5); /* 半透明背景 */
  display: flex;
  justify-content: center;
  align-items: center;
}

.review-modal {
  background: white;
  padding: 20px;
  border-radius: 8px;
  width: 80%;
  max-width: 400px;
}

textarea {
  width: 100%;
  padding: 10px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: none;
}

button {
  padding: 10px 15px;
  margin: 5px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.btn-submit {
  background-color: #28a745;
  color: white;
}

.btn-cancel {
  background-color: #dc3545;
  color: white;
}

.btn-review {
  background-color: #007bff;
  color: white;
}
.transportation-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
}

.transportation-button:hover {
  background-color: #45a049;
}

.transportation-form {
  margin-top: 20px;
  padding: 20px;
  border: 1px solid #ddd;
  background-color: #f9f9f9;
}

.transportation-form textarea {
  width: 100%;
  padding: 8px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
  resize: vertical;
}

.transportation-form button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  cursor: pointer;
  margin-right: 10px;
}

.transportation-form button:hover {
  background-color: #45a049;
}
.order-detail-container {
  font-family: 'Arial', sans-serif;
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.order-title {
  text-align: center;
  color: #333;
  font-size: 2rem;
  margin-bottom: 20px;
}

.order-info {
  background-color: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.order-item {
  margin-bottom: 10px;
}

.order-item strong {
  color: #333;
}

.order-item p {
  color: #666;
}

.loading-message {
  text-align: center;
  color: #ff4d4d;
}

.action-buttons {
  display: flex;
  justify-content: space-around;
  margin-top: 20px;
}

.btn {
  padding: 10px 20px;
  font-size: 1rem;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn:hover {
  opacity: 0.8;
}

.btn-pay {
  background-color: #4caf50;
  color: white;
}

.btn-pay:hover {
  background-color: #45a049;
}

.btn-review {
  background-color: #ff9800;
  color: white;
}

.btn-review:hover {
  background-color: #fb8c00;
}
</style>