import dayjs from 'dayjs'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/uz'

// Initialize dayjs plugins
dayjs.extend(relativeTime)
dayjs.locale('uz')

/**
 * Format date to readable string
 * @param {string|Date} date 
 * @param {string} format 
 * @returns {string}
 */
export function formatDate(date, format = 'D MMMM YYYY') {
  if (!date) return '-'
  return dayjs(date).format(format)
}

/**
 * Format date with time
 * @param {string|Date} date 
 * @returns {string}
 */
export function formatDateTime(date) {
  if (!date) return '-'
  return dayjs(date).format('D MMMM YYYY, HH:mm')
}

/**
 * Format date as relative time (e.g., "2 hours ago")
 * @param {string|Date} date 
 * @returns {string}
 */
export function formatRelativeTime(date) {
  if (!date) return '-'
  return dayjs(date).fromNow()
}

/**
 * Format short date
 * @param {string|Date} date 
 * @returns {string}
 */
export function formatShortDate(date) {
  if (!date) return '-'
  return dayjs(date).format('DD.MM.YYYY')
}

/**
 * Check if date is today
 * @param {string|Date} date 
 * @returns {boolean}
 */
export function isToday(date) {
  return dayjs(date).isSame(dayjs(), 'day')
}

/**
 * Check if date is this week
 * @param {string|Date} date 
 * @returns {boolean}
 */
export function isThisWeek(date) {
  return dayjs(date).isSame(dayjs(), 'week')
}
