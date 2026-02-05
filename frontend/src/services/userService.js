/**
 * User Management API Service
 * Super Admin only - CRUD operations for users
 */

import api from './api'

// Development mode check
const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'

// Mock data for development
const MOCK_USERS = [
  { id: 1, username: 'superadmin', full_name: 'Super Admin', email: 'admin@example.com', role: 'superadmin', department: 'IT', is_active: true },
  { id: 2, username: 'admin1', full_name: 'Admin User', email: 'admin1@example.com', role: 'admin', department: 'Pedagogika', is_active: true },
  { id: 3, username: 'teacher1', full_name: 'Aliyev Vali', email: 'teacher1@example.com', role: 'teacher', department: 'Pedagogika', is_active: true },
  { id: 4, username: 'teacher2', full_name: 'Karimova Nilufar', email: 'teacher2@example.com', role: 'teacher', department: 'IT', is_active: true },
  { id: 5, username: 'teacher3', full_name: 'Rahimov Jasur', email: 'teacher3@example.com', role: 'teacher', department: 'Tarix', is_active: false }
]

const MOCK_USER_STATS = {
  total: 156,
  by_role: { superadmin: 2, admin: 10, teacher: 144 },
  active: 148,
  inactive: 8
}

export const userService = {
  /**
   * Get all users (Super Admin only)
   * @param {Object} params - Query parameters
   * @param {string} params.role - Filter by role
   * @param {string} params.search - Search query
   * @returns {Promise<Object>} Users list with count
   */
  async getUsers(params = {}) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      let users = [...MOCK_USERS]
      if (params.role) {
        users = users.filter(u => u.role === params.role)
      }
      if (params.search) {
        const search = params.search.toLowerCase()
        users = users.filter(u => 
          u.full_name.toLowerCase().includes(search) || 
          u.email.toLowerCase().includes(search)
        )
      }
      return { results: users, count: users.length }
    }
    const response = await api.get('/api/accounts/users/', { params })
    return response.data
  },
  
  /**
   * Get single user by ID
   * @param {number} userId - User ID
   * @returns {Promise<Object>} User data
   */
  async getUser(userId) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_USERS.find(u => u.id === userId) || MOCK_USERS[0]
    }
    const response = await api.get(`/api/accounts/users/${userId}/`)
    return response.data
  },
  
  /**
   * Get user statistics (Super Admin only)
   * @returns {Promise<Object>} User stats
   */
  async getUserStats() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_USER_STATS
    }
    const response = await api.get('/api/accounts/users/stats/')
    return response.data
  },
  
  /**
   * Create new user (Super Admin only)
   * @param {Object} data - User data
   * @returns {Promise<Object>} Created user
   */
  async createUser(data) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { id: Date.now(), ...data }
    }
    const response = await api.post('/api/accounts/users/', data)
    return response.data
  },
  
  /**
   * Update user (Super Admin only)
   * @param {number} userId - User ID
   * @param {Object} data - User data to update
   * @returns {Promise<Object>} Updated user
   */
  async updateUser(userId, data) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { id: userId, ...data }
    }
    const response = await api.put(`/api/accounts/users/${userId}/`, data)
    return response.data
  },
  
  /**
   * Delete user (Super Admin only)
   * @param {number} userId - User ID
   * @returns {Promise<Object>} Delete confirmation
   */
  async deleteUser(userId) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { success: true }
    }
    const response = await api.delete(`/api/accounts/users/${userId}/`)
    return response.data
  }
}

export default userService
