"""
URL patterns for analytics app.
"""

from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    # Dashboard
    path('dashboard/overview/', views.DashboardOverviewView.as_view(), name='dashboard_overview'),
    path('dashboard/widgets/', views.DashboardWidgetsView.as_view(), name='dashboard_widgets'),
    
    # Charts
    path('charts/<str:chart_type>/', views.ChartDataView.as_view(), name='chart_data'),
    
    # Analytics
    path('portfolios/', views.PortfolioAnalyticsView.as_view(), name='portfolio_analytics'),
    path('assignments/', views.AssignmentAnalyticsView.as_view(), name='assignment_analytics'),
    path('teachers/', views.TeacherPerformanceView.as_view(), name='teacher_performance'),
    path('teachers/<int:teacher_id>/', views.TeacherPerformanceView.as_view(), name='teacher_performance_detail'),
    
    # Reports
    path('reports/', views.ReportListView.as_view(), name='report_list'),
    path('reports/<int:report_id>/', views.ReportDetailView.as_view(), name='report_detail'),
    path('reports/<int:report_id>/download/', views.ReportDownloadView.as_view(), name='report_download'),
    
    # Export
    path('export/', views.ExportView.as_view(), name='export'),
    
    # Cache management
    path('cache/', views.CacheManagementView.as_view(), name='cache_management'),
]
