"""
Views for analytics app.
Dashboard and reports API endpoints.
"""

import json
from datetime import datetime
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect

from apps.accounts.permissions import admin_required, superadmin_required
from apps.accounts.views import get_client_ip
from apps.accounts.models import UserActivity
from .models import Report, ReportStatus, ReportFormat, DashboardWidget, AnalyticsCache
from .services import AnalyticsService
from .exporters import get_exporter


# ==================== DASHBOARD VIEWS ====================

class DashboardOverviewView(View):
    """
    GET /api/analytics/dashboard/overview/
    Get overview statistics for dashboard
    """
    
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # Check permission
        if request.user.role not in ['admin', 'superadmin']:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Try to get from cache
        cache_key = 'dashboard_overview'
        
        def get_stats():
            return AnalyticsService.get_overview_stats()
        
        # Cache for 5 minutes
        data = AnalyticsCache.get_or_set(cache_key, get_stats, timeout=300)
        
        return JsonResponse(data)


class DashboardWidgetsView(View):
    """
    GET /api/analytics/dashboard/widgets/
    Get dashboard widgets configuration for current user
    """
    
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        widgets = DashboardWidget.objects.filter(is_active=True)
        
        # Filter by user role
        user_widgets = [w for w in widgets if w.is_visible_to(request.user)]
        
        data = [{
            'id': w.id,
            'name': w.name,
            'type': w.widget_type,
            'data_source': w.data_source,
            'config': w.config,
            'order': w.order,
        } for w in user_widgets]
        
        return JsonResponse({'widgets': data})


class ChartDataView(View):
    """
    GET /api/analytics/charts/<chart_type>/
    Get data for specific chart
    """
    
    def get(self, request, chart_type):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        period = request.GET.get('period', 'month')
        
        if period not in ['week', 'month', 'year']:
            return JsonResponse({'error': 'Invalid period'}, status=400)
        
        valid_charts = [
            'portfolio_trend', 'assignment_status', 'category_distribution',
            'teacher_performance', 'grade_distribution'
        ]
        
        if chart_type not in valid_charts:
            return JsonResponse({
                'error': f"Invalid chart type. Valid: {', '.join(valid_charts)}"
            }, status=400)
        
        # Cache key
        cache_key = f'chart_{chart_type}_{period}'
        
        def get_chart():
            return AnalyticsService.get_chart_data(chart_type, period)
        
        data = AnalyticsCache.get_or_set(cache_key, get_chart, timeout=600)
        
        return JsonResponse(data)


# ==================== ANALYTICS VIEWS ====================

class PortfolioAnalyticsView(View):
    """
    GET /api/analytics/portfolios/
    Get portfolio analytics
    """
    
    @method_decorator(admin_required)
    def get(self, request):
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        # Parse dates
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
            date_to = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        
        data = AnalyticsService.get_portfolio_analytics(date_from, date_to)
        
        return JsonResponse(data)


class AssignmentAnalyticsView(View):
    """
    GET /api/analytics/assignments/
    Get assignment analytics
    """
    
    @method_decorator(admin_required)
    def get(self, request):
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
            date_to = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        
        data = AnalyticsService.get_assignment_analytics(date_from, date_to)
        
        return JsonResponse(data)


class TeacherPerformanceView(View):
    """
    GET /api/analytics/teachers/
    GET /api/analytics/teachers/<teacher_id>/
    Get teacher performance analytics
    """
    
    @method_decorator(admin_required)
    def get(self, request, teacher_id=None):
        date_from = request.GET.get('date_from')
        date_to = request.GET.get('date_to')
        
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
            date_to = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None
        except ValueError:
            return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD'}, status=400)
        
        data = AnalyticsService.get_teacher_performance(teacher_id, date_from, date_to)
        
        return JsonResponse(data)


# ==================== REPORT VIEWS ====================

class ReportListView(View):
    """
    GET /api/analytics/reports/ - List reports
    POST /api/analytics/reports/ - Create new report
    """
    
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # Admins see all, teachers see their own
        if request.user.role in ['admin', 'superadmin']:
            reports = Report.objects.all()
        else:
            reports = Report.objects.filter(created_by=request.user)
        
        # Filters
        report_type = request.GET.get('type')
        status = request.GET.get('status')
        
        if report_type:
            reports = reports.filter(report_type=report_type)
        if status:
            reports = reports.filter(status=status)
        
        # Pagination
        page = int(request.GET.get('page', 1))
        per_page = int(request.GET.get('per_page', 20))
        
        start = (page - 1) * per_page
        end = start + per_page
        
        total = reports.count()
        reports = reports[start:end]
        
        data = [{
            'id': r.id,
            'title': r.title,
            'report_type': r.report_type,
            'report_type_display': r.get_report_type_display(),
            'format': r.format,
            'status': r.status,
            'status_display': r.get_status_display(),
            'created_by': r.created_by.get_full_name() or r.created_by.username,
            'created_at': r.created_at.isoformat(),
            'completed_at': r.completed_at.isoformat() if r.completed_at else None,
            'file_size': r.file_size_display,
            'has_file': bool(r.file),
        } for r in reports]
        
        return JsonResponse({
            'reports': data,
            'total': total,
            'page': page,
            'per_page': per_page,
            'total_pages': (total + per_page - 1) // per_page,
        })
    
    @method_decorator(csrf_protect)
    def post(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Validation
        title = data.get('title', '').strip()
        report_type = data.get('report_type', 'custom_report')
        format = data.get('format', 'json')
        
        if not title:
            return JsonResponse({'error': 'Title is required'}, status=400)
        
        # Create report
        report = Report.objects.create(
            title=title,
            report_type=report_type,
            format=format,
            date_from=data.get('date_from'),
            date_to=data.get('date_to'),
            filters=data.get('filters', {}),
            created_by=request.user,
        )
        
        # Generate report async (or sync for now)
        from .tasks import generate_report
        generate_report.delay(report.id)
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_CREATE,
            target_model='Report',
            target_id=report.id,
            description=f'Created report: {report.title}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Report created and processing started',
            'report': {
                'id': report.id,
                'title': report.title,
                'status': report.status,
            }
        }, status=201)


class ReportDetailView(View):
    """
    GET /api/analytics/reports/<report_id>/
    DELETE /api/analytics/reports/<report_id>/
    """
    
    def get(self, request, report_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return JsonResponse({'error': 'Report not found'}, status=404)
        
        # Check permission
        if request.user.role not in ['admin', 'superadmin'] and report.created_by != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        return JsonResponse({
            'id': report.id,
            'title': report.title,
            'report_type': report.report_type,
            'report_type_display': report.get_report_type_display(),
            'format': report.format,
            'status': report.status,
            'status_display': report.get_status_display(),
            'date_from': report.date_from.isoformat() if report.date_from else None,
            'date_to': report.date_to.isoformat() if report.date_to else None,
            'filters': report.filters,
            'data': report.data if report.status == 'completed' else None,
            'file_url': report.file.url if report.file else None,
            'file_size': report.file_size_display,
            'created_by': {
                'id': report.created_by.id,
                'name': report.created_by.get_full_name() or report.created_by.username,
            },
            'created_at': report.created_at.isoformat(),
            'completed_at': report.completed_at.isoformat() if report.completed_at else None,
            'processing_time': report.processing_time,
            'error_message': report.error_message if report.status == 'failed' else None,
        })
    
    @method_decorator(csrf_protect)
    def delete(self, request, report_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return JsonResponse({'error': 'Report not found'}, status=404)
        
        # Check permission
        if request.user.role not in ['admin', 'superadmin'] and report.created_by != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        title = report.title
        report_id_saved = report.id
        
        # Delete file if exists
        if report.file:
            report.file.delete()
        
        report.delete()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_DELETE,
            target_model='Report',
            target_id=report_id_saved,
            description=f'Deleted report: {title}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({'message': 'Report deleted successfully'})


class ReportDownloadView(View):
    """
    GET /api/analytics/reports/<report_id>/download/
    Download report file
    """
    
    def get(self, request, report_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            report = Report.objects.get(id=report_id)
        except Report.DoesNotExist:
            return JsonResponse({'error': 'Report not found'}, status=404)
        
        # Check permission
        if request.user.role not in ['admin', 'superadmin'] and report.created_by != request.user:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        if report.status != 'completed':
            return JsonResponse({'error': 'Report is not ready yet'}, status=400)
        
        # If file exists, return it
        if report.file:
            from django.http import FileResponse
            return FileResponse(report.file.open('rb'), as_attachment=True)
        
        # Otherwise generate on-the-fly
        if not report.data:
            return JsonResponse({'error': 'No data available'}, status=400)
        
        try:
            exporter = get_exporter(report.format, report.data, report.title)
            filename = f"{report.title.replace(' ', '_')}_{report.created_at.strftime('%Y%m%d')}.{report.format}"
            return exporter.get_response(filename)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


class ExportView(View):
    """
    POST /api/analytics/export/
    Quick export without saving report
    """
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def post(self, request):
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        export_type = data.get('type', 'overview')
        format = data.get('format', 'excel')
        date_from = data.get('date_from')
        date_to = data.get('date_to')
        
        # Parse dates
        try:
            date_from = datetime.strptime(date_from, '%Y-%m-%d') if date_from else None
            date_to = datetime.strptime(date_to, '%Y-%m-%d') if date_to else None
        except ValueError:
            return JsonResponse({'error': 'Invalid date format'}, status=400)
        
        # Get data based on type
        if export_type == 'overview':
            export_data = AnalyticsService.get_overview_stats()
            title = 'Umumiy statistika'
        elif export_type == 'portfolios':
            export_data = AnalyticsService.get_portfolio_analytics(date_from, date_to)
            title = 'Portfolio hisoboti'
        elif export_type == 'assignments':
            export_data = AnalyticsService.get_assignment_analytics(date_from, date_to)
            title = 'Topshiriqlar hisoboti'
        elif export_type == 'teachers':
            export_data = AnalyticsService.get_teacher_performance(None, date_from, date_to)
            title = 'O\'qituvchilar hisoboti'
        else:
            return JsonResponse({'error': 'Invalid export type'}, status=400)
        
        try:
            exporter = get_exporter(format, export_data, title)
            filename = f"{title.replace(' ', '_')}_{timezone.now().strftime('%Y%m%d_%H%M')}.{format}"
            return exporter.get_response(filename)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)


# ==================== CACHE MANAGEMENT ====================

class CacheManagementView(View):
    """
    DELETE /api/analytics/cache/
    Clear analytics cache (SuperAdmin only)
    """
    
    @method_decorator(csrf_protect)
    @method_decorator(superadmin_required)
    def delete(self, request):
        key_pattern = request.GET.get('pattern')
        
        deleted = AnalyticsCache.invalidate(key_pattern)
        
        return JsonResponse({
            'message': 'Cache cleared successfully',
            'pattern': key_pattern or 'all',
        })
