import axios from "axios";
import { signIn } from "next-auth/react";

export const snippetApi = axios.create({
    baseURL: "http://localhost:8000",
});

export const savesApi = axios.create({
    baseURL: "http://localhost:8001"
})

snippetApi.interceptors.response.use(
    (response) => {
        return response;
    },
    async (error) => {
        if (error.response && error.response.status === 401) {
            if (typeof window !== "undefined") {
                signIn("keycloak", { callbackUrl: window.location.href });
            }
        }

        return Promise.reject(error);
    }
);

export const setBearerAuthToken = (token: string | null) => {
    if (token === null) {
        delete snippetApi.defaults.headers.common["Authorization"]
        delete savesApi.defaults.headers.common["Authorization"]
        return
    }
    snippetApi.defaults.headers.common["Authorization"] = `Bearer ${token}`;
    savesApi.defaults.headers.common["Authorization"] = `Bearer ${token}`;
};
