<template>
  <div class="animate-fade-in">
    <!-- Page header -->
    <div class="mb-6">
      <div class="flex items-center gap-2 text-sm text-gray-500 mb-2">
        <RouterLink to="/profile" class="hover:text-primary-600">Profil</RouterLink>
        <ChevronRightIcon class="w-4 h-4" />
        <span class="text-gray-900">Tahrirlash</span>
      </div>
      <h1 class="text-2xl font-bold text-gray-900">Profilni tahrirlash</h1>
      <p class="mt-1 text-sm text-gray-500">
        Shaxsiy ma'lumotlaringizni yangilang
      </p>
    </div>
    
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
      <!-- Avatar upload card -->
      <div class="card">
        <div class="card-body text-center">
          <div class="relative inline-block">
            <div 
              class="w-32 h-32 mx-auto rounded-full flex items-center justify-center overflow-hidden border-4 border-gray-100"
              :class="avatarPreview ? '' : 'bg-primary-100'"
            >
              <img v-if="avatarPreview" :src="avatarPreview" alt="Avatar" class="w-full h-full object-cover" />
              <span v-else class="text-4xl font-bold text-primary-600">
                {{ userInitials }}
              </span>
            </div>
            <label 
              class="absolute bottom-0 right-0 w-10 h-10 bg-primary-600 hover:bg-primary-700 rounded-full flex items-center justify-center cursor-pointer shadow-lg transition-colors"
            >
              <CameraIcon class="w-5 h-5 text-white" />
              <input 
                type="file" 
                accept="image/*" 
                class="hidden" 
                @change="handleAvatarChange"
              />
            </label>
          </div>
          <p class="text-sm text-gray-500 mt-4">
            JPG, PNG yoki GIF (maks. 5MB)
          </p>
          <button 
            v-if="avatarPreview && avatarPreview !== originalAvatar"
            @click="removeAvatar"
            class="btn-ghost btn-sm text-danger-600 mt-2"
          >
            <TrashIcon class="w-4 h-4 mr-1" />
            Rasmni olib tashlash
          </button>
        </div>
      </div>
      
      <!-- Edit form -->
      <div class="lg:col-span-2 space-y-6">
        <!-- Personal Info -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <UserIcon class="w-5 h-5 text-gray-400" />
              Shaxsiy ma'lumotlar
            </h2>
          </div>
          <div class="card-body space-y-4">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
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
                <p v-if="errors.first_name" class="form-error">{{ errors.first_name }}</p>
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
                <p v-if="errors.last_name" class="form-error">{{ errors.last_name }}</p>
              </div>
            </div>
            
            <!-- Email (read-only from Hemis) -->
            <div>
              <label class="form-label">Email</label>
              <input
                :value="userStore.user?.email"
                type="email"
                class="form-input bg-gray-50"
                disabled
              />
              <p class="text-xs text-gray-400 mt-1">Hemis tizimidan olingan</p>
            </div>
            
            <!-- Phone -->
            <div>
              <label for="phone_number" class="form-label">Telefon raqam</label>
              <div class="relative">
                <PhoneIcon class="w-5 h-5 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" />
                <input
                  id="phone_number"
                  v-model="form.phone_number"
                  type="tel"
                  class="form-input pl-10"
                  placeholder="+998 90 123 45 67"
                />
              </div>
              <p v-if="errors.phone_number" class="form-error">{{ errors.phone_number }}</p>
            </div>
          </div>
        </div>
        
        <!-- Bio -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <DocumentTextIcon class="w-5 h-5 text-gray-400" />
              Biografiya
            </h2>
          </div>
          <div class="card-body">
            <textarea
              v-model="form.bio"
              rows="5"
              class="form-input"
              placeholder="O'zingiz haqingizda qisqacha ma'lumot..."
              maxlength="500"
            ></textarea>
            <p class="text-xs text-gray-400 mt-1 text-right">
              {{ form.bio?.length || 0 }} / 500
            </p>
          </div>
        </div>
        
        <!-- Social Links -->
        <div class="card">
          <div class="card-header">
            <h2 class="text-lg font-semibold text-gray-900 flex items-center gap-2">
              <LinkIcon class="w-5 h-5 text-gray-400" />
              Ijtimoiy tarmoqlar
            </h2>
          </div>
          <div class="card-body space-y-4">
            <!-- Telegram -->
            <div>
              <label class="form-label">Telegram</label>
              <div class="relative">
                <span class="text-gray-400 absolute left-3 top-1/2 -translate-y-1/2">@</span>
                <input
                  v-model="form.telegram"
                  type="text"
                  class="form-input pl-8"
                  placeholder="username"
                />
              </div>
            </div>
            
            <!-- LinkedIn -->
            <div>
              <label class="form-label">LinkedIn</label>
              <input
                v-model="form.linkedin"
                type="url"
                class="form-input"
                placeholder="https://linkedin.com/in/username"
              />
            </div>
            
            <!-- Website -->
            <div>
              <label class="form-label">Shaxsiy veb-sayt</label>
              <input
                v-model="form.website"
                type="url"
                class="form-input"
                placeholder="https://example.com"
              />
            </div>
          </div>
        </div>
        
        <!-- Actions -->
        <div class="flex items-center justify-end gap-4">
          <RouterLink to="/profile" class="btn-secondary">
            Bekor qilish
          </RouterLink>
          <button @click="handleSubmit" class="btn-primary" :disabled="isSubmitting">
            <LoadingSpinner v-if="isSubmitting" size="xs" color="white" class="mr-2" />
            <CheckIcon v-else class="w-5 h-5 mr-2" />
            {{ isSubmitting ? 'Saqlanmoqda...' : 'Saqlash' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useToast } from 'vue-toastification'
import { 
  ChevronRightIcon,
  CameraIcon,
  TrashIcon,
  UserIcon,
  PhoneIcon,
  DocumentTextIcon,
  LinkIcon,
  CheckIcon
} from '@heroicons/vue/24/outline'
import { LoadingSpinner } from '@/components/common'
import { useUserStore } from '@/stores'
import { authService } from '@/services'

const router = useRouter()
const toast = useToast()
const userStore = useUserStore()

const isSubmitting = ref(false)
const avatarPreview = ref(null)
const originalAvatar = ref(null)
const avatarFile = ref(null)
const errors = reactive({})

const form = reactive({
  first_name: '',
  last_name: '',
  phone_number: '',
  bio: '',
  telegram: '',
  linkedin: '',
  website: ''
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
    form.telegram = userStore.user.telegram || ''
    form.linkedin = userStore.user.linkedin || ''
    form.website = userStore.user.website || ''
    
    if (userStore.user.avatar) {
      avatarPreview.value = userStore.user.avatar
      originalAvatar.value = userStore.user.avatar
    }
  }
})

function handleAvatarChange(event) {
  const file = event.target.files[0]
  if (!file) return
  
  // Validate file size (max 5MB)
  if (file.size > 5 * 1024 * 1024) {
    toast.error('Rasm hajmi 5MB dan oshmasligi kerak')
    return
  }
  
  // Validate file type
  if (!['image/jpeg', 'image/png', 'image/gif'].includes(file.type)) {
    toast.error('Faqat JPG, PNG yoki GIF formatdagi rasmlar qabul qilinadi')
    return
  }
  
  avatarFile.value = file
  
  // Create preview
  const reader = new FileReader()
  reader.onload = (e) => {
    avatarPreview.value = e.target.result
  }
  reader.readAsDataURL(file)
}

function removeAvatar() {
  avatarPreview.value = null
  avatarFile.value = null
}

function validateForm() {
  Object.keys(errors).forEach(key => delete errors[key])
  
  if (!form.first_name?.trim()) {
    errors.first_name = 'Ism kiritilishi shart'
  }
  
  if (!form.last_name?.trim()) {
    errors.last_name = 'Familiya kiritilishi shart'
  }
  
  if (form.phone_number && !/^\+?[0-9\s-]{9,}$/.test(form.phone_number)) {
    errors.phone_number = "Noto'g'ri telefon raqam formati"
  }
  
  return Object.keys(errors).length === 0
}

async function handleSubmit() {
  if (!validateForm()) {
    toast.error("Iltimos, xatolarni tuzating")
    return
  }
  
  isSubmitting.value = true
  
  try {
    // Prepare form data
    const formData = new FormData()
    formData.append('first_name', form.first_name)
    formData.append('last_name', form.last_name)
    formData.append('phone_number', form.phone_number || '')
    formData.append('bio', form.bio || '')
    formData.append('telegram', form.telegram || '')
    formData.append('linkedin', form.linkedin || '')
    formData.append('website', form.website || '')
    
    if (avatarFile.value) {
      formData.append('avatar', avatarFile.value)
    } else if (!avatarPreview.value && originalAvatar.value) {
      formData.append('remove_avatar', 'true')
    }
    
    // Update profile
    await userStore.updateProfile({
      first_name: form.first_name,
      last_name: form.last_name,
      phone_number: form.phone_number,
      bio: form.bio,
      telegram: form.telegram,
      linkedin: form.linkedin,
      website: form.website
    })
    
    toast.success('Profil muvaffaqiyatli yangilandi')
    router.push('/profile')
  } catch (error) {
    console.error('Failed to update profile:', error)
    toast.error('Profilni yangilashda xatolik')
  } finally {
    isSubmitting.value = false
  }
}
</script>
