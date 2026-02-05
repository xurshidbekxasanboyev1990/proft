<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="mb-6">
      <RouterLink to="/admin/users" class="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-2">
        <ArrowLeftIcon class="w-4 h-4 mr-1" />
        Orqaga
      </RouterLink>
      <h1 class="text-2xl font-bold text-gray-900">Yangi foydalanuvchi</h1>
      <p class="mt-1 text-sm text-gray-500">
        Tizimga yangi foydalanuvchi qo'shing
      </p>
    </div>
    
    <div class="max-w-2xl">
      <div class="card">
        <form @submit.prevent="handleSubmit" class="card-body space-y-6">
          <AlertBox v-if="error" type="error" :message="error" @close="error = null" />
          
          <!-- Username -->
          <div>
            <label for="username" class="form-label">Username <span class="text-danger-500">*</span></label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-input"
              :class="{ 'border-danger-500': errors.username }"
              placeholder="username"
            />
            <p v-if="errors.username" class="form-error">{{ errors.username }}</p>
          </div>
          
          <!-- Email -->
          <div>
            <label for="email" class="form-label">Email</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-input"
              :class="{ 'border-danger-500': errors.email }"
              placeholder="email@example.com"
            />
            <p v-if="errors.email" class="form-error">{{ errors.email }}</p>
          </div>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <!-- First name -->
            <div>
              <label for="first_name" class="form-label">Ism</label>
              <input
                id="first_name"
                v-model="form.first_name"
                type="text"
                class="form-input"
                placeholder="Ism"
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
                placeholder="Familiya"
              />
            </div>
          </div>
          
          <!-- Role -->
          <div>
            <label for="role" class="form-label">Rol <span class="text-danger-500">*</span></label>
            <select 
              id="role" 
              v-model="form.role" 
              class="form-input"
              :class="{ 'border-danger-500': errors.role }"
            >
              <option value="">Rolni tanlang</option>
              <option value="superadmin">Super Admin</option>
              <option value="admin">Admin</option>
              <option value="teacher">O'qituvchi</option>
            </select>
            <p v-if="errors.role" class="form-error">{{ errors.role }}</p>
          </div>
          
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6">
            <!-- Department -->
            <div>
              <label for="department" class="form-label">Bo'lim</label>
              <input
                id="department"
                v-model="form.department"
                type="text"
                class="form-input"
                placeholder="Bo'lim nomi"
              />
            </div>
            
            <!-- Position -->
            <div>
              <label for="position" class="form-label">Lavozim</label>
              <input
                id="position"
                v-model="form.position"
                type="text"
                class="form-input"
                placeholder="Lavozim"
              />
            </div>
          </div>
          
          <!-- Password -->
          <div>
            <label for="password" class="form-label">Parol <span class="text-danger-500">*</span></label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              class="form-input"
              :class="{ 'border-danger-500': errors.password }"
              placeholder="••••••••"
            />
            <p v-if="errors.password" class="form-error">{{ errors.password }}</p>
            <p class="form-helper">Kamida 8 belgidan iborat bo'lishi kerak</p>
          </div>
          
          <!-- Is active -->
          <div class="flex items-center">
            <input
              id="is_active"
              v-model="form.is_active"
              type="checkbox"
              class="w-4 h-4 text-primary-600 border-gray-300 rounded focus:ring-primary-500"
            />
            <label for="is_active" class="ml-2 text-sm text-gray-700">Faol foydalanuvchi</label>
          </div>
          
          <!-- Actions -->
          <div class="flex items-center justify-end gap-4 pt-4 border-t border-gray-200">
            <RouterLink to="/admin/users" class="btn-secondary">Bekor qilish</RouterLink>
            <button type="submit" class="btn-primary" :disabled="isSubmitting">
              <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
              <span v-else>Yaratish</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ArrowLeftIcon } from '@heroicons/vue/24/outline'
import { LoadingSpinner, AlertBox } from '@/components/common'
import { useUserStore } from '@/stores'

const router = useRouter()
const userStore = useUserStore()

const isSubmitting = ref(false)
const error = ref(null)
const errors = reactive({
  username: null,
  email: null,
  role: null,
  password: null
})

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  role: '',
  department: '',
  position: '',
  password: '',
  is_active: true
})

function validateForm() {
  let isValid = true
  
  // Reset errors
  Object.keys(errors).forEach(key => errors[key] = null)
  
  if (!form.username.trim()) {
    errors.username = 'Username kiritish majburiy'
    isValid = false
  }
  
  if (form.email && !isValidEmail(form.email)) {
    errors.email = 'Email formati noto\'g\'ri'
    isValid = false
  }
  
  if (!form.role) {
    errors.role = 'Rolni tanlash majburiy'
    isValid = false
  }
  
  if (!form.password || form.password.length < 8) {
    errors.password = 'Parol kamida 8 belgidan iborat bo\'lishi kerak'
    isValid = false
  }
  
  return isValid
}

function isValidEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)
}

async function handleSubmit() {
  if (!validateForm()) return
  
  isSubmitting.value = true
  error.value = null
  
  try {
    await userStore.createUser(form)
    router.push('/admin/users')
  } catch (err) {
    error.value = err.response?.data?.detail || 'Foydalanuvchi yaratishda xatolik yuz berdi'
    
    // Handle field-specific errors
    if (err.response?.data) {
      const data = err.response.data
      if (data.username) errors.username = data.username[0]
      if (data.email) errors.email = data.email[0]
      if (data.password) errors.password = data.password[0]
    }
  } finally {
    isSubmitting.value = false
  }
}
</script>
