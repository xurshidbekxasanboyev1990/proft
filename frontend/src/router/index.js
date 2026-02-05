/**
 * Vue Router Configuration
 * Role-based routing with navigation guards
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores'

// Layouts
import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'

// Views - Lazy loaded for performance
const LoginView = () => import('@/views/auth/LoginView.vue')
const CallbackView = () => import('@/views/auth/CallbackView.vue')
const ForbiddenView = () => import('@/views/errors/ForbiddenView.vue')
const NotFoundView = () => import('@/views/errors/NotFoundView.vue')

// Dashboard
const DashboardView = () => import('@/views/dashboard/DashboardView.vue')

// Portfolio (Teacher)
const PortfolioListView = () => import('@/views/portfolio/PortfolioListView.vue')
const PortfolioCreateView = () => import('@/views/portfolio/PortfolioCreateView.vue')
const PortfolioEditView = () => import('@/views/portfolio/PortfolioEditView.vue')
const PortfolioDetailView = () => import('@/views/portfolio/PortfolioDetailView.vue')

// Profile
const ProfileView = () => import('@/views/profile/ProfileView.vue')

// Approval (Admin)
const ApprovalListView = () => import('@/views/approval/ApprovalListView.vue')
const ApprovalDetailView = () => import('@/views/approval/ApprovalDetailView.vue')

// Assignments
const AssignmentsListView = () => import('@/views/assignments/AssignmentsListView.vue')
const AssignmentDetailView = () => import('@/views/assignments/AssignmentDetailView.vue')
const AssignmentCreateView = () => import('@/views/assignments/AssignmentCreateView.vue')
const AssignmentEditView = () => import('@/views/assignments/AssignmentEditView.vue')
const MyAssignmentsView = () => import('@/views/assignments/MyAssignmentsView.vue')

// Categories
const CategoriesListView = () => import('@/views/categories/CategoriesListView.vue')

// Grading
const ScoreHistoryView = () => import('@/views/grading/ScoreHistoryView.vue')
const SubmissionsListView = () => import('@/views/grading/SubmissionsListView.vue')

// Teacher - Submissions & Scores
const SubmitAssignmentView = () => import('@/views/assignments/SubmitAssignmentView.vue')
const MySubmissionsView = () => import('@/views/submissions/MySubmissionsView.vue')
const MyScoresView = () => import('@/views/scores/MyScoresView.vue')

// Notifications
const NotificationsView = () => import('@/views/notifications/NotificationsView.vue')

// Analytics
const AnalyticsDashboardView = () => import('@/views/analytics/AnalyticsDashboardView.vue')

// Reports
const ReportsListView = () => import('@/views/reports/ReportsListView.vue')

// Admin Panel (Super Admin)
const AdminDashboardView = () => import('@/views/admin/AdminDashboardView.vue')
const UserManagementView = () => import('@/views/admin/UserManagementView.vue')
const UserCreateView = () => import('@/views/admin/UserCreateView.vue')
const UserEditView = () => import('@/views/admin/UserEditView.vue')
const ReportsView = () => import('@/views/admin/ReportsView.vue')

const routes = [
  // Auth routes (no auth required)
  {
    path: '/',
    component: AuthLayout,
    children: [
      {
        path: '',
        redirect: '/login'
      },
      {
        path: 'login',
        name: 'login',
        component: LoginView,
        meta: { 
          requiresAuth: false,
          title: 'Kirish'
        }
      },
      {
        path: 'callback',
        name: 'callback',
        component: CallbackView,
        meta: { 
          requiresAuth: false,
          title: 'Qayta yo\'naltirish...'
        }
      }
    ]
  },
  
  // Main app routes (auth required)
  {
    path: '/',
    component: MainLayout,
    meta: { requiresAuth: true },
    children: [
      // Dashboard - All authenticated users
      {
        path: 'dashboard',
        name: 'dashboard',
        component: DashboardView,
        meta: { 
          title: 'Bosh sahifa',
          roles: ['superadmin', 'admin', 'teacher']
        }
      },
      
      // Portfolio routes - Teacher (and SuperAdmin can view/manage all)
      {
        path: 'portfolios',
        name: 'portfolios',
        component: PortfolioListView,
        meta: { 
          title: 'Portfolio',
          roles: ['teacher', 'superadmin']
        }
      },
      {
        path: 'portfolios/create',
        name: 'portfolio-create',
        component: PortfolioCreateView,
        meta: { 
          title: 'Yangi portfolio',
          roles: ['teacher', 'superadmin']
        }
      },
      {
        path: 'portfolios/:id',
        name: 'portfolio-detail',
        component: PortfolioDetailView,
        meta: { 
          title: 'Portfolio',
          roles: ['teacher', 'admin', 'superadmin']
        }
      },
      {
        path: 'portfolios/:id/edit',
        name: 'portfolio-edit',
        component: PortfolioEditView,
        meta: { 
          title: 'Portfolioni tahrirlash',
          roles: ['teacher', 'superadmin']
        }
      },
      
      // Profile - All authenticated users
      {
        path: 'profile',
        name: 'profile',
        component: ProfileView,
        meta: { 
          title: 'Profil',
          roles: ['superadmin', 'admin', 'teacher']
        }
      },
      
      // Approval routes - Admin only
      {
        path: 'approval',
        name: 'approval',
        component: ApprovalListView,
        meta: { 
          title: 'Tasdiqlash',
          roles: ['admin', 'superadmin']
        }
      },
      {
        path: 'approval/:id',
        name: 'approval-detail',
        component: ApprovalDetailView,
        meta: { 
          title: "Ko'rib chiqish",
          roles: ['admin', 'superadmin']
        }
      },

      // Assignments routes
      {
        path: 'assignments',
        name: 'assignments',
        component: AssignmentsListView,
        meta: { 
          title: 'Topshiriqlar',
          roles: ['admin', 'superadmin']
        }
      },
      {
        path: 'assignments/create',
        name: 'assignment-create',
        component: AssignmentCreateView,
        meta: { 
          title: 'Yangi topshiriq',
          roles: ['admin', 'superadmin']
        }
      },
      {
        path: 'assignments/:id',
        name: 'assignment-detail',
        component: AssignmentDetailView,
        meta: { 
          title: 'Topshiriq',
          roles: ['teacher', 'admin', 'superadmin']
        }
      },
      {
        path: 'assignments/:id/edit',
        name: 'assignment-edit',
        component: AssignmentEditView,
        meta: { 
          title: 'Topshiriqni tahrirlash',
          roles: ['admin', 'superadmin']
        }
      },
      {
        path: 'my-assignments',
        name: 'my-assignments',
        component: MyAssignmentsView,
        meta: { 
          title: 'Mening topshiriqlarim',
          roles: ['teacher']
        }
      },
      {
        path: 'assignments/:id/submit',
        name: 'submit-assignment',
        component: SubmitAssignmentView,
        meta: { 
          title: 'Javob yuborish',
          roles: ['teacher']
        }
      },
      {
        path: 'my-submissions',
        name: 'my-submissions',
        component: MySubmissionsView,
        meta: { 
          title: 'Mening javoblarim',
          roles: ['teacher']
        }
      },
      {
        path: 'my-scores',
        name: 'my-scores',
        component: MyScoresView,
        meta: { 
          title: 'Mening ballarim',
          roles: ['teacher']
        }
      },
      {
        path: 'notifications',
        name: 'notifications',
        component: NotificationsView,
        meta: { 
          title: 'Bildirishnomalar',
          roles: ['teacher', 'admin', 'superadmin']
        }
      },

      // Grading routes
      {
        path: 'submissions',
        name: 'submissions',
        component: SubmissionsListView,
        meta: { 
          title: 'Javoblar',
          roles: ['admin', 'superadmin']
        }
      },
      {
        path: 'score-history',
        name: 'score-history',
        component: ScoreHistoryView,
        meta: { 
          title: 'Ball tarixi',
          roles: ['admin', 'superadmin']
        }
      },

      // Categories routes
      {
        path: 'categories',
        name: 'categories',
        component: CategoriesListView,
        meta: { 
          title: 'Kategoriyalar',
          roles: ['admin', 'superadmin']
        }
      },

      // Analytics routes
      {
        path: 'analytics',
        name: 'analytics',
        component: AnalyticsDashboardView,
        meta: { 
          title: 'Analitika',
          roles: ['admin', 'superadmin']
        }
      },

      // Reports routes
      {
        path: 'reports',
        name: 'reports-list',
        component: ReportsListView,
        meta: { 
          title: 'Hisobotlar',
          roles: ['admin', 'superadmin']
        }
      },
      
      // Super Admin routes
      {
        path: 'admin',
        name: 'admin-dashboard',
        component: AdminDashboardView,
        meta: { 
          title: 'Admin panel',
          roles: ['superadmin']
        }
      },
      {
        path: 'admin/users',
        name: 'users',
        component: UserManagementView,
        meta: { 
          title: 'Foydalanuvchilar',
          roles: ['superadmin']
        }
      },
      {
        path: 'admin/users/create',
        name: 'user-create',
        component: UserCreateView,
        meta: { 
          title: 'Yangi foydalanuvchi',
          roles: ['superadmin']
        }
      },
      {
        path: 'admin/users/:id/edit',
        name: 'user-edit',
        component: UserEditView,
        meta: { 
          title: 'Foydalanuvchini tahrirlash',
          roles: ['superadmin']
        }
      },
      {
        path: 'admin/reports',
        name: 'reports',
        component: ReportsView,
        meta: { 
          title: 'Hisobotlar',
          roles: ['superadmin']
        }
      }
    ]
  },
  
  // Error pages
  {
    path: '/403',
    name: 'forbidden',
    component: ForbiddenView,
    meta: { 
      requiresAuth: false,
      title: 'Ruxsat berilmagan'
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: NotFoundView,
    meta: { 
      requiresAuth: false,
      title: 'Sahifa topilmadi'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // Update page title
  document.title = to.meta.title 
    ? `${to.meta.title} | Proft` 
    : 'Proft - Portfolio Management System'
  
  // Check if route requires auth
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // If route doesn't require auth, allow access
  if (!requiresAuth) {
    // If user is already authenticated and tries to access login, redirect to dashboard
    if (to.name === 'login') {
      try {
        const isAuth = await userStore.checkAuth()
        if (isAuth) {
          return next({ name: 'dashboard' })
        }
      } catch (error) {
        console.warn('Auth check failed:', error.message)
      }
    }
    return next()
  }
  
  // Check authentication
  if (!userStore.isAuthenticated) {
    try {
      const isAuth = await userStore.checkAuth()
      if (!isAuth) {
        // Not authenticated, redirect to login
        return next({ 
          name: 'login', 
          query: { redirect: to.fullPath } 
        })
      }
    } catch (error) {
      console.warn('Auth check failed:', error.message)
      // On error, redirect to login
      return next({ 
        name: 'login', 
        query: { redirect: to.fullPath } 
      })
    }
  }
  
  // Check role-based access
  const allowedRoles = to.meta.roles
  if (allowedRoles && allowedRoles.length > 0) {
    const userRole = userStore.role
    if (!allowedRoles.includes(userRole)) {
      // User doesn't have required role
      return next({ name: 'forbidden' })
    }
  }
  
  // All checks passed
  next()
})

export default router
