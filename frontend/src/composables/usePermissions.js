import { computed } from 'vue'
import { useUserStore } from '@/stores'

/**
 * Permission check composable
 */
export function usePermissions() {
  const userStore = useUserStore()
  
  const role = computed(() => userStore.role)
  const isAuthenticated = computed(() => userStore.isAuthenticated)
  
  const isSuperAdmin = computed(() => role.value === 'superadmin')
  const isAdmin = computed(() => role.value === 'admin' || role.value === 'superadmin')
  const isTeacher = computed(() => role.value === 'teacher')
  
  /**
   * Check if user has specific role
   */
  function hasRole(requiredRole) {
    if (!requiredRole) return true
    if (Array.isArray(requiredRole)) {
      return requiredRole.includes(role.value)
    }
    return role.value === requiredRole
  }
  
  /**
   * Check if user has admin access (admin or superadmin)
   */
  function hasAdminAccess() {
    return isAdmin.value
  }
  
  /**
   * Check if user can approve portfolios
   */
  function canApprove() {
    return isAdmin.value
  }
  
  /**
   * Check if user can manage users
   */
  function canManageUsers() {
    return isSuperAdmin.value
  }
  
  /**
   * Check if user can view reports
   */
  function canViewReports() {
    return isSuperAdmin.value
  }
  
  /**
   * Check if user owns a portfolio
   */
  function ownsPortfolio(portfolio) {
    if (!portfolio || !userStore.user) return false
    return portfolio.teacher?.id === userStore.user.id || portfolio.teacher === userStore.user.id
  }
  
  /**
   * Check if user can edit a portfolio
   */
  function canEditPortfolio(portfolio) {
    if (isSuperAdmin.value) return true
    if (isTeacher.value && ownsPortfolio(portfolio)) {
      // Teachers can only edit pending or rejected portfolios
      return ['pending', 'rejected'].includes(portfolio.status)
    }
    return false
  }
  
  /**
   * Check if user can delete a portfolio
   */
  function canDeletePortfolio(portfolio) {
    if (isSuperAdmin.value) return true
    if (isTeacher.value && ownsPortfolio(portfolio)) {
      // Teachers can only delete their own pending portfolios
      return portfolio.status === 'pending'
    }
    return false
  }
  
  return {
    role,
    isAuthenticated,
    isSuperAdmin,
    isAdmin,
    isTeacher,
    hasRole,
    hasAdminAccess,
    canApprove,
    canManageUsers,
    canViewReports,
    ownsPortfolio,
    canEditPortfolio,
    canDeletePortfolio
  }
}
