/**
 * Authentication API Service
 * Handles Hemis OAuth 2.0 login, logout, and session management
 */

import api, { fetchCSRFToken } from './api'

// Development mode check
const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'

// Mock user for development
const MOCK_USER = {
  id: 1,
  username: 'test_superadmin',
  email: 'admin@example.com',
  first_name: 'Super',
  last_name: 'Admin',
  full_name: 'Super Admin',
  role: 'superadmin',
  hemis_id: '12345',
  department: 'IT Bo\'limi',
  position: 'Tizim administratori',
  permissions: {
    can_manage_users: true,
    can_approve_portfolios: true,
    can_manage_all_portfolios: true
  }
}

export const authService = {
  /**
   * Get CSRF token for forms
   */
  async getCSRFToken() {
    if (DEV_MODE) return 'mock-csrf-token'
    return await fetchCSRFToken()
  },
  
  /**
   * Check authentication status
   * @returns {Promise<Object>} Auth status with user data if authenticated
   */
  async checkStatus() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { authenticated: true, user: MOCK_USER }
    }
    const response = await api.get('/auth/status/')
    return response.data
  },
  
  /**
   * Get current user information
   * @returns {Promise<Object>} Current user data
   */
  async getCurrentUser() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_USER
    }
    const response = await api.get('/api/accounts/me/')
    return response.data
  },
  
  /**
   * Update current user profile
   * @param {Object} data - Profile data to update
   * @returns {Promise<Object>} Updated user data
   */
  async updateProfile(data) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { ...MOCK_USER, ...data }
    }
    const response = await api.put('/api/accounts/me/', data)
    return response.data
  },
  
  /**
   * Initiate Hemis OAuth 2.0 login
   * Redirects to Hemis authorization page
   * @param {string} next - URL to redirect after login
   */
  login(next = '/dashboard') {
    if (DEV_MODE) {
      // DEV_MODE da login sahifasiga redirect qilmaslik
      window.location.href = next
      return
    }
    const baseUrl = import.meta.env.VITE_API_BASE_URL || ''
    window.location.href = `${baseUrl}/auth/hemis/login/?next=${encodeURIComponent(next)}`
  },
  
  /**
   * Logout current user
   * @returns {Promise<Object>} Logout response
   */
  async logout() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { success: true }
    }
    const response = await api.post('/auth/hemis/logout/')
    return response.data
  }
}

export default authService
