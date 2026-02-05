/**
 * Assignment API Service
 * Topshiriqlar va Javoblar CRUD operatsiyalari
 */

import api from './api'

// Development mode check
const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'

// Mock data for development
const MOCK_ASSIGNMENTS = [
  {
    id: '1',
    title: 'Ilmiy maqola yozish',
    description: 'Pedagogika sohasida ilmiy maqola tayyorlash',
    category: { id: '1', name: 'Ilmiy maqola', color: '#3B82F6' },
    status: 'in_progress',
    priority: 'high',
    deadline: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000).toISOString(),
    progress: 45,
    created_at: new Date().toISOString(),
    assigned_to: { id: 1, full_name: 'Test User' },
    created_by: { id: 2, full_name: 'Admin User' }
  },
  {
    id: '2',
    title: 'Esse tayyorlash',
    description: 'Zamonaviy ta\'lim metodlari haqida esse',
    category: { id: '2', name: 'Esse', color: '#10B981' },
    status: 'pending',
    priority: 'medium',
    deadline: new Date(Date.now() + 14 * 24 * 60 * 60 * 1000).toISOString(),
    progress: 0,
    created_at: new Date().toISOString(),
    assigned_to: { id: 1, full_name: 'Test User' },
    created_by: { id: 2, full_name: 'Admin User' }
  },
  {
    id: '3',
    title: 'Loyiha hisoboti',
    description: 'Yakuniy loyiha hisobotini tayyorlash',
    category: { id: '3', name: 'Hisobot', color: '#F59E0B' },
    status: 'completed',
    priority: 'low',
    deadline: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    progress: 100,
    created_at: new Date().toISOString(),
    assigned_to: { id: 1, full_name: 'Test User' },
    created_by: { id: 2, full_name: 'Admin User' }
  },
  {
    id: '4',
    title: 'Muddati o\'tgan topshiriq',
    description: 'Bu topshiriq muddati o\'tgan',
    category: { id: '1', name: 'Ilmiy maqola', color: '#3B82F6' },
    status: 'overdue',
    priority: 'high',
    deadline: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    progress: 20,
    created_at: new Date().toISOString(),
    assigned_to: { id: 1, full_name: 'Test User' },
    created_by: { id: 2, full_name: 'Admin User' }
  }
]

export const assignmentService = {
  // =====================
  // ASSIGNMENTS
  // =====================

  /**
   * Barcha topshiriqlarni olish
   * @param {Object} params - Query parametrlari
   * @param {string} params.status - pending|in_progress|completed|overdue|cancelled
   * @param {string} params.priority - low|medium|high
   * @param {string} params.category - Kategoriya ID
   * @param {string} params.assigned_to - Foydalanuvchi ID
   * @param {boolean} params.overdue - Muddati o'tganlar
   * @param {boolean} params.upcoming - 7 kun ichida
   * @param {string} params.search - Qidiruv
   * @param {string} params.ordering - Tartiblash
   * @returns {Promise<Object>} Topshiriqlar ro'yxati
   */
  async getAssignments(params = {}) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { results: MOCK_ASSIGNMENTS, count: MOCK_ASSIGNMENTS.length }
    }
    const response = await api.get('/api/assignments/v2/assignments/', { params })
    return response.data
  },

  /**
   * Bitta topshiriqni olish
   * @param {string} assignmentId - Topshiriq ID
   * @returns {Promise<Object>} Topshiriq
   */
  async getAssignment(assignmentId) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_ASSIGNMENTS.find(a => a.id === assignmentId) || MOCK_ASSIGNMENTS[0]
    }
    const response = await api.get(`/api/assignments/v2/assignments/${assignmentId}/`)
    return response.data
  },

  /**
   * Yangi topshiriq yaratish (Admin)
   * @param {Object} data - Topshiriq ma'lumotlari
   * @returns {Promise<Object>} Yaratilgan topshiriq
   */
  async createAssignment(data) {
    const response = await api.post('/api/assignments/v2/assignments/', data)
    return response.data
  },

  /**
   * Topshiriqni yangilash
   * @param {string} assignmentId - Topshiriq ID
   * @param {Object} data - Yangilanadigan ma'lumotlar
   * @returns {Promise<Object>} Yangilangan topshiriq
   */
  async updateAssignment(assignmentId, data) {
    const response = await api.put(`/api/assignments/v2/assignments/${assignmentId}/`, data)
    return response.data
  },

  /**
   * Topshiriqni o'chirish
   * @param {string} assignmentId - Topshiriq ID
   * @returns {Promise<Object>} O'chirish natijasi
   */
  async deleteAssignment(assignmentId) {
    const response = await api.delete(`/api/assignments/v2/assignments/${assignmentId}/`)
    return response.data
  },

  /**
   * Topshiriq statusini yangilash
   * @param {string} assignmentId - Topshiriq ID
   * @param {string} status - Yangi status
   * @returns {Promise<Object>} Yangilangan topshiriq
   */
  async updateStatus(assignmentId, status) {
    const response = await api.patch(`/api/assignments/v2/assignments/${assignmentId}/update_status/`, { status })
    return response.data
  },

  /**
   * Mening topshiriqlarim (Teacher)
   * @param {Object} params - Query parametrlari
   * @returns {Promise<Object>} Topshiriqlar ro'yxati
   */
  async getMyAssignments(params = {}) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_ASSIGNMENTS
    }
    const response = await api.get('/api/assignments/v2/assignments/my_assignments/', { params })
    return response.data
  },

  /**
   * Topshiriq statistikasi
   * @returns {Promise<Object>} Statistika
   */
  async getStatistics() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return {
        total: MOCK_ASSIGNMENTS.length,
        pending: MOCK_ASSIGNMENTS.filter(a => a.status === 'pending').length,
        in_progress: MOCK_ASSIGNMENTS.filter(a => a.status === 'in_progress').length,
        completed: MOCK_ASSIGNMENTS.filter(a => a.status === 'completed').length,
        overdue: MOCK_ASSIGNMENTS.filter(a => a.status === 'overdue').length,
        cancelled: 0,
        completion_rate: 25,
        average_grade: 85
      }
    }
    const response = await api.get('/api/assignments/v2/assignments/statistics/')
    return response.data
  },

  /**
   * Topshiriqga javob yuborish
   * @param {string} assignmentId - Topshiriq ID
   * @param {Object} data - Javob ma'lumotlari
   * @returns {Promise<Object>} Submission
   */
  async submitAssignment(assignmentId, data) {
    const response = await api.post(`/api/assignments/v2/assignments/${assignmentId}/submit/`, data)
    return response.data
  },

  // =====================
  // SUBMISSIONS
  // =====================

  /**
   * Barcha javoblarni olish
   * @param {Object} params - Query parametrlari
   * @returns {Promise<Object>} Javoblar ro'yxati
   */
  async getSubmissions(params = {}) {
    const response = await api.get('/api/assignments/v2/submissions/', { params })
    return response.data
  },

  /**
   * Bitta javobni olish
   * @param {string} submissionId - Javob ID
   * @returns {Promise<Object>} Javob
   */
  async getSubmission(submissionId) {
    const response = await api.get(`/api/assignments/v2/submissions/${submissionId}/`)
    return response.data
  },

  /**
   * Yangi javob yaratish
   * @param {Object} data - Javob ma'lumotlari
   * @returns {Promise<Object>} Yaratilgan javob
   */
  async createSubmission(data) {
    const response = await api.post('/api/assignments/v2/submissions/', data)
    return response.data
  },

  /**
   * Javobni baholash (Admin)
   * @param {string} submissionId - Javob ID
   * @param {Object} gradeData - Baholash ma'lumotlari
   * @param {number} gradeData.score - Ball (0-100)
   * @param {string} gradeData.feedback - Izoh
   * @returns {Promise<Object>} Baholangan javob
   */
  async gradeSubmission(submissionId, gradeData) {
    const response = await api.patch(`/api/assignments/v2/submissions/${submissionId}/grade/`, gradeData)
    return response.data
  },

  // =====================
  // SCORING
  // =====================

  /**
   * Topshiriq ball sozlamalarini olish
   * @param {string} assignmentId - Topshiriq ID
   * @returns {Promise<Object>} Ball sozlamalari
   */
  async getScoreSettings(assignmentId) {
    const response = await api.get(`/api/assignments/${assignmentId}/score/`)
    return response.data
  },

  /**
   * Topshiriq ball sozlamalarini yangilash
   * @param {string} assignmentId - Topshiriq ID
   * @param {Object} scoreData - Ball sozlamalari
   * @returns {Promise<Object>} Yangilangan sozlamalar
   */
  async updateScoreSettings(assignmentId, scoreData) {
    const response = await api.put(`/api/assignments/${assignmentId}/score/`, scoreData)
    return response.data
  },

  /**
   * Topshiriq ball tarixini olish
   * @param {string} assignmentId - Topshiriq ID
   * @returns {Promise<Array>} Ball tarixi
   */
  async getScoreHistory(assignmentId) {
    const response = await api.get(`/api/assignments/${assignmentId}/score-history/`)
    return response.data
  },

  /**
   * Progress baholash
   * @param {string} progressId - Progress ID
   * @param {Object} gradeData - Baholash ma'lumotlari
   * @returns {Promise<Object>} Baholangan progress
   */
  async gradeProgress(progressId, gradeData) {
    const response = await api.put(`/api/assignments/progress/${progressId}/grade/`, gradeData)
    return response.data
  },

  /**
   * Barcha ball tarixini olish
   * @returns {Promise<Array>} Ball tarixi
   */
  async getAllScoreHistory(params = {}) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      const mockHistory = [
        {
          id: 1,
          assignment: { id: '1', title: 'Ilmiy maqola yozish', category: { name: 'Ilmiy maqola' } },
          teacher: { id: 1, full_name: 'Test Teacher', department: 'Pedagogika' },
          change_type: 'grade',
          old_value: null,
          new_value: 85,
          changed_by: { full_name: 'Admin User', role: 'admin' },
          note: 'Dastlabki baholash',
          created_at: new Date().toISOString()
        },
        {
          id: 2,
          assignment: { id: '1', title: 'Ilmiy maqola yozish', category: { name: 'Ilmiy maqola' } },
          teacher: { id: 1, full_name: 'Test Teacher', department: 'Pedagogika' },
          change_type: 'score_update',
          old_value: 85,
          new_value: 90,
          changed_by: { full_name: 'Admin User', role: 'admin' },
          note: 'Ball oshirildi',
          created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 3,
          assignment: { id: '2', title: 'Esse tayyorlash', category: { name: 'Esse' } },
          teacher: { id: 2, full_name: 'Another Teacher', department: 'IT' },
          change_type: 'multiplier',
          old_value: 1,
          new_value: 1.5,
          changed_by: { full_name: 'Super Admin', role: 'superadmin' },
          note: '1.5x bonus qo\'llanildi',
          created_at: new Date(Date.now() - 2 * 60 * 60 * 1000).toISOString()
        },
        {
          id: 4,
          assignment: { id: '3', title: 'Loyiha hisoboti', category: { name: 'Loyiha' } },
          teacher: { id: 1, full_name: 'Test Teacher', department: 'Pedagogika' },
          change_type: 'grade',
          old_value: null,
          new_value: 78,
          changed_by: { full_name: 'Admin User', role: 'admin' },
          created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
        }
      ]
      return { results: mockHistory, count: mockHistory.length }
    }
    const response = await api.get('/api/assignments/score-history/', { params })
    return response.data
  },

  /**
   * Bulk ball yangilash
   * @param {Object} data - Bulk yangilash ma'lumotlari
   * @returns {Promise<Object>} Natija
   */
  async bulkScoreUpdate(data) {
    // DEV_MODE da mock response qaytarish
    if (DEV_MODE) {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve({
            updated_count: data.assignment_ids?.length || 0,
            message: 'Topshiriqlar muvaffaqiyatli yangilandi'
          })
        }, 1000)
      })
    }
    const response = await api.post('/api/assignments/bulk-score-update/', data)
    return response.data
  }
}

// Status konstantalari
export const ASSIGNMENT_STATUSES = [
  { value: 'pending', label: 'Kutilmoqda', color: 'warning' },
  { value: 'in_progress', label: 'Bajarilmoqda', color: 'info' },
  { value: 'completed', label: 'Bajarildi', color: 'success' },
  { value: 'overdue', label: "Muddati o'tgan", color: 'danger' },
  { value: 'cancelled', label: 'Bekor qilindi', color: 'gray' }
]

// Priority konstantalari
export const ASSIGNMENT_PRIORITIES = [
  { value: 'low', label: 'Past', color: 'gray' },
  { value: 'medium', label: "O'rta", color: 'warning' },
  { value: 'high', label: 'Yuqori', color: 'danger' }
]

export default assignmentService
