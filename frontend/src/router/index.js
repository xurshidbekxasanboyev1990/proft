/**
 * Vue Router Configuration
 * Role-based routing with separate layouts for each role
 */

import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores'

// Layouts
import AuthLayout from '@/layouts/AuthLayout.vue'
import TeacherLayout from '@/layouts/TeacherLayout.vue'
import AdminLayout from '@/layouts/AdminLayout.vue'
import SuperAdminLayout from '@/layouts/SuperAdminLayout.vue'

// Views - Lazy loaded for performance
const HemisLoginView = () => import('@/views/auth/HemisLoginView.vue')
const HemisCallbackView = () => import('@/views/auth/HemisCallbackView.vue')
const LogoutView = () => import('@/views/auth/LogoutView.vue')
const AuthStatusView = () => import('@/views/auth/AuthStatusView.vue')
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
const ProfileEditView = () => import('@/views/profile/ProfileEditView.vue')

// Approval (Admin)
const ApprovalListView = () => import('@/views/approval/ApprovalListView.vue')
const ApprovalDetailView = () => import('@/views/approval/ApprovalDetailView.vue')

// Assignments
const AssignmentsListView = () => import('@/views/assignments/AssignmentsListView.vue')
const AssignmentDetailView = () => import('@/views/assignments/AssignmentDetailView.vue')
const AssignmentCreateView = () => import('@/views/assignments/AssignmentCreateView.vue')
const AssignmentEditView = () => import('@/views/assignments/AssignmentEditView.vue')
const MyAssignmentsView = () => import('@/views/assignments/MyAssignmentsView.vue')
const SubmitAssignmentView = () => import('@/views/assignments/SubmitAssignmentView.vue')

// Categories
const CategoriesListView = () => import('@/views/categories/CategoriesListView.vue')

// Grading
const ScoreHistoryView = () => import('@/views/grading/ScoreHistoryView.vue')
const SubmissionsListView = () => import('@/views/grading/SubmissionsListView.vue')

// Teacher - Submissions & Scores
const MySubmissionsView = () => import('@/views/submissions/MySubmissionsView.vue')
const MyScoresView = () => import('@/views/scores/MyScoresView.vue')

// Notifications
const NotificationsView = () => import('@/views/notifications/NotificationsView.vue')

// Analytics
const AnalyticsDashboardView = () => import('@/views/analytics/AnalyticsDashboardView.vue')

// Reports
const ReportsListView = () => import('@/views/reports/ReportsListView.vue')
const ReportGeneratorView = () => import('@/views/reports/ReportGeneratorView.vue')

// Admin Panel (Super Admin)
const AdminDashboardView = () => import('@/views/admin/AdminDashboardView.vue')
const UserManagementView = () => import('@/views/admin/UserManagementView.vue')
const UserCreateView = () => import('@/views/admin/UserCreateView.vue')
const UserEditView = () => import('@/views/admin/UserEditView.vue')

// Teachers management (for Admin)
const TeachersListView = () => import('@/views/teachers/TeachersListView.vue')

const routes = [
  // ========================================
  // AUTH ROUTES (No auth required)
  // ========================================
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
        component: HemisLoginView,
        meta: { 
          requiresAuth: false,
          title: 'Kirish'
        }
      },
      {
        path: 'callback',
        name: 'callback',
        component: HemisCallbackView,
        meta: { 
          requiresAuth: false,
          title: 'Qayta yo\'naltirish...'
        }
      },
      {
        path: 'logout',
        name: 'logout',
        component: LogoutView,
        meta: { 
          requiresAuth: false,
          title: 'Chiqish'
        }
      },
      {
        path: 'auth-status',
        name: 'auth-status',
        component: AuthStatusView,
        meta: { 
          requiresAuth: false,
          title: 'Autentifikatsiya holati'
        }
      }
    ]
  },

  // ========================================
  // TEACHER ROUTES
  // ========================================
  {
    path: '/teacher',
    component: TeacherLayout,
    meta: { requiresAuth: true, roles: ['teacher'] },
    children: [
      {
        path: '',
        name: 'teacher-dashboard',
        component: DashboardView,
        meta: { 
          title: 'Bosh sahifa',
          roles: ['teacher']
        }
      },
      {
        path: 'portfolios',
        name: 'teacher-portfolios',
        component: PortfolioListView,
        meta: { 
          title: 'Portfoliolarim',
          roles: ['teacher']
        }
      },
      {
        path: 'portfolios/new',
        name: 'teacher-portfolio-create',
        component: PortfolioCreateView,
        meta: { 
          title: 'Yangi portfolio',
          roles: ['teacher']
        }
      },
      {
        path: 'portfolios/:id',
        name: 'teacher-portfolio-detail',
        component: PortfolioDetailView,
        meta: { 
          title: 'Portfolio',
          roles: ['teacher']
        }
      },
      {
        path: 'portfolios/:id/edit',
        name: 'teacher-portfolio-edit',
        component: PortfolioEditView,
        meta: { 
          title: 'Portfolioni tahrirlash',
          roles: ['teacher']
        }
      },
      {
        path: 'tasks',
        name: 'teacher-tasks',
        component: MyAssignmentsView,
        meta: { 
          title: 'Topshiriqlarim',
          roles: ['teacher']
        }
      },
      {
        path: 'tasks/:id',
        name: 'teacher-task-detail',
        component: AssignmentDetailView,
        meta: { 
          title: 'Topshiriq',
          roles: ['teacher']
        }
      },
      {
        path: 'tasks/:id/submit',
        name: 'teacher-task-submit',
        component: SubmitAssignmentView,
        meta: { 
          title: 'Javob yuborish',
          roles: ['teacher']
        }
      },
      {
        path: 'responses',
        name: 'teacher-responses',
        component: MySubmissionsView,
        meta: { 
          title: 'Javoblarim',
          roles: ['teacher']
        }
      },
      {
        path: 'scores',
        name: 'teacher-scores',
        component: MyScoresView,
        meta: { 
          title: 'Ballarim',
          roles: ['teacher']
        }
      },
      {
        path: 'notifications',
        name: 'teacher-notifications',
        component: NotificationsView,
        meta: { 
          title: 'Bildirishnomalar',
          roles: ['teacher']
        }
      },
      {
        path: 'profile',
        name: 'teacher-profile',
        component: ProfileView,
        meta: { 
          title: 'Profil',
          roles: ['teacher']
        }
      },
      {
        path: 'profile/edit',
        name: 'teacher-profile-edit',
        component: ProfileEditView,
        meta: { 
          title: 'Profilni tahrirlash',
          roles: ['teacher']
        }
      }
    ]
  },

  // ========================================
  // ADMIN ROUTES
  // ========================================
  {
    path: '/admin-panel',
    component: AdminLayout,
    meta: { requiresAuth: true, roles: ['admin'] },
    children: [
      {
        path: '',
        name: 'admin-dashboard',
        component: DashboardView,
        meta: { 
          title: 'Admin Dashboard',
          roles: ['admin']
        }
      },
      {
        path: 'approvals',
        name: 'admin-approvals',
        component: ApprovalListView,
        meta: { 
          title: 'Tasdiqlash',
          roles: ['admin']
        }
      },
      {
        path: 'approvals/:id',
        name: 'admin-approval-detail',
        component: ApprovalDetailView,
        meta: { 
          title: "Ko'rib chiqish",
          roles: ['admin']
        }
      },
      {
        path: 'tasks',
        name: 'admin-tasks',
        component: AssignmentsListView,
        meta: { 
          title: 'Topshiriqlar',
          roles: ['admin']
        }
      },
      {
        path: 'tasks/new',
        name: 'admin-task-create',
        component: AssignmentCreateView,
        meta: { 
          title: 'Yangi topshiriq',
          roles: ['admin']
        }
      },
      {
        path: 'tasks/:id',
        name: 'admin-task-detail',
        component: AssignmentDetailView,
        meta: { 
          title: 'Topshiriq',
          roles: ['admin']
        }
      },
      {
        path: 'tasks/:id/edit',
        name: 'admin-task-edit',
        component: AssignmentEditView,
        meta: { 
          title: 'Topshiriqni tahrirlash',
          roles: ['admin']
        }
      },
      {
        path: 'categories',
        name: 'admin-categories',
        component: CategoriesListView,
        meta: { 
          title: 'Kategoriyalar',
          roles: ['admin']
        }
      },
      {
        path: 'responses',
        name: 'admin-responses',
        component: SubmissionsListView,
        meta: { 
          title: 'Javoblar',
          roles: ['admin']
        }
      },
      {
        path: 'scoring',
        name: 'admin-scoring',
        component: SubmissionsListView,
        meta: { 
          title: 'Baholash',
          roles: ['admin']
        }
      },
      {
        path: 'score-history',
        name: 'admin-score-history',
        component: ScoreHistoryView,
        meta: { 
          title: 'Ball tarixi',
          roles: ['admin']
        }
      },
      {
        path: 'teachers',
        name: 'admin-teachers',
        component: TeachersListView,
        meta: { 
          title: "O'qituvchilar",
          roles: ['admin']
        }
      },
      {
        path: 'profile',
        name: 'admin-profile',
        component: ProfileView,
        meta: { 
          title: 'Profil',
          roles: ['admin']
        }
      },
      {
        path: 'profile/edit',
        name: 'admin-profile-edit',
        component: ProfileEditView,
        meta: { 
          title: 'Profilni tahrirlash',
          roles: ['admin']
        }
      }
    ]
  },

  // ========================================
  // SUPER ADMIN ROUTES
  // ========================================
  {
    path: '/super-admin',
    component: SuperAdminLayout,
    meta: { requiresAuth: true, roles: ['superadmin'] },
    children: [
      {
        path: '',
        name: 'superadmin-dashboard',
        component: AdminDashboardView,
        meta: { 
          title: 'Super Admin Dashboard',
          roles: ['superadmin']
        }
      },
      {
        path: 'users',
        name: 'superadmin-users',
        component: UserManagementView,
        meta: { 
          title: 'Foydalanuvchilar',
          roles: ['superadmin']
        }
      },
      {
        path: 'users/new',
        name: 'superadmin-user-create',
        component: UserCreateView,
        meta: { 
          title: 'Yangi foydalanuvchi',
          roles: ['superadmin']
        }
      },
      {
        path: 'users/:id/edit',
        name: 'superadmin-user-edit',
        component: UserEditView,
        meta: { 
          title: 'Foydalanuvchini tahrirlash',
          roles: ['superadmin']
        }
      },
      {
        path: 'categories',
        name: 'superadmin-categories',
        component: CategoriesListView,
        meta: { 
          title: 'Kategoriyalar',
          roles: ['superadmin']
        }
      },
      {
        path: 'tasks',
        name: 'superadmin-tasks',
        component: AssignmentsListView,
        meta: { 
          title: 'Topshiriqlar',
          roles: ['superadmin']
        }
      },
      {
        path: 'tasks/new',
        name: 'superadmin-task-create',
        component: AssignmentCreateView,
        meta: { 
          title: 'Yangi topshiriq',
          roles: ['superadmin']
        }
      },
      {
        path: 'tasks/:id',
        name: 'superadmin-task-detail',
        component: AssignmentDetailView,
        meta: { 
          title: 'Topshiriq',
          roles: ['superadmin']
        }
      },
      {
        path: 'tasks/:id/edit',
        name: 'superadmin-task-edit',
        component: AssignmentEditView,
        meta: { 
          title: 'Topshiriqni tahrirlash',
          roles: ['superadmin']
        }
      },
      {
        path: 'approvals',
        name: 'superadmin-approvals',
        component: ApprovalListView,
        meta: { 
          title: 'Tasdiqlash',
          roles: ['superadmin']
        }
      },
      {
        path: 'approvals/:id',
        name: 'superadmin-approval-detail',
        component: ApprovalDetailView,
        meta: { 
          title: "Ko'rib chiqish",
          roles: ['superadmin']
        }
      },
      {
        path: 'analytics',
        name: 'superadmin-analytics',
        component: AnalyticsDashboardView,
        meta: { 
          title: 'Analitika',
          roles: ['superadmin']
        }
      },
      {
        path: 'reports',
        name: 'superadmin-reports',
        component: ReportsListView,
        meta: { 
          title: 'Hisobotlar',
          roles: ['superadmin']
        }
      },
      {
        path: 'reports/new',
        name: 'superadmin-report-create',
        component: ReportGeneratorView,
        meta: { 
          title: 'Hisobot yaratish',
          roles: ['superadmin']
        }
      },
      {
        path: 'settings',
        name: 'superadmin-settings',
        component: ProfileEditView,
        meta: { 
          title: 'Sozlamalar',
          roles: ['superadmin']
        }
      },
      {
        path: 'profile',
        name: 'superadmin-profile',
        component: ProfileView,
        meta: { 
          title: 'Profil',
          roles: ['superadmin']
        }
      },
      {
        path: 'profile/edit',
        name: 'superadmin-profile-edit',
        component: ProfileEditView,
        meta: { 
          title: 'Profilni tahrirlash',
          roles: ['superadmin']
        }
      }
    ]
  },

  // ========================================
  // ERROR PAGES
  // ========================================
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

// Helper to get dashboard route based on role
const getDashboardRoute = (role) => {
  switch (role) {
    case 'teacher':
      return { name: 'teacher-dashboard' }
    case 'admin':
      return { name: 'admin-dashboard' }
    case 'superadmin':
      return { name: 'superadmin-dashboard' }
    default:
      return { name: 'login' }
  }
}

// Check if DEV_MODE is enabled
const isDevMode = import.meta.env.VITE_DEV_MODE === 'true'

// Navigation guard
router.beforeEach(async (to, from, next) => {
  const userStore = useUserStore()
  
  // Update page title
  document.title = to.meta.title 
    ? `${to.meta.title} | Proft` 
    : 'Proft - Portfolio Management System'
  
  // DEV_MODE: Skip all auth and role checks - allow access to all pages
  if (isDevMode) {
    return next()
  }
  
  // Check if route requires auth
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  
  // If route doesn't require auth, allow access
  if (!requiresAuth) {
    // If user is already authenticated and tries to access login, redirect to their dashboard
    if (to.name === 'login') {
      try {
        const isAuth = await userStore.checkAuth()
        if (isAuth) {
          const role = userStore.role
          return next(getDashboardRoute(role))
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
  const allowedRoles = to.meta.roles || to.matched.find(r => r.meta.roles)?.meta.roles
  if (allowedRoles && allowedRoles.length > 0) {
    const userRole = userStore.role
    if (!allowedRoles.includes(userRole)) {
      // User doesn't have required role, redirect to their own dashboard
      return next(getDashboardRoute(userRole))
    }
  }
  
  // All checks passed
  next()
})

// Export getDashboardRoute for use in other components
export { getDashboardRoute }

export default router
