/**
 * Analytics Store - Pinia
 * Dashboard, Charts, Reports
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { analyticsService } from '@/services'
import { useToast } from 'vue-toastification'

export const useAnalyticsStore = defineStore('analytics', () => {
  const toast = useToast()

  // State
  const dashboardOverview = ref(null)
  const dashboardWidgets = ref([])
  const portfolioTrend = ref(null)
  const assignmentStatus = ref(null)
  const categoryDistribution = ref(null)
  const portfolioAnalytics = ref(null)
  const assignmentAnalytics = ref(null)
  const teachersPerformance = ref([])
  const reports = ref([])
  const currentReport = ref(null)
  const isLoading = ref(false)
  const chartPeriod = ref('month')

  // Getters
  const hasReports = computed(() => reports.value.length > 0)
  
  const pendingReports = computed(() => 
    reports.value.filter(r => r.status === 'pending' || r.status === 'processing')
  )

  const completedReports = computed(() => 
    reports.value.filter(r => r.status === 'completed')
  )

  // =====================
  // DASHBOARD
  // =====================

  async function fetchDashboardOverview() {
    isLoading.value = true
    try {
      const data = await analyticsService.getDashboardOverview()
      dashboardOverview.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch dashboard overview:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function fetchDashboardWidgets() {
    try {
      const data = await analyticsService.getDashboardWidgets()
      dashboardWidgets.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch dashboard widgets:', error)
      throw error
    }
  }

  // =====================
  // CHARTS
  // =====================

  async function fetchPortfolioTrend(period = null) {
    try {
      const p = period || chartPeriod.value
      const data = await analyticsService.getPortfolioTrend(p)
      portfolioTrend.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch portfolio trend:', error)
      throw error
    }
  }

  async function fetchAssignmentStatus(period = null) {
    try {
      const p = period || chartPeriod.value
      const data = await analyticsService.getAssignmentStatus(p)
      assignmentStatus.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch assignment status:', error)
      throw error
    }
  }

  async function fetchCategoryDistribution(period = null) {
    try {
      const p = period || chartPeriod.value
      const data = await analyticsService.getCategoryDistribution(p)
      categoryDistribution.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch category distribution:', error)
      throw error
    }
  }

  async function fetchAllCharts(period = null) {
    if (period) chartPeriod.value = period
    await Promise.all([
      fetchPortfolioTrend(period),
      fetchAssignmentStatus(period),
      fetchCategoryDistribution(period)
    ])
  }

  // =====================
  // ANALYTICS
  // =====================

  async function fetchPortfolioAnalytics(params = {}) {
    isLoading.value = true
    try {
      const data = await analyticsService.getPortfolioAnalytics(params)
      portfolioAnalytics.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch portfolio analytics:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function fetchAssignmentAnalytics(params = {}) {
    isLoading.value = true
    try {
      const data = await analyticsService.getAssignmentAnalytics(params)
      assignmentAnalytics.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch assignment analytics:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function fetchTeachersPerformance(params = {}) {
    isLoading.value = true
    try {
      const data = await analyticsService.getTeachersPerformance(params)
      teachersPerformance.value = data.results || data
      return data
    } catch (error) {
      console.error('Failed to fetch teachers performance:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // =====================
  // REPORTS
  // =====================

  async function fetchReports() {
    isLoading.value = true
    try {
      const data = await analyticsService.getReports()
      reports.value = data.results || data
      return data
    } catch (error) {
      console.error('Failed to fetch reports:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function fetchReport(reportId) {
    isLoading.value = true
    try {
      const data = await analyticsService.getReport(reportId)
      currentReport.value = data
      return data
    } catch (error) {
      console.error('Failed to fetch report:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function createReport(reportData) {
    isLoading.value = true
    try {
      const data = await analyticsService.createReport(reportData)
      reports.value.unshift(data)
      toast.success('Hisobot yaratildi')
      return data
    } catch (error) {
      console.error('Failed to create report:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  async function deleteReport(reportId) {
    try {
      await analyticsService.deleteReport(reportId)
      reports.value = reports.value.filter(r => r.id !== reportId)
      toast.success("Hisobot o'chirildi")
    } catch (error) {
      console.error('Failed to delete report:', error)
      throw error
    }
  }

  async function downloadReport(reportId) {
    try {
      const blob = await analyticsService.downloadReport(reportId)
      // Create download link
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      const report = reports.value.find(r => r.id === reportId)
      link.download = report?.filename || `report_${reportId}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      toast.success('Yuklab olindi')
    } catch (error) {
      console.error('Failed to download report:', error)
      throw error
    }
  }

  // =====================
  // EXPORT
  // =====================

  async function quickExport(exportData) {
    isLoading.value = true
    try {
      const blob = await analyticsService.quickExport(exportData)
      // Create download link
      const url = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = url
      const ext = exportData.format === 'excel' ? 'xlsx' : exportData.format
      link.download = `export_${exportData.type}_${new Date().toISOString().split('T')[0]}.${ext}`
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(url)
      toast.success('Export muvaffaqiyatli')
      return true
    } catch (error) {
      console.error('Failed to export:', error)
      throw error
    } finally {
      isLoading.value = false
    }
  }

  // =====================
  // CACHE
  // =====================

  async function clearCache(pattern = null) {
    try {
      await analyticsService.clearCache(pattern)
      toast.success('Kesh tozalandi')
      // Refresh data
      await fetchDashboardOverview()
    } catch (error) {
      console.error('Failed to clear cache:', error)
      throw error
    }
  }

  // =====================
  // HELPERS
  // =====================

  function setChartPeriod(period) {
    chartPeriod.value = period
  }

  return {
    // State
    dashboardOverview,
    dashboardWidgets,
    portfolioTrend,
    assignmentStatus,
    categoryDistribution,
    portfolioAnalytics,
    assignmentAnalytics,
    teachersPerformance,
    reports,
    currentReport,
    isLoading,
    chartPeriod,

    // Getters
    hasReports,
    pendingReports,
    completedReports,

    // Dashboard
    fetchDashboardOverview,
    fetchDashboardWidgets,

    // Charts
    fetchPortfolioTrend,
    fetchAssignmentStatus,
    fetchCategoryDistribution,
    fetchAllCharts,

    // Analytics
    fetchPortfolioAnalytics,
    fetchAssignmentAnalytics,
    fetchTeachersPerformance,

    // Reports
    fetchReports,
    fetchReport,
    createReport,
    deleteReport,
    downloadReport,

    // Export
    quickExport,

    // Cache
    clearCache,

    // Helpers
    setChartPeriod
  }
})
