"""
Signals for assignments app.
Handles notifications when assignments are created or updated.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Assignment, AssignmentSubmission


@receiver(post_save, sender=Assignment)
def assignment_created_notification(sender, instance, created, **kwargs):
    """
    Send notification when a new assignment is created.
    """
    if created:
        # Send email notification to assigned teacher
        if instance.assigned_to and instance.assigned_to.email:
            try:
                send_mail(
                    subject=f'Yangi topshiriq: {instance.title}',
                    message=f'''
Hurmatli {instance.assigned_to.get_full_name() or instance.assigned_to.username},

Sizga yangi topshiriq berildi:

Sarlavha: {instance.title}
Kategoriya: {instance.category.name}
Muddat: {instance.deadline.strftime("%Y-%m-%d %H:%M")}

Tavsif:
{instance.description}

Topshiriqni bajarish uchun tizimga kiring.

Hurmat bilan,
Portfolio Tizimi
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.assigned_to.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email yuborishda xatolik: {e}")


@receiver(pre_save, sender=Assignment)
def check_assignment_status_change(sender, instance, **kwargs):
    """
    Track assignment status changes.
    """
    if instance.pk:
        try:
            old_instance = Assignment.objects.get(pk=instance.pk)
            if old_instance.status != instance.status:
                # Status changed
                instance._status_changed = True
                instance._old_status = old_instance.status
            else:
                instance._status_changed = False
        except Assignment.DoesNotExist:
            instance._status_changed = False
    else:
        instance._status_changed = False


@receiver(post_save, sender=Assignment)
def assignment_status_changed_notification(sender, instance, created, **kwargs):
    """
    Send notification when assignment status changes.
    """
    if not created and getattr(instance, '_status_changed', False):
        old_status = getattr(instance, '_old_status', None)
        
        # Notify teacher about status change
        if instance.assigned_to and instance.assigned_to.email:
            status_labels = dict(Assignment.STATUS_CHOICES)
            old_label = status_labels.get(old_status, old_status)
            new_label = status_labels.get(instance.status, instance.status)
            
            try:
                send_mail(
                    subject=f'Topshiriq holati o\'zgardi: {instance.title}',
                    message=f'''
Hurmatli {instance.assigned_to.get_full_name() or instance.assigned_to.username},

"{instance.title}" topshirig'ingiz holati o'zgardi:

Avvalgi holat: {old_label}
Yangi holat: {new_label}

Tizimga kirib, batafsil ma'lumot olishingiz mumkin.

Hurmat bilan,
Portfolio Tizimi
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.assigned_to.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email yuborishda xatolik: {e}")


@receiver(post_save, sender=AssignmentSubmission)
def submission_notification(sender, instance, created, **kwargs):
    """
    Send notification when a submission is made.
    """
    if created:
        assignment = instance.assignment
        
        # Notify admin/creator about new submission
        if assignment.created_by and assignment.created_by.email:
            try:
                send_mail(
                    subject=f'Yangi javob: {assignment.title}',
                    message=f'''
Hurmatli {assignment.created_by.get_full_name() or assignment.created_by.username},

"{assignment.title}" topshirig'iga yangi javob keldi:

O'qituvchi: {assignment.assigned_to.get_full_name() or assignment.assigned_to.username}
Yuborilgan vaqt: {instance.submitted_at.strftime("%Y-%m-%d %H:%M")}

Tizimga kirib, javobni tekshirishingiz mumkin.

Hurmat bilan,
Portfolio Tizimi
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[assignment.created_by.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email yuborishda xatolik: {e}")


@receiver(pre_save, sender=AssignmentSubmission)
def check_submission_grade_change(sender, instance, **kwargs):
    """
    Track submission grade changes.
    """
    if instance.pk:
        try:
            old_instance = AssignmentSubmission.objects.get(pk=instance.pk)
            if old_instance.grade != instance.grade and instance.grade is not None:
                instance._grade_changed = True
                instance._old_grade = old_instance.grade
            else:
                instance._grade_changed = False
        except AssignmentSubmission.DoesNotExist:
            instance._grade_changed = False
    else:
        instance._grade_changed = False


@receiver(post_save, sender=AssignmentSubmission)
def submission_graded_notification(sender, instance, created, **kwargs):
    """
    Send notification when submission is graded.
    """
    if not created and getattr(instance, '_grade_changed', False):
        assignment = instance.assignment
        
        # Notify teacher about grading
        if assignment.assigned_to and assignment.assigned_to.email:
            try:
                send_mail(
                    subject=f'Topshiriq baholandi: {assignment.title}',
                    message=f'''
Hurmatli {assignment.assigned_to.get_full_name() or assignment.assigned_to.username},

"{assignment.title}" topshirig'ingiz baholandi:

Baho: {instance.grade}/100

Izoh:
{instance.feedback or "Izoh yo'q"}

Tizimga kirib, batafsil ma'lumot olishingiz mumkin.

Hurmat bilan,
Portfolio Tizimi
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[assignment.assigned_to.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email yuborishda xatolik: {e}")
