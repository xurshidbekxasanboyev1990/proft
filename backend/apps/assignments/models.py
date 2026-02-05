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
    
    # ==================== BALL TIZIMI ====================
    # Default ball - kategoriya uchun standart maksimal ball
    default_score = models.PositiveIntegerField(
        _('default score'),
        default=10,
        help_text=_('Bu kategoriya uchun standart maksimal ball (masalan: Esse=10, Tezis=15)')
    )
    
    min_score = models.PositiveIntegerField(
        _('minimum score'),
        default=0,
        help_text=_('Minimal ball (odatda 0)')
    )
    
    # Ball og'irligi - umumiy ballni hisoblashda koeffitsient
    score_weight = models.DecimalField(
        _('score weight'),
        max_digits=4,
        decimal_places=2,
        default=1.00,
        help_text=_('Ball koeffitsienti (1.0=100%, 1.5=150% bonus)')
    )
    
    # Points/weight for this category (legacy, kept for compatibility)
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
    
    # ==================== MAXSUS BALL TIZIMI ====================
    # Admin/SuperAdmin alohida topshiriq uchun ball o'zgartirishi mumkin
    use_custom_score = models.BooleanField(
        _('use custom score'),
        default=False,
        help_text=_('True bo\'lsa, kategoriya default balini emas, maxsus ballni ishlatadi')
    )
    
    custom_max_score = models.PositiveIntegerField(
        _('custom maximum score'),
        null=True,
        blank=True,
        help_text=_('Maxsus maksimal ball (masalan: oddiy esse=10, kuchli esse=20)')
    )
    
    custom_min_score = models.PositiveIntegerField(
        _('custom minimum score'),
        null=True,
        blank=True,
        default=0,
        help_text=_('Maxsus minimal ball')
    )
    
    score_multiplier = models.DecimalField(
        _('score multiplier'),
        max_digits=4,
        decimal_places=2,
        default=1.00,
        help_text=_('Ball koeffitsienti (1.0=normal, 1.5=50% bonus, 2.0=2x ball)')
    )
    
    score_note = models.CharField(
        _('score note'),
        max_length=255,
        blank=True,
        null=True,
        help_text=_('Ball o\'zgartirilgan sababi (masalan: "Ilmiy jurnal uchun bonus")')
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
    
    # ==================== BALL HISOBLASH ====================
    @property
    def max_score(self):
        """Maksimal ballni qaytaradi (custom yoki category default)."""
        if self.use_custom_score and self.custom_max_score is not None:
            return self.custom_max_score
        return self.category.default_score
    
    @property
    def min_score_value(self):
        """Minimal ballni qaytaradi."""
        if self.use_custom_score and self.custom_min_score is not None:
            return self.custom_min_score
        return self.category.min_score
    
    @property
    def effective_weight(self):
        """Effektiv og'irlikni qaytaradi (category weight * assignment multiplier)."""
        return float(self.category.score_weight) * float(self.score_multiplier)
    
    @property
    def weighted_max_score(self):
        """Og'irlik bilan hisoblangan maksimal ball."""
        return round(self.max_score * self.effective_weight, 2)
    
    @property
    def score_info(self):
        """Ball haqida to'liq ma'lumot."""
        return {
            'max_score': self.max_score,
            'min_score': self.min_score_value,
            'is_custom': self.use_custom_score,
            'category_default': self.category.default_score,
            'multiplier': float(self.score_multiplier),
            'weight': float(self.category.score_weight),
            'effective_weight': self.effective_weight,
            'weighted_max': self.weighted_max_score,
            'note': self.score_note,
        }
    
    def calculate_final_score(self, raw_score):
        """
        Berilgan raw ballni final ballga aylantiradi.
        
        Args:
            raw_score: Baholangan ball (0 dan max_score gacha)
        
        Returns:
            Og'irlik bilan hisoblangan final ball
        """
        if raw_score < self.min_score_value:
            raw_score = self.min_score_value
        if raw_score > self.max_score:
            raw_score = self.max_score
        
        return round(raw_score * self.effective_weight, 2)

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
    
    # ==================== BAHOLASH ====================
    raw_score = models.PositiveIntegerField(
        _('raw score'),
        null=True,
        blank=True,
        help_text=_('Baholangan ball (0 dan max_score gacha)')
    )
    
    final_score = models.DecimalField(
        _('final score'),
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        help_text=_('Og\'irlik bilan hisoblangan yakuniy ball')
    )
    
    graded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='graded_progress'
    )
    
    graded_at = models.DateTimeField(
        _('graded at'),
        null=True,
        blank=True
    )
    
    grade_note = models.TextField(
        _('grade note'),
        blank=True,
        null=True,
        help_text=_('Baholash haqida izoh')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('assignment progress')
        verbose_name_plural = _('assignment progress items')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.assignment} - Progress"
    
    def set_score(self, raw_score, graded_by=None, note=None):
        """
        Ballni o'rnatish va final ballni hisoblash.
        
        Args:
            raw_score: Baholangan ball
            graded_by: Baholagan foydalanuvchi
            note: Izoh
        """
        self.raw_score = raw_score
        self.final_score = self.assignment.calculate_final_score(raw_score)
        self.graded_by = graded_by
        self.graded_at = timezone.now()
        if note:
            self.grade_note = note
        self.save()
    
    @property
    def score_percentage(self):
        """Ballni foizda qaytaradi."""
        if self.raw_score is None or self.assignment.max_score == 0:
            return None
        return round((self.raw_score / self.assignment.max_score) * 100, 1)
    
    def save(self, *args, **kwargs):
        # Auto-calculate final_score if raw_score is set
        if self.raw_score is not None and self.final_score is None:
            self.final_score = self.assignment.calculate_final_score(self.raw_score)
        
        super().save(*args, **kwargs)
        
        # Update assignment completed quantity
        if self.counted and self.portfolio:
            counted_items = self.assignment.progress_items.filter(counted=True).count()
            self.assignment.completed_quantity = counted_items
            self.assignment.check_and_update_status()


class ScoreHistory(models.Model):
    """
    Ball o'zgarishlar tarixi.
    Admin/SuperAdmin ball o'zgartirganda log qiladi.
    """
    
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name='score_history'
    )
    
    progress = models.ForeignKey(
        AssignmentProgress,
        on_delete=models.CASCADE,
        related_name='score_history',
        null=True,
        blank=True
    )
    
    action = models.CharField(
        max_length=50,
        choices=[
            ('score_set', 'Ball o\'rnatildi'),
            ('score_changed', 'Ball o\'zgartirildi'),
            ('custom_score_enabled', 'Maxsus ball yoqildi'),
            ('custom_score_disabled', 'Maxsus ball o\'chirildi'),
            ('multiplier_changed', 'Koeffitsient o\'zgartirildi'),
        ]
    )
    
    old_value = models.CharField(max_length=100, blank=True, null=True)
    new_value = models.CharField(max_length=100, blank=True, null=True)
    
    note = models.TextField(blank=True, null=True)
    
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='score_changes'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('score history')
        verbose_name_plural = _('score histories')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.assignment} - {self.action}"
