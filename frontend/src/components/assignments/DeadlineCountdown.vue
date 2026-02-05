<template>
  <div 
    class="flex items-center gap-2 px-3 py-2 rounded-lg text-sm"
    :class="containerClass"
  >
    <ClockIcon class="w-4 h-4 flex-shrink-0" />
    <span class="font-medium">{{ displayText }}</span>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { ClockIcon } from '@heroicons/vue/24/outline'
import dayjs from 'dayjs'
import duration from 'dayjs/plugin/duration'
import relativeTime from 'dayjs/plugin/relativeTime'
import 'dayjs/locale/uz'

dayjs.extend(duration)
dayjs.extend(relativeTime)
dayjs.locale('uz')

const props = defineProps({
  deadline: {
    type: String,
    required: true
  }
})

const now = ref(dayjs())
let interval = null

onMounted(() => {
  interval = setInterval(() => {
    now.value = dayjs()
  }, 60000) // Update every minute
})

onUnmounted(() => {
  if (interval) clearInterval(interval)
})

const deadlineDate = computed(() => dayjs(props.deadline))

const diff = computed(() => {
  return deadlineDate.value.diff(now.value)
})

const isOverdue = computed(() => diff.value < 0)

const displayText = computed(() => {
  if (isOverdue.value) {
    const absDiff = Math.abs(diff.value)
    const d = dayjs.duration(absDiff)
    if (d.asDays() >= 1) {
      return `${Math.floor(d.asDays())} kun oldin tugagan`
    } else if (d.asHours() >= 1) {
      return `${Math.floor(d.asHours())} soat oldin tugagan`
    } else {
      return `${Math.floor(d.asMinutes())} daqiqa oldin tugagan`
    }
  } else {
    const d = dayjs.duration(diff.value)
    if (d.asDays() >= 1) {
      return `${Math.floor(d.asDays())} kun ${Math.floor(d.hours())} soat qoldi`
    } else if (d.asHours() >= 1) {
      return `${Math.floor(d.asHours())} soat ${Math.floor(d.minutes())} daqiqa qoldi`
    } else {
      return `${Math.floor(d.asMinutes())} daqiqa qoldi`
    }
  }
})

const containerClass = computed(() => {
  if (isOverdue.value) {
    return 'bg-danger-50 text-danger-700'
  }
  
  const hours = dayjs.duration(diff.value).asHours()
  if (hours < 24) {
    return 'bg-warning-50 text-warning-700'
  } else if (hours < 72) {
    return 'bg-orange-50 text-orange-700'
  }
  return 'bg-gray-50 text-gray-600'
})
</script>
