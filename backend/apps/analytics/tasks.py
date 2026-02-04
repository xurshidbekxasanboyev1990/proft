"""
Celery tasks for analytics app.
Async report generation and scheduled analytics updates.
"""

from celery import shared_task
from django.utils import timezone
from django.core.files.base import ContentFile
import traceback


@shared_task
def generate_report(report_id):
    """
    Generate report asynchronously.
    
    Args:
        report_id: Report ID to generate
    """
    from .models import Report, ReportStatus
    from .services import AnalyticsService
    from .exporters import get_exporter
    
    try:
        report = Report.objects.get(id=report_id)
    except Report.DoesNotExist:
        return f"Report {report_id} not found"
    
    # Update status
    report.status = ReportStatus.PROCESSING
    report.save(update_fields=['status'])
    
    try:
        # Get data based on report type
        date_from = report.date_from
        date_to = report.date_to
        
        if report.report_type == 'portfolio_summary':
            data = AnalyticsService.get_portfolio_analytics(date_from, date_to)
        elif report.report_type == 'assignment_summary':
            data = AnalyticsService.get_assignment_analytics(date_from, date_to)
        elif report.report_type == 'teacher_performance':
            teacher_id = report.filters.get('teacher_id')
            data = AnalyticsService.get_teacher_performance(teacher_id, date_from, date_to)
        elif report.report_type == 'category_analytics':
            data = AnalyticsService.get_assignment_analytics(date_from, date_to)
        elif report.report_type in ['monthly_report', 'yearly_report']:
            # Combined report
            data = {
                'overview': AnalyticsService.get_overview_stats(),
                'portfolios': AnalyticsService.get_portfolio_analytics(date_from, date_to),
                'assignments': AnalyticsService.get_assignment_analytics(date_from, date_to),
            }
        else:
            # Custom report - use filters
            data = AnalyticsService.get_overview_stats()
        
        # Store data
        report.data = data
        
        # Generate file if not JSON
        if report.format != 'json':
            try:
                exporter = get_exporter(report.format, data, report.title)
                file_content = exporter.export()
                
                filename = f"{report.title.replace(' ', '_')}_{report.created_at.strftime('%Y%m%d')}.{report.format}"
                report.file.save(filename, ContentFile(file_content), save=False)
                report.file_size = len(file_content)
            except Exception as e:
                # File generation failed, but data is saved
                report.error_message = f"File generation failed: {str(e)}"
        
        report.status = ReportStatus.COMPLETED
        report.completed_at = timezone.now()
        report.save()
        
        return f"Report {report_id} generated successfully"
        
    except Exception as e:
        report.status = ReportStatus.FAILED
        report.error_message = f"{str(e)}\n{traceback.format_exc()}"
        report.completed_at = timezone.now()
        report.save()
        
        return f"Report {report_id} failed: {str(e)}"


@shared_task
def cleanup_old_reports(days=30):
    """
    Clean up old reports and their files.
    
    Args:
        days: Delete reports older than this many days
    """
    from .models import Report
    
    cutoff_date = timezone.now() - timezone.timedelta(days=days)
    
    old_reports = Report.objects.filter(created_at__lt=cutoff_date)
    
    deleted_count = 0
    for report in old_reports:
        if report.file:
            report.file.delete()
        report.delete()
        deleted_count += 1
    
    return f"Deleted {deleted_count} old reports"


@shared_task
def cleanup_expired_cache():
    """
    Clean up expired cache entries.
    """
    from .models import AnalyticsCache
    
    count, _ = AnalyticsCache.cleanup_expired()
    
    return f"Cleaned up {count} expired cache entries"


@shared_task
def refresh_dashboard_cache():
    """
    Refresh dashboard cache periodically.
    """
    from .models import AnalyticsCache
    from .services import AnalyticsService
    
    # Refresh overview stats
    AnalyticsCache.invalidate('dashboard_overview')
    data = AnalyticsService.get_overview_stats()
    AnalyticsCache.get_or_set('dashboard_overview', lambda: data, timeout=300)
    
    # Refresh chart data
    for chart_type in ['portfolio_trend', 'assignment_status', 'category_distribution']:
        for period in ['week', 'month']:
            cache_key = f'chart_{chart_type}_{period}'
            AnalyticsCache.invalidate(cache_key)
            chart_data = AnalyticsService.get_chart_data(chart_type, period)
            AnalyticsCache.get_or_set(cache_key, lambda: chart_data, timeout=600)
    
    return "Dashboard cache refreshed"


@shared_task
def generate_monthly_report():
    """
    Generate automatic monthly report.
    Runs on first day of each month.
    """
    from .models import Report
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    # Get superadmin user for report ownership
    superadmin = User.objects.filter(role='superadmin').first()
    if not superadmin:
        return "No superadmin found"
    
    now = timezone.now()
    last_month = now.replace(day=1) - timezone.timedelta(days=1)
    first_day = last_month.replace(day=1)
    
    # Create monthly report
    report = Report.objects.create(
        title=f"Oylik hisobot - {last_month.strftime('%Y-%m')}",
        report_type='monthly_report',
        format='excel',
        date_from=first_day.date(),
        date_to=last_month.date(),
        created_by=superadmin,
    )
    
    # Generate report
    generate_report.delay(report.id)
    
    return f"Monthly report {report.id} created for {last_month.strftime('%Y-%m')}"


@shared_task
def generate_yearly_report():
    """
    Generate automatic yearly report.
    Runs on first day of each year.
    """
    from .models import Report
    from django.contrib.auth import get_user_model
    
    User = get_user_model()
    
    superadmin = User.objects.filter(role='superadmin').first()
    if not superadmin:
        return "No superadmin found"
    
    now = timezone.now()
    last_year = now.year - 1
    first_day = timezone.datetime(last_year, 1, 1).date()
    last_day = timezone.datetime(last_year, 12, 31).date()
    
    report = Report.objects.create(
        title=f"Yillik hisobot - {last_year}",
        report_type='yearly_report',
        format='excel',
        date_from=first_day,
        date_to=last_day,
        created_by=superadmin,
    )
    
    generate_report.delay(report.id)
    
    return f"Yearly report {report.id} created for {last_year}"
