<template>
    <div class="user-card">
      <div class="user-avatar">
        <img :src="user.avatar || defaultAvatar" alt="用户头像" />
      </div>
      <div class="user-info">
        <h3>{{ user.username }}</h3>
        <p><strong>邮箱：</strong>{{ user.email }}</p>
        <p><strong>注册时间：</strong>{{ formatDate(user.registeredAt) }}</p>
        <p v-if="user.role"><strong>角色：</strong>{{ user.role }}</p>
      </div>
      <div class="user-actions">
        <button @click.stop="viewDetails" class="view-details-btn">查看详情</button>
        <button @click.stop="deleteUser" class="delete-user-btn">删除用户</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from 'axios';
  
  export default {
    props: {
      user: {
        type: Object,
        required: true,
      },
    },
    data() {
      return {
        defaultAvatar: "https://via.placeholder.com/150", // 默认头像
      };
    },
    methods: {
      // 格式化日期
      formatDate(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString();
      },
  
      // 查看用户详情
      viewDetails() {
        this.$router.push(`/user/${this.user.id}`);
      },
  
      // 删除用户
      async deleteUser() {
        if (!confirm('确定要删除此用户吗？')) {
          return;
        }
  
        try {
          // 发送 DELETE 请求删除用户
          await axios.delete(`/api/user/${this.user.id}`);
          // 提示删除成功
          alert('用户删除成功');
          
          // 更新本地状态（如果需要）
          this.$emit('user-deleted', this.user.id); // 可选：通知父组件或其他监听者
          
          // 如果是单个组件实例且不需要与父组件交互，则可以不使用 $emit
          // 直接从列表中移除当前用户（假设有一个包含所有用户的数据源）
          // 注意：这种方法适用于单个组件实例，对于列表中的多个组件实例可能不合适
          // this.$parent.users = this.$parent.users.filter(u => u.id !== this.user.id);
        } catch (error) {
          console.error('删除用户失败:', error);
          alert('删除用户失败，请重试');
        }
      }
    }
  };
  </script>
  
  <style scoped>
  /* 样式可以根据你的设计需求调整 */
  .user-card {
    display: flex;
    align-items: center;
    padding: 16px;
    border: 1px solid #ddd;
    border-radius: 8px;
    transition: box-shadow 0.3s ease;
  }
  
  .user-avatar img {
    width: 75px;
    height: 75px;
    border-radius: 50%;
    margin-right: 16px;
  }
  
  .user-info {
    flex-grow: 1;
  }
  
  .user-actions {
    display: flex;
    gap: 8px;
    margin-top: 8px;
  }
  
  .view-details-btn,
  .delete-user-btn {
    padding: 8px 16px;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  .view-details-btn {
    background-color: #007bff;
    color: white;
  }
  
  .delete-user-btn {
    background-color: #dc3545;
    color: white;
  }
  
  /* 阻止点击按钮时触发整个卡片的点击事件 */
  .view-details-btn:hover,
  .delete-user-btn:hover {
    opacity: 0.9;
  }
  </style>