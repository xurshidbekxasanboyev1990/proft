"""
URL patterns for accounts app.
"""

from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    # Current user
    path('me/', views.CurrentUserView.as_view(), name='current_user'),
    
    # User management (Super Admin only)
    path('users/', views.UserListView.as_view(), name='user_list'),
    path('users/stats/', views.UserStatsView.as_view(), name='user_stats'),
    path('users/<int:user_id>/', views.UserDetailView.as_view(), name='user_detail'),
]
