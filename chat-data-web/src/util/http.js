// http.js
import axios from 'axios';

export const BASE_URL = 'https://bluevision.aib.lol/api/v1';
// export const BASE_URL = 'http://139.185.43.100:5000/api/v1';

const instance = axios.create({
  baseURL: BASE_URL, // 配置基本URL，根据实际情况修改
  timeout: 600000, // 设置请求超时时间
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
