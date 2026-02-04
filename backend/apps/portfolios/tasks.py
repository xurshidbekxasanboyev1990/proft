"""
Celery tasks for async operations.
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_notification_email(self, user_email, subject, message):
    """
    Send notification email asynchronously.
    
    Args:
        user_email: Recipient email address
        subject: Email subject
        message: Email body
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user_email],
            fail_silently=False,
        )
        logger.info(f"Email sent to {user_email}: {subject}")
        return True
    except Exception as exc:
        logger.error(f"Failed to send email to {user_email}: {exc}")
        raise self.retry(exc=exc, countdown=60)


@shared_task
def notify_portfolio_status_change(portfolio_id, old_status, new_status, reviewer_name=None):
    """
    Notify teacher when their portfolio status changes.
    
    Args:
        portfolio_id: ID of the portfolio
        old_status: Previous status
        new_status: New status
        reviewer_name: Name of the reviewer (for approved/rejected)
    """
    from apps.portfolios.models import Portfolio
    
    try:
        portfolio = Portfolio.objects.select_related('teacher').get(id=portfolio_id)
        teacher = portfolio.teacher
        
        if not teacher.email:
            logger.warning(f"Teacher {teacher.username} has no email")
            return False
        
        status_messages = {
            'approved': f"Congratulations! Your portfolio '{portfolio.title}' has been approved by {reviewer_name or 'an administrator'}.",
            'rejected': f"Your portfolio '{portfolio.title}' has been rejected by {reviewer_name or 'an administrator'}. Please review the feedback and make necessary changes.",
            'pending': f"Your portfolio '{portfolio.title}' is now pending review.",
        }
        
        subject = f"Portfolio Status Update: {portfolio.title}"
        message = status_messages.get(new_status, f"Your portfolio '{portfolio.title}' status has been updated to {new_status}.")
        
        if portfolio.review_comment:
            message += f"\n\nReview Comment: {portfolio.review_comment}"
        
        send_notification_email.delay(teacher.email, subject, message)
        logger.info(f"Notification queued for portfolio {portfolio_id} status change")
        return True
        
    except Portfolio.DoesNotExist:
        logger.error(f"Portfolio {portfolio_id} not found")
        return False
    except Exception as exc:
        logger.error(f"Failed to notify portfolio status change: {exc}")
        return False


@shared_task
def cleanup_old_activities():
    """
    Cleanup old user activities (older than 90 days).
    """
    from django.utils import timezone
    from datetime import timedelta
    from apps.accounts.models import UserActivity
    
    threshold = timezone.now() - timedelta(days=90)
    deleted_count, _ = UserActivity.objects.filter(created_at__lt=threshold).delete()
    
    logger.info(f"Cleaned up {deleted_count} old user activities")
    return deleted_count


@shared_task
def generate_portfolio_report():
    """
    Generate daily portfolio statistics report.
    """
    from django.db.models import Count
    from apps.portfolios.models import Portfolio
    from django.utils import timezone
    from datetime import timedelta
    
    today = timezone.now().date()
    yesterday = today - timedelta(days=1)
    
    stats = {
        'date': str(today),
        'total_portfolios': Portfolio.objects.count(),
        'pending': Portfolio.objects.filter(status='pending').count(),
        'approved': Portfolio.objects.filter(status='approved').count(),
        'rejected': Portfolio.objects.filter(status='rejected').count(),
        'created_yesterday': Portfolio.objects.filter(
            created_at__date=yesterday
        ).count(),
        'approved_yesterday': Portfolio.objects.filter(
            status='approved',
            reviewed_at__date=yesterday
        ).count(),
    }
    
    logger.info(f"Daily portfolio report: {stats}")
    return stats
