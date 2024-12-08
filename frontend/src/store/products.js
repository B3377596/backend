export default {
    state: {
      products: [],
    },
    mutations: {
      SET_PRODUCTS(state, products) {
        state.products = products;
      },
    },
    actions: {
      async fetchProducts({ commit }) {
        try {
          const response = await fetch('/api/products');
          const data = await response.json();
          commit('SET_PRODUCTS', data);
        } catch (error) {
          console.error('获取商品失败', error);
        }
      },
    },
    getters: {
      products: (state) => state.products,
    },
  };
  