// http.js
import axios from 'axios';

const instance = axios.create({
  baseURL: 'http://localhost:5000', // 配置基本URL，根据实际情况修改
  timeout: 5000, // 设置请求超时时间
});

// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    // 在这里可以处理一些请求前的逻辑，例如添加认证信息等
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// 响应拦截器
instance.interceptors.response.use(
  (response) => {
    // 在这里可以处理一些响应数据前的逻辑，例如格式化数据等
    return response.data;
  },
  (error) => {
    // 在这里可以处理一些响应错误的逻辑，例如弹出错误信息等
    return Promise.reject(error);
  }
);

export const get = (url, params) => {
  return instance.get(url, { params });
};

export const post = (url, data) => {
  return instance.post(url, data);
};

// 根据需要，可以继续添加其他 HTTP 方法，例如 put、delete 等
