/**
 * Portfolio Store - Pinia
 * Manages portfolios, approval workflow, and statistics
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { portfolioService } from '@/services'
import { useToast } from 'vue-toastification'

export const usePortfolioStore = defineStore('portfolio', () => {
  const toast = useToast()
  
  // State
  const portfolios = ref([])
  const currentPortfolio = ref(null)
  const pagination = ref({
    page: 1,
    page_size: 20,
    total_pages: 1,
    total_count: 0,
    has_next: false,
    has_previous: false
  })
  const stats = ref({
    total: 0,
    pending: 0,
    approved: 0,
    rejected: 0,
    by_category: {},
    recent: []
  })
  const isLoading = ref(false)
  const filters = ref({
    status: '',
    category: '',
    search: '',
    ordering: '-created_at'
  })
  
  // Getters
  const pendingPortfolios = computed(() => 
    portfolios.value.filter(p => p.status === 'pending')
  )
  
  const approvedPortfolios = computed(() => 
    portfolios.value.filter(p => p.status === 'approved')
  )
  
  const rejectedPortfolios = computed(() => 
    portfolios.value.filter(p => p.status === 'rejected')
  )
  
  const hasPortfolios = computed(() => portfolios.value.length > 0)
  
  // Actions
  
  /**
   * Fetch portfolios with optional filters
   */
  async function fetchPortfolios(params = {}) {
    isLoading.value = true
    try {
      // Merge with current filters
      const queryParams = {
        ...filters.value,
        ...params,
        page: params.page || pagination.value.page,
        page_size: params.page_size || pagination.value.page_size
      }
      
      // Remove empty values
      Object.keys(queryParams).forEach(key => {
        if (!queryParams[key]) delete queryParams[key]
      })
      
      const data = await portfolioService.getPortfolios(queryParams)
      portfolios.value = data.portfolios
      pagination.value = data.pagination
      
      return data
    } catch (error) {
      console.error('Failed to fetch portfolios:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Fetch pending portfolios (for admin approval)
   */
  async function fetchPendingPortfolios(params = {}) {
    return fetchPortfolios({ ...params, status: 'pending' })
  }
  
  /**
   * Fetch single portfolio by ID
   */
  async function fetchPortfolio(portfolioId) {
    isLoading.value = true
    try {
      const data = await portfolioService.getPortfolio(portfolioId)
      currentPortfolio.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch portfolio:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Create new portfolio
   */
  async function createPortfolio(data) {
    isLoading.value = true
    try {
      const response = await portfolioService.createPortfolio(data)
      toast.success("Portfolio muvaffaqiyatli yaratildi")
      
      // Add to local list
      await fetchPortfolios()
      
      return response
    } catch (error) {
      console.error('Failed to create portfolio:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Update portfolio
   */
  async function updatePortfolio(portfolioId, data) {
    isLoading.value = true
    try {
      const response = await portfolioService.updatePortfolio(portfolioId, data)
      toast.success("Portfolio muvaffaqiyatli yangilandi")
      
      // Update in local list
      const index = portfolios.value.findIndex(p => p.id === portfolioId)
      if (index !== -1) {
        portfolios.value[index] = { ...portfolios.value[index], ...data, ...response.portfolio }
      }
      
      // Update current if viewing
      if (currentPortfolio.value?.id === portfolioId) {
        currentPortfolio.value = { ...currentPortfolio.value, ...data }
      }
      
      return response
    } catch (error) {
      console.error('Failed to update portfolio:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Delete portfolio
   */
  async function deletePortfolio(portfolioId) {
    isLoading.value = true
    try {
      await portfolioService.deletePortfolio(portfolioId)
      toast.success("Portfolio muvaffaqiyatli o'chirildi")
      
      // Remove from local list
      portfolios.value = portfolios.value.filter(p => p.id !== portfolioId)
      pagination.value.total_count--
      
      // Clear current if deleted
      if (currentPortfolio.value?.id === portfolioId) {
        currentPortfolio.value = null
      }
    } catch (error) {
      console.error('Failed to delete portfolio:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }
  
  /**
   * Approve portfolio (Admin/Super Admin)
   */
  async function approvePortfolio(portfolioId, comment = '') {
    try {
      const response = await portfolioService.approvePortfolio(portfolioId, comment)
      toast.success("Portfolio tasdiqlandi")
      
      // Update in local list
      const index = portfolios.value.findIndex(p => p.id === portfolioId)
      if (index !== -1) {
        portfolios.value[index].status = 'approved'
      }
      
      // Update current if viewing
      if (currentPortfolio.value?.id === portfolioId) {
        currentPortfolio.value.status = 'approved'
      }
      
      return response
    } catch (error) {
      console.error('Failed to approve portfolio:', error)
      throw error
    }
  }
  
  /**
   * Reject portfolio (Admin/Super Admin)
   */
  async function rejectPortfolio(portfolioId, comment) {
    if (!comment) {
      toast.error("Rad etish uchun izoh kiritish majburiy")
      return
    }
    
    try {
      const response = await portfolioService.rejectPortfolio(portfolioId, comment)
      toast.success("Portfolio rad etildi")
      
      // Update in local list
      const index = portfolios.value.findIndex(p => p.id === portfolioId)
      if (index !== -1) {
        portfolios.value[index].status = 'rejected'
      }
      
      // Update current if viewing
      if (currentPortfolio.value?.id === portfolioId) {
        currentPortfolio.value.status = 'rejected'
      }
      
      return response
    } catch (error) {
      console.error('Failed to reject portfolio:', error)
      throw error
    }
  }
  
  /**
   * Add comment to portfolio
   */
  async function addComment(portfolioId, content, parentId = null) {
    try {
      const response = await portfolioService.addComment(portfolioId, content, parentId)
      toast.success("Izoh qo'shildi")
      
      // Add to current portfolio if viewing
      if (currentPortfolio.value?.id === portfolioId) {
        currentPortfolio.value.comments = [
          ...currentPortfolio.value.comments,
          response.comment
        ]
      }
      
      return response
    } catch (error) {
      console.error('Failed to add comment:', error)
      throw error
    }
  }
  
  /**
   * Fetch portfolio statistics
   */
  async function fetchStats() {
    try {
      const data = await portfolioService.getStats()
      stats.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch stats:', error)
      throw error
    }
  }
  
  /**
   * Update filters and refetch
   */
  async function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1 // Reset to first page
    return fetchPortfolios()
  }
  
  /**
   * Clear filters
   */
  async function clearFilters() {
    filters.value = {
      status: '',
      category: '',
      search: '',
      ordering: '-created_at'
    }
    pagination.value.page = 1
    return fetchPortfolios()
  }
  
  /**
   * Go to specific page
   */
  async function goToPage(page) {
    pagination.value.page = page
    return fetchPortfolios()
  }
  
  /**
   * Clear current portfolio
   */
  function clearCurrentPortfolio() {
    currentPortfolio.value = null
  }
  
  return {
    // State
    portfolios,
    currentPortfolio,
    pagination,
    stats,
    isLoading,
    filters,
    
    // Getters
    pendingPortfolios,
    approvedPortfolios,
    rejectedPortfolios,
    hasPortfolios,
    
    // Actions
    fetchPortfolios,
    fetchPendingPortfolios,
    fetchPortfolio,
    createPortfolio,
    updatePortfolio,
    deletePortfolio,
    approvePortfolio,
    rejectPortfolio,
    addComment,
    fetchStats,
    setFilters,
    clearFilters,
    goToPage,
    clearCurrentPortfolio
  }
})
