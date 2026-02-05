<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 mb-6">
      <div>
        <h1 class="text-2xl font-bold text-gray-900 dark:text-white">Profil</h1>
        <p class="mt-1 text-sm text-gray-500 dark:text-gray-400">
          Shaxsiy ma'lumotlaringizni ko'ring va tahrirlang
        </p>
      </div>
      <RouterLink to="/profile/edit" class="btn-primary">
        <PencilSquareIcon class="w-5 h-5 mr-2" />
        Tahrirlash
      </RouterLink>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Profile card -->
      <div class="card">
        <div class="card-body text-center">
          <div class="w-24 h-24 mx-auto bg-primary-100 rounded-full flex items-center justify-center mb-4">
            <span class="text-3xl font-bold text-primary-600">
              {{ userInitials }}
            </span>
          </div>
          <h2 class="text-xl font-semibold text-gray-900">{{ userStore.fullName }}</h2>
          <p class="text-sm text-gray-500 mb-3">{{ userStore.user?.email || 'Email ko\'rsatilmagan' }}</p>
          <StatusBadge :variant="userStore.role" size="lg">
            {{ getRoleDisplay(userStore.role) }}
          </StatusBadge>
        </div>
      </div>
      
      <!-- Edit form -->
      <div class="lg:col-span-2">
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Shaxsiy ma'lumotlar</h2>
          </div>
          <form @submit.prevent="handleSubmit" class="card-body space-y-6">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
              <!-- First name -->
              <div>
                <label for="first_name" class="form-label">Ism</label>
                <input
                  id="first_name"
                  v-model="form.first_name"
                  type="text"
                  class="form-input"
                  placeholder="Ismingiz"
                />
              </div>
              
              <!-- Last name -->
              <div>
                <label for="last_name" class="form-label">Familiya</label>
                <input
                  id="last_name"
                  v-model="form.last_name"
                  type="text"
                  class="form-input"
                  placeholder="Familiyangiz"
                />
              </div>
            </div>
            
            <!-- Phone -->
            <div>
              <label for="phone_number" class="form-label">Telefon raqam</label>
              <input
                id="phone_number"
                v-model="form.phone_number"
                type="tel"
                class="form-input"
                placeholder="+998 90 123 45 67"
              />
            </div>
            
            <!-- Bio -->
            <div>
              <label for="bio" class="form-label">Biografiya</label>
              <textarea
                id="bio"
                v-model="form.bio"
                rows="4"
                class="form-input"
                placeholder="O'zingiz haqingizda qisqacha..."
              ></textarea>
            </div>
            
            <!-- Actions -->
            <div class="flex items-center justify-end gap-4 pt-4 border-t border-gray-200">
              <button type="button" @click="resetForm" class="btn-secondary">
                Bekor qilish
              </button>
              <button type="submit" class="btn-primary" :disabled="isSubmitting">
                <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
                <span v-else>Saqlash</span>
              </button>
            </div>
          </form>
        </div>
        
        <!-- Account info (read-only) -->
        <div class="card mt-6">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900">Hisob ma'lumotlari</h2>
          </div>
          <div class="card-body space-y-4">
            <div class="flex justify-between items-center py-2 border-b border-gray-100">
              <span class="text-sm text-gray-500">Username</span>
              <span class="text-sm font-medium text-gray-900">{{ userStore.user?.username }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-gray-100">
              <span class="text-sm text-gray-500">Email</span>
              <span class="text-sm font-medium text-gray-900">{{ userStore.user?.email || '-' }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-gray-100">
              <span class="text-sm text-gray-500">Hemis ID</span>
              <span class="text-sm font-medium text-gray-900">{{ userStore.user?.hemis_id || '-' }}</span>
            </div>
            <div class="flex justify-between items-center py-2 border-b border-gray-100">
              <span class="text-sm text-gray-500">Bo'lim</span>
              <span class="text-sm font-medium text-gray-900">{{ userStore.user?.department || '-' }}</span>
            </div>
            <div class="flex justify-between items-center py-2">
              <span class="text-sm text-gray-500">Lavozim</span>
              <span class="text-sm font-medium text-gray-900">{{ userStore.user?.position || '-' }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { PencilSquareIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner, StatusBadge } from '@/components/common'
import { useUserStore } from '@/stores'

const userStore = useUserStore()

const isSubmitting = ref(false)

const form = reactive({
  first_name: '',
  last_name: '',
  phone_number: '',
  bio: ''
})

const userInitials = computed(() => {
  const name = userStore.fullName
  if (!name) return '?'
  const parts = name.split(' ')
  if (parts.length >= 2) {
    return (parts[0][0] + parts[1][0]).toUpperCase()
  }
  return name.substring(0, 2).toUpperCase()
})

onMounted(() => {
  if (userStore.user) {
    form.first_name = userStore.user.first_name || ''
    form.last_name = userStore.user.last_name || ''
    form.phone_number = userStore.user.phone_number || ''
    form.bio = userStore.user.bio || ''
  }
})

function getRoleDisplay(role) {
  const roles = {
    superadmin: 'Super Admin',
    admin: 'Admin',
    teacher: "O'qituvchi"
  }
  return roles[role] || role
}

function resetForm() {
  if (userStore.user) {
    form.first_name = userStore.user.first_name || ''
    form.last_name = userStore.user.last_name || ''
    form.phone_number = userStore.user.phone_number || ''
    form.bio = userStore.user.bio || ''
  }
}

async function handleSubmit() {
  isSubmitting.value = true
  try {
    await userStore.updateProfile({
      first_name: form.first_name,
      last_name: form.last_name,
      phone_number: form.phone_number,
      bio: form.bio
    })
  } catch (error) {
    console.error('Failed to update profile:', error)
  } finally {
    isSubmitting.value = false
  }
}
</script>
