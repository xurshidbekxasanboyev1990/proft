"""
Admin configuration for accounts app.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User, UserActivity


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Admin configuration for custom User model."""
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'role', 'hemis_id', 'is_active', 'created_at'
    )
    list_filter = ('role', 'is_active', 'is_staff', 'created_at')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'hemis_id')
    ordering = ('-created_at',)
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {
            'fields': ('first_name', 'last_name', 'email', 'avatar', 'phone_number')
        }),
        (_('Role & Hemis'), {
            'fields': ('role', 'hemis_id', 'department', 'position', 'bio')
        }),
        (_('Hemis OAuth Tokens'), {
            'fields': ('hemis_access_token', 'hemis_refresh_token', 'hemis_token_expires_at'),
            'classes': ('collapse',)
        }),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
            'classes': ('collapse',)
        }),
        (_('Important dates'), {
            'fields': ('last_login', 'date_joined'),
            'classes': ('collapse',)
        }),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'username', 'password1', 'password2', 
                'role', 'email', 'first_name', 'last_name'
            ),
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at', 'last_login', 'date_joined')


@admin.register(UserActivity)
class UserActivityAdmin(admin.ModelAdmin):
    """Admin configuration for UserActivity model."""
    
    list_display = (
        'user', 'action', 'target_model', 'target_id', 
        'ip_address', 'created_at'
    )
    list_filter = ('action', 'target_model', 'created_at')
    search_fields = ('user__username', 'description', 'ip_address')
    ordering = ('-created_at',)
    readonly_fields = (
        'user', 'action', 'target_model', 'target_id', 
        'description', 'ip_address', 'user_agent', 'created_at'
    )
    
    def has_add_permission(self, request):
        return False
    
    def has_change_permission(self, request, obj=None):
        return False
