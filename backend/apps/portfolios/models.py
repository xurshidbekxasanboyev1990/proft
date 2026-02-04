"""
Portfolio model for the portfolio management system.
"""

from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Portfolio(models.Model):
    """
    Portfolio model for teachers.
    
    Status workflow:
    - pending: Initial state when created by teacher
    - approved: Approved by admin/superadmin
    - rejected: Rejected by admin/superadmin
    """
    
    STATUS_PENDING = 'pending'
    STATUS_APPROVED = 'approved'
    STATUS_REJECTED = 'rejected'
    
    STATUS_CHOICES = [
        (STATUS_PENDING, _('Pending')),
        (STATUS_APPROVED, _('Approved')),
        (STATUS_REJECTED, _('Rejected')),
    ]
    
    CATEGORY_CHOICES = [
        ('teaching', _('Teaching Materials')),
        ('research', _('Research & Publications')),
        ('certificates', _('Certificates & Awards')),
        ('projects', _('Projects')),
        ('professional', _('Professional Development')),
        ('other', _('Other')),
    ]
    
    # Relationships
    teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolios',
        limit_choices_to={'role': 'teacher'}
    )
    
    # Basic info
    title = models.CharField(
        _('title'),
        max_length=255
    )
    description = models.TextField(
        _('description')
    )
    category = models.CharField(
        _('category'),
        max_length=50,
        choices=CATEGORY_CHOICES,
        default='other',
        db_index=True
    )
    
    # Status
    status = models.CharField(
        _('status'),
        max_length=10,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
        db_index=True
    )
    
    # Approval info
    reviewed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='reviewed_portfolios'
    )
    reviewed_at = models.DateTimeField(
        _('reviewed at'),
        null=True,
        blank=True
    )
    review_comment = models.TextField(
        _('review comment'),
        blank=True,
        null=True
    )
    
    # Additional metadata (JSON field for flexible data)
    meta_data = models.JSONField(
        _('metadata'),
        null=True,
        blank=True,
        default=dict,
        help_text=_('Additional information like attachments, links, notes')
    )
    
    # Visibility
    is_public = models.BooleanField(
        _('is public'),
        default=False,
        help_text=_('Whether this portfolio is visible to everyone')
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('portfolio')
        verbose_name_plural = _('portfolios')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['teacher']),
            models.Index(fields=['category']),
            models.Index(fields=['created_at']),
            models.Index(fields=['status', 'teacher']),
        ]
    
    def __str__(self):
        return f"{self.title} - {self.teacher.get_full_name() or self.teacher.username}"
    
    @property
    def is_pending(self):
        return self.status == self.STATUS_PENDING
    
    @property
    def is_approved(self):
        return self.status == self.STATUS_APPROVED
    
    @property
    def is_rejected(self):
        return self.status == self.STATUS_REJECTED
    
    def approve(self, reviewer, comment=None):
        """Approve the portfolio."""
        from django.utils import timezone
        
        self.status = self.STATUS_APPROVED
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()
        if comment:
            self.review_comment = comment
        self.save()
    
    def reject(self, reviewer, comment=None):
        """Reject the portfolio."""
        from django.utils import timezone
        
        self.status = self.STATUS_REJECTED
        self.reviewed_by = reviewer
        self.reviewed_at = timezone.now()
        if comment:
            self.review_comment = comment
        self.save()
    
    def reset_to_pending(self):
        """Reset portfolio status to pending."""
        self.status = self.STATUS_PENDING
        self.reviewed_by = None
        self.reviewed_at = None
        self.review_comment = None
        self.save()


class PortfolioAttachment(models.Model):
    """
    Attachments for portfolios (files, images, documents).
    """
    
    FILE_TYPE_CHOICES = [
        ('image', _('Image')),
        ('document', _('Document')),
        ('video', _('Video')),
        ('other', _('Other')),
    ]
    
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='attachments'
    )
    
    title = models.CharField(
        _('title'),
        max_length=255
    )
    file = models.FileField(
        _('file'),
        upload_to='portfolio_attachments/%Y/%m/'
    )
    file_type = models.CharField(
        _('file type'),
        max_length=20,
        choices=FILE_TYPE_CHOICES,
        default='other'
    )
    file_size = models.PositiveIntegerField(
        _('file size'),
        default=0,
        help_text=_('File size in bytes')
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('portfolio attachment')
        verbose_name_plural = _('portfolio attachments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} - {self.portfolio.title}"
    
    def save(self, *args, **kwargs):
        if self.file:
            self.file_size = self.file.size
        super().save(*args, **kwargs)


class PortfolioComment(models.Model):
    """
    Comments on portfolios (for review/feedback).
    """
    
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='comments'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='portfolio_comments'
    )
    content = models.TextField(_('content'))
    
    # For threaded comments
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('portfolio comment')
        verbose_name_plural = _('portfolio comments')
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.portfolio.title}"


class PortfolioHistory(models.Model):
    """
    Track portfolio status changes for audit purposes.
    """
    
    portfolio = models.ForeignKey(
        Portfolio,
        on_delete=models.CASCADE,
        related_name='history'
    )
    changed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True
    )
    
    old_status = models.CharField(
        max_length=10,
        choices=Portfolio.STATUS_CHOICES,
        null=True,
        blank=True
    )
    new_status = models.CharField(
        max_length=10,
        choices=Portfolio.STATUS_CHOICES
    )
    comment = models.TextField(
        blank=True,
        null=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('portfolio history')
        verbose_name_plural = _('portfolio histories')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.portfolio.title}: {self.old_status} -> {self.new_status}"
