<template>
  <div class="min-h-screen bg-gradient-to-br from-primary-600 to-primary-800 flex flex-col justify-center py-12 sm:px-6 lg:px-8">
    <!-- Logo -->
    <div class="sm:mx-auto sm:w-full sm:max-w-md">
      <div class="flex justify-center">
        <div class="w-16 h-16 bg-white rounded-2xl shadow-lg flex items-center justify-center">
          <span class="text-primary-600 font-bold text-3xl">P</span>
        </div>
      </div>
      <h2 class="mt-6 text-center text-3xl font-bold text-white">
        Proft
      </h2>
      <p class="mt-2 text-center text-sm text-primary-200">
        Professional Portfolio Management System
      </p>
    </div>
    
    <!-- Content -->
    <div class="mt-8 sm:mx-auto sm:w-full sm:max-w-md">
      <div class="bg-white py-8 px-4 shadow-xl rounded-2xl sm:px-10">
        <RouterView />
      </div>
    </div>
    
    <!-- Footer -->
    <div class="mt-8 text-center text-sm text-primary-200">
      &copy; 2026 Proft. Barcha huquqlar himoyalangan.
    </div>
  </div>
</template>

<script setup>
</script>
