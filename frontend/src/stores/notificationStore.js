/**
 * Notification Store
 * Manages user notifications state
 */

import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const DEV_MODE = import.meta.env.VITE_DEV_MODE === 'true'

export const useNotificationStore = defineStore('notification', () => {
  // State
  const notifications = ref([])
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const unreadCount = computed(() => {
    return notifications.value.filter(n => !n.is_read).length
  })

  const allNotifications = computed(() => notifications.value)

  // Actions
  async function fetchNotifications() {
    loading.value = true
    error.value = null

    try {
      if (DEV_MODE) {
        // Mock notifications for DEV_MODE
        await new Promise(resolve => setTimeout(resolve, 500))
        notifications.value = [
          {
            id: 1,
            title: 'Yangi topshiriq',
            message: 'Sizga yangi topshiriq berildi: "Ilmiy maqola yuklash"',
            type: 'assignment',
            is_read: false,
            created_at: new Date().toISOString()
          },
          {
            id: 2,
            title: 'Portfolio tasdiqlandi',
            message: 'Sizning "Metodik qo\'llanma" portfoliongiz tasdiqlandi',
            type: 'approval',
            is_read: false,
            created_at: new Date(Date.now() - 86400000).toISOString()
          },
          {
            id: 3,
            title: 'Ball qo\'shildi',
            message: 'Sizga 50 ball qo\'shildi',
            type: 'score',
            is_read: true,
            created_at: new Date(Date.now() - 172800000).toISOString()
          }
        ]
        return notifications.value
      }

      // Real API call would go here
      const response = await fetch('/api/notifications/')
      notifications.value = await response.json()
      return notifications.value
    } catch (err) {
      console.error('Failed to fetch notifications:', err)
      error.value = err.message
      throw err
    } finally {
      loading.value = false
    }
  }

  async function markAsRead(notificationId) {
    try {
      if (DEV_MODE) {
        const notification = notifications.value.find(n => n.id === notificationId)
        if (notification) {
          notification.is_read = true
        }
        return
      }

      // Real API call
      await fetch(`/api/notifications/${notificationId}/read/`, { method: 'POST' })
      const notification = notifications.value.find(n => n.id === notificationId)
      if (notification) {
        notification.is_read = true
      }
    } catch (err) {
      console.error('Failed to mark notification as read:', err)
      throw err
    }
  }

  async function markAllAsRead() {
    try {
      if (DEV_MODE) {
        notifications.value.forEach(n => {
          n.is_read = true
        })
        return
      }

      // Real API call
      await fetch('/api/notifications/read-all/', { method: 'POST' })
      notifications.value.forEach(n => {
        n.is_read = true
      })
    } catch (err) {
      console.error('Failed to mark all notifications as read:', err)
      throw err
    }
  }

  function $reset() {
    notifications.value = []
    loading.value = false
    error.value = null
  }

  return {
    // State
    notifications,
    loading,
    error,
    // Getters
    unreadCount,
    allNotifications,
    // Actions
    fetchNotifications,
    markAsRead,
    markAllAsRead,
    $reset
  }
})
