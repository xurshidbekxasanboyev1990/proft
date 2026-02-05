/**
 * Assignment Store - Pinia
 * Topshiriqlar va javoblarni boshqarish
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { assignmentService, categoryService } from '@/services'
import { useToast } from 'vue-toastification'

export const useAssignmentStore = defineStore('assignment', () => {
  const toast = useToast()

  // State
  const assignments = ref([])
  const myAssignments = ref([])
  const currentAssignment = ref(null)
  const categories = ref([])
  const submissions = ref([])
  const statistics = ref(null)
  const isLoading = ref(false)
  const pagination = ref({
    page: 1,
    page_size: 20,
    total_pages: 1,
    total_count: 0,
    has_next: false,
    has_previous: false
  })
  const filters = ref({
    status: '',
    priority: '',
    category: '',
    search: '',
    ordering: '-created_at'
  })

  // Getters
  const pendingAssignments = computed(() =>
    assignments.value.filter(a => a.status === 'pending')
  )

  const overdueAssignments = computed(() =>
    assignments.value.filter(a => a.status === 'overdue')
  )

  const completedAssignments = computed(() =>
    assignments.value.filter(a => a.status === 'completed')
  )

  const hasAssignments = computed(() => assignments.value.length > 0)

  // =====================
  // CATEGORIES
  // =====================

  async function fetchCategories() {
    try {
      const data = await categoryService.getCategories()
      categories.value = data.results || data
      return data
    } catch (error) {
      console.error('Failed to fetch categories:', error)
      throw error
    }
  }

  async function createCategory(categoryData) {
    isLoading.value = true
    try {
      const data = await categoryService.createCategory(categoryData)
      categories.value.push(data)
      toast.success('Kategoriya yaratildi')
      return data
    } catch (error) {
      console.error('Failed to create category:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function updateCategory(categoryId, categoryData) {
    isLoading.value = true
    try {
      const data = await categoryService.updateCategory(categoryId, categoryData)
      const index = categories.value.findIndex(c => c.id === categoryId)
      if (index !== -1) {
        categories.value[index] = data
      }
      toast.success('Kategoriya yangilandi')
      return data
    } catch (error) {
      console.error('Failed to update category:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function deleteCategory(categoryId) {
    isLoading.value = true
    try {
      await categoryService.deleteCategory(categoryId)
      categories.value = categories.value.filter(c => c.id !== categoryId)
      toast.success("Kategoriya o'chirildi")
    } catch (error) {
      console.error('Failed to delete category:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // =====================
  // ASSIGNMENTS
  // =====================

  async function fetchAssignments(params = {}) {
    isLoading.value = true
    try {
      const queryParams = {
        ...filters.value,
        ...params,
        page: params.page || pagination.value.page
      }

      // Remove empty values
      Object.keys(queryParams).forEach(key => {
        if (!queryParams[key]) delete queryParams[key]
      })

      const data = await assignmentService.getAssignments(queryParams)
      assignments.value = data.results || data
      if (data.count !== undefined) {
        pagination.value = {
          ...pagination.value,
          total_count: data.count,
          total_pages: Math.ceil(data.count / pagination.value.page_size),
          has_next: !!data.next,
          has_previous: !!data.previous
        }
      }
      return data
    } catch (error) {
      console.error('Failed to fetch assignments:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function fetchMyAssignments(params = {}) {
    isLoading.value = true
    try {
      const data = await assignmentService.getMyAssignments(params)
      myAssignments.value = data.results || data
      return data
    } catch (error) {
      console.error('Failed to fetch my assignments:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function fetchAssignment(assignmentId) {
    isLoading.value = true
    try {
      const data = await assignmentService.getAssignment(assignmentId)
      currentAssignment.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch assignment:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function createAssignment(assignmentData) {
    isLoading.value = true
    try {
      const data = await assignmentService.createAssignment(assignmentData)
      assignments.value.unshift(data)
      toast.success('Topshiriq yaratildi')
      return data
    } catch (error) {
      console.error('Failed to create assignment:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function updateAssignment(assignmentId, assignmentData) {
    isLoading.value = true
    try {
      const data = await assignmentService.updateAssignment(assignmentId, assignmentData)
      const index = assignments.value.findIndex(a => a.id === assignmentId)
      if (index !== -1) {
        assignments.value[index] = data
      }
      if (currentAssignment.value?.id === assignmentId) {
        currentAssignment.value = data
      }
      toast.success('Topshiriq yangilandi')
      return data
    } catch (error) {
      console.error('Failed to update assignment:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function deleteAssignment(assignmentId) {
    isLoading.value = true
    try {
      await assignmentService.deleteAssignment(assignmentId)
      assignments.value = assignments.value.filter(a => a.id !== assignmentId)
      toast.success("Topshiriq o'chirildi")
    } catch (error) {
      console.error('Failed to delete assignment:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function updateAssignmentStatus(assignmentId, status) {
    try {
      const data = await assignmentService.updateStatus(assignmentId, status)
      const index = assignments.value.findIndex(a => a.id === assignmentId)
      if (index !== -1) {
        assignments.value[index].status = status
      }
      toast.success('Status yangilandi')
      return data
    } catch (error) {
      console.error('Failed to update status:', error)
      throw error
    }
  }

  // =====================
  // SUBMISSIONS
  // =====================

  async function submitAssignment(assignmentId, submissionData) {
    isLoading.value = true
    try {
      const data = await assignmentService.submitAssignment(assignmentId, submissionData)
      toast.success('Javob yuborildi')
      // Update assignment status in local list
      const index = myAssignments.value.findIndex(a => a.id === assignmentId)
      if (index !== -1) {
        myAssignments.value[index].status = 'completed'
      }
      return data
    } catch (error) {
      console.error('Failed to submit assignment:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function fetchSubmissions(params = {}) {
    isLoading.value = true
    try {
      const data = await assignmentService.getSubmissions(params)
      submissions.value = data.results || data
      return data
    } catch (error) {
      console.error('Failed to fetch submissions:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function gradeSubmission(submissionId, gradeData) {
    try {
      const data = await assignmentService.gradeSubmission(submissionId, gradeData)
      const index = submissions.value.findIndex(s => s.id === submissionId)
      if (index !== -1) {
        submissions.value[index] = { ...submissions.value[index], ...data }
      }
      toast.success('Baholandi')
      return data
    } catch (error) {
      console.error('Failed to grade submission:', error)
      throw error
    }
  }

  // =====================
  // STATISTICS
  // =====================

  async function fetchStatistics() {
    try {
      const data = await assignmentService.getStatistics()
      statistics.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch statistics:', error)
      throw error
    }
  }

  // =====================
  // FILTERS
  // =====================

  async function setFilters(newFilters) {
    filters.value = { ...filters.value, ...newFilters }
    pagination.value.page = 1
    return fetchAssignments()
  }

  async function clearFilters() {
    filters.value = {
      status: '',
      priority: '',
      category: '',
      search: '',
      ordering: '-created_at'
    }
    pagination.value.page = 1
    return fetchAssignments()
  }

  async function goToPage(page) {
    pagination.value.page = page
    return fetchAssignments()
  }

  function clearCurrentAssignment() {
    currentAssignment.value = null
  }

  return {
    // State
    assignments,
    myAssignments,
    currentAssignment,
    categories,
    submissions,
    statistics,
    isLoading,
    pagination,
    filters,

    // Getters
    pendingAssignments,
    overdueAssignments,
    completedAssignments,
    hasAssignments,

    // Category Actions
    fetchCategories,
    createCategory,
    updateCategory,
    deleteCategory,

    // Assignment Actions
    fetchAssignments,
    fetchMyAssignments,
    fetchAssignment,
    createAssignment,
    updateAssignment,
    deleteAssignment,
    updateAssignmentStatus,

    // Submission Actions
    submitAssignment,
    fetchSubmissions,
    gradeSubmission,

    // Statistics
    fetchStatistics,

    // Filters
    setFilters,
    clearFilters,
    goToPage,
    clearCurrentAssignment
  }
})
