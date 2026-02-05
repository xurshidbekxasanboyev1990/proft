"""
Signals for assignments app.
Handles notifications when assignments are created or updated.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone

from .models import Assignment, AssignmentProgress


@receiver(post_save, sender=Assignment)
def assignment_created_notification(sender, instance, created, **kwargs):
    """
    Send notification when a new assignment is created.
    """
    if created:
        # Send email notification to assigned teacher
        if instance.teacher and instance.teacher.email:
            try:
                send_mail(
                    subject=f'Yangi topshiriq: {instance.title}',
                    message=f'''
Hurmatli {instance.teacher.get_full_name() or instance.teacher.username},

Sizga yangi topshiriq berildi:

Sarlavha: {instance.title}
Kategoriya: {instance.category.name}
Muddat: {instance.deadline.strftime("%Y-%m-%d %H:%M") if instance.deadline else "Belgilanmagan"}

Tavsif:
{instance.description or "Tavsif yo'q"}

Topshiriqni bajarish uchun tizimga kiring.

Hurmat bilan,
Portfolio Tizimi
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.teacher.email],
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
        if instance.teacher and instance.teacher.email:
            status_labels = dict(Assignment.STATUS_CHOICES)
            old_label = status_labels.get(old_status, old_status)
            new_label = status_labels.get(instance.status, instance.status)
            
            try:
                send_mail(
                    subject=f'Topshiriq holati o\'zgardi: {instance.title}',
                    message=f'''
Hurmatli {instance.teacher.get_full_name() or instance.teacher.username},

"{instance.title}" topshirig'ingiz holati o'zgardi:

Avvalgi holat: {old_label}
Yangi holat: {new_label}

Tizimga kirib, batafsil ma'lumot olishingiz mumkin.

Hurmat bilan,
Portfolio Tizimi
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[instance.teacher.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email yuborishda xatolik: {e}")


@receiver(post_save, sender=AssignmentProgress)
def progress_notification(sender, instance, created, **kwargs):
    """
    Send notification when a progress is recorded.
    """
    if created:
        assignment = instance.assignment
        
        # Notify admin/creator about new progress
        if assignment.created_by and assignment.created_by.email:
            try:
                send_mail(
                    subject=f'Yangi progress: {assignment.title}',
                    message=f'''
Hurmatli {assignment.created_by.get_full_name() or assignment.created_by.username},

"{assignment.title}" topshirig'iga yangi progress qo'shildi:

O'qituvchi: {assignment.teacher.get_full_name() or assignment.teacher.username}
Vaqt: {instance.created_at.strftime("%Y-%m-%d %H:%M")}

Tizimga kirib, progressni tekshirishingiz mumkin.

Hurmat bilan,
Portfolio Tizimi
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[assignment.created_by.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email yuborishda xatolik: {e}")


@receiver(pre_save, sender=AssignmentProgress)
def check_progress_grade_change(sender, instance, **kwargs):
    """
    Track progress grade changes.
    """
    if instance.pk:
        try:
            old_instance = AssignmentProgress.objects.get(pk=instance.pk)
            if old_instance.raw_score != instance.raw_score and instance.raw_score is not None:
                instance._grade_changed = True
                instance._old_grade = old_instance.raw_score
            else:
                instance._grade_changed = False
        except AssignmentProgress.DoesNotExist:
            instance._grade_changed = False
    else:
        instance._grade_changed = False


@receiver(post_save, sender=AssignmentProgress)
def progress_graded_notification(sender, instance, created, **kwargs):
    """
    Send notification when progress is graded.
    """
    if not created and getattr(instance, '_grade_changed', False):
        assignment = instance.assignment
        
        # Notify teacher about grading
        if assignment.teacher and assignment.teacher.email:
            try:
                send_mail(
                    subject=f'Topshiriq baholandi: {assignment.title}',
                    message=f'''
Hurmatli {assignment.teacher.get_full_name() or assignment.teacher.username},

"{assignment.title}" topshirig'ingiz baholandi:

Xom ball: {instance.raw_score}
Yakuniy ball: {instance.final_score}

Izoh:
{instance.grade_note or "Izoh yo'q"}

Tizimga kirib, batafsil ma'lumot olishingiz mumkin.

Hurmat bilan,
Portfolio Tizimi
                    '''.strip(),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[assignment.teacher.email],
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Email yuborishda xatolik: {e}")
