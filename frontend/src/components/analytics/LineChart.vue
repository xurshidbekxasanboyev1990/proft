<template>
  <Line :data="chartData" :options="chartOptions" />
</template>

<script setup>
import { computed } from 'vue'
import { Line } from 'vue-chartjs'
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
} from 'chart.js'

ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
  Filler
)

const props = defineProps({
  data: {
    type: Object,
    required: true
  },
  title: {
    type: String,
    default: ''
  },
  showLegend: {
    type: Boolean,
    default: true
  },
  fill: {
    type: Boolean,
    default: true
  }
})

const chartData = computed(() => ({
  labels: props.data.labels || [],
  datasets: (props.data.datasets || []).map((dataset, index) => ({
    ...dataset,
    fill: props.fill,
    tension: 0.4,
    borderColor: dataset.borderColor || getColor(index),
    backgroundColor: props.fill 
      ? (dataset.backgroundColor || getColorWithOpacity(index, 0.1)) 
      : 'transparent',
    pointBackgroundColor: dataset.pointBackgroundColor || getColor(index),
    pointBorderColor: '#fff',
    pointBorderWidth: 2,
    pointRadius: 4,
    pointHoverRadius: 6
  }))
}))

const chartOptions = computed(() => ({
  responsive: true,
  maintainAspectRatio: false,
  plugins: {
    legend: {
      display: props.showLegend,
      position: 'top',
      labels: {
        usePointStyle: true,
        padding: 20
      }
    },
    title: {
      display: !!props.title,
      text: props.title,
      font: {
        size: 16,
        weight: 'bold'
      }
    },
    tooltip: {
      mode: 'index',
      intersect: false,
      backgroundColor: 'rgba(0, 0, 0, 0.8)',
      titleFont: { size: 14 },
      bodyFont: { size: 13 },
      padding: 12,
      cornerRadius: 8
    }
  },
  scales: {
    x: {
      grid: {
        display: false
      }
    },
    y: {
      beginAtZero: true,
      grid: {
        color: 'rgba(0, 0, 0, 0.05)'
      }
    }
  },
  interaction: {
    mode: 'nearest',
    axis: 'x',
    intersect: false
  }
}))

const colors = [
  '#6366F1', // primary
  '#22C55E', // success
  '#F59E0B', // warning
  '#EF4444', // danger
  '#8B5CF6', // purple
  '#EC4899', // pink
  '#06B6D4', // cyan
  '#14B8A6'  // teal
]

function getColor(index) {
  return colors[index % colors.length]
}

function getColorWithOpacity(index, opacity) {
  const hex = getColor(index)
  const r = parseInt(hex.slice(1, 3), 16)
  const g = parseInt(hex.slice(3, 5), 16)
  const b = parseInt(hex.slice(5, 7), 16)
  return `rgba(${r}, ${g}, ${b}, ${opacity})`
}
</script>
