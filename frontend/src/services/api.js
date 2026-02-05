/**
 * Axios HTTP Client Configuration
 * Session-based authentication with cookies
 */

import axios from 'axios'
import { useToast } from 'vue-toastification'
import router from '@/router'

// Development mode check
const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'

// Create axios instance
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 30000,
  withCredentials: true, // Important: Send cookies with every request
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
})

// CSRF token storage
let csrfToken = null

/**
 * Get CSRF token from backend
 */
export async function fetchCSRFToken() {
  // DEV_MODE da mock token qaytarish
  if (DEV_MODE) {
    csrfToken = 'mock-csrf-token'
    return csrfToken
  }
  try {
    const response = await api.get('/auth/csrf/')
    csrfToken = response.data.csrfToken
    return csrfToken
  } catch (error) {
    console.error('Failed to fetch CSRF token:', error)
    throw error
  }
}

/**
 * Request interceptor
 * - Add CSRF token to mutating requests
 * - Log requests in development
 */
api.interceptors.request.use(
  async (config) => {
    // DEV_MODE da API chaqiruvlarini bloklash
    if (DEV_MODE) {
      // DEV_MODE da haqiqiy API chaqiruvlarni to'xtatish
      // Bu yerda abort qilamiz, servislar mock data qaytaradi
      const controller = new AbortController()
      config.signal = controller.signal
      controller.abort('DEV_MODE: API calls blocked')
      return config
    }
    
    // Add CSRF token to mutating requests (POST, PUT, DELETE, PATCH)
    const mutatingMethods = ['post', 'put', 'delete', 'patch']
    if (mutatingMethods.includes(config.method?.toLowerCase())) {
      // Fetch CSRF token if not available
      if (!csrfToken) {
        try {
          await fetchCSRFToken()
        } catch (error) {
          console.error('Could not fetch CSRF token')
        }
      }
      
      if (csrfToken) {
        config.headers['X-CSRFToken'] = csrfToken
      }
    }
    
    // Log requests in development
    if (import.meta.env.DEV) {
      console.log(`🚀 [${config.method?.toUpperCase()}] ${config.url}`, config.data || '')
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

/**
 * Response interceptor
 * - Handle common errors
 * - Show toast notifications
 * - Redirect on 401/403
 */
api.interceptors.response.use(
  (response) => {
    // Log responses in development
    if (import.meta.env.DEV) {
      console.log(`✅ [${response.config.method?.toUpperCase()}] ${response.config.url}`, response.data)
    }
    return response
  },
  (error) => {
    // DEV_MODE da xatoliklarni e'tiborsiz qoldirish
    if (DEV_MODE) {
      console.log('DEV_MODE: API error ignored', error.message)
      return Promise.reject(error)
    }
    
    const toast = useToast()
    const status = error.response?.status
    const message = error.response?.data?.error || error.response?.data?.message || error.message
    
    // Log errors
    console.error(`❌ API Error [${status}]:`, message)
    
    switch (status) {
      case 401:
        // Unauthorized - redirect to login
        toast.error("Siz tizimga kirmagansiz. Iltimos, qaytadan kiring.")
        router.push('/login')
        break
      
      case 403:
        // Forbidden - no permission
        toast.error("Sizda bu amalni bajarish uchun ruxsat yo'q.")
        router.push('/403')
        break
      
      case 404:
        toast.error("So'ralgan ma'lumot topilmadi.")
        break
      
      case 422:
        // Validation error
        toast.error(message || "Ma'lumotlar noto'g'ri kiritilgan.")
        break
      
      case 500:
        toast.error("Server xatosi yuz berdi. Iltimos, qaytadan urinib ko'ring.")
        break
      
      default:
        if (!navigator.onLine) {
          toast.error("Internet aloqasi yo'q. Iltimos, tarmoqni tekshiring.")
        } else {
          toast.error(message || "Xatolik yuz berdi.")
        }
    }
    
    return Promise.reject(error)
  }
)

export default api
