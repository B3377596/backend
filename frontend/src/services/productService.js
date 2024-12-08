import axios from 'axios';

export const fetchProducts = async (page = 1, searchQuery = '', categoryId = null) => {
  try {
    const response = await axios.get(`/api/searchproducts`, {
      headers: {
        'Content-Type': 'application/json'
      },
      params: {
        query: searchQuery,
        page:page,
        category: categoryId,
      },
    });
    console.log(response.status)
    return response.data;
  } catch (error) {
    console.error('Error fetching products:', error);
    return { products: [], total: 0 };
  }
};


// src/services/productService.js
export async function getProductDetail(productId) {
  try {
    const response = await fetch(`/api/products/${productId}`);
    if (!response.ok) {
      throw new Error("商品详情获取失败");
    }
    return await response.json();
  } catch (error) {
    console.error("获取商品详情失败", error);
    throw error;
  }
}
