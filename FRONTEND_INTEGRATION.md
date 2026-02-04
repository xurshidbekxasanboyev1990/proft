# Frontend Integration Documentation

## 📋 Overview

Bu hujjat Vue.js (yoki boshqa SPA framework) frontend ilovasini Proft backend bilan qanday ulashni to'liq tushuntiradi.

---

## 🔧 Backend Configuration

### Base URLs

| Environment | Backend URL | Frontend URL |
|-------------|-------------|--------------|
| Development | `http://localhost:8000` | `http://localhost:3000` |
| Production | `https://api.yoursite.uz` | `https://yoursite.uz` |

### CORS Settings (Backend)

Backend allaqachon quyidagi CORS sozlamalari bilan configuratsiya qilingan:

```python
# backend/config/settings.py

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",  # Vite default port
    "http://127.0.0.1:3000",
]

CORS_ALLOW_CREDENTIALS = True  # Cookie yuborish uchun muhim!

CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:5173",
]
```

---

## 🔐 Authentication Flow

### Session-Based Authentication

Backend **session-based authentication** ishlatadi (JWT emas). Bu degani:
- Login qilganda server `sessionid` cookie o'rnatadi
- Har bir requestda cookie avtomatik yuboriladi
- Logout qilganda session o'chiriladi

### Hemis OAuth 2.0 Login Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │     │   Backend   │     │    Hemis    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │ 1. Click Login    │                   │
       │──────────────────>│                   │
       │                   │                   │
       │ 2. Redirect to    │                   │
       │<──────────────────│                   │
       │   /auth/hemis/login/                  │
       │                   │                   │
       │ 3. Redirect to Hemis                  │
       │───────────────────────────────────────>
       │                   │                   │
       │ 4. User logs in   │                   │
       │<───────────────────────────────────────
       │                   │                   │
       │ 5. Callback with code                 │
       │──────────────────>│                   │
       │                   │ 6. Exchange code  │
       │                   │──────────────────>│
       │                   │                   │
       │                   │ 7. Get user info  │
       │                   │<──────────────────│
       │                   │                   │
       │ 8. Set session &  │                   │
       │    redirect       │                   │
       │<──────────────────│                   │
       │                   │                   │
```

---

## 🌐 API Endpoints

### Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `GET` | `/auth/hemis/login/` | Hemis OAuth login boshlash | ❌ |
| `GET` | `/auth/hemis/callback/` | OAuth callback (internal) | ❌ |
| `POST` | `/auth/hemis/logout/` | Logout | ✅ |
| `GET` | `/auth/hemis/logout/` | Logout (browser) | ✅ |
| `GET` | `/auth/status/` | Auth holatini tekshirish | ❌ |
| `GET` | `/auth/csrf/` | CSRF token olish | ❌ |

### User Management Endpoints

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/accounts/me/` | Joriy user ma'lumotlari | ✅ | Any |
| `PUT` | `/api/accounts/me/` | Profilni yangilash | ✅ | Any |
| `GET` | `/api/accounts/users/` | Barcha userlar ro'yxati | ✅ | Super Admin |
| `POST` | `/api/accounts/users/` | Yangi user yaratish | ✅ | Super Admin |
| `GET` | `/api/accounts/users/{id}/` | User ma'lumotlari | ✅ | Super Admin |
| `PUT` | `/api/accounts/users/{id}/` | User yangilash | ✅ | Super Admin |
| `DELETE` | `/api/accounts/users/{id}/` | User o'chirish | ✅ | Super Admin |

### Portfolio Endpoints

| Method | Endpoint | Description | Auth | Role |
|--------|----------|-------------|------|------|
| `GET` | `/api/portfolios/` | Portfolio ro'yxati | ✅ | Any |
| `POST` | `/api/portfolios/` | Portfolio yaratish | ✅ | Teacher |
| `GET` | `/api/portfolios/{id}/` | Portfolio batafsil | ✅ | Any* |
| `PUT` | `/api/portfolios/{id}/` | Portfolio yangilash | ✅ | Owner/SuperAdmin |
| `DELETE` | `/api/portfolios/{id}/` | Portfolio o'chirish | ✅ | Owner/SuperAdmin |
| `POST` | `/api/portfolios/{id}/approve/` | Tasdiqlash | ✅ | Admin/SuperAdmin |
| `POST` | `/api/portfolios/{id}/reject/` | Rad etish | ✅ | Admin/SuperAdmin |
| `POST` | `/api/portfolios/{id}/comments/` | Izoh qo'shish | ✅ | Any* |
| `GET` | `/api/portfolios/stats/` | Statistika | ✅ | Any |

> *Any = role ga qarab filtered data qaytaradi

---

## 📦 Request/Response Formats

### CSRF Token Olish

```javascript
// GET /auth/csrf/
// Response:
{
  "csrfToken": "abc123xyz..."
}
```

### Auth Status Tekshirish

```javascript
// GET /auth/status/
// Response (authenticated):
{
  "authenticated": true,
  "user": {
    "id": 1,
    "username": "teacher1",
    "email": "teacher1@example.com",
    "role": "teacher",
    "role_display": "Teacher",
    "full_name": "John Teacher",
    "hemis_id": "12345",
    "permissions": {
      "can_manage_users": false,
      "can_approve_portfolios": false,
      "can_manage_all_portfolios": false
    }
  }
}

// Response (not authenticated):
{
  "authenticated": false,
  "user": null
}
```

### Current User

```javascript
// GET /api/accounts/me/
// Response:
{
  "id": 1,
  "username": "teacher1",
  "email": "teacher1@example.com",
  "first_name": "John",
  "last_name": "Teacher",
  "full_name": "John Teacher",
  "role": "teacher",
  "role_display": "Teacher",
  "hemis_id": "12345",
  "department": "Computer Science",
  "position": "Senior Lecturer",
  "bio": "...",
  "phone_number": "+998901234567",
  "permissions": {
    "can_manage_users": false,
    "can_approve_portfolios": false,
    "can_manage_all_portfolios": false
  },
  "is_superadmin": false,
  "is_admin": false,
  "is_teacher": true
}
```

### Portfolio List

```javascript
// GET /api/portfolios/?status=pending&page=1&page_size=20
// Response:
{
  "portfolios": [
    {
      "id": 1,
      "title": "My Teaching Portfolio",
      "description": "Description text...",
      "category": "teaching",
      "category_display": "Teaching Materials",
      "status": "pending",
      "status_display": "Pending",
      "is_public": false,
      "teacher": {
        "id": 1,
        "username": "teacher1",
        "full_name": "John Teacher"
      },
      "reviewed_by": null,
      "reviewed_at": null,
      "created_at": "2026-02-04T10:30:00Z",
      "updated_at": "2026-02-04T10:30:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_pages": 5,
    "total_count": 100,
    "has_next": true,
    "has_previous": false
  }
}
```

### Portfolio Detail

```javascript
// GET /api/portfolios/1/
// Response:
{
  "id": 1,
  "title": "My Teaching Portfolio",
  "description": "Full description...",
  "category": "teaching",
  "category_display": "Teaching Materials",
  "status": "pending",
  "status_display": "Pending",
  "is_public": false,
  "meta_data": {
    "links": ["https://example.com"],
    "notes": "Additional notes"
  },
  "teacher": {
    "id": 1,
    "username": "teacher1",
    "full_name": "John Teacher",
    "department": "Computer Science",
    "position": "Senior Lecturer"
  },
  "reviewed_by": null,
  "reviewed_at": null,
  "review_comment": null,
  "attachments": [
    {
      "id": 1,
      "title": "Syllabus.pdf",
      "file": "/media/portfolio_attachments/2026/02/syllabus.pdf",
      "file_type": "document",
      "file_size": 102400,
      "created_at": "2026-02-04T10:30:00Z"
    }
  ],
  "comments": [
    {
      "id": 1,
      "author": {
        "id": 2,
        "username": "admin",
        "full_name": "Admin User"
      },
      "content": "Please add more details.",
      "created_at": "2026-02-04T11:00:00Z"
    }
  ],
  "history": [
    {
      "id": 1,
      "changed_by": "teacher1",
      "old_status": null,
      "new_status": "pending",
      "comment": "Portfolio created",
      "created_at": "2026-02-04T10:30:00Z"
    }
  ],
  "created_at": "2026-02-04T10:30:00Z",
  "updated_at": "2026-02-04T10:30:00Z",
  "permissions": {
    "can_edit": true,
    "can_delete": true,
    "can_approve": false
  }
}
```

### Create Portfolio

```javascript
// POST /api/portfolios/
// Request:
{
  "title": "My Teaching Portfolio",
  "description": "Detailed description of my work...",
  "category": "teaching",  // teaching, research, certificates, projects, professional, other
  "is_public": false,
  "meta_data": {
    "links": ["https://example.com"],
    "notes": "Additional notes"
  }
}

// Response (201):
{
  "message": "Portfolio created successfully",
  "portfolio": {
    "id": 1,
    "title": "My Teaching Portfolio",
    "status": "pending"
  }
}
```

### Approve Portfolio

```javascript
// POST /api/portfolios/1/approve/
// Request:
{
  "comment": "Great work! Approved."  // optional
}

// Response:
{
  "message": "Portfolio approved successfully",
  "portfolio": {
    "id": 1,
    "title": "My Teaching Portfolio",
    "status": "approved"
  }
}
```

### Reject Portfolio

```javascript
// POST /api/portfolios/1/reject/
// Request:
{
  "comment": "Please add more teaching materials."  // required!
}

// Response:
{
  "message": "Portfolio rejected successfully",
  "portfolio": {
    "id": 1,
    "title": "My Teaching Portfolio",
    "status": "rejected"
  }
}
```

### Portfolio Statistics

```javascript
// GET /api/portfolios/stats/
// Response:
{
  "total": 150,
  "pending": 25,
  "approved": 100,
  "rejected": 25,
  "by_category": {
    "teaching": 50,
    "research": 30,
    "certificates": 20,
    "projects": 25,
    "professional": 15,
    "other": 10
  },
  "recent": [
    {
      "id": 150,
      "title": "Latest Portfolio",
      "status": "pending",
      "updated_at": "2026-02-04T12:00:00Z"
    }
  ]
}
```

---

## 🔌 Vue.js Integration

### Project Setup

```bash
# Create Vue project
npm create vite@latest frontend -- --template vue
cd frontend
npm install

# Install dependencies
npm install axios pinia vue-router
```

### Directory Structure

```
frontend/
├── src/
│   ├── api/
│   │   ├── index.js          # Axios instance
│   │   ├── auth.js           # Auth API
│   │   ├── portfolios.js     # Portfolio API
│   │   └── users.js          # User API
│   ├── stores/
│   │   ├── auth.js           # Auth store (Pinia)
│   │   └── portfolio.js      # Portfolio store
│   ├── composables/
│   │   ├── useAuth.js        # Auth composable
│   │   └── usePermissions.js # Permission checks
│   ├── router/
│   │   └── index.js          # Vue Router with guards
│   ├── views/
│   │   ├── LoginView.vue
│   │   ├── DashboardView.vue
│   │   ├── PortfolioListView.vue
│   │   ├── PortfolioDetailView.vue
│   │   ├── PortfolioCreateView.vue
│   │   └── AdminUsersView.vue
│   ├── components/
│   │   ├── PortfolioCard.vue
│   │   ├── PortfolioForm.vue
│   │   ├── ApprovalButtons.vue
│   │   └── UserTable.vue
│   ├── App.vue
│   └── main.js
├── .env
├── .env.production
└── vite.config.js
```

### Environment Variables

```env
# .env (development)
VITE_API_URL=http://localhost:8000

# .env.production
VITE_API_URL=https://api.yoursite.uz
```

### Vite Config

```javascript
// vite.config.js
import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
      '/auth': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
```

### Axios Instance

```javascript
// src/api/index.js
import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || '',
  withCredentials: true, // MUHIM! Cookie yuborish uchun
  headers: {
    'Content-Type': 'application/json',
  },
})

// CSRF token ni har bir requestga qo'shish
let csrfToken = null

export async function getCsrfToken() {
  if (!csrfToken) {
    const response = await api.get('/auth/csrf/')
    csrfToken = response.data.csrfToken
  }
  return csrfToken
}

// Request interceptor
api.interceptors.request.use(async (config) => {
  // CSRF token kerak bo'lgan methodlar
  if (['post', 'put', 'patch', 'delete'].includes(config.method)) {
    const token = await getCsrfToken()
    config.headers['X-CSRFToken'] = token
  }
  return config
})

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      window.location.href = '/login'
    }
    return Promise.reject(error)
  }
)

export default api
```

### Auth API

```javascript
// src/api/auth.js
import api from './index'

export const authApi = {
  // Auth holatini tekshirish
  async getStatus() {
    const response = await api.get('/auth/status/')
    return response.data
  },

  // Hemis login URL
  getLoginUrl(nextUrl = '/dashboard') {
    const baseUrl = import.meta.env.VITE_API_URL || ''
    return `${baseUrl}/auth/hemis/login/?next=${encodeURIComponent(nextUrl)}`
  },

  // Logout
  async logout() {
    const response = await api.post('/auth/hemis/logout/')
    return response.data
  },

  // Current user
  async getCurrentUser() {
    const response = await api.get('/api/accounts/me/')
    return response.data
  },

  // Update profile
  async updateProfile(data) {
    const response = await api.put('/api/accounts/me/', data)
    return response.data
  },
}
```

### Portfolio API

```javascript
// src/api/portfolios.js
import api from './index'

export const portfolioApi = {
  // List portfolios
  async getList(params = {}) {
    const response = await api.get('/api/portfolios/', { params })
    return response.data
  },

  // Get single portfolio
  async getById(id) {
    const response = await api.get(`/api/portfolios/${id}/`)
    return response.data
  },

  // Create portfolio
  async create(data) {
    const response = await api.post('/api/portfolios/', data)
    return response.data
  },

  // Update portfolio
  async update(id, data) {
    const response = await api.put(`/api/portfolios/${id}/`, data)
    return response.data
  },

  // Delete portfolio
  async delete(id) {
    const response = await api.delete(`/api/portfolios/${id}/`)
    return response.data
  },

  // Approve portfolio
  async approve(id, comment = '') {
    const response = await api.post(`/api/portfolios/${id}/approve/`, { comment })
    return response.data
  },

  // Reject portfolio
  async reject(id, comment) {
    const response = await api.post(`/api/portfolios/${id}/reject/`, { comment })
    return response.data
  },

  // Add comment
  async addComment(id, content, parentId = null) {
    const response = await api.post(`/api/portfolios/${id}/comments/`, {
      content,
      parent_id: parentId,
    })
    return response.data
  },

  // Get statistics
  async getStats() {
    const response = await api.get('/api/portfolios/stats/')
    return response.data
  },
}
```

### Auth Store (Pinia)

```javascript
// src/stores/auth.js
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authApi } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const isLoading = ref(true)
  const isAuthenticated = ref(false)

  // Getters
  const isSuperAdmin = computed(() => user.value?.role === 'superadmin')
  const isAdmin = computed(() => user.value?.role === 'admin')
  const isTeacher = computed(() => user.value?.role === 'teacher')
  const canApprove = computed(() => user.value?.permissions?.can_approve_portfolios)
  const canManageUsers = computed(() => user.value?.permissions?.can_manage_users)

  // Actions
  async function checkAuth() {
    isLoading.value = true
    try {
      const status = await authApi.getStatus()
      isAuthenticated.value = status.authenticated
      user.value = status.user
    } catch (error) {
      isAuthenticated.value = false
      user.value = null
    } finally {
      isLoading.value = false
    }
  }

  async function fetchUser() {
    try {
      user.value = await authApi.getCurrentUser()
      isAuthenticated.value = true
    } catch (error) {
      user.value = null
      isAuthenticated.value = false
    }
  }

  function login(nextUrl = '/dashboard') {
    window.location.href = authApi.getLoginUrl(nextUrl)
  }

  async function logout() {
    try {
      await authApi.logout()
    } finally {
      user.value = null
      isAuthenticated.value = false
      window.location.href = '/login'
    }
  }

  async function updateProfile(data) {
    const result = await authApi.updateProfile(data)
    await fetchUser() // Refresh user data
    return result
  }

  return {
    // State
    user,
    isLoading,
    isAuthenticated,
    // Getters
    isSuperAdmin,
    isAdmin,
    isTeacher,
    canApprove,
    canManageUsers,
    // Actions
    checkAuth,
    fetchUser,
    login,
    logout,
    updateProfile,
  }
})
```

### Vue Router with Guards

```javascript
// src/router/index.js
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guest: true },
  },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/portfolios',
    name: 'portfolios',
    component: () => import('@/views/PortfolioListView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/portfolios/create',
    name: 'portfolio-create',
    component: () => import('@/views/PortfolioCreateView.vue'),
    meta: { requiresAuth: true, roles: ['teacher', 'superadmin'] },
  },
  {
    path: '/portfolios/:id',
    name: 'portfolio-detail',
    component: () => import('@/views/PortfolioDetailView.vue'),
    meta: { requiresAuth: true },
  },
  {
    path: '/admin/users',
    name: 'admin-users',
    component: () => import('@/views/AdminUsersView.vue'),
    meta: { requiresAuth: true, roles: ['superadmin'] },
  },
  {
    path: '/admin/approvals',
    name: 'admin-approvals',
    component: () => import('@/views/AdminApprovalsView.vue'),
    meta: { requiresAuth: true, roles: ['admin', 'superadmin'] },
  },
  {
    path: '/',
    redirect: '/dashboard',
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // Check auth status on first load
  if (authStore.isLoading) {
    await authStore.checkAuth()
  }

  // Guest only pages (login)
  if (to.meta.guest && authStore.isAuthenticated) {
    return next('/dashboard')
  }

  // Protected pages
  if (to.meta.requiresAuth && !authStore.isAuthenticated) {
    return next('/login')
  }

  // Role-based access
  if (to.meta.roles && authStore.user) {
    if (!to.meta.roles.includes(authStore.user.role)) {
      return next('/dashboard') // or show 403 page
    }
  }

  next()
})

export default router
```

### Login View

```vue
<!-- src/views/LoginView.vue -->
<template>
  <div class="login-container">
    <div class="login-card">
      <h1>Portfolio Management System</h1>
      <p>O'qituvchilar uchun portfolio boshqaruv tizimi</p>
      
      <button @click="loginWithHemis" class="hemis-login-btn">
        <img src="@/assets/hemis-logo.png" alt="Hemis" />
        Hemis orqali kirish
      </button>
    </div>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

function loginWithHemis() {
  authStore.login('/dashboard')
}
</script>

<style scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}

.login-card {
  background: white;
  padding: 3rem;
  border-radius: 1rem;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
  text-align: center;
  max-width: 400px;
}

.hemis-login-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  width: 100%;
  padding: 1rem;
  font-size: 1.1rem;
  background: #1a73e8;
  color: white;
  border: none;
  border-radius: 0.5rem;
  cursor: pointer;
  transition: background 0.3s;
}

.hemis-login-btn:hover {
  background: #1557b0;
}

.hemis-login-btn img {
  height: 24px;
}
</style>
```

### Dashboard View

```vue
<!-- src/views/DashboardView.vue -->
<template>
  <div class="dashboard">
    <header class="dashboard-header">
      <h1>Dashboard</h1>
      <div class="user-info">
        <span>{{ authStore.user?.full_name }}</span>
        <span class="role-badge">{{ authStore.user?.role_display }}</span>
        <button @click="logout">Chiqish</button>
      </div>
    </header>

    <div class="stats-grid" v-if="stats">
      <div class="stat-card">
        <h3>Jami</h3>
        <p class="stat-number">{{ stats.total }}</p>
      </div>
      <div class="stat-card pending">
        <h3>Kutilmoqda</h3>
        <p class="stat-number">{{ stats.pending }}</p>
      </div>
      <div class="stat-card approved">
        <h3>Tasdiqlangan</h3>
        <p class="stat-number">{{ stats.approved }}</p>
      </div>
      <div class="stat-card rejected">
        <h3>Rad etilgan</h3>
        <p class="stat-number">{{ stats.rejected }}</p>
      </div>
    </div>

    <div class="quick-actions">
      <router-link 
        v-if="authStore.isTeacher || authStore.isSuperAdmin" 
        to="/portfolios/create" 
        class="action-btn primary"
      >
        + Yangi Portfolio
      </router-link>
      
      <router-link to="/portfolios" class="action-btn">
        Portfoliolarni ko'rish
      </router-link>
      
      <router-link 
        v-if="authStore.canApprove" 
        to="/admin/approvals" 
        class="action-btn"
      >
        Tasdiqlash kutayotganlar ({{ stats?.pending || 0 }})
      </router-link>
      
      <router-link 
        v-if="authStore.canManageUsers" 
        to="/admin/users" 
        class="action-btn"
      >
        Foydalanuvchilarni boshqarish
      </router-link>
    </div>

    <div class="recent-portfolios" v-if="stats?.recent?.length">
      <h2>So'nggi yangilangan</h2>
      <div class="portfolio-list">
        <router-link 
          v-for="p in stats.recent" 
          :key="p.id" 
          :to="`/portfolios/${p.id}`"
          class="portfolio-item"
        >
          <span class="title">{{ p.title }}</span>
          <span :class="['status', p.status]">{{ p.status }}</span>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { portfolioApi } from '@/api/portfolios'

const authStore = useAuthStore()
const stats = ref(null)

onMounted(async () => {
  stats.value = await portfolioApi.getStats()
})

async function logout() {
  await authStore.logout()
}
</script>
```

### Portfolio List View

```vue
<!-- src/views/PortfolioListView.vue -->
<template>
  <div class="portfolio-list-page">
    <header>
      <h1>Portfoliolar</h1>
      <router-link 
        v-if="authStore.isTeacher || authStore.isSuperAdmin" 
        to="/portfolios/create"
        class="btn-primary"
      >
        + Yangi Portfolio
      </router-link>
    </header>

    <!-- Filters -->
    <div class="filters">
      <select v-model="filters.status" @change="fetchPortfolios">
        <option value="">Barcha statuslar</option>
        <option value="pending">Kutilmoqda</option>
        <option value="approved">Tasdiqlangan</option>
        <option value="rejected">Rad etilgan</option>
      </select>

      <select v-model="filters.category" @change="fetchPortfolios">
        <option value="">Barcha kategoriyalar</option>
        <option value="teaching">O'qitish materiallari</option>
        <option value="research">Ilmiy ishlar</option>
        <option value="certificates">Sertifikatlar</option>
        <option value="projects">Loyihalar</option>
        <option value="professional">Kasbiy rivojlanish</option>
        <option value="other">Boshqa</option>
      </select>

      <input 
        v-model="filters.search" 
        @input="debouncedSearch"
        placeholder="Qidirish..."
      />
    </div>

    <!-- Portfolio Grid -->
    <div class="portfolio-grid" v-if="portfolios.length">
      <PortfolioCard 
        v-for="portfolio in portfolios" 
        :key="portfolio.id" 
        :portfolio="portfolio"
        @click="$router.push(`/portfolios/${portfolio.id}`)"
      />
    </div>

    <div v-else-if="!loading" class="empty-state">
      Portfolio topilmadi
    </div>

    <!-- Pagination -->
    <div class="pagination" v-if="pagination.total_pages > 1">
      <button 
        @click="goToPage(pagination.page - 1)" 
        :disabled="!pagination.has_previous"
      >
        Oldingi
      </button>
      <span>{{ pagination.page }} / {{ pagination.total_pages }}</span>
      <button 
        @click="goToPage(pagination.page + 1)" 
        :disabled="!pagination.has_next"
      >
        Keyingi
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { portfolioApi } from '@/api/portfolios'
import PortfolioCard from '@/components/PortfolioCard.vue'

const authStore = useAuthStore()
const loading = ref(false)
const portfolios = ref([])
const pagination = ref({})

const filters = reactive({
  status: '',
  category: '',
  search: '',
  page: 1,
  page_size: 20,
})

async function fetchPortfolios() {
  loading.value = true
  try {
    const params = { ...filters }
    // Remove empty values
    Object.keys(params).forEach(k => !params[k] && delete params[k])
    
    const data = await portfolioApi.getList(params)
    portfolios.value = data.portfolios
    pagination.value = data.pagination
  } finally {
    loading.value = false
  }
}

function goToPage(page) {
  filters.page = page
  fetchPortfolios()
}

// Debounce search
let searchTimeout
function debouncedSearch() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    filters.page = 1
    fetchPortfolios()
  }, 300)
}

onMounted(fetchPortfolios)
</script>
```

### Portfolio Detail View with Approval

```vue
<!-- src/views/PortfolioDetailView.vue -->
<template>
  <div class="portfolio-detail" v-if="portfolio">
    <header>
      <div>
        <h1>{{ portfolio.title }}</h1>
        <span :class="['status-badge', portfolio.status]">
          {{ portfolio.status_display }}
        </span>
      </div>
      
      <div class="actions">
        <button 
          v-if="portfolio.permissions.can_edit" 
          @click="editMode = true"
          class="btn-secondary"
        >
          Tahrirlash
        </button>
        
        <button 
          v-if="portfolio.permissions.can_delete" 
          @click="deletePortfolio"
          class="btn-danger"
        >
          O'chirish
        </button>
      </div>
    </header>

    <!-- Approval Section (Admin/SuperAdmin only) -->
    <div 
      v-if="portfolio.permissions.can_approve && portfolio.status === 'pending'" 
      class="approval-section"
    >
      <h3>Tasdiqlash</h3>
      <textarea 
        v-model="approvalComment" 
        placeholder="Izoh (rad etish uchun majburiy)"
      ></textarea>
      <div class="approval-buttons">
        <button @click="approve" class="btn-success">
          ✓ Tasdiqlash
        </button>
        <button @click="reject" class="btn-danger">
          ✗ Rad etish
        </button>
      </div>
    </div>

    <!-- Review Info -->
    <div v-if="portfolio.reviewed_by" class="review-info">
      <p>
        <strong>Ko'rib chiqilgan:</strong> 
        {{ portfolio.reviewed_by.full_name }} 
        ({{ formatDate(portfolio.reviewed_at) }})
      </p>
      <p v-if="portfolio.review_comment">
        <strong>Izoh:</strong> {{ portfolio.review_comment }}
      </p>
    </div>

    <!-- Content -->
    <div class="content">
      <div class="meta">
        <span><strong>Kategoriya:</strong> {{ portfolio.category_display }}</span>
        <span><strong>O'qituvchi:</strong> {{ portfolio.teacher.full_name }}</span>
        <span><strong>Bo'lim:</strong> {{ portfolio.teacher.department }}</span>
        <span><strong>Yaratilgan:</strong> {{ formatDate(portfolio.created_at) }}</span>
      </div>

      <div class="description">
        <h3>Tavsif</h3>
        <p>{{ portfolio.description }}</p>
      </div>

      <!-- Attachments -->
      <div v-if="portfolio.attachments?.length" class="attachments">
        <h3>Fayllar</h3>
        <ul>
          <li v-for="file in portfolio.attachments" :key="file.id">
            <a :href="file.file" target="_blank">
              {{ file.title }} ({{ formatFileSize(file.file_size) }})
            </a>
          </li>
        </ul>
      </div>

      <!-- Comments -->
      <div class="comments">
        <h3>Izohlar ({{ portfolio.comments?.length || 0 }})</h3>
        
        <div v-for="comment in portfolio.comments" :key="comment.id" class="comment">
          <strong>{{ comment.author.full_name }}</strong>
          <span class="date">{{ formatDate(comment.created_at) }}</span>
          <p>{{ comment.content }}</p>
        </div>

        <div class="add-comment">
          <textarea 
            v-model="newComment" 
            placeholder="Izoh qo'shish..."
          ></textarea>
          <button @click="addComment" :disabled="!newComment.trim()">
            Yuborish
          </button>
        </div>
      </div>

      <!-- History -->
      <div v-if="portfolio.history?.length" class="history">
        <h3>Tarix</h3>
        <ul>
          <li v-for="h in portfolio.history" :key="h.id">
            <span class="date">{{ formatDate(h.created_at) }}</span>
            <span>{{ h.changed_by }}: {{ h.old_status }} → {{ h.new_status }}</span>
            <span v-if="h.comment" class="comment">{{ h.comment }}</span>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { portfolioApi } from '@/api/portfolios'

const route = useRoute()
const router = useRouter()

const portfolio = ref(null)
const approvalComment = ref('')
const newComment = ref('')
const editMode = ref(false)

async function fetchPortfolio() {
  portfolio.value = await portfolioApi.getById(route.params.id)
}

async function approve() {
  await portfolioApi.approve(portfolio.value.id, approvalComment.value)
  await fetchPortfolio()
  approvalComment.value = ''
}

async function reject() {
  if (!approvalComment.value.trim()) {
    alert('Rad etish uchun izoh majburiy!')
    return
  }
  await portfolioApi.reject(portfolio.value.id, approvalComment.value)
  await fetchPortfolio()
  approvalComment.value = ''
}

async function deletePortfolio() {
  if (confirm('Rostdan ham o\'chirmoqchimisiz?')) {
    await portfolioApi.delete(portfolio.value.id)
    router.push('/portfolios')
  }
}

async function addComment() {
  if (!newComment.value.trim()) return
  await portfolioApi.addComment(portfolio.value.id, newComment.value)
  await fetchPortfolio()
  newComment.value = ''
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString('uz-UZ')
}

function formatFileSize(bytes) {
  if (bytes < 1024) return bytes + ' B'
  if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(1) + ' KB'
  return (bytes / 1024 / 1024).toFixed(1) + ' MB'
}

onMounted(fetchPortfolio)
</script>
```

### App.vue

```vue
<!-- src/App.vue -->
<template>
  <div id="app">
    <nav v-if="authStore.isAuthenticated" class="main-nav">
      <router-link to="/dashboard">Dashboard</router-link>
      <router-link to="/portfolios">Portfoliolar</router-link>
      <router-link v-if="authStore.canApprove" to="/admin/approvals">
        Tasdiqlash
      </router-link>
      <router-link v-if="authStore.canManageUsers" to="/admin/users">
        Foydalanuvchilar
      </router-link>
      
      <div class="user-menu">
        <span>{{ authStore.user?.full_name }}</span>
        <button @click="authStore.logout()">Chiqish</button>
      </div>
    </nav>

    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()

onMounted(async () => {
  await authStore.checkAuth()
})
</script>
```

### main.js

```javascript
// src/main.js
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'
import './style.css'

const app = createApp(App)

app.use(createPinia())
app.use(router)

app.mount('#app')
```

---

## 🔒 Security Checklist

### Frontend

- [x] `withCredentials: true` barcha API requestlarda
- [x] CSRF token har bir POST/PUT/DELETE requestda
- [x] Route guards authentication tekshirish uchun
- [x] Role-based navigation va component visibility
- [x] Input validation (client-side)
- [x] XSS prevention (Vue auto-escaping)

### Backend (allaqachon configuratsiya qilingan)

- [x] CORS `credentials: true` bilan
- [x] CSRF protection
- [x] HttpOnly session cookies
- [x] Secure cookies (production)
- [x] SameSite=Lax cookies
- [x] Role-based permissions
- [x] Object-level permissions

---

## 🧪 Testing

### Frontend Testing

```javascript
// Test auth flow
describe('Auth', () => {
  it('should redirect to login when not authenticated', async () => {
    // Test route guard
  })

  it('should show user info when authenticated', async () => {
    // Test dashboard
  })
})

// Test API calls
describe('Portfolio API', () => {
  it('should fetch portfolios with correct params', async () => {
    // Test API call
  })

  it('should handle approval correctly', async () => {
    // Test approve/reject
  })
})
```

### API Testing with curl

```bash
# Get CSRF token
curl -c cookies.txt http://localhost:8000/auth/csrf/

# Check auth status
curl -b cookies.txt http://localhost:8000/auth/status/

# Get portfolios (after login)
curl -b cookies.txt http://localhost:8000/api/portfolios/

# Create portfolio
curl -X POST -b cookies.txt \
  -H "X-CSRFToken: YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title":"Test","description":"Test desc","category":"teaching"}' \
  http://localhost:8000/api/portfolios/
```

---

## 📱 Mobile/PWA Considerations

Agar mobil ilova yoki PWA qilmoqchi bo'lsangiz:

1. **Token-based auth** qo'shish mumkin (JWT)
2. Backend allaqachon session + token parallel ishlashga tayyor
3. `django-rest-framework` qo'shib REST API kengaytirish mumkin

---

## 🚀 Deployment Checklist

### Frontend (Vercel/Netlify)

1. Build: `npm run build`
2. Environment: `VITE_API_URL=https://api.yoursite.uz`
3. Redirects: All routes → `index.html`

### Backend (Docker/VPS)

1. `DEBUG=False`
2. `SECRET_KEY` - yangi xavfsiz kalit
3. `ALLOWED_HOSTS` - production domain
4. `CORS_ALLOWED_ORIGINS` - frontend domain
5. `CSRF_TRUSTED_ORIGINS` - frontend domain
6. SSL/HTTPS - nginx reverse proxy

---

## 📞 Support

Savollar bo'lsa:
- GitHub Issues: https://github.com/xurshidbekxasanboyev1990/proft/issues
- Documentation: README.md

---

*Last updated: February 4, 2026*
