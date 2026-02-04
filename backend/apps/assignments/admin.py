"""
Admin configuration for assignments app.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Category, Assignment, AssignmentProgress


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    
    list_display = (
        'name', 'slug', 'color_display', 'points', 
        'is_active', 'order', 'created_at'
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'name_uz', 'name_ru', 'name_en', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Localization'), {
            'fields': ('name_uz', 'name_ru', 'name_en'),
            'classes': ('collapse',)
        }),
        (_('Appearance'), {
            'fields': ('icon', 'color', 'order')
        }),
        (_('Settings'), {
            'fields': ('points', 'is_active')
        }),
    )
    
    def color_display(self, obj):
        """Display color as colored box."""
        return format_html(
            '<span style="background-color: {}; padding: 5px 15px; '
            'border-radius: 3px; color: white;">{}</span>',
            obj.color, obj.color
        )
    color_display.short_description = _('Color')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class AssignmentProgressInline(admin.TabularInline):
    """Inline admin for assignment progress."""
    model = AssignmentProgress
    extra = 0
    readonly_fields = ('portfolio', 'created_at')


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    """Admin configuration for Assignment model."""
    
    list_display = (
        'teacher', 'category', 'required_quantity', 'completed_quantity',
        'progress_display', 'deadline_display', 'status_badge', 'priority_badge'
    )
    list_filter = ('status', 'priority', 'category', 'deadline', 'created_at')
    search_fields = ('teacher__username', 'teacher__first_name', 'teacher__last_name', 'title')
    ordering = ('-created_at',)
    date_hierarchy = 'deadline'
    autocomplete_fields = ['teacher', 'category']
    
    fieldsets = (
        (None, {
            'fields': ('teacher', 'category', 'title', 'description')
        }),
        (_('Requirements'), {
            'fields': ('required_quantity', 'completed_quantity', 'deadline')
        }),
        (_('Status'), {
            'fields': ('status', 'priority')
        }),
        (_('Info'), {
            'fields': ('assigned_by', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('completed_at',)
    inlines = [AssignmentProgressInline]
    
    def progress_display(self, obj):
        """Display progress as bar."""
        percentage = obj.progress_percentage
        color = '#28A745' if percentage >= 100 else '#FFC107' if percentage >= 50 else '#DC3545'
        return format_html(
            '<div style="width: 100px; background: #e9ecef; border-radius: 4px;">'
            '<div style="width: {}%; background: {}; height: 20px; border-radius: 4px; '
            'text-align: center; color: white; font-size: 11px; line-height: 20px;">'
            '{}/{}</div></div>',
            percentage, color, obj.completed_quantity, obj.required_quantity
        )
    progress_display.short_description = _('Progress')
    
    def deadline_display(self, obj):
        """Display deadline with time remaining."""
        now = timezone.now()
        is_overdue = obj.deadline < now
        
        color = '#DC3545' if is_overdue else '#28A745'
        icon = '⚠️' if is_overdue else '📅'
        
        return format_html(
            '<span style="color: {};">{} {} <br><small>{}</small></span>',
            color, icon, obj.deadline.strftime('%Y-%m-%d %H:%M'),
            obj.time_remaining_display
        )
    deadline_display.short_description = _('Deadline')
    deadline_display.admin_order_field = 'deadline'
    
    def status_badge(self, obj):
        """Display status as colored badge."""
        colors = {
            'active': '#17A2B8',
            'completed': '#28A745',
            'overdue': '#DC3545',
            'cancelled': '#6C757D',
        }
        color = colors.get(obj.status, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = _('Status')
    status_badge.admin_order_field = 'status'
    
    def priority_badge(self, obj):
        """Display priority as colored badge."""
        colors = {
            'low': '#6C757D',
            'medium': '#17A2B8',
            'high': '#FFC107',
            'urgent': '#DC3545',
        }
        color = colors.get(obj.priority, '#6C757D')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_priority_display()
        )
    priority_badge.short_description = _('Priority')
    
    def save_model(self, request, obj, form, change):
        if not change:
            obj.assigned_by = request.user
        super().save_model(request, obj, form, change)
    
    actions = ['mark_completed', 'mark_cancelled', 'extend_deadline_1_month']
    
    @admin.action(description=_('Mark as completed'))
    def mark_completed(self, request, queryset):
        for assignment in queryset:
            assignment.mark_completed()
        self.message_user(request, f'{queryset.count()} assignments marked as completed.')
    
    @admin.action(description=_('Mark as cancelled'))
    def mark_cancelled(self, request, queryset):
        queryset.update(status=Assignment.STATUS_CANCELLED)
        self.message_user(request, f'{queryset.count()} assignments cancelled.')
    
    @admin.action(description=_('Extend deadline by 1 month'))
    def extend_deadline_1_month(self, request, queryset):
        from datetime import timedelta
        for assignment in queryset:
            assignment.deadline += timedelta(days=30)
            assignment.check_and_update_status()
        self.message_user(request, f'{queryset.count()} deadlines extended by 1 month.')


@admin.register(AssignmentProgress)
class AssignmentProgressAdmin(admin.ModelAdmin):
    """Admin configuration for AssignmentProgress model."""
    
    list_display = ('assignment', 'portfolio', 'counted', 'created_at')
    list_filter = ('counted', 'created_at')
    search_fields = ('assignment__teacher__username', 'assignment__category__name')
    ordering = ('-created_at',)
