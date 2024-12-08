<template>
  <div class="product-card" @click="goToProductDetail">
    <h3>{{ product.name }}</h3>
    <p>{{ product.description }}</p>
    <p>价格: ￥{{ product.price }}</p>
  </div>
</template>

<script>
export default {
  props: {
    product: Object,
  },
  methods: {
    goToProductDetail() {
      this.$router.push(`/product/${this.product.id}`);
    },
  },
};
</script>

<style scoped>
.product-card {
  border: 1px solid #ccc;
  padding: 1rem;
  cursor: pointer;
}
.product-card:hover {
  background: #f9f9f9;
}
</style>
