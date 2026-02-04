"""
Permission decorators and mixins for role-based access control.
"""

from functools import wraps
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied
import rules


def role_required(*required_roles):
    """
    Decorator that checks if the user has one of the required roles.
    
    Usage:
        @role_required('superadmin', 'admin')
        def my_view(request):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'error': 'Authentication required',
                    'code': 'UNAUTHORIZED'
                }, status=401)
            
            if request.user.role not in required_roles:
                return JsonResponse({
                    'error': 'Permission denied',
                    'code': 'FORBIDDEN',
                    'required_roles': list(required_roles),
                    'user_role': request.user.role
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def superadmin_required(view_func):
    """Decorator that checks if the user is a superadmin."""
    return role_required('superadmin')(view_func)


def admin_required(view_func):
    """Decorator that checks if the user is an admin or superadmin."""
    return role_required('admin', 'superadmin')(view_func)


def teacher_required(view_func):
    """Decorator that checks if the user is a teacher."""
    return role_required('teacher', 'admin', 'superadmin')(view_func)


def permission_required(permission):
    """
    Decorator that checks if the user has the required permission using django-rules.
    
    Usage:
        @permission_required('portfolios.approve_portfolio')
        def approve_portfolio(request, portfolio_id):
            ...
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse({
                    'error': 'Authentication required',
                    'code': 'UNAUTHORIZED'
                }, status=401)
            
            if not rules.has_perm(permission, request.user):
                return JsonResponse({
                    'error': 'Permission denied',
                    'code': 'FORBIDDEN',
                    'required_permission': permission
                }, status=403)
            
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


class RoleRequiredMixin(AccessMixin):
    """
    Mixin that checks if the user has one of the required roles.
    
    Usage:
        class MyView(RoleRequiredMixin, View):
            required_roles = ['superadmin', 'admin']
    """
    required_roles = []
    
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        
        if self.required_roles and request.user.role not in self.required_roles:
            raise PermissionDenied('You do not have permission to access this page.')
        
        return super().dispatch(request, *args, **kwargs)


class SuperAdminRequiredMixin(RoleRequiredMixin):
    """Mixin that requires superadmin role."""
    required_roles = ['superadmin']


class AdminRequiredMixin(RoleRequiredMixin):
    """Mixin that requires admin or superadmin role."""
    required_roles = ['admin', 'superadmin']


class TeacherRequiredMixin(RoleRequiredMixin):
    """Mixin that requires teacher role (or higher)."""
    required_roles = ['teacher', 'admin', 'superadmin']


# ==================== DRF Permission Classes ====================

from rest_framework.permissions import BasePermission


class IsAdminOrSuperAdmin(BasePermission):
    """
    DRF Permission class that allows only admins and superadmins.
    """
    message = 'Bu amal uchun admin yoki superadmin huquqi kerak.'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['admin', 'superadmin']


class IsSuperAdmin(BasePermission):
    """
    DRF Permission class that allows only superadmins.
    """
    message = 'Bu amal uchun superadmin huquqi kerak.'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role == 'superadmin'


class IsTeacher(BasePermission):
    """
    DRF Permission class that allows teachers, admins, and superadmins.
    """
    message = 'Bu amal uchun o\'qituvchi huquqi kerak.'
    
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        return request.user.role in ['teacher', 'admin', 'superadmin']


class IsOwnerOrAdmin(BasePermission):
    """
    DRF Permission class that allows owners or admins.
    Object-level permission.
    """
    message = 'Bu ob\'ektga kirish uchun ruxsat yo\'q.'
    
    def has_object_permission(self, request, view, obj):
        if not request.user.is_authenticated:
            return False
        
        # Admin/superadmin can access any object
        if request.user.role in ['admin', 'superadmin']:
            return True
        
        # Check if user is owner
        if hasattr(obj, 'user'):
            return obj.user == request.user
        if hasattr(obj, 'created_by'):
            return obj.created_by == request.user
        if hasattr(obj, 'assigned_to'):
            return obj.assigned_to == request.user
        if hasattr(obj, 'submitted_by'):
            return obj.submitted_by == request.user
        
        return False


class IsReadOnly(BasePermission):
    """
    DRF Permission class that allows read-only access.
    """
    def has_permission(self, request, view):
        return request.method in ['GET', 'HEAD', 'OPTIONS']
