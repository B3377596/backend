// src/services/authService.js

export async function login(username, password) {
    try {
      const response = await fetch('/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });
  
      if (!response.ok) {
        throw new Error('登录失败');
      }
      const data = await response.json();
      return data; 
    } catch (error) {
      console.error('Error during login:', error);
      throw error;
    }
  }
  


// src/services/authService.js

export async function register(username, email, password) {
    try {
      const response = await fetch('/api/register', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, email, password }),
      });
  
      if (!response.ok) {
        throw new Error('注册失败');
      }
  
      const data = await response.json();
      return data; // 返回用户信息（假设后端返回注册成功的信息）
    } catch (error) {
      console.error('Error during register:', error);
      throw error;
    }
  }
  