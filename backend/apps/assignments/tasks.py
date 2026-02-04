"""
Celery tasks for assignments app.
Handles async notifications and deadline reminders.
"""

from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


@shared_task
def send_assignment_notification(assignment_id, notification_type='created'):
    """
    Send email notification for assignment.
    
    Args:
        assignment_id: Assignment ID
        notification_type: 'created', 'updated', 'deadline_reminder'
    """
    from .models import Assignment
    
    try:
        assignment = Assignment.objects.select_related(
            'assigned_to', 'created_by', 'category'
        ).get(pk=assignment_id)
    except Assignment.DoesNotExist:
        return f"Assignment {assignment_id} not found"
    
    if not assignment.assigned_to or not assignment.assigned_to.email:
        return "No recipient email"
    
    teacher = assignment.assigned_to
    teacher_name = teacher.get_full_name() or teacher.username
    
    if notification_type == 'created':
        subject = f'Yangi topshiriq: {assignment.title}'
        message = f'''
Hurmatli {teacher_name},

Sizga yangi topshiriq berildi:

Sarlavha: {assignment.title}
Kategoriya: {assignment.category.name}
Muddat: {assignment.deadline.strftime("%Y-%m-%d %H:%M")}

Tavsif:
{assignment.description}

Topshiriqni bajarish uchun tizimga kiring.

Hurmat bilan,
Portfolio Tizimi
        '''.strip()
        
    elif notification_type == 'deadline_reminder':
        time_left = assignment.deadline - timezone.now()
        hours_left = int(time_left.total_seconds() / 3600)
        
        subject = f'Muddat yaqinlashmoqda: {assignment.title}'
        message = f'''
Hurmatli {teacher_name},

"{assignment.title}" topshirig'ining muddati yaqinlashmoqda!

Qolgan vaqt: {hours_left} soat
Muddat: {assignment.deadline.strftime("%Y-%m-%d %H:%M")}

Iltimos, topshiriqni o'z vaqtida bajaring.

Hurmat bilan,
Portfolio Tizimi
        '''.strip()
        
    else:
        return "Unknown notification type"
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[teacher.email],
            fail_silently=False,
        )
        return f"Notification sent to {teacher.email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@shared_task
def check_deadline_reminders():
    """
    Check for assignments with approaching deadlines and send reminders.
    Runs periodically via Celery Beat.
    """
    from .models import Assignment
    
    now = timezone.now()
    
    # Remind 24 hours before deadline
    reminder_24h = now + timedelta(hours=24)
    reminder_48h = now + timedelta(hours=48)
    
    # Get assignments due in 24-48 hours that haven't been reminded
    assignments_to_remind = Assignment.objects.filter(
        status__in=['pending', 'in_progress'],
        deadline__gt=now,
        deadline__lte=reminder_48h,
    ).exclude(
        # Exclude already completed or overdue
        status__in=['completed', 'overdue', 'cancelled']
    ).select_related('assigned_to', 'category')
    
    reminded_count = 0
    for assignment in assignments_to_remind:
        time_left = assignment.deadline - now
        hours_left = time_left.total_seconds() / 3600
        
        # Send reminder only once in the 24-48 hour window
        if 20 <= hours_left <= 28:
            send_assignment_notification.delay(
                assignment.id, 
                notification_type='deadline_reminder'
            )
            reminded_count += 1
    
    return f"Sent {reminded_count} deadline reminders"


@shared_task
def update_overdue_assignments():
    """
    Mark assignments as overdue if deadline has passed.
    Runs periodically via Celery Beat.
    """
    from .models import Assignment
    
    now = timezone.now()
    
    # Get pending/in_progress assignments past deadline
    overdue_assignments = Assignment.objects.filter(
        status__in=['pending', 'in_progress'],
        deadline__lt=now
    )
    
    updated_count = overdue_assignments.update(status='overdue')
    
    return f"Updated {updated_count} assignments to overdue"


@shared_task
def send_submission_notification(submission_id, notification_type='submitted'):
    """
    Send email notification for submission.
    
    Args:
        submission_id: AssignmentSubmission ID
        notification_type: 'submitted', 'graded'
    """
    from .models import AssignmentSubmission
    
    try:
        submission = AssignmentSubmission.objects.select_related(
            'assignment', 
            'assignment__assigned_to', 
            'assignment__created_by',
            'assignment__category'
        ).get(pk=submission_id)
    except AssignmentSubmission.DoesNotExist:
        return f"Submission {submission_id} not found"
    
    assignment = submission.assignment
    
    if notification_type == 'submitted':
        # Notify admin/creator
        if not assignment.created_by or not assignment.created_by.email:
            return "No admin email"
        
        recipient = assignment.created_by
        recipient_name = recipient.get_full_name() or recipient.username
        teacher_name = assignment.assigned_to.get_full_name() or assignment.assigned_to.username
        
        subject = f'Yangi javob: {assignment.title}'
        message = f'''
Hurmatli {recipient_name},

"{assignment.title}" topshirig'iga yangi javob keldi:

O'qituvchi: {teacher_name}
Yuborilgan vaqt: {submission.submitted_at.strftime("%Y-%m-%d %H:%M")}

Tizimga kirib, javobni tekshirishingiz mumkin.

Hurmat bilan,
Portfolio Tizimi
        '''.strip()
        
        recipient_email = recipient.email
        
    elif notification_type == 'graded':
        # Notify teacher
        if not assignment.assigned_to or not assignment.assigned_to.email:
            return "No teacher email"
        
        teacher = assignment.assigned_to
        teacher_name = teacher.get_full_name() or teacher.username
        
        subject = f'Topshiriq baholandi: {assignment.title}'
        message = f'''
Hurmatli {teacher_name},

"{assignment.title}" topshirig'ingiz baholandi:

Baho: {submission.grade}/100

Izoh:
{submission.feedback or "Izoh yo'q"}

Tizimga kirib, batafsil ma'lumot olishingiz mumkin.

Hurmat bilan,
Portfolio Tizimi
        '''.strip()
        
        recipient_email = teacher.email
        
    else:
        return "Unknown notification type"
    
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[recipient_email],
            fail_silently=False,
        )
        return f"Notification sent to {recipient_email}"
    except Exception as e:
        return f"Failed to send email: {str(e)}"


@shared_task
def generate_assignment_report(user_id, date_from=None, date_to=None):
    """
    Generate assignment statistics report.
    
    Args:
        user_id: User ID to generate report for (or None for all)
        date_from: Start date (ISO format string)
        date_to: End date (ISO format string)
    """
    from .models import Assignment
    from django.db.models import Count, Avg
    from datetime import datetime
    
    queryset = Assignment.objects.all()
    
    if user_id:
        queryset = queryset.filter(assigned_to_id=user_id)
    
    if date_from:
        date_from = datetime.fromisoformat(date_from)
        queryset = queryset.filter(created_at__gte=date_from)
    
    if date_to:
        date_to = datetime.fromisoformat(date_to)
        queryset = queryset.filter(created_at__lte=date_to)
    
    # Get statistics
    from django.db.models import Q
    stats = queryset.aggregate(
        total=Count('id'),
        completed=Count('id', filter=Q(status='completed')),
        pending=Count('id', filter=Q(status='pending')),
        in_progress=Count('id', filter=Q(status='in_progress')),
        overdue=Count('id', filter=Q(status='overdue')),
    )
    
    # Get average grade
    from .models import AssignmentSubmission
    submissions = AssignmentSubmission.objects.filter(
        assignment__in=queryset,
        grade__isnull=False
    )
    avg_grade = submissions.aggregate(avg=Avg('grade'))['avg']
    
    stats['average_grade'] = round(avg_grade, 2) if avg_grade else None
    
    return stats
