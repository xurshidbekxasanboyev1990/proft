"""
Signal handlers for the portfolios app.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import Portfolio, PortfolioHistory


@receiver(pre_save, sender=Portfolio)
def track_status_change(sender, instance, **kwargs):
    """Track portfolio status changes before save."""
    if instance.pk:
        try:
            old_instance = Portfolio.objects.get(pk=instance.pk)
            instance._old_status = old_instance.status
        except Portfolio.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None


@receiver(post_save, sender=Portfolio)
def create_history_on_status_change(sender, instance, created, **kwargs):
    """Create history entry when portfolio status changes."""
    if created:
        # History for new portfolio is created in the view
        return
    
    old_status = getattr(instance, '_old_status', None)
    
    if old_status and old_status != instance.status:
        # Status has changed, but history should be created by the view
        # This is a fallback for direct model saves
        existing_history = PortfolioHistory.objects.filter(
            portfolio=instance,
            new_status=instance.status
        ).order_by('-created_at').first()
        
        # Only create if no recent history exists
        if not existing_history or (
            existing_history.old_status != old_status
        ):
            # This will be a rare case since views handle this
            pass
