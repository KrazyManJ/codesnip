import axios from "axios";
import { signOut } from "next-auth/react";

export const codesnipApi = axios.create({
    baseURL: "http://localhost:8000"
})

codesnipApi.interceptors.response.use(
  (response) => {
    return response;
  },
  async (error) => {
    if (error.response && error.response.status === 401) {
      
      await signOut({ callbackUrl: "" });
    }

    return Promise.reject(error);
  }
);

export const setBearerAuthToken = (token: string | null) => {
    codesnipApi.defaults.headers.common["Authorization"] = `Bearer ${token}`;
};