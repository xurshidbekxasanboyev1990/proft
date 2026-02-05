"""
Admin configuration for assignments app.
"""

from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from .models import Category, Assignment, AssignmentProgress, ScoreHistory


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for Category model."""
    
    list_display = (
        'name', 'slug', 'color_display', 'score_display', 'weight_display',
        'is_active', 'order', 'created_at'
    )
    list_filter = ('is_active', 'created_at')
    search_fields = ('name', 'name_uz', 'name_ru', 'name_en', 'description')
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('order', 'name')
    list_editable = ('order', 'is_active')
    
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
        (_('Ball Tizimi'), {
            'fields': ('default_score', 'min_score', 'score_weight'),
            'description': _('Kategoriya uchun standart ball sozlamalari')
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
    
    def score_display(self, obj):
        """Display default score."""
        return format_html(
            '<strong>{}</strong> <small>(min: {})</small>',
            obj.default_score, obj.min_score
        )
    score_display.short_description = _('Default Ball')
    
    def weight_display(self, obj):
        """Display score weight."""
        color = '#28A745' if obj.score_weight > 1 else '#6C757D' if obj.score_weight == 1 else '#DC3545'
        return format_html(
            '<span style="color: {};">×{}</span>',
            color, obj.score_weight
        )
    weight_display.short_description = _('Og\'irlik')
    
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
        'progress_display', 'score_info_display', 'deadline_display', 
        'status_badge', 'priority_badge'
    )
    list_filter = ('status', 'priority', 'category', 'use_custom_score', 'deadline', 'created_at')
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
        (_('Ball Tizimi'), {
            'fields': (
                'use_custom_score', 'custom_max_score', 'custom_min_score',
                'score_multiplier', 'score_note'
            ),
            'description': _('Maxsus ball sozlamalari. use_custom_score ni yoqsangiz, kategoriya default balini emas, maxsus ballni ishlatadi.')
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
    
    def score_info_display(self, obj):
        """Display score info with custom indicator."""
        if obj.use_custom_score:
            return format_html(
                '<span style="color: #DC3545; font-weight: bold;">'
                '🎯 {}</span> <small>(maxsus)</small><br>'
                '<small>×{} = <strong>{}</strong></small>',
                obj.max_score, obj.score_multiplier, obj.weighted_max_score
            )
        return format_html(
            '<span>{}</span><br>'
            '<small>×{} = <strong>{}</strong></small>',
            obj.max_score, obj.score_multiplier, obj.weighted_max_score
        )
    score_info_display.short_description = _('Ball')
    
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
    
    @admin.action(description=_('Enable custom score (2x bonus)'))
    def enable_double_score(self, request, queryset):
        for assignment in queryset:
            old_value = f"custom={assignment.use_custom_score}, multiplier={assignment.score_multiplier}"
            assignment.use_custom_score = True
            assignment.custom_max_score = assignment.category.default_score * 2
            assignment.score_multiplier = 1.0
            assignment.score_note = "Admin tomonidan 2x bonus berildi"
            assignment.save()
            
            # Log score change
            ScoreHistory.objects.create(
                assignment=assignment,
                action='custom_score_enabled',
                old_value=old_value,
                new_value=f"custom_max={assignment.custom_max_score}",
                note="Bulk action: 2x bonus",
                changed_by=request.user
            )
        self.message_user(request, f'{queryset.count()} assignments given 2x bonus.')
    
    @admin.action(description=_('Reset to default score'))
    def reset_to_default_score(self, request, queryset):
        for assignment in queryset:
            old_value = f"custom={assignment.use_custom_score}, max={assignment.custom_max_score}"
            assignment.use_custom_score = False
            assignment.custom_max_score = None
            assignment.custom_min_score = None
            assignment.score_multiplier = 1.0
            assignment.score_note = ""
            assignment.save()
            
            ScoreHistory.objects.create(
                assignment=assignment,
                action='custom_score_disabled',
                old_value=old_value,
                new_value="default",
                note="Bulk action: Reset to default",
                changed_by=request.user
            )
        self.message_user(request, f'{queryset.count()} assignments reset to default score.')


@admin.register(AssignmentProgress)
class AssignmentProgressAdmin(admin.ModelAdmin):
    """Admin configuration for AssignmentProgress model."""
    
    list_display = (
        'assignment', 'portfolio', 'score_display', 
        'counted', 'graded_by', 'created_at'
    )
    list_filter = ('counted', 'created_at', 'graded_at')
    search_fields = ('assignment__teacher__username', 'assignment__category__name')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {
            'fields': ('assignment', 'portfolio', 'note', 'counted')
        }),
        (_('Baholash'), {
            'fields': ('raw_score', 'final_score', 'grade_note'),
            'description': _('raw_score ni kiritsangiz, final_score avtomatik hisoblanadi')
        }),
        (_('Meta'), {
            'fields': ('graded_by', 'graded_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('final_score', 'graded_at')
    
    def score_display(self, obj):
        """Display score info."""
        if obj.raw_score is not None:
            return format_html(
                '<strong>{}</strong>/{} <small>({}%)</small><br>'
                '<small>Final: <strong>{}</strong></small>',
                obj.raw_score, obj.assignment.max_score,
                obj.score_percentage, obj.final_score
            )
        return '-'
    score_display.short_description = _('Ball')
    
    def save_model(self, request, obj, form, change):
        if 'raw_score' in form.changed_data and obj.raw_score is not None:
            obj.graded_by = request.user
            obj.graded_at = timezone.now()
            obj.final_score = obj.assignment.calculate_final_score(obj.raw_score)
        super().save_model(request, obj, form, change)


@admin.register(ScoreHistory)
class ScoreHistoryAdmin(admin.ModelAdmin):
    """Admin configuration for ScoreHistory model."""
    
    list_display = ('assignment', 'action', 'old_value', 'new_value', 'changed_by', 'created_at')
    list_filter = ('action', 'created_at')
    search_fields = ('assignment__teacher__username', 'note')
    ordering = ('-created_at',)
    readonly_fields = ('assignment', 'progress', 'action', 'old_value', 'new_value', 'note', 'changed_by', 'created_at')
