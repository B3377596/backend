export default {
    state: {
      bought: [],
      sold: [],
    },
    mutations: {
      SET_BOUGHT_ORDERS(state, orders) {
        state.bought = orders;
      },
      SET_SOLD_ORDERS(state, orders) {
        state.sold = orders;
      },
    },
    actions: {
      async fetchBoughtOrders({ commit, state }) {
        try {
          const response = await fetch(`/api/user/bought-orders/${state.user.id}`);
          const data = await response.json();
          commit('SET_BOUGHT_ORDERS', data);
        } catch (error) {
          console.error('获取已购买订单失败', error);
        }
      },
      async fetchSoldOrders({ commit, state }) {
        try {
          const response = await fetch(`/api/user/sold-orders/${state.user.id}`);
          const data = await response.json();
          commit('SET_SOLD_ORDERS', data);
        } catch (error) {
          console.error('获取已售出订单失败', error);
        }
      },
    },
    getters: {
      boughtOrders: (state) => state.bought,
      soldOrders: (state) => state.sold,
    },
  };
  