/**
 * User Store - Pinia
 * Manages authentication state and user data
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService, userService } from '@/services'
import { useToast } from 'vue-toastification'

// Development mode mock user 
// Set VITE_DEV_MODE=true in .env to enable mock mode
// Or set it here directly for quick testing
const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true' || false
const MOCK_USER = {
  id: 1,
  username: 'test_superadmin',
  email: 'admin@example.com',
  first_name: 'Super',
  last_name: 'Admin',
  full_name: 'Super Admin',
  role: 'superadmin', // superadmin has access to ALL pages
  hemis_id: '12345',
  department: 'IT Bo\'limi',
  position: 'Tizim administratori',
  permissions: {
    can_manage_users: true,
    can_approve_portfolios: true,
    can_manage_all_portfolios: true
  }
}

export const useUserStore = defineStore('user', () => {
  const toast = useToast()
  
  // State
  const user = ref(null)
  const isAuthenticated = ref(false)
  const isLoading = ref(false)
  const users = ref([])
  const usersCount = ref(0)
  
  // Getters
  const role = computed(() => user.value?.role || null)
  const isSuperAdmin = computed(() => role.value === 'superadmin')
  const isAdmin = computed(() => role.value === 'admin')
  const isTeacher = computed(() => role.value === 'teacher')
  const isAdminOrSuperAdmin = computed(() => isSuperAdmin.value || isAdmin.value)
  const fullName = computed(() => user.value?.full_name || user.value?.username || '')
  const permissions = computed(() => user.value?.permissions || {})
  
  // Actions
  
  /**
   * Check authentication status and fetch user data
   */
  async function checkAuth() {
    // Dev mode - use mock user
    if (DEV_MODE) {
      user.value = MOCK_USER
      isAuthenticated.value = true
      return true
    }
    
    isLoading.value = true
    try {
      const status = await authService.checkStatus()
      isAuthenticated.value = status.authenticated
      
      if (status.authenticated && status.user) {
        user.value = status.user
      } else {
        user.value = null
      }
      
      return status.authenticated
    } catch (error) {
      isAuthenticated.value = false
      user.value = null
      return false
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Fetch current user details
   */
  async function fetchCurrentUser() {
    isLoading.value = true
    try {
      const data = await authService.getCurrentUser()
      user.value = data
      isAuthenticated.value = true
      return data
    } catch (error) {
      console.error('Failed to fetch user:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Update user profile
   */
  async function updateProfile(data) {
    try {
      const response = await authService.updateProfile(data)
      // Update local user data
      if (response.user) {
        user.value = { ...user.value, ...response.user }
      }
      toast.success("Profil muvaffaqiyatli yangilandi")
      return response
    } catch (error) {
      console.error('Failed to update profile:', error)
      throw error
    }
  }
  
  /**
   * Login via Hemis OAuth
   */
  function login(next = '/dashboard') {
    authService.login(next)
  }
  
  /**
   * Logout user
   */
  async function logout() {
    try {
      await authService.logout()
      user.value = null
      isAuthenticated.value = false
      toast.success("Tizimdan muvaffaqiyatli chiqdingiz")
    } catch (error) {
      console.error('Logout failed:', error)
      // Clear local state anyway
      user.value = null
      isAuthenticated.value = false
    }
  }
  
  // ========== User Management (Super Admin) ==========
  
  /**
   * Fetch all users (Super Admin only)
   */
  async function fetchUsers(params = {}) {
    isLoading.value = true
    try {
      const data = await userService.getUsers(params)
      users.value = data.users
      usersCount.value = data.count
      return data
    } catch (error) {
      console.error('Failed to fetch users:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Create new user (Super Admin only)
   */
  async function createUser(userData) {
    try {
      const response = await userService.createUser(userData)
      toast.success("Foydalanuvchi muvaffaqiyatli yaratildi")
      // Refresh users list
      await fetchUsers()
      return response
    } catch (error) {
      console.error('Failed to create user:', error)
      throw error
    }
  }
  
  /**
   * Update user (Super Admin only)
   */
  async function updateUser(userId, userData) {
    try {
      const response = await userService.updateUser(userId, userData)
      toast.success("Foydalanuvchi muvaffaqiyatli yangilandi")
      // Update local list
      const index = users.value.findIndex(u => u.id === userId)
      if (index !== -1) {
        users.value[index] = { ...users.value[index], ...userData }
      }
      return response
    } catch (error) {
      console.error('Failed to update user:', error)
      throw error
    }
  }
  
  /**
   * Delete user (Super Admin only)
   */
  async function deleteUser(userId) {
    try {
      await userService.deleteUser(userId)
      toast.success("Foydalanuvchi muvaffaqiyatli o'chirildi")
      // Remove from local list
      users.value = users.value.filter(u => u.id !== userId)
      usersCount.value--
    } catch (error) {
      console.error('Failed to delete user:', error)
      throw error
    }
  }
  
  /**
   * Fetch single user by ID (Super Admin only)
   */
  async function fetchUserById(userId) {
    try {
      const data = await userService.getUser(userId)
      return data
    } catch (error) {
      console.error('Failed to fetch user:', error)
      throw error
    }
  }
  
  /**
   * Fetch user statistics (Super Admin only)
   */
  async function fetchUserStats() {
    try {
      const data = await userService.getUserStats()
      return data
    } catch (error) {
      console.error('Failed to fetch user stats:', error)
      throw error
    }
  }
  
  return {
    // State
    user,
    isAuthenticated,
    isLoading,
    users,
    usersCount,
    
    // Getters
    role,
    isSuperAdmin,
    isAdmin,
    isTeacher,
    isAdminOrSuperAdmin,
    fullName,
    permissions,
    
    // Actions
    checkAuth,
    fetchCurrentUser,
    updateProfile,
    login,
    logout,
    
    // User Management
    fetchUsers,
    fetchUserById,
    fetchUserStats,
    createUser,
    updateUser,
    deleteUser
  }
})
