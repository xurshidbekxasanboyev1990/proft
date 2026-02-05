/**
 * Category API Service
 * Kategoriyalar CRUD operatsiyalari
 */

import api from './api'

// Development mode check
const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'

// Mock data for development
const MOCK_CATEGORIES = [
  {
    id: '1',
    name: 'Ilmiy maqola',
    name_uz: 'Ilmiy maqola',
    description: 'Ilmiy jurnallarda chop etilgan maqolalar',
    color: '#3B82F6',
    icon: 'document',
    default_score: 10,
    min_score: 5,
    score_weight: 1.5,
    is_active: true,
    order: 1,
    assignments_count: 15
  },
  {
    id: '2',
    name: 'Esse',
    name_uz: 'Esse',
    description: 'Ijodiy esse va insholar',
    color: '#10B981',
    icon: 'pencil',
    default_score: 5,
    min_score: 2,
    score_weight: 1.0,
    is_active: true,
    order: 2,
    assignments_count: 12
  },
  {
    id: '3',
    name: 'Loyiha',
    name_uz: 'Loyiha',
    description: 'Innovatsion loyihalar',
    color: '#F59E0B',
    icon: 'folder',
    default_score: 20,
    min_score: 10,
    score_weight: 2.0,
    is_active: true,
    order: 3,
    assignments_count: 8
  },
  {
    id: '4',
    name: 'Hisobot',
    name_uz: 'Hisobot',
    description: 'Oylik va yillik hisobotlar',
    color: '#8B5CF6',
    icon: 'chart',
    default_score: 10,
    min_score: 5,
    score_weight: 1.2,
    is_active: true,
    order: 4,
    assignments_count: 10
  }
]

export const categoryService = {
  /**
   * Barcha kategoriyalarni olish
   * @returns {Promise<Array>} Kategoriyalar ro'yxati
   */
  async getCategories() {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return { results: MOCK_CATEGORIES }
    }
    const response = await api.get('/api/assignments/v2/categories/')
    return response.data
  },

  /**
   * Bitta kategoriyani olish
   * @param {string} categoryId - Kategoriya ID
   * @returns {Promise<Object>} Kategoriya
   */
  async getCategory(categoryId) {
    // DEV_MODE da mock data qaytarish
    if (DEV_MODE) {
      return MOCK_CATEGORIES.find(c => c.id === categoryId) || MOCK_CATEGORIES[0]
    }
    const response = await api.get(`/api/assignments/v2/categories/${categoryId}/`)
    return response.data
  },

  /**
   * Yangi kategoriya yaratish (Admin)
   * @param {Object} data - Kategoriya ma'lumotlari
   * @param {string} data.name - Kategoriya nomi
   * @param {string} data.description - Tavsif
   * @param {number} data.default_score - Standart ball
   * @param {number} data.min_score - Minimal ball
   * @param {number} data.score_weight - Vazn
   * @returns {Promise<Object>} Yaratilgan kategoriya
   */
  async createCategory(data) {
    const response = await api.post('/api/assignments/v2/categories/', data)
    return response.data
  },

  /**
   * Kategoriyani yangilash
   * @param {string} categoryId - Kategoriya ID
   * @param {Object} data - Yangilanadigan ma'lumotlar
   * @returns {Promise<Object>} Yangilangan kategoriya
   */
  async updateCategory(categoryId, data) {
    const response = await api.put(`/api/assignments/v2/categories/${categoryId}/`, data)
    return response.data
  },

  /**
   * Kategoriyani o'chirish
   * @param {string} categoryId - Kategoriya ID
   * @returns {Promise<Object>} O'chirish natijasi
   */
  async deleteCategory(categoryId) {
    const response = await api.delete(`/api/assignments/v2/categories/${categoryId}/`)
    return response.data
  },

  /**
   * Kategoriya ball sozlamalarini yangilash
   * @param {string} categoryId - Kategoriya ID
   * @param {Object} scoreData - Ball sozlamalari
   * @returns {Promise<Object>} Yangilangan kategoriya
   */
  async updateCategoryScore(categoryId, scoreData) {
    const response = await api.put(`/api/assignments/categories/${categoryId}/score/`, scoreData)
    return response.data
  },

  /**
   * Kategoriyaga tegishli topshiriqlarni olish
   * @param {string} categoryId - Kategoriya ID
   * @returns {Promise<Array>} Topshiriqlar ro'yxati
   */
  async getCategoryAssignments(categoryId) {
    const response = await api.get(`/api/assignments/v2/categories/${categoryId}/assignments/`)
    return response.data
  }
}

export default categoryService
