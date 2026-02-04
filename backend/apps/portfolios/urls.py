"""
URL patterns for portfolios app.
"""

from django.urls import path
from . import views

app_name = 'portfolios'

urlpatterns = [
    # Portfolio CRUD
    path('', views.PortfolioListView.as_view(), name='list'),
    path('<int:portfolio_id>/', views.PortfolioDetailView.as_view(), name='detail'),
    
    # Approval workflow
    path('<int:portfolio_id>/approve/', views.PortfolioApproveView.as_view(), name='approve'),
    path('<int:portfolio_id>/reject/', views.PortfolioRejectView.as_view(), name='reject'),
    
    # Comments
    path('<int:portfolio_id>/comments/', views.PortfolioCommentView.as_view(), name='comments'),
    
    # Statistics
    path('stats/', views.PortfolioStatsView.as_view(), name='stats'),
]
