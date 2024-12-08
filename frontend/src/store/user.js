// store/modules/user.js

const state = {
    isLoggedIn:false, 
    userInfo: JSON.parse(localStorage.getItem('user')) || null,  
};
  
const mutations = {
    SET_LOGIN_STATUS(state, status) {
      state.isLoggedIn = status;
    },
    SET_USER_INFO(state, info) {
      state.userInfo = info;
    },
};
  
const actions = {
    login({ commit }, userInfo) {
      commit("SET_LOGIN_STATUS", true);
      commit("SET_USER_INFO", userInfo);
    },
    
    logout({ commit }) {
      
      commit("SET_LOGIN_STATUS", false);
      commit("SET_USER_INFO", null);
    },

};

  
export default {
    namespaced: true,
    state,
    mutations,
    actions,
};
  

