/**
 * Portfolio API Service
 * CRUD operations and approval workflow
 */

import api from './api'

// Development mode check
const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'

// Mock data for development
const MOCK_PORTFOLIOS = [
  {
    id: 1,
    title: 'Ilmiy maqola - Pedagogika',
    description: 'Zamonaviy pedagogika usullari haqida ilmiy maqola',
    category: 'ilmiy_maqola',
    status: 'approved',
    is_public: true,
    teacher: { id: 1, full_name: 'Test Teacher', department: 'Pedagogika' },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: 2,
    title: 'Loyiha - IT innovatsiyalar',
    description: 'Ta\'limda IT texnologiyalarni qo\'llash loyihasi',
    category: 'loyiha',
    status: 'pending',
    is_public: false,
    teacher: { id: 1, full_name: 'Test Teacher', department: 'IT' },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  },
  {
    id: 3,
    title: 'Esse - Milliy qadriyatlar',
    description: 'Milliy qadriyatlar va ta\'lim tizimi',
    category: 'esse',
    status: 'rejected',
    is_public: false,
    teacher: { id: 2, full_name: 'Another Teacher', department: 'Tarix' },
    created_at: new Date().toISOString(),
    updated_at: new Date().toISOString()
  }
]

const MOCK_STATS = {
  total: 45,
  pending: 12,
  approved: 28,
  rejected: 5,
  by_category: {
    ilmiy_maqola: 15,
    esse: 12,
    loyiha: 10,
    hisobot: 8
  },
  recent_activity: 8,
  approval_rate: 82
}

export const portfolioService = {
  /**
   * Get portfolios list
   * @param {Object} params - Query parameters
   * @param {string} params.status - Filter by status (pending, approved, rejected)
   * @param {string} params.category - Filter by category
   * @param {number} params.teacher_id - Filter by teacher ID
   * @param {string} params.search - Search query
   * @param {string} params.ordering - Order by field
   * @param {number} params.page - Page number
   * @param {number} params.page_size - Items per page
   * @returns {Promise<Object>} Portfolios list with pagination
   */
  async getPortfolios(params = {}) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { results: MOCK_PORTFOLIOS, count: MOCK_PORTFOLIOS.length }
    }
    const response = await api.get('/api/portfolios/', { params })
    return response.data
  },
  
  /**
   * Get single portfolio by ID
   * @param {number} portfolioId - Portfolio ID
   * @returns {Promise<Object>} Portfolio details with attachments, comments, history
   */
  async getPortfolio(portfolioId) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_PORTFOLIOS.find(p => p.id === portfolioId) || MOCK_PORTFOLIOS[0]
    }
    const response = await api.get(`/api/portfolios/${portfolioId}/`)
    return response.data
  },
  
  /**
   * Create new portfolio (Teachers only)
   * @param {Object} data - Portfolio data
   * @param {string} data.title - Portfolio title
   * @param {string} data.description - Portfolio description
   * @param {string} data.category - Portfolio category
   * @param {boolean} data.is_public - Is public
   * @param {Object} data.meta_data - Additional metadata
   * @returns {Promise<Object>} Created portfolio
   */
  async createPortfolio(data) {
    const response = await api.post('/api/portfolios/', data)
    return response.data
  },
  
  /**
   * Update portfolio
   * @param {number} portfolioId - Portfolio ID
   * @param {Object} data - Portfolio data to update
   * @returns {Promise<Object>} Updated portfolio
   */
  async updatePortfolio(portfolioId, data) {
    const response = await api.put(`/api/portfolios/${portfolioId}/`, data)
    return response.data
  },
  
  /**
   * Delete portfolio
   * @param {number} portfolioId - Portfolio ID
   * @returns {Promise<Object>} Delete confirmation
   */
  async deletePortfolio(portfolioId) {
    const response = await api.delete(`/api/portfolios/${portfolioId}/`)
    return response.data
  },
  
  /**
   * Approve portfolio (Admin/Super Admin only)
   * @param {number} portfolioId - Portfolio ID
   * @param {string} comment - Approval comment (optional)
   * @returns {Promise<Object>} Approval response
   */
  async approvePortfolio(portfolioId, comment = '') {
    const response = await api.post(`/api/portfolios/${portfolioId}/approve/`, { comment })
    return response.data
  },
  
  /**
   * Reject portfolio (Admin/Super Admin only)
   * @param {number} portfolioId - Portfolio ID
   * @param {string} comment - Rejection reason (required)
   * @returns {Promise<Object>} Rejection response
   */
  async rejectPortfolio(portfolioId, comment) {
    const response = await api.post(`/api/portfolios/${portfolioId}/reject/`, { comment })
    return response.data
  },
  
  /**
   * Add comment to portfolio
   * @param {number} portfolioId - Portfolio ID
   * @param {string} content - Comment content
   * @param {number} parentId - Parent comment ID for replies (optional)
   * @returns {Promise<Object>} Created comment
   */
  async addComment(portfolioId, content, parentId = null) {
    const data = { content }
    if (parentId) {
      data.parent_id = parentId
    }
    const response = await api.post(`/api/portfolios/${portfolioId}/comments/`, data)
    return response.data
  },
  
  /**
   * Get portfolio statistics
   * @returns {Promise<Object>} Statistics data
   */
  async getStats() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_STATS
    }
    const response = await api.get('/api/portfolios/stats/')
    return response.data
  },
  
  /**
   * Upload attachments to portfolio
   * @param {number} portfolioId - Portfolio ID
   * @param {File[]} files - Array of files to upload
   * @param {Function} onProgress - Progress callback (0-100)
   * @returns {Promise<Object>} Upload response
   */
  async uploadAttachments(portfolioId, files, onProgress = null) {
    const formData = new FormData()
    files.forEach(file => {
      formData.append('files', file)
    })
    
    const response = await api.post(`/api/portfolios/${portfolioId}/attachments/`, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const percentCompleted = Math.round((progressEvent.loaded * 100) / progressEvent.total)
          onProgress(percentCompleted)
        }
      }
    })
    return response.data
  },
  
  /**
   * Delete attachment
   * @param {number} portfolioId - Portfolio ID
   * @param {number} attachmentId - Attachment ID
   * @returns {Promise<Object>} Delete confirmation
   */
  async deleteAttachment(portfolioId, attachmentId) {
    const response = await api.delete(`/api/portfolios/${portfolioId}/attachments/${attachmentId}/`)
    return response.data
  },
  
  /**
   * Get portfolio history (status changes)
   * @param {number} portfolioId - Portfolio ID
   * @returns {Promise<Array>} History list
   */
  async getHistory(portfolioId) {
    const response = await api.get(`/api/portfolios/${portfolioId}/history/`)
    return response.data
  }
}

// Portfolio categories for forms
export const PORTFOLIO_CATEGORIES = [
  { value: 'teaching', label: "O'quv materiallari" },
  { value: 'research', label: "Ilmiy ishlar va nashrlar" },
  { value: 'certificates', label: "Sertifikatlar va mukofotlar" },
  { value: 'projects', label: "Loyihalar" },
  { value: 'professional', label: "Kasbiy rivojlanish" },
  { value: 'other', label: "Boshqa" }
]

// Portfolio statuses
export const PORTFOLIO_STATUSES = [
  { value: 'pending', label: "Kutilmoqda", color: 'warning' },
  { value: 'approved', label: "Tasdiqlangan", color: 'success' },
  { value: 'rejected', label: "Rad etilgan", color: 'danger' }
]

export default portfolioService
