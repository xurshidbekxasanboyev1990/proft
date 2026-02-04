"""
Admin configuration for analytics app.
"""

from django.contrib import admin
from django.utils.html import format_html
from .models import Report, DashboardWidget, AnalyticsCache


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'report_type', 'format', 'status_badge', 
        'created_by', 'created_at', 'file_link'
    ]
    list_filter = ['report_type', 'format', 'status', 'created_at']
    search_fields = ['title', 'created_by__username', 'created_by__first_name']
    readonly_fields = [
        'data', 'file_size', 'created_at', 'completed_at', 
        'processing_time', 'error_message'
    ]
    date_hierarchy = 'created_at'
    ordering = ['-created_at']
    
    fieldsets = (
        ('Asosiy ma\'lumotlar', {
            'fields': ('title', 'report_type', 'format', 'status')
        }),
        ('Filterlar', {
            'fields': ('date_from', 'date_to', 'filters'),
            'classes': ('collapse',)
        }),
        ('Natija', {
            'fields': ('data', 'file', 'file_size'),
            'classes': ('collapse',)
        }),
        ('Meta', {
            'fields': ('created_by', 'created_at', 'completed_at', 'processing_time', 'error_message'),
        }),
    )
    
    def status_badge(self, obj):
        colors = {
            'pending': '#ffc107',
            'processing': '#17a2b8',
            'completed': '#28a745',
            'failed': '#dc3545',
        }
        color = colors.get(obj.status, '#6c757d')
        return format_html(
            '<span style="background-color: {}; color: white; padding: 3px 10px; '
            'border-radius: 3px; font-size: 11px;">{}</span>',
            color, obj.get_status_display()
        )
    status_badge.short_description = 'Holat'
    
    def file_link(self, obj):
        if obj.file:
            return format_html(
                '<a href="{}" target="_blank">📥 Yuklab olish ({})</a>',
                obj.file.url, obj.file_size_display
            )
        return '-'
    file_link.short_description = 'Fayl'
    
    def processing_time(self, obj):
        if obj.processing_time:
            return f"{obj.processing_time:.2f} sekund"
        return '-'
    processing_time.short_description = 'Yaratish vaqti'


@admin.register(DashboardWidget)
class DashboardWidgetAdmin(admin.ModelAdmin):
    list_display = [
        'name', 'widget_type', 'data_source', 'order', 
        'is_active', 'visibility_info'
    ]
    list_filter = ['widget_type', 'is_active', 'visible_to_superadmin', 'visible_to_admin', 'visible_to_teacher']
    search_fields = ['name', 'data_source']
    list_editable = ['order', 'is_active']
    ordering = ['order']
    
    fieldsets = (
        ('Asosiy', {
            'fields': ('name', 'widget_type', 'data_source', 'order', 'is_active')
        }),
        ('Sozlamalar', {
            'fields': ('config',),
            'classes': ('collapse',)
        }),
        ('Ko\'rinish', {
            'fields': ('visible_to_superadmin', 'visible_to_admin', 'visible_to_teacher'),
        }),
    )
    
    def visibility_info(self, obj):
        roles = []
        if obj.visible_to_superadmin:
            roles.append('SA')
        if obj.visible_to_admin:
            roles.append('A')
        if obj.visible_to_teacher:
            roles.append('T')
        return ', '.join(roles) if roles else 'Hech kim'
    visibility_info.short_description = 'Ko\'radi'


@admin.register(AnalyticsCache)
class AnalyticsCacheAdmin(admin.ModelAdmin):
    list_display = ['key', 'expires_at', 'is_expired_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['key']
    readonly_fields = ['key', 'data', 'expires_at', 'created_at']
    ordering = ['-created_at']
    
    def is_expired_display(self, obj):
        if obj.is_expired:
            return format_html('<span style="color: red;">✗ Muddati o\'tgan</span>')
        return format_html('<span style="color: green;">✓ Faol</span>')
    is_expired_display.short_description = 'Holat'
    
    actions = ['clear_expired_cache', 'clear_all_cache']
    
    def clear_expired_cache(self, request, queryset):
        count, _ = AnalyticsCache.cleanup_expired()
        self.message_user(request, f"{count} ta muddati o'tgan kesh tozalandi")
    clear_expired_cache.short_description = "Muddati o'tgan keshlarni tozalash"
    
    def clear_all_cache(self, request, queryset):
        AnalyticsCache.invalidate()
        self.message_user(request, "Barcha keshlar tozalandi")
    clear_all_cache.short_description = "Barcha keshlarni tozalash"
