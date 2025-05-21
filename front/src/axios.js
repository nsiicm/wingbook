// src/axios.js
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.API_BASE_URL || 'http://localhost:8012/api/', // your Django API base URL
});

export default api;