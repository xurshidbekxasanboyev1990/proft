<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900">Foydalanuvchilar</h1>
        <p class="mt-1 text-sm text-gray-500">
          Tizim foydalanuvchilarini boshqarish
        </p>
      </div>
      <RouterLink to="/admin/users/new" class="btn-primary">
        <PlusIcon class="w-5 h-5 mr-2" />
        Yangi foydalanuvchi
      </RouterLink>
    </div>
    
    <!-- Stats row -->
    <div class="grid grid-cols-2 md:grid-cols-4 gap-4 mb-6">
      <StatsCard
        title="Jami"
        :value="stats.total"
        icon="users"
        color="gray"
      />
      <StatsCard
        title="Super adminlar"
        :value="stats.superadmin"
        icon="shield"
        color="purple"
      />
      <StatsCard
        title="Adminlar"
        :value="stats.admin"
        icon="user-group"
        color="blue"
      />
      <StatsCard
        title="O'qituvchilar"
        :value="stats.teacher"
        icon="academic-cap"
        color="green"
      />
    </div>
    
    <!-- Filters -->
    <div class="card mb-6">
      <div class="card-body">
        <div class="grid grid-cols-1 sm:grid-cols-4 gap-4">
          <!-- Search -->
          <div class="sm:col-span-2">
            <div class="relative">
              <MagnifyingGlassIcon class="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                v-model="filters.search"
                type="text"
                placeholder="Qidirish (ism, username, email)..."
                class="form-input pl-10"
                @input="debouncedSearch"
              />
            </div>
          </div>
          
          <!-- Role filter -->
          <select v-model="filters.role" @change="applyFilters" class="form-input">
            <option value="">Barcha rollar</option>
            <option value="superadmin">Super Admin</option>
            <option value="admin">Admin</option>
            <option value="teacher">O'qituvchi</option>
          </select>
          
          <!-- Status filter -->
          <select v-model="filters.is_active" @change="applyFilters" class="form-input">
            <option value="">Barcha statuslar</option>
            <option value="true">Faol</option>
            <option value="false">Nofaol</option>
          </select>
        </div>
      </div>
    </div>
    
    <!-- Loading state -->
    <div v-if="isLoading" class="space-y-4">
      <SkeletonLoader v-for="i in 5" :key="i" type="table-row" />
    </div>
    
    <!-- Users table -->
    <div v-else-if="users.length > 0" class="card">
      <div class="table-container">
        <table class="table">
          <thead>
            <tr>
              <th>Foydalanuvchi</th>
              <th>Rol</th>
              <th>Bo'lim</th>
              <th>Status</th>
              <th>Oxirgi faollik</th>
              <th class="text-right">Amallar</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200 bg-white">
            <tr v-for="user in users" :key="user.id">
              <td>
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full flex items-center justify-center text-white font-medium"
                       :class="getRoleColor(user.role)">
                    {{ getUserInitials(user) }}
                  </div>
                  <div>
                    <p class="font-medium text-gray-900">{{ user.full_name || user.username }}</p>
                    <p class="text-xs text-gray-500">{{ user.email || user.username }}</p>
                  </div>
                </div>
              </td>
              <td>
                <StatusBadge :variant="user.role" size="sm">
                  {{ getRoleDisplay(user.role) }}
                </StatusBadge>
              </td>
              <td>
                <span class="text-sm text-gray-600">{{ user.department || '-' }}</span>
              </td>
              <td>
                <span 
                  class="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium"
                  :class="user.is_active ? 'bg-success-100 text-success-700' : 'bg-gray-100 text-gray-600'"
                >
                  <span class="w-1.5 h-1.5 rounded-full mr-1.5"
                        :class="user.is_active ? 'bg-success-500' : 'bg-gray-400'"></span>
                  {{ user.is_active ? 'Faol' : 'Nofaol' }}
                </span>
              </td>
              <td>
                <span class="text-sm text-gray-500">{{ formatDate(user.last_activity) }}</span>
              </td>
              <td class="text-right">
                <Menu as="div" class="relative inline-block text-left">
                  <MenuButton class="p-2 text-gray-400 hover:text-gray-600 rounded-md hover:bg-gray-100">
                    <EllipsisVerticalIcon class="w-5 h-5" />
                  </MenuButton>
                  <transition
                    enter-active-class="transition duration-100 ease-out"
                    enter-from-class="transform scale-95 opacity-0"
                    enter-to-class="transform scale-100 opacity-100"
                    leave-active-class="transition duration-75 ease-in"
                    leave-from-class="transform scale-100 opacity-100"
                    leave-to-class="transform scale-95 opacity-0"
                  >
                    <MenuItems class="absolute right-0 mt-2 w-48 bg-white border border-gray-200 rounded-lg shadow-lg z-10">
                      <div class="py-1">
                        <MenuItem v-slot="{ active }">
                          <RouterLink
                            :to="`/admin/users/${user.id}/edit`"
                            :class="[active ? 'bg-gray-50' : '', 'flex items-center px-4 py-2 text-sm text-gray-700']"
                          >
                            <PencilIcon class="w-4 h-4 mr-2" />
                            Tahrirlash
                          </RouterLink>
                        </MenuItem>
                        <MenuItem v-if="user.role === 'teacher'" v-slot="{ active }">
                          <RouterLink
                            :to="`/admin/users/${user.id}/portfolios`"
                            :class="[active ? 'bg-gray-50' : '', 'flex items-center px-4 py-2 text-sm text-gray-700']"
                          >
                            <FolderIcon class="w-4 h-4 mr-2" />
                            Portfoliolar
                          </RouterLink>
                        </MenuItem>
                        <MenuItem v-slot="{ active }">
                          <button
                            @click="toggleUserStatus(user)"
                            :class="[active ? 'bg-gray-50' : '', 'flex items-center w-full px-4 py-2 text-sm text-gray-700']"
                          >
                            <template v-if="user.is_active">
                              <NoSymbolIcon class="w-4 h-4 mr-2" />
                              Nofaol qilish
                            </template>
                            <template v-else>
                              <CheckCircleIcon class="w-4 h-4 mr-2" />
                              Faollashtirish
                            </template>
                          </button>
                        </MenuItem>
                        <MenuItem v-slot="{ active }">
                          <button
                            @click="openDeleteModal(user)"
                            :class="[active ? 'bg-red-50' : '', 'flex items-center w-full px-4 py-2 text-sm text-danger-600']"
                          >
                            <TrashIcon class="w-4 h-4 mr-2" />
                            O'chirish
                          </button>
                        </MenuItem>
                      </div>
                    </MenuItems>
                  </transition>
                </Menu>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      
      <!-- Pagination -->
      <Pagination
        :current-page="pagination.page"
        :total-pages="pagination.total_pages"
        :total-count="pagination.total_count"
        :page-size="pagination.page_size"
        :has-next="pagination.has_next"
        :has-previous="pagination.has_previous"
        @page-change="handlePageChange"
      />
    </div>
    
    <!-- Empty state -->
    <EmptyState 
      v-else
      title="Foydalanuvchi topilmadi"
      description="Qidiruv natijasi bo'sh"
      type="user"
    />
    
    <!-- Delete confirmation modal -->
    <ConfirmModal
      :is-open="showDeleteModal"
      title="Foydalanuvchini o'chirish"
      :message="`${selectedUser?.full_name || selectedUser?.username} foydalanuvchisini o'chirishga ishonchingiz komilmi? Bu amal qaytarilmaydi.`"
      type="danger"
      confirm-text="O'chirish"
      :is-loading="isDeleting"
      @confirm="confirmDelete"
      @cancel="showDeleteModal = false"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { Menu, MenuButton, MenuItem, MenuItems } from '@headlessui/vue'
import { 
  PlusIcon, 
  MagnifyingGlassIcon,
  EllipsisVerticalIcon,
  PencilIcon,
  FolderIcon,
  TrashIcon,
  NoSymbolIcon,
  CheckCircleIcon
} from '@heroicons/vue/24/outline'
import { SkeletonLoader, StatusBadge, Pagination, EmptyState, ConfirmModal, StatsCard } from '@/components/common'
import { useUserStore } from '@/stores'
import dayjs from 'dayjs'

const userStore = useUserStore()

const isLoading = ref(true)
const users = ref([])
const pagination = ref({
  page: 1,
  page_size: 20,
  total_count: 0,
  total_pages: 1,
  has_next: false,
  has_previous: false
})
const stats = ref({
  total: 0,
  superadmin: 0,
  admin: 0,
  teacher: 0
})

const filters = reactive({
  search: '',
  role: '',
  is_active: ''
})

const showDeleteModal = ref(false)
const selectedUser = ref(null)
const isDeleting = ref(false)

let searchTimeout = null

onMounted(async () => {
  await fetchUsers()
  await fetchStats()
})

async function fetchUsers() {
  isLoading.value = true
  try {
    const params = {
      page: pagination.value.page,
      search: filters.search,
      role: filters.role,
      is_active: filters.is_active
    }
    
    // Remove empty params
    Object.keys(params).forEach(key => {
      if (!params[key]) delete params[key]
    })
    
    const response = await userStore.fetchUsers(params)
    if (response) {
      users.value = response.results || []
      pagination.value = {
        page: response.page || 1,
        page_size: response.page_size || 20,
        total_count: response.count || 0,
        total_pages: response.total_pages || 1,
        has_next: response.has_next || false,
        has_previous: response.has_previous || false
      }
    }
  } catch (error) {
    console.error('Failed to fetch users:', error)
  } finally {
    isLoading.value = false
  }
}

async function fetchStats() {
  try {
    const response = await userStore.fetchUserStats()
    if (response) {
      stats.value = response
    }
  } catch (error) {
    console.error('Failed to fetch user stats:', error)
  }
}

function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    applyFilters()
  }, 300)
}

function applyFilters() {
  pagination.value.page = 1
  fetchUsers()
}

function handlePageChange(page) {
  pagination.value.page = page
  fetchUsers()
}

function getRoleColor(role) {
  const colors = {
    superadmin: 'bg-purple-600',
    admin: 'bg-blue-600',
    teacher: 'bg-green-600'
  }
  return colors[role] || 'bg-gray-600'
}

function getRoleDisplay(role) {
  const roles = {
    superadmin: 'Super Admin',
    admin: 'Admin',
    teacher: "O'qituvchi"
  }
  return roles[role] || role
}

function getUserInitials(user) {
  const name = user.full_name || user.username
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
}

function formatDate(date) {
  if (!date) return 'Hech qachon'
  return dayjs(date).format('D MMM, HH:mm')
}

async function toggleUserStatus(user) {
  try {
    await userStore.updateUser(user.id, { is_active: !user.is_active })
    await fetchUsers()
    await fetchStats()
  } catch (error) {
    console.error('Failed to toggle user status:', error)
  }
}

function openDeleteModal(user) {
  selectedUser.value = user
  showDeleteModal.value = true
}

async function confirmDelete() {
  if (!selectedUser.value) return
  
  isDeleting.value = true
  try {
    await userStore.deleteUser(selectedUser.value.id)
    showDeleteModal.value = false
    selectedUser.value = null
    await fetchUsers()
    await fetchStats()
  } catch (error) {
    console.error('Failed to delete user:', error)
  } finally {
    isDeleting.value = false
  }
}
</script>
