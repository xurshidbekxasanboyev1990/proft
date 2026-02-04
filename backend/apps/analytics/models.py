"""
Models for analytics app.
Report generation and caching.
"""

from django.db import models
from django.conf import settings
from django.utils import timezone


class ReportType(models.TextChoices):
    PORTFOLIO_SUMMARY = 'portfolio_summary', 'Portfolio Summary'
    ASSIGNMENT_SUMMARY = 'assignment_summary', 'Assignment Summary'
    TEACHER_PERFORMANCE = 'teacher_performance', 'Teacher Performance'
    CATEGORY_ANALYTICS = 'category_analytics', 'Category Analytics'
    MONTHLY_REPORT = 'monthly_report', 'Monthly Report'
    YEARLY_REPORT = 'yearly_report', 'Yearly Report'
    CUSTOM_REPORT = 'custom_report', 'Custom Report'


class ReportFormat(models.TextChoices):
    JSON = 'json', 'JSON'
    PDF = 'pdf', 'PDF'
    EXCEL = 'excel', 'Excel'
    CSV = 'csv', 'CSV'


class ReportStatus(models.TextChoices):
    PENDING = 'pending', 'Kutilmoqda'
    PROCESSING = 'processing', 'Jarayonda'
    COMPLETED = 'completed', 'Tayyor'
    FAILED = 'failed', 'Xatolik'


class Report(models.Model):
    """Generated reports model"""
    title = models.CharField(max_length=255, verbose_name='Sarlavha')
    report_type = models.CharField(
        max_length=50,
        choices=ReportType.choices,
        default=ReportType.CUSTOM_REPORT,
        verbose_name='Hisobot turi'
    )
    format = models.CharField(
        max_length=10,
        choices=ReportFormat.choices,
        default=ReportFormat.JSON,
        verbose_name='Format'
    )
    status = models.CharField(
        max_length=20,
        choices=ReportStatus.choices,
        default=ReportStatus.PENDING,
        verbose_name='Holat'
    )
    
    # Filters
    date_from = models.DateField(null=True, blank=True, verbose_name='Boshlanish sanasi')
    date_to = models.DateField(null=True, blank=True, verbose_name='Tugash sanasi')
    filters = models.JSONField(default=dict, blank=True, verbose_name='Filterlar')
    
    # Result
    data = models.JSONField(default=dict, blank=True, verbose_name='Ma\'lumotlar')
    file = models.FileField(
        upload_to='reports/%Y/%m/', 
        null=True, 
        blank=True,
        verbose_name='Fayl'
    )
    file_size = models.PositiveIntegerField(default=0, verbose_name='Fayl hajmi')
    
    # Meta
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='reports',
        verbose_name='Yaratuvchi'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Yaratilgan vaqt')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Tugallangan vaqt')
    error_message = models.TextField(blank=True, verbose_name='Xatolik xabari')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Hisobot'
        verbose_name_plural = 'Hisobotlar'
    
    def __str__(self):
        return f"{self.title} ({self.get_report_type_display()})"
    
    @property
    def processing_time(self):
        """Hisobot yaratish vaqti (sekundlarda)"""
        if self.completed_at and self.created_at:
            return (self.completed_at - self.created_at).total_seconds()
        return None
    
    @property
    def file_size_display(self):
        """Fayl hajmini o'qish uchun qulay formatda"""
        if self.file_size < 1024:
            return f"{self.file_size} B"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        else:
            return f"{self.file_size / (1024 * 1024):.1f} MB"


class DashboardWidget(models.Model):
    """Dashboard widget configuration"""
    WIDGET_TYPES = [
        ('counter', 'Counter - Raqam ko\'rsatkich'),
        ('pie_chart', 'Pie Chart - Doira diagramma'),
        ('bar_chart', 'Bar Chart - Ustun diagramma'),
        ('line_chart', 'Line Chart - Chiziqli grafik'),
        ('table', 'Table - Jadval'),
        ('progress', 'Progress Bar - Progress'),
        ('stat_card', 'Stat Card - Statistika karta'),
    ]
    
    name = models.CharField(max_length=100, verbose_name='Nomi')
    widget_type = models.CharField(
        max_length=20, 
        choices=WIDGET_TYPES,
        verbose_name='Widget turi'
    )
    data_source = models.CharField(
        max_length=100,
        verbose_name='Ma\'lumot manbasi',
        help_text='API endpoint yoki funksiya nomi'
    )
    config = models.JSONField(default=dict, blank=True, verbose_name='Sozlamalar')
    order = models.PositiveIntegerField(default=0, verbose_name='Tartib')
    is_active = models.BooleanField(default=True, verbose_name='Faol')
    
    # Role-based visibility
    visible_to_superadmin = models.BooleanField(default=True, verbose_name='SuperAdmin ko\'radi')
    visible_to_admin = models.BooleanField(default=True, verbose_name='Admin ko\'radi')
    visible_to_teacher = models.BooleanField(default=False, verbose_name='O\'qituvchi ko\'radi')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = 'Dashboard Widget'
        verbose_name_plural = 'Dashboard Widgets'
    
    def __str__(self):
        return f"{self.name} ({self.get_widget_type_display()})"
    
    def is_visible_to(self, user):
        """Foydalanuvchi uchun ko'rinadimi"""
        if user.role == 'superadmin':
            return self.visible_to_superadmin
        elif user.role == 'admin':
            return self.visible_to_admin
        elif user.role == 'teacher':
            return self.visible_to_teacher
        return False


class AnalyticsCache(models.Model):
    """Cache for expensive analytics queries"""
    key = models.CharField(max_length=255, unique=True, db_index=True)
    data = models.JSONField()
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = 'Analytics Cache'
        verbose_name_plural = 'Analytics Cache'
    
    def __str__(self):
        return self.key
    
    @property
    def is_expired(self):
        return timezone.now() > self.expires_at
    
    @classmethod
    def get_or_set(cls, key, callback, timeout=3600):
        """Get cached data or compute and store"""
        try:
            cache_entry = cls.objects.get(key=key, expires_at__gt=timezone.now())
            return cache_entry.data
        except cls.DoesNotExist:
            data = callback()
            cls.objects.update_or_create(
                key=key,
                defaults={
                    'data': data,
                    'expires_at': timezone.now() + timezone.timedelta(seconds=timeout)
                }
            )
            return data
    
    @classmethod
    def invalidate(cls, key_pattern=None):
        """Invalidate cache by key pattern"""
        if key_pattern:
            cls.objects.filter(key__contains=key_pattern).delete()
        else:
            cls.objects.all().delete()
    
    @classmethod
    def cleanup_expired(cls):
        """Remove expired cache entries"""
        return cls.objects.filter(expires_at__lt=timezone.now()).delete()
