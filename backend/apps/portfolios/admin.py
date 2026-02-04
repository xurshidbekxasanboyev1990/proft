"""
Admin configuration for portfolios app.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from .models import Portfolio, PortfolioAttachment, PortfolioComment, PortfolioHistory


class PortfolioAttachmentInline(admin.TabularInline):
    """Inline admin for portfolio attachments."""
    model = PortfolioAttachment
    extra = 0
    readonly_fields = ('file_size', 'created_at')


class PortfolioCommentInline(admin.TabularInline):
    """Inline admin for portfolio comments."""
    model = PortfolioComment
    extra = 0
    readonly_fields = ('author', 'created_at', 'updated_at')


class PortfolioHistoryInline(admin.TabularInline):
    """Inline admin for portfolio history."""
    model = PortfolioHistory
    extra = 0
    readonly_fields = ('changed_by', 'old_status', 'new_status', 'comment', 'created_at')
    can_delete = False
    
    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Portfolio)
class PortfolioAdmin(admin.ModelAdmin):
    """Admin configuration for Portfolio model."""
    
    list_display = (
        'title', 'teacher', 'category', 'status_badge', 
        'is_public', 'created_at', 'reviewed_by'
    )
    list_filter = ('status', 'category', 'is_public', 'created_at')
    search_fields = ('title', 'description', 'teacher__username', 'teacher__email')
    ordering = ('-created_at',)
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('teacher', 'title', 'description', 'category')
        }),
        (_('Status & Review'), {
            'fields': ('status', 'reviewed_by', 'reviewed_at', 'review_comment')
        }),
        (_('Visibility'), {
            'fields': ('is_public',)
        }),
        (_('Metadata'), {
            'fields': ('meta_data',),
            'classes': ('collapse',)
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'reviewed_at')
    inlines = [PortfolioAttachmentInline, PortfolioCommentInline, PortfolioHistoryInline]
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'pending': '#FFC107',   # Yellow
            'approved': '#28A745',  # Green
            'rejected': '#DC3545',  # Red
        }
        color = colors.get(obj.status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = _('Status')
    status_badge.admin_order_field = 'status'
    
    def save_model(self, request, obj, form, change):
        """Create history entry on status change."""
        if change:
            old_obj = Portfolio.objects.get(pk=obj.pk)
            if old_obj.status != obj.status:
                PortfolioHistory.objects.create(
                    portfolio=obj,
                    changed_by=request.user,
                    old_status=old_obj.status,
                    new_status=obj.status,
                    comment=f"Status changed via admin by {request.user.username}"
                )
        super().save_model(request, obj, form, change)
    
    actions = ['approve_selected', 'reject_selected', 'reset_to_pending']
    
    @admin.action(description=_('Approve selected portfolios'))
    def approve_selected(self, request, queryset):
        for portfolio in queryset:
            if portfolio.status != Portfolio.STATUS_APPROVED:
                old_status = portfolio.status
                portfolio.approve(request.user, 'Approved via admin bulk action')
                PortfolioHistory.objects.create(
                    portfolio=portfolio,
                    changed_by=request.user,
                    old_status=old_status,
                    new_status=Portfolio.STATUS_APPROVED,
                    comment='Approved via admin bulk action'
                )
        self.message_user(request, f'{queryset.count()} portfolios approved.')
    
    @admin.action(description=_('Reject selected portfolios'))
    def reject_selected(self, request, queryset):
        for portfolio in queryset:
            if portfolio.status != Portfolio.STATUS_REJECTED:
                old_status = portfolio.status
                portfolio.reject(request.user, 'Rejected via admin bulk action')
                PortfolioHistory.objects.create(
                    portfolio=portfolio,
                    changed_by=request.user,
                    old_status=old_status,
                    new_status=Portfolio.STATUS_REJECTED,
                    comment='Rejected via admin bulk action'
                )
        self.message_user(request, f'{queryset.count()} portfolios rejected.')
    
    @admin.action(description=_('Reset to pending'))
    def reset_to_pending(self, request, queryset):
        for portfolio in queryset:
            if portfolio.status != Portfolio.STATUS_PENDING:
                old_status = portfolio.status
                portfolio.reset_to_pending()
                PortfolioHistory.objects.create(
                    portfolio=portfolio,
                    changed_by=request.user,
                    old_status=old_status,
                    new_status=Portfolio.STATUS_PENDING,
                    comment='Reset to pending via admin bulk action'
                )
        self.message_user(request, f'{queryset.count()} portfolios reset to pending.')


@admin.register(PortfolioAttachment)
class PortfolioAttachmentAdmin(admin.ModelAdmin):
    """Admin configuration for PortfolioAttachment model."""
    
    list_display = ('title', 'portfolio', 'file_type', 'file_size_display', 'created_at')
    list_filter = ('file_type', 'created_at')
    search_fields = ('title', 'portfolio__title')
    ordering = ('-created_at',)
    
    def file_size_display(self, obj):
        """Display file size in human-readable format."""
        size = obj.file_size
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"
    file_size_display.short_description = _('File Size')


@admin.register(PortfolioComment)
class PortfolioCommentAdmin(admin.ModelAdmin):
    """Admin configuration for PortfolioComment model."""
    
    list_display = ('portfolio', 'author', 'content_preview', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('content', 'portfolio__title', 'author__username')
    ordering = ('-created_at',)
    
    def content_preview(self, obj):
        """Display truncated content."""
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_preview.short_description = _('Content')


@admin.register(PortfolioHistory)
class PortfolioHistoryAdmin(admin.ModelAdmin):
    """Admin configuration for PortfolioHistory model."""
    
    list_display = ('portfolio', 'changed_by', 'old_status', 'new_status', 'created_at')
    list_filter = ('old_status', 'new_status', 'created_at')
    search_fields = ('portfolio__title', 'changed_by__username', 'comment')
    ordering = ('-created_at',)
    readonly_fields = ('portfolio', 'changed_by', 'old_status', 'new_status', 'comment', 'created_at')
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
