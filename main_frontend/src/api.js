import axios from "axios"
import { ACCESS_TOKEN } from "./constants"

const apiURL = "https://1861532d-e0b4-4bf5-ac48-8d07fc1e3a9c-dev.e1-us-cdp-2.choreoapis.dev/filmbertbackend/backend/v1.0"

const api = axios.create({
    baseURL: import.meta.env.VITE_API_URL ? import.meta.env.VITE_API_URL : apiUrl,
});

api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem(ACCESS_TOKEN);
        if (token) {
            config.headers.Authorization = `Bearer ${token}`
        }
        return config
    },
    (error) => {
        return Promise.reject(error)
    }
)

export default api