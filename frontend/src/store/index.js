import { createStore } from 'vuex';
import user from './user';
import products from './products';
import orders from './orders';

export default createStore({
  modules: {
    user,
    products,
    orders,
  },
});
