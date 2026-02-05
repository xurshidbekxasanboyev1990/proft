<template>
  <BaseModal :is-open="isOpen" title="Bulk ball yangilash" size="lg" @close="$emit('close')">
    <div class="space-y-6">
      <!-- Selected assignments info -->
      <div class="p-4 bg-primary-50 rounded-lg">
        <div class="flex items-center gap-3">
          <div class="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
            <DocumentDuplicateIcon class="w-5 h-5 text-primary-600" />
          </div>
          <div>
            <p class="font-medium text-primary-900">{{ selectedCount }} ta topshiriq tanlandi</p>
            <p class="text-sm text-primary-700">Quyidagi sozlamalar barcha tanlangan topshiriqlarga qo'llanadi</p>
          </div>
        </div>
      </div>

      <!-- Preset actions -->
      <div>
        <label class="form-label">Tezkor amallar</label>
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
          <button
            v-for="preset in presets"
            :key="preset.id"
            type="button"
            @click="applyPreset(preset)"
            :class="[
              'p-4 rounded-lg border-2 text-center transition-all',
              activePreset === preset.id
                ? 'border-primary-500 bg-primary-50'
                : 'border-gray-200 hover:border-primary-300'
            ]"
          >
            <component :is="preset.icon" class="w-6 h-6 mx-auto mb-2" :class="preset.iconColor" />
            <p class="text-sm font-medium text-gray-900">{{ preset.label }}</p>
            <p class="text-xs text-gray-500 mt-1">{{ preset.description }}</p>
          </button>
        </div>
      </div>

      <div class="border-t border-gray-200 pt-6">
        <p class="text-sm font-medium text-gray-700 mb-4">Yoki maxsus sozlamalar:</p>

        <!-- Custom max score -->
        <div class="grid grid-cols-2 gap-4">
          <div>
            <label class="form-label">Maksimal ball</label>
            <input
              v-model.number="form.custom_max_score"
              type="number"
              min="1"
              max="1000"
              class="form-input"
              placeholder="O'zgartirmaslik"
            />
          </div>

          <!-- Score multiplier -->
          <div>
            <label class="form-label">Ball ko'paytiruvchi</label>
            <div class="flex items-center gap-2">
              <input
                v-model.number="form.score_multiplier"
                type="number"
                min="0.1"
                max="10"
                step="0.1"
                class="form-input"
                placeholder="1.0"
              />
              <span class="text-gray-500">x</span>
            </div>
          </div>
        </div>

        <!-- Score note -->
        <div class="mt-4">
          <label class="form-label">Izoh (ixtiyoriy)</label>
          <textarea
            v-model="form.score_note"
            rows="2"
            class="form-input"
            placeholder="Bu o'zgarish haqida izoh..."
          ></textarea>
        </div>
      </div>

      <!-- Preview -->
      <div v-if="hasChanges" class="p-4 bg-warning-50 border border-warning-200 rounded-lg">
        <div class="flex items-start gap-3">
          <ExclamationTriangleIcon class="w-5 h-5 text-warning-600 flex-shrink-0 mt-0.5" />
          <div>
            <p class="font-medium text-warning-800">O'zgarishlar:</p>
            <ul class="text-sm text-warning-700 mt-1 space-y-1">
              <li v-if="form.custom_max_score">• Maksimal ball: {{ form.custom_max_score }}</li>
              <li v-if="form.score_multiplier && form.score_multiplier !== 1">• Ko'paytiruvchi: {{ form.score_multiplier }}x</li>
              <li v-if="form.score_note">• Izoh qo'shiladi</li>
            </ul>
          </div>
        </div>
      </div>
    </div>

    <template #footer>
      <button @click="$emit('close')" class="btn-secondary" :disabled="isSubmitting">
        Bekor qilish
      </button>
      <button 
        @click="handleSubmit" 
        class="btn-primary" 
        :disabled="!hasChanges || isSubmitting"
      >
        <LoadingSpinner v-if="isSubmitting" size="xs" color="white" />
        <span v-else>{{ selectedCount }} ta topshiriqni yangilash</span>
      </button>
    </template>
  </BaseModal>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { 
  DocumentDuplicateIcon,
  SparklesIcon,
  ArrowPathIcon,
  RocketLaunchIcon,
  GiftIcon,
  ExclamationTriangleIcon
} from '@heroicons/vue/24/outline'
import { BaseModal, LoadingSpinner } from '@/components/common'
import { assignmentService } from '@/services'
import { useToast } from 'vue-toastification'

const props = defineProps({
  isOpen: {
    type: Boolean,
    required: true
  },
  selectedAssignments: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'updated'])

const toast = useToast()

const isSubmitting = ref(false)
const activePreset = ref(null)

const form = reactive({
  custom_max_score: null,
  score_multiplier: null,
  score_note: ''
})

const presets = [
  {
    id: '2x_bonus',
    label: '2x Bonus',
    description: 'Ikki baravar ball',
    icon: SparklesIcon,
    iconColor: 'text-warning-600',
    values: { score_multiplier: 2, score_note: '2x bonus qo\'llanildi' }
  },
  {
    id: '1.5x_bonus',
    label: '1.5x Bonus',
    description: 'Yarim qo\'shimcha',
    icon: GiftIcon,
    iconColor: 'text-success-600',
    values: { score_multiplier: 1.5, score_note: '1.5x bonus qo\'llanildi' }
  },
  {
    id: 'reset',
    label: 'Standart',
    description: 'Asl holatga',
    icon: ArrowPathIcon,
    iconColor: 'text-gray-600',
    values: { score_multiplier: 1, score_note: 'Standart holatga qaytarildi' }
  },
  {
    id: 'max_100',
    label: '100 ball',
    description: 'Maks ballni 100 qilish',
    icon: RocketLaunchIcon,
    iconColor: 'text-primary-600',
    values: { custom_max_score: 100, score_note: 'Maksimal ball 100 ga o\'rnatildi' }
  }
]

const selectedCount = computed(() => props.selectedAssignments.length)

const hasChanges = computed(() => {
  return form.custom_max_score || (form.score_multiplier && form.score_multiplier !== 1) || form.score_note
})

watch(() => props.isOpen, (isOpen) => {
  if (isOpen) {
    // Reset form
    form.custom_max_score = null
    form.score_multiplier = null
    form.score_note = ''
    activePreset.value = null
  }
})

function applyPreset(preset) {
  activePreset.value = preset.id
  if (preset.values.custom_max_score) {
    form.custom_max_score = preset.values.custom_max_score
  }
  if (preset.values.score_multiplier) {
    form.score_multiplier = preset.values.score_multiplier
  }
  if (preset.values.score_note) {
    form.score_note = preset.values.score_note
  }
}

async function handleSubmit() {
  if (!hasChanges.value || selectedCount.value === 0) return

  isSubmitting.value = true
  try {
    const data = {
      assignment_ids: props.selectedAssignments.map(a => a.id)
    }

    if (form.custom_max_score) {
      data.custom_max_score = form.custom_max_score
    }
    if (form.score_multiplier && form.score_multiplier !== 1) {
      data.score_multiplier = form.score_multiplier
    }
    if (form.score_note) {
      data.score_note = form.score_note
    }

    await assignmentService.bulkScoreUpdate(data)
    
    toast.success(`${selectedCount.value} ta topshiriq muvaffaqiyatli yangilandi`)
    emit('updated')
    emit('close')
  } catch (error) {
    console.error('Bulk update failed:', error)
    toast.error('Yangilashda xatolik yuz berdi')
  } finally {
    isSubmitting.value = false
  }
}
</script>
