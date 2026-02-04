"""
Models for assignments and categories.
Admin/SuperAdmin can create categories (tezis, esse, etc.) and assign tasks to teachers.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from datetime import timedelta


class Category(models.Model):
    """
    Dynamic categories for portfolio items.
    Examples: Tezis, Esse, Maqola, Sertifikat, etc.
    Only Admin/SuperAdmin can create/edit.
    """
    
    name = models.CharField(
        _('name'),
        max_length=100,
        unique=True
    )
    name_uz = models.CharField(
        _('name (Uzbek)'),
        max_length=100,
        blank=True,
        null=True
    )
    name_ru = models.CharField(
        _('name (Russian)'),
        max_length=100,
        blank=True,
        null=True
    )
    name_en = models.CharField(
        _('name (English)'),
        max_length=100,
        blank=True,
        null=True
    )
    
    slug = models.SlugField(
        _('slug'),
        max_length=100,
        unique=True
    )
    
    description = models.TextField(
        _('description'),
        blank=True,
        null=True
    )
    
    icon = models.CharField(
        _('icon'),
        max_length=50,
        blank=True,
        null=True,
        help_text=_('Icon class name (e.g., fa-file-text)')
    )
    
    color = models.CharField(
        _('color'),
        max_length=20,
        default='#3498db',
        help_text=_('Hex color code')
    )
    
    # Points/weight for this category
    points = models.PositiveIntegerField(
        _('points'),
        default=1,
        help_text=_('Points awarded for completing one item of this category')
    )
    
    is_active = models.BooleanField(
        _('is active'),
        default=True
    )
    
    # Ordering
    order = models.PositiveIntegerField(
        _('order'),
        default=0
    )
    
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_categories'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def get_localized_name(self, lang='uz'):
        """Get localized name based on language."""
        if lang == 'uz' and self.name_uz:
            return self.name_uz
        elif lang == 'ru' and self.name_ru:
            return self.name_ru
        elif lang == 'en' and self.name_en:
            return self.name_en
        return self.name


class Assignment(models.Model):
    """
    Task/Assignment given to a teacher by Admin/SuperAdmin.
    Example: "3 ta tezis, 2 ta esse" with deadline.
    """
    
    STATUS_ACTIVE = 'active'
    STATUS_COMPLETED = 'completed'
    STATUS_OVERDUE = 'overdue'
    STATUS_CANCELLED = 'cancelled'
    
    STATUS_CHOICES = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_COMPLETED, _('Completed')),
        (STATUS_OVERDUE, _('Overdue')),
        (STATUS_CANCELLED, _('Cancelled')),
    ]
    
    # Who is assigned
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='assignments',
        limit_choices_to={'role': 'teacher'}
    )
    
    # What category
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='assignments'
    )
    
    # How many items required
    required_quantity = models.PositiveIntegerField(
        _('required quantity'),
        default=1
    )
    
    # How many completed
    completed_quantity = models.PositiveIntegerField(
        _('completed quantity'),
        default=0
    )
    
    # Deadline
    deadline = models.DateTimeField(
        _('deadline')
    )
    
    # Title and description
    title = models.CharField(
        _('title'),
        max_length=255,
        blank=True,
        null=True
    )
    
    description = models.TextField(
        _('description'),
        blank=True,
        null=True,
        help_text=_('Additional instructions for the teacher')
    )
    
    # Status
    status = models.CharField(
        _('status'),
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_ACTIVE,
        db_index=True
    )
    
    # Priority
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'
    PRIORITY_URGENT = 'urgent'
    
    PRIORITY_CHOICES = [
        (PRIORITY_LOW, _('Low')),
        (PRIORITY_MEDIUM, _('Medium')),
        (PRIORITY_HIGH, _('High')),
        (PRIORITY_URGENT, _('Urgent')),
    ]
    
    priority = models.CharField(
        _('priority'),
        max_length=20,
        choices=PRIORITY_CHOICES,
        default=PRIORITY_MEDIUM
    )
    
    # Assigned by
    assigned_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='given_assignments'
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(
        _('completed at'),
        null=True,
        blank=True
    )
    
    class Meta:
        verbose_name = _('assignment')
        verbose_name_plural = _('assignments')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['teacher', 'status']),
            models.Index(fields=['deadline']),
            models.Index(fields=['category']),
        ]
    
    def __str__(self):
        return f"{self.teacher.get_full_name()} - {self.category.name} ({self.required_quantity})"
    
    @property
    def is_overdue(self):
        """Check if assignment is overdue."""
        if self.status == self.STATUS_COMPLETED:
            return False
        return timezone.now() > self.deadline
    
    @property
    def remaining_quantity(self):
        """Get remaining items to complete."""
        return max(0, self.required_quantity - self.completed_quantity)
    
    @property
    def progress_percentage(self):
        """Get completion percentage."""
        if self.required_quantity == 0:
            return 100
        return min(100, int((self.completed_quantity / self.required_quantity) * 100))
    
    @property
    def time_remaining(self):
        """Get time remaining until deadline."""
        if self.status == self.STATUS_COMPLETED:
            return timedelta(0)
        
        now = timezone.now()
        if now > self.deadline:
            return timedelta(0)
        
        return self.deadline - now
    
    @property
    def time_remaining_display(self):
        """Get human-readable time remaining."""
        remaining = self.time_remaining
        
        if remaining.total_seconds() <= 0:
            return _("Muddat o'tgan")
        
        days = remaining.days
        hours = remaining.seconds // 3600
        minutes = (remaining.seconds % 3600) // 60
        
        if days > 30:
            months = days // 30
            return f"{months} oy qoldi"
        elif days > 0:
            return f"{days} kun {hours} soat qoldi"
        elif hours > 0:
            return f"{hours} soat {minutes} daqiqa qoldi"
        else:
            return f"{minutes} daqiqa qoldi"
    
    @property
    def days_remaining(self):
        """Get days remaining."""
        return self.time_remaining.days
    
    def mark_completed(self):
        """Mark assignment as completed."""
        self.status = self.STATUS_COMPLETED
        self.completed_at = timezone.now()
        self.save()
    
    def increment_completed(self, count=1):
        """Increment completed quantity."""
        self.completed_quantity += count
        if self.completed_quantity >= self.required_quantity:
            self.mark_completed()
        else:
            self.save()
    
    def check_and_update_status(self):
        """Check and update status based on deadline and completion."""
        if self.status == self.STATUS_CANCELLED:
            return
        
        if self.completed_quantity >= self.required_quantity:
            if self.status != self.STATUS_COMPLETED:
                self.mark_completed()
        elif self.is_overdue:
            if self.status != self.STATUS_OVERDUE:
                self.status = self.STATUS_OVERDUE
                self.save()
        elif self.status == self.STATUS_OVERDUE:
            # Reset if deadline was extended
            self.status = self.STATUS_ACTIVE
            self.save()


class AssignmentProgress(models.Model):
    """
    Track individual progress items for an assignment.
    Links to portfolios submitted for this assignment.
    """
    
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='progress_items'
    )
    
    portfolio = models.ForeignKey(
        'portfolios.Portfolio',
        on_delete=models.CASCADE,
        related_name='assignment_progress',
        null=True,
        blank=True
    )
    
    note = models.TextField(
        _('note'),
        blank=True,
        null=True
    )
    
    # Counts towards assignment
    counted = models.BooleanField(
        _('counted'),
        default=False,
        help_text=_('Whether this progress counts towards the assignment')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('assignment progress')
        verbose_name_plural = _('assignment progress items')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.assignment} - Progress"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        # Update assignment completed quantity
        if self.counted and self.portfolio:
            counted_items = self.assignment.progress_items.filter(counted=True).count()
            self.assignment.completed_quantity = counted_items
            self.assignment.check_and_update_status()
