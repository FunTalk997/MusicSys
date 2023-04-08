import axios from "axios";

const service = axios.create({
  baseURL: "/api",
  timeout: 20000,
});

service.interceptors.request.use((config) => {
  config.headers["Content-Type"] = "application/x-www-form-urlencoded";
  return config;
});

export default service;
