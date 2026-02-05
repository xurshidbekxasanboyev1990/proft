/**
 * Analytics API Service
 * Dashboard, Grafiklar, Hisobotlar
 */

import api from './api'

// Development mode check
const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'

// Mock data for development
const MOCK_OVERVIEW = {
  total_users: 156,
  total_teachers: 120,
  total_portfolios: 450,
  total_assignments: 89,
  pending_portfolios: 23,
  pending_assignments: 15,
  completed_this_month: 42,
  approval_rate: 85
}

const MOCK_WIDGETS = [
  { id: 1, type: 'stat', title: 'Foydalanuvchilar', value: 156, change: 12, change_type: 'increase' },
  { id: 2, type: 'stat', title: 'Portfoliolar', value: 450, change: 8, change_type: 'increase' },
  { id: 3, type: 'stat', title: 'Topshiriqlar', value: 89, change: 5, change_type: 'increase' },
  { id: 4, type: 'stat', title: "Bajarilgan", value: 42, change: 15, change_type: 'increase' }
]

const MOCK_CHART_DATA = {
  labels: ['Yan', 'Fev', 'Mar', 'Apr', 'May', 'Iyn'],
  datasets: [
    { label: 'Portfoliolar', data: [45, 52, 48, 61, 55, 72] },
    { label: 'Topshiriqlar', data: [23, 28, 32, 29, 38, 42] }
  ]
}

const MOCK_PIE_DATA = {
  labels: ['Bajarildi', 'Jarayonda', 'Kutilmoqda', "Muddati o'tgan"],
  datasets: [{ data: [42, 28, 15, 4] }]
}

const MOCK_REPORTS = [
  { id: 1, title: 'Oylik hisobot - Yanvar 2026', type: 'monthly', format: 'excel', status: 'completed', created_at: new Date().toISOString() },
  { id: 2, title: 'Portfolio statistikasi', type: 'portfolios', format: 'pdf', status: 'completed', created_at: new Date().toISOString() }
]

export const analyticsService = {
  // =====================
  // DASHBOARD
  // =====================

  /**
   * Dashboard umumiy statistika
   * @returns {Promise<Object>} Overview ma'lumotlari
   */
  async getDashboardOverview() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_OVERVIEW
    }
    const response = await api.get('/api/analytics/dashboard/overview/')
    return response.data
  },

  /**
   * Dashboard widgetlar
   * @returns {Promise<Array>} Widgetlar ro'yxati
   */
  async getDashboardWidgets() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_WIDGETS
    }
    const response = await api.get('/api/analytics/dashboard/widgets/')
    return response.data
  },

  // =====================
  // CHARTS
  // =====================

  /**
   * Portfolio trend grafigi
   * @param {string} period - week|month|year
   * @returns {Promise<Object>} Chart ma'lumotlari
   */
  async getPortfolioTrend(period = 'month') {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_CHART_DATA
    }
    const response = await api.get('/api/analytics/charts/portfolio_trend/', { params: { period } })
    return response.data
  },

  /**
   * Topshiriq status pie chart
   * @param {string} period - week|month|year
   * @returns {Promise<Object>} Chart ma'lumotlari
   */
  async getAssignmentStatus(period = 'month') {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_PIE_DATA
    }
    const response = await api.get('/api/analytics/charts/assignment_status/', { params: { period } })
    return response.data
  },

  /**
   * Kategoriya distribution
   * @param {string} period - week|month|year
   * @returns {Promise<Object>} Chart ma'lumotlari
   */
  async getCategoryDistribution(period = 'month') {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return {
        labels: ['Ilmiy maqola', 'Esse', 'Loyiha', 'Hisobot'],
        datasets: [{ data: [35, 25, 22, 18] }]
      }
    }
    const response = await api.get('/api/analytics/charts/category_distribution/', { params: { period } })
    return response.data
  },

  // =====================
  // ANALYTICS
  // =====================

  /**
   * Portfolio analytics
   * @param {Object} params - date_from, date_to
   * @returns {Promise<Object>} Analytics ma'lumotlari
   */
  async getPortfolioAnalytics(params = {}) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return {
        total: 450,
        by_status: { pending: 23, approved: 412, rejected: 15 },
        by_category: { ilmiy_maqola: 150, esse: 120, loyiha: 100, hisobot: 80 },
        monthly_trend: MOCK_CHART_DATA
      }
    }
    const response = await api.get('/api/analytics/portfolios/', { params })
    return response.data
  },

  /**
   * Assignment analytics
   * @param {Object} params - date_from, date_to
   * @returns {Promise<Object>} Analytics ma'lumotlari
   */
  async getAssignmentAnalytics(params = {}) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return {
        total: 89,
        by_status: { pending: 15, in_progress: 28, completed: 42, overdue: 4 },
        by_priority: { high: 20, medium: 45, low: 24 },
        average_grade: 78.5
      }
    }
    const response = await api.get('/api/analytics/assignments/', { params })
    return response.data
  },

  /**
   * Barcha o'qituvchilar performance
   * @param {Object} params - date_from, date_to
   * @returns {Promise<Array>} O'qituvchilar ro'yxati
   */
  async getTeachersPerformance(params = {}) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return [
        { id: 1, full_name: 'Aliyev Vali', department: 'Pedagogika', portfolios_count: 12, assignments_completed: 8, performance_score: 92 },
        { id: 2, full_name: 'Karimova Nilufar', department: 'IT', portfolios_count: 15, assignments_completed: 10, performance_score: 88 },
        { id: 3, full_name: 'Rahimov Jasur', department: 'Tarix', portfolios_count: 8, assignments_completed: 6, performance_score: 85 }
      ]
    }
    const response = await api.get('/api/analytics/teachers/', { params })
    return response.data
  },

  /**
   * Bitta o'qituvchi performance
   * @param {string} teacherId - O'qituvchi ID
   * @param {Object} params - date_from, date_to
   * @returns {Promise<Object>} O'qituvchi performance
   */
  async getTeacherPerformance(teacherId, params = {}) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { id: teacherId, full_name: 'Test Teacher', portfolios_count: 12, assignments_completed: 8, performance_score: 92 }
    }
    const response = await api.get(`/api/analytics/teachers/${teacherId}/`, { params })
    return response.data
  },

  // =====================
  // REPORTS
  // =====================

  /**
   * Hisobotlar ro'yxati
   * @returns {Promise<Array>} Hisobotlar
   */
  async getReports() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return [
        { id: 1, title: 'Oylik hisobot - Yanvar 2026', type: 'monthly', format: 'excel', status: 'completed', created_at: new Date().toISOString() },
        { id: 2, title: 'Portfolio statistikasi', type: 'portfolios', format: 'pdf', status: 'completed', created_at: new Date().toISOString() }
      ]
    }
    const response = await api.get('/api/analytics/reports/')
    return response.data
  },

  /**
   * Hisobot tafsilotlari
   * @param {string} reportId - Hisobot ID
   * @returns {Promise<Object>} Hisobot
   */
  async getReport(reportId) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { id: reportId, title: 'Test hisobot', type: 'overview', format: 'excel', status: 'completed' }
    }
    const response = await api.get(`/api/analytics/reports/${reportId}/`)
    return response.data
  },

  /**
   * Yangi hisobot yaratish
   * @param {Object} data - Hisobot ma'lumotlari
   * @param {string} data.type - overview|portfolios|assignments|teachers
   * @param {string} data.format - excel|pdf|csv|json
   * @param {string} data.date_from - Boshlanish sanasi
   * @param {string} data.date_to - Tugash sanasi
   * @returns {Promise<Object>} Yaratilgan hisobot
   */
  async createReport(data) {
    const response = await api.post('/api/analytics/reports/', data)
    return response.data
  },

  /**
   * Hisobotni o'chirish
   * @param {string} reportId - Hisobot ID
   * @returns {Promise<Object>} O'chirish natijasi
   */
  async deleteReport(reportId) {
    const response = await api.delete(`/api/analytics/reports/${reportId}/`)
    return response.data
  },

  /**
   * Hisobotni yuklab olish
   * @param {string} reportId - Hisobot ID
   * @returns {Promise<Blob>} Fayl
   */
  async downloadReport(reportId) {
    const response = await api.get(`/api/analytics/reports/${reportId}/download/`, {
      responseType: 'blob'
    })
    return response.data
  },

  // =====================
  // EXPORT
  // =====================

  /**
   * Tezkor export (fayl saqlamaydi)
   * @param {Object} data - Export ma'lumotlari
   * @param {string} data.type - overview|portfolios|assignments|teachers
   * @param {string} data.format - excel|pdf|csv|json
   * @param {string} data.date_from - Boshlanish sanasi
   * @param {string} data.date_to - Tugash sanasi
   * @returns {Promise<Blob>} Fayl
   */
  async quickExport(data) {
    const response = await api.post('/api/analytics/export/', data, {
      responseType: 'blob'
    })
    return response.data
  },

  // =====================
  // CACHE (SuperAdmin)
  // =====================

  /**
   * Keshni tozalash
   * @param {string} pattern - dashboard (ixtiyoriy)
   * @returns {Promise<Object>} Natija
   */
  async clearCache(pattern = null) {
    const params = pattern ? { pattern } : {}
    const response = await api.delete('/api/analytics/cache/', { params })
    return response.data
  }
}

// Report type konstantalari
export const REPORT_TYPES = [
  { value: 'overview', label: 'Umumiy ko\'rinish' },
  { value: 'portfolios', label: 'Portfoliolar' },
  { value: 'assignments', label: 'Topshiriqlar' },
  { value: 'teachers', label: "O'qituvchilar" }
]

// Export format konstantalari
export const EXPORT_FORMATS = [
  { value: 'excel', label: 'Excel (.xlsx)', icon: 'table' },
  { value: 'pdf', label: 'PDF', icon: 'document' },
  { value: 'csv', label: 'CSV', icon: 'table' },
  { value: 'json', label: 'JSON', icon: 'code' }
]

// Period konstantalari
export const CHART_PERIODS = [
  { value: 'week', label: 'Hafta' },
  { value: 'month', label: 'Oy' },
  { value: 'year', label: 'Yil' }
]

export default analyticsService
