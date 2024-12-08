// src/services/postProductService.js

export async function submitProduct(productData) {
    const accessToken = localStorage.getItem('access_token');
    if (!accessToken) {
      console.error("没有找到有效的 access_token");
    }
    try {
      console.log('Access Token:', accessToken);
      console.log('Request Headers:', {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`
      });
      const response = await fetch('/api/createproducts', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${accessToken}`
        },
        body: JSON.stringify(productData), // 将产品数据转化为 JSON
      });
  
      if (!response.ok) {
        throw new Error('发布商品失败');
      }
  
      const data = await response.json();
      return data; // 返回后端响应的数据（可能是成功消息、商品ID等）
    } catch (error) {
      console.error('Error submitting product:', error);
      throw error; // 将错误抛出
    }
  }
  
  export async function fetchCategories() {
    try {
      const response = await fetch('/api/categories');
      if (!response.ok) {
        throw new Error('获取商品分类失败');
      }
      const data = await response.json();
      return data; // 返回商品分类数据
    } catch (error) {
      console.error('Error fetching categories:', error);
      throw error;
    }
  }
  