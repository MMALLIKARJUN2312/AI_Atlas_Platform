import axios from "axios";
import toast from "react-hot-toast";

import { clearStoredToken, getStoredToken } from "@/lib/auth-storage";

export const apiClient = axios.create({
  baseURL:
    process.env.NEXT_PUBLIC_API_URL ?? "https://ai-atlas-platform-lf0b.onrender.com/api/v1",
  headers: {
    "Content-Type": "application/json",
  },
});

apiClient.interceptors.request.use((config) => {
  const token = getStoredToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (axios.isAxiosError(error) && (error.response?.status === 401 || error.response?.status === 403)) {
      clearStoredToken();
      toast.error("Session expired. Please log in again.");
    }
    return Promise.reject(error);
  }
);