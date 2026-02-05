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
    path('categories/<int:category_id>/score/', views.CategoryScoreUpdateView.as_view(), name='category_score'),
    
    # Assignments (legacy/custom views)
    path('list/', views.AssignmentListView.as_view(), name='list'),
    path('<int:assignment_id>/', views.AssignmentDetailView.as_view(), name='detail'),
    path('bulk/', views.BulkAssignmentView.as_view(), name='bulk_create'),
    
    # Ball (Score) Tizimi endpoints
    path('<int:assignment_id>/score/', views.AssignmentScoreUpdateView.as_view(), name='assignment_score'),
    path('<int:assignment_id>/score-history/', views.ScoreHistoryListView.as_view(), name='assignment_score_history'),
    path('progress/<int:progress_id>/grade/', views.AssignmentProgressGradeView.as_view(), name='progress_grade'),
    path('score-history/', views.ScoreHistoryListView.as_view(), name='score_history_all'),
    path('bulk-score-update/', views.BulkScoreUpdateView.as_view(), name='bulk_score_update'),
    
    # Teacher dashboard
    path('my-dashboard/', views.TeacherAssignmentDashboardView.as_view(), name='teacher_dashboard'),
    
    # Admin stats
    path('stats/', views.AssignmentStatsView.as_view(), name='stats'),
]
