"""
URL patterns for assignments app.
"""

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from . import api_views

app_name = 'assignments'

# DRF Router for ViewSets
router = DefaultRouter()
router.register(r'v2/categories', api_views.CategoryViewSet, basename='category')
router.register(r'v2/assignments', api_views.AssignmentViewSet, basename='assignment')
router.register(r'v2/submissions', api_views.AssignmentSubmissionViewSet, basename='submission')

urlpatterns = [
    # DRF API v2 (REST Framework ViewSets)
    path('', include(router.urls)),
    
    # Categories (legacy/custom views)
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
    path('categories/<int:category_id>/', views.CategoryDetailView.as_view(), name='category_detail'),
    
    # Assignments (legacy/custom views)
    path('list/', views.AssignmentListView.as_view(), name='list'),
    path('<int:assignment_id>/', views.AssignmentDetailView.as_view(), name='detail'),
    path('bulk/', views.BulkAssignmentView.as_view(), name='bulk_create'),
    
    # Teacher dashboard
    path('my-dashboard/', views.TeacherAssignmentDashboardView.as_view(), name='teacher_dashboard'),
    
    # Admin stats
    path('stats/', views.AssignmentStatsView.as_view(), name='stats'),
]
