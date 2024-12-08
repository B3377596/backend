const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true
})

module.exports = {
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',  // 后端的地址
        changeOrigin: true,  // 是否更改源
        secure: false,  // 如果后端使用https，设置为true
      },
    },
  },
};

