import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_BASE_URL, // Replace with your FastAPI backend URL
});

export default api;
