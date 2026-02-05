<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Bildirishnomalar</h1>
        <p class="mt-1 text-sm text-gray-500">
          Barcha bildirishnomalar va xabarlar
        </p>
      </div>

      <!-- Actions -->
      <div class="flex items-center gap-3">
        <button
          v-if="unreadCount > 0"
          @click="markAllAsRead"
          class="inline-flex items-center gap-2 px-4 py-2 text-sm text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
        >
          <CheckIcon class="w-5 h-5" />
          Barchasini o'qilgan deb belgilash
        </button>
        <button
          @click="showSettings = true"
          class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-gray-300 text-gray-700 rounded-lg hover:bg-gray-50 transition-colors"
        >
          <Cog6ToothIcon class="w-5 h-5" />
          Sozlamalar
        </button>
      </div>
    </div>

    <!-- Stats cards -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6">
      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-primary-100 rounded-xl flex items-center justify-center">
            <BellIcon class="w-5 h-5 text-primary-600" />
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ totalCount }}</p>
            <p class="text-sm text-gray-500">Jami</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-warning-100 rounded-xl flex items-center justify-center">
            <BellAlertIcon class="w-5 h-5 text-warning-600" />
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ unreadCount }}</p>
            <p class="text-sm text-gray-500">O'qilmagan</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-success-100 rounded-xl flex items-center justify-center">
            <StarIcon class="w-5 h-5 text-success-600" />
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ importantCount }}</p>
            <p class="text-sm text-gray-500">Muhim</p>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-gray-100 rounded-xl flex items-center justify-center">
            <ArchiveBoxIcon class="w-5 h-5 text-gray-600" />
          </div>
          <div>
            <p class="text-2xl font-bold text-gray-900">{{ archivedCount }}</p>
            <p class="text-sm text-gray-500">Arxivlangan</p>
          </div>
        </div>
      </div>
    </div>

    <!-- Filters and search -->
    <div class="bg-white rounded-xl shadow-sm border border-gray-200 p-4 mb-6">
      <div class="flex flex-col sm:flex-row sm:items-center gap-4">
        <!-- Search -->
        <div class="flex-1 relative">
          <MagnifyingGlassIcon class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Bildirishnomalarni qidirish..."
            class="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-500"
          />
        </div>

        <!-- Filter buttons -->
        <div class="flex items-center gap-2">
          <button
            v-for="filter in filterOptions"
            :key="filter.value"
            @click="activeFilter = filter.value"
            :class="[
              'px-4 py-2 text-sm rounded-lg transition-colors',
              activeFilter === filter.value
                ? 'bg-primary-100 text-primary-700'
                : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
            ]"
          >
            {{ filter.label }}
            <span 
              v-if="filter.count > 0" 
              class="ml-1 px-1.5 py-0.5 text-xs rounded-full"
              :class="activeFilter === filter.value ? 'bg-primary-200' : 'bg-gray-200'"
            >
              {{ filter.count }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Notifications list -->
    <div class="space-y-3">
      <TransitionGroup name="list">
        <div
          v-for="notification in filteredNotifications"
          :key="notification.id"
          :class="[
            'bg-white rounded-xl shadow-sm border p-4 cursor-pointer transition-all hover:shadow-md',
            notification.read ? 'border-gray-200' : 'border-primary-200 bg-primary-50/30'
          ]"
          @click="openNotification(notification)"
        >
          <div class="flex items-start gap-4">
            <!-- Icon -->
            <div 
              class="w-12 h-12 rounded-xl flex items-center justify-center flex-shrink-0"
              :class="getNotificationIconClass(notification.type)"
            >
              <component :is="getNotificationIcon(notification.type)" class="w-6 h-6" />
            </div>

            <!-- Content -->
            <div class="flex-1 min-w-0">
              <div class="flex items-start justify-between gap-4">
                <div>
                  <h3 :class="[
                    'text-sm',
                    notification.read ? 'text-gray-700' : 'font-semibold text-gray-900'
                  ]">
                    {{ notification.title }}
                  </h3>
                  <p class="mt-1 text-sm text-gray-500 line-clamp-2">
                    {{ notification.message }}
                  </p>
                </div>

                <!-- Actions -->
                <div class="flex items-center gap-2 flex-shrink-0">
                  <span class="text-xs text-gray-400">{{ formatRelativeTime(notification.created_at) }}</span>
                  
                  <div class="relative" @click.stop>
                    <button
                      @click="toggleMenu(notification.id)"
                      class="p-1 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
                    >
                      <EllipsisVerticalIcon class="w-5 h-5" />
                    </button>

                    <!-- Dropdown menu -->
                    <Transition name="dropdown">
                      <div 
                        v-if="openMenuId === notification.id"
                        class="absolute right-0 mt-1 w-48 bg-white rounded-lg shadow-lg border border-gray-200 py-1 z-10"
                      >
                        <button
                          v-if="!notification.read"
                          @click="markAsRead(notification)"
                          class="w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                        >
                          <CheckIcon class="w-4 h-4" />
                          O'qilgan deb belgilash
                        </button>
                        <button
                          v-else
                          @click="markAsUnread(notification)"
                          class="w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                        >
                          <EnvelopeIcon class="w-4 h-4" />
                          O'qilmagan deb belgilash
                        </button>
                        <button
                          @click="toggleImportant(notification)"
                          class="w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                        >
                          <StarIcon class="w-4 h-4" />
                          {{ notification.important ? 'Muhimlardan olib tashlash' : 'Muhim deb belgilash' }}
                        </button>
                        <button
                          @click="archiveNotification(notification)"
                          class="w-full px-4 py-2 text-sm text-left text-gray-700 hover:bg-gray-100 flex items-center gap-2"
                        >
                          <ArchiveBoxIcon class="w-4 h-4" />
                          Arxivlash
                        </button>
                        <hr class="my-1" />
                        <button
                          @click="deleteNotification(notification)"
                          class="w-full px-4 py-2 text-sm text-left text-danger-600 hover:bg-danger-50 flex items-center gap-2"
                        >
                          <TrashIcon class="w-4 h-4" />
                          O'chirish
                        </button>
                      </div>
                    </Transition>
                  </div>
                </div>
              </div>

              <!-- Tags -->
              <div class="mt-2 flex items-center gap-2">
                <span 
                  class="px-2 py-0.5 text-xs rounded-full"
                  :class="getNotificationTypeClass(notification.type)"
                >
                  {{ getNotificationTypeLabel(notification.type) }}
                </span>
                <span v-if="notification.important" class="px-2 py-0.5 text-xs rounded-full bg-warning-100 text-warning-700 flex items-center gap-1">
                  <StarIcon class="w-3 h-3" />
                  Muhim
                </span>
                <span v-if="!notification.read" class="w-2 h-2 bg-primary-500 rounded-full"></span>
              </div>
            </div>
          </div>
        </div>
      </TransitionGroup>

      <!-- Empty state -->
      <div v-if="filteredNotifications.length === 0" class="bg-white rounded-xl shadow-sm border border-gray-200 p-12 text-center">
        <BellSlashIcon class="w-16 h-16 text-gray-300 mx-auto mb-4" />
        <h3 class="text-lg font-medium text-gray-900 mb-2">Bildirishnomalar topilmadi</h3>
        <p class="text-gray-500">
          {{ activeFilter === 'all' ? 'Hozircha hech qanday bildirishnoma yo\'q' : 'Bu filtrdagi bildirishnomalar yo\'q' }}
        </p>
      </div>
    </div>

    <!-- Load more -->
    <div v-if="hasMore && filteredNotifications.length > 0" class="mt-6 text-center">
      <button
        @click="loadMore"
        class="px-6 py-2 text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
      >
        Ko'proq yuklash
      </button>
    </div>

    <!-- Notification detail modal -->
    <Transition name="modal">
      <div v-if="selectedNotification" class="fixed inset-0 z-50 overflow-y-auto" @click="selectedNotification = null">
        <div class="flex items-center justify-center min-h-screen p-4">
          <div class="fixed inset-0 bg-black/50"></div>
          
          <div 
            class="relative bg-white rounded-2xl shadow-xl max-w-lg w-full p-6"
            @click.stop
          >
            <button
              @click="selectedNotification = null"
              class="absolute right-4 top-4 p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
            >
              <XMarkIcon class="w-5 h-5" />
            </button>

            <div class="flex items-start gap-4">
              <div 
                class="w-14 h-14 rounded-xl flex items-center justify-center flex-shrink-0"
                :class="getNotificationIconClass(selectedNotification.type)"
              >
                <component :is="getNotificationIcon(selectedNotification.type)" class="w-7 h-7" />
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900">{{ selectedNotification.title }}</h3>
                <p class="text-sm text-gray-500">{{ formatDate(selectedNotification.created_at) }}</p>
              </div>
            </div>

            <div class="mt-6">
              <p class="text-gray-700 whitespace-pre-line">{{ selectedNotification.message }}</p>
            </div>

            <div v-if="selectedNotification.action_url" class="mt-6">
              <router-link
                :to="transformActionUrl(selectedNotification.action_url)"
                class="inline-flex items-center gap-2 px-4 py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                {{ selectedNotification.action_text || 'Ko\'rish' }}
                <ArrowRightIcon class="w-4 h-4" />
              </router-link>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- Settings modal -->
    <Transition name="modal">
      <div v-if="showSettings" class="fixed inset-0 z-50 overflow-y-auto" @click="showSettings = false">
        <div class="flex items-center justify-center min-h-screen p-4">
          <div class="fixed inset-0 bg-black/50"></div>
          
          <div 
            class="relative bg-white rounded-2xl shadow-xl max-w-md w-full p-6"
            @click.stop
          >
            <div class="flex items-center justify-between mb-6">
              <h3 class="text-lg font-semibold text-gray-900">Bildirishnoma sozlamalari</h3>
              <button
                @click="showSettings = false"
                class="p-2 text-gray-400 hover:text-gray-600 rounded-lg hover:bg-gray-100"
              >
                <XMarkIcon class="w-5 h-5" />
              </button>
            </div>

            <div class="space-y-4">
              <label class="flex items-center justify-between">
                <div>
                  <p class="font-medium text-gray-900">Topshiriq yangiliklari</p>
                  <p class="text-sm text-gray-500">Yangi topshiriqlar haqida xabar</p>
                </div>
                <input type="checkbox" v-model="settings.assignments" class="toggle" />
              </label>

              <label class="flex items-center justify-between">
                <div>
                  <p class="font-medium text-gray-900">Ball yangiliklari</p>
                  <p class="text-sm text-gray-500">Baholar qo'yilganda xabar</p>
                </div>
                <input type="checkbox" v-model="settings.scores" class="toggle" />
              </label>

              <label class="flex items-center justify-between">
                <div>
                  <p class="font-medium text-gray-900">Muddat eslatmalari</p>
                  <p class="text-sm text-gray-500">Muddatlar yaqinlashganda eslatma</p>
                </div>
                <input type="checkbox" v-model="settings.deadlines" class="toggle" />
              </label>

              <label class="flex items-center justify-between">
                <div>
                  <p class="font-medium text-gray-900">Tizim xabarlari</p>
                  <p class="text-sm text-gray-500">Texnik yangilanishlar haqida</p>
                </div>
                <input type="checkbox" v-model="settings.system" class="toggle" />
              </label>
            </div>

            <div class="mt-6 pt-6 border-t border-gray-200">
              <button
                @click="saveSettings"
                class="w-full py-2 bg-primary-600 text-white rounded-lg hover:bg-primary-700 transition-colors"
              >
                Saqlash
              </button>
            </div>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute } from 'vue-router'
import {
  BellIcon,
  BellAlertIcon,
  BellSlashIcon,
  StarIcon,
  ArchiveBoxIcon,
  MagnifyingGlassIcon,
  CheckIcon,
  Cog6ToothIcon,
  EllipsisVerticalIcon,
  EnvelopeIcon,
  TrashIcon,
  XMarkIcon,
  ArrowRightIcon,
  DocumentTextIcon,
  AcademicCapIcon,
  ClockIcon,
  ExclamationCircleIcon,
  CheckCircleIcon,
  InformationCircleIcon
} from '@heroicons/vue/24/outline'
import { formatDate } from '@/utils/date'
import { useToast } from 'vue-toastification'

const route = useRoute()
const toast = useToast()

// Transform action_url based on current route context
function transformActionUrl(url) {
  if (!url) return url
  
  // Handle /assignments/X paths
  if (url.startsWith('/assignments/')) {
    const id = url.replace('/assignments/', '')
    const path = route.path
    if (path.startsWith('/teacher')) return `/teacher/tasks/${id}`
    if (path.startsWith('/admin-panel')) return `/admin-panel/tasks/${id}`
    if (path.startsWith('/super-admin')) return `/super-admin/tasks/${id}`
    return `/teacher/tasks/${id}`
  }
  
  return url
}

const searchQuery = ref('')
const activeFilter = ref('all')
const openMenuId = ref(null)
const selectedNotification = ref(null)
const showSettings = ref(false)
const hasMore = ref(true)

const settings = ref({
  assignments: true,
  scores: true,
  deadlines: true,
  system: false
})

// Mock notifications
const notifications = ref([
  {
    id: 1,
    type: 'assignment',
    title: 'Yangi topshiriq qo\'shildi',
    message: 'Ilmiy maqola yozish topshirig\'i qo\'shildi. Muddat: 2024-02-15',
    read: false,
    important: true,
    archived: false,
    created_at: new Date().toISOString(),
    action_url: '/assignments/1',
    action_text: 'Topshiriqni ko\'rish'
  },
  {
    id: 2,
    type: 'score',
    title: 'Baholandingiz!',
    message: 'Esse - Ta\'lim metodlari topshirig\'ingiz baholandi. Ball: 45/50 (90%)',
    read: false,
    important: false,
    archived: false,
    created_at: new Date(Date.now() - 1 * 60 * 60 * 1000).toISOString(),
    action_url: '/my-scores',
    action_text: 'Ballarni ko\'rish'
  },
  {
    id: 3,
    type: 'deadline',
    title: 'Muddat yaqinlashmoqda',
    message: 'Loyiha hisoboti topshirig\'ining muddati tugashiga 2 kun qoldi!',
    read: true,
    important: true,
    archived: false,
    created_at: new Date(Date.now() - 3 * 60 * 60 * 1000).toISOString(),
    action_url: '/assignments/2',
    action_text: 'Topshiriqni ko\'rish'
  },
  {
    id: 4,
    type: 'system',
    title: 'Tizim yangilandi',
    message: 'ProFT tizimi yangi funksiyalar bilan yangilandi. Endi siz o\'z portfoliyongizni PDF formatida yuklab olishingiz mumkin.',
    read: true,
    important: false,
    archived: false,
    created_at: new Date(Date.now() - 24 * 60 * 60 * 1000).toISOString()
  },
  {
    id: 5,
    type: 'score',
    title: 'Baholandingiz!',
    message: 'Ilmiy maqola - IT topshirig\'ingiz baholandi. Ball: 88/100 (88%)',
    read: true,
    important: false,
    archived: false,
    created_at: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000).toISOString(),
    action_url: '/my-scores'
  },
  {
    id: 6,
    type: 'info',
    title: 'Yangi kategoriya qo\'shildi',
    message: 'Metodologiya bo\'yicha yangi kategoriya qo\'shildi. Hoziroq portfoliyongizni to\'ldiring!',
    read: true,
    important: false,
    archived: false,
    created_at: new Date(Date.now() - 5 * 24 * 60 * 60 * 1000).toISOString(),
    action_url: '/categories'
  }
])

const filterOptions = computed(() => [
  { value: 'all', label: 'Barchasi', count: notifications.value.filter(n => !n.archived).length },
  { value: 'unread', label: 'O\'qilmagan', count: unreadCount.value },
  { value: 'important', label: 'Muhim', count: importantCount.value },
  { value: 'archived', label: 'Arxiv', count: archivedCount.value }
])

const totalCount = computed(() => notifications.value.length)
const unreadCount = computed(() => notifications.value.filter(n => !n.read && !n.archived).length)
const importantCount = computed(() => notifications.value.filter(n => n.important && !n.archived).length)
const archivedCount = computed(() => notifications.value.filter(n => n.archived).length)

const filteredNotifications = computed(() => {
  let result = [...notifications.value]

  // Filter by active filter
  switch (activeFilter.value) {
    case 'unread':
      result = result.filter(n => !n.read && !n.archived)
      break
    case 'important':
      result = result.filter(n => n.important && !n.archived)
      break
    case 'archived':
      result = result.filter(n => n.archived)
      break
    default:
      result = result.filter(n => !n.archived)
  }

  // Filter by search
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(n => 
      n.title.toLowerCase().includes(query) ||
      n.message.toLowerCase().includes(query)
    )
  }

  // Sort by date (newest first)
  result.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))

  return result
})

function getNotificationIcon(type) {
  switch (type) {
    case 'assignment': return DocumentTextIcon
    case 'score': return AcademicCapIcon
    case 'deadline': return ClockIcon
    case 'system': return ExclamationCircleIcon
    case 'success': return CheckCircleIcon
    default: return InformationCircleIcon
  }
}

function getNotificationIconClass(type) {
  switch (type) {
    case 'assignment': return 'bg-blue-100 text-blue-600'
    case 'score': return 'bg-success-100 text-success-600'
    case 'deadline': return 'bg-warning-100 text-warning-600'
    case 'system': return 'bg-purple-100 text-purple-600'
    case 'success': return 'bg-success-100 text-success-600'
    default: return 'bg-gray-100 text-gray-600'
  }
}

function getNotificationTypeLabel(type) {
  switch (type) {
    case 'assignment': return 'Topshiriq'
    case 'score': return 'Baho'
    case 'deadline': return 'Muddat'
    case 'system': return 'Tizim'
    case 'success': return 'Muvaffaqiyat'
    default: return 'Ma\'lumot'
  }
}

function getNotificationTypeClass(type) {
  switch (type) {
    case 'assignment': return 'bg-blue-100 text-blue-700'
    case 'score': return 'bg-success-100 text-success-700'
    case 'deadline': return 'bg-warning-100 text-warning-700'
    case 'system': return 'bg-purple-100 text-purple-700'
    default: return 'bg-gray-100 text-gray-700'
  }
}

function formatRelativeTime(dateString) {
  const date = new Date(dateString)
  const now = new Date()
  const diffMs = now - date
  const diffMins = Math.floor(diffMs / 60000)
  const diffHours = Math.floor(diffMins / 60)
  const diffDays = Math.floor(diffHours / 24)

  if (diffMins < 1) return 'Hozir'
  if (diffMins < 60) return `${diffMins} daqiqa oldin`
  if (diffHours < 24) return `${diffHours} soat oldin`
  if (diffDays < 7) return `${diffDays} kun oldin`
  return formatDate(dateString)
}

function toggleMenu(id) {
  openMenuId.value = openMenuId.value === id ? null : id
}

function openNotification(notification) {
  selectedNotification.value = notification
  if (!notification.read) {
    markAsRead(notification)
  }
}

function markAsRead(notification) {
  notification.read = true
  openMenuId.value = null
}

function markAsUnread(notification) {
  notification.read = false
  openMenuId.value = null
}

function toggleImportant(notification) {
  notification.important = !notification.important
  openMenuId.value = null
  toast.success(notification.important ? 'Muhim deb belgilandi' : 'Muhimlardan olib tashlandi')
}

function archiveNotification(notification) {
  notification.archived = true
  openMenuId.value = null
  toast.success('Arxivlandi')
}

function deleteNotification(notification) {
  const index = notifications.value.findIndex(n => n.id === notification.id)
  if (index > -1) {
    notifications.value.splice(index, 1)
  }
  openMenuId.value = null
  toast.success('O\'chirildi')
}

function markAllAsRead() {
  notifications.value.forEach(n => n.read = true)
  toast.success('Barcha bildirishnomalar o\'qilgan deb belgilandi')
}

function loadMore() {
  // Load more notifications
  hasMore.value = false
}

function saveSettings() {
  showSettings.value = false
  toast.success('Sozlamalar saqlandi')
}

// Close menu on click outside
function handleClickOutside(e) {
  if (openMenuId.value && !e.target.closest('[data-menu]')) {
    openMenuId.value = null
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.toggle {
  width: 44px;
  height: 24px;
  background-color: #e5e7eb;
  border-radius: 9999px;
  position: relative;
  appearance: none;
  cursor: pointer;
  transition: background-color 0.2s;
}

.toggle::after {
  content: '';
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background: white;
  border-radius: 50%;
  transition: transform 0.2s;
  box-shadow: 0 1px 3px rgba(0,0,0,0.1);
}

.toggle:checked::after {
  transform: translateX(20px);
}

.toggle:checked {
  background-color: #4f46e5;
}

.list-enter-active,
.list-leave-active {
  transition: all 0.3s ease;
}

.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateY(-10px);
}

.dropdown-enter-active,
.dropdown-leave-active {
  transition: all 0.15s ease;
}

.dropdown-enter-from,
.dropdown-leave-to {
  opacity: 0;
  transform: translateY(-5px);
}

.modal-enter-active,
.modal-leave-active {
  transition: all 0.2s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

.modal-enter-from .relative,
.modal-leave-to .relative {
  transform: scale(0.95);
}
</style>
