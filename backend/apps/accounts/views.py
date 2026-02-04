"""
Views for accounts app.
"""

import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth import get_user_model

from .permissions import superadmin_required, admin_required, role_required
from .models import UserActivity

User = get_user_model()


class UserListView(View):
    """
    List all users (Super Admin only).
    GET /api/accounts/users/
    """
    
    @method_decorator(superadmin_required)
    def get(self, request):
        users = User.objects.all().values(
            'id', 'username', 'email', 'first_name', 'last_name',
            'role', 'hemis_id', 'department', 'position',
            'is_active', 'created_at'
        )
        
        # Filter by role if specified
        role = request.GET.get('role')
        if role:
            users = users.filter(role=role)
        
        # Search
        search = request.GET.get('search')
        if search:
            users = users.filter(
                models.Q(username__icontains=search) |
                models.Q(email__icontains=search) |
                models.Q(first_name__icontains=search) |
                models.Q(last_name__icontains=search)
            )
        
        return JsonResponse({
            'users': list(users),
            'count': users.count()
        })
    
    @method_decorator(superadmin_required)
    @method_decorator(csrf_protect)
    def post(self, request):
        """Create a new user (Super Admin only)."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        required_fields = ['username', 'role']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        if data['role'] not in ['superadmin', 'admin', 'teacher']:
            return JsonResponse({'error': 'Invalid role'}, status=400)
        
        if User.objects.filter(username=data['username']).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        user = User.objects.create_user(
            username=data['username'],
            email=data.get('email', ''),
            password=data.get('password', User.objects.make_random_password()),
            role=data['role'],
            first_name=data.get('first_name', ''),
            last_name=data.get('last_name', ''),
            department=data.get('department', ''),
            position=data.get('position', ''),
        )
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_CREATE,
            target_model='User',
            target_id=user.id,
            description=f'Created user: {user.username}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'User created successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
            }
        }, status=201)


class UserDetailView(View):
    """
    Get, update, or delete a specific user (Super Admin only).
    GET/PUT/DELETE /api/accounts/users/<user_id>/
    """
    
    @method_decorator(superadmin_required)
    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'role': user.role,
            'hemis_id': user.hemis_id,
            'department': user.department,
            'position': user.position,
            'bio': user.bio,
            'phone_number': user.phone_number,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat(),
            'updated_at': user.updated_at.isoformat(),
        })
    
    @method_decorator(superadmin_required)
    @method_decorator(csrf_protect)
    def put(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Update fields
        updatable_fields = [
            'email', 'first_name', 'last_name', 'role',
            'department', 'position', 'bio', 'phone_number', 'is_active'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(user, field, data[field])
        
        user.save()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_UPDATE,
            target_model='User',
            target_id=user.id,
            description=f'Updated user: {user.username}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role,
            }
        })
    
    @method_decorator(superadmin_required)
    @method_decorator(csrf_protect)
    def delete(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User not found'}, status=404)
        
        # Prevent self-deletion
        if user.id == request.user.id:
            return JsonResponse({'error': 'Cannot delete yourself'}, status=400)
        
        username = user.username
        user.delete()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_DELETE,
            target_model='User',
            target_id=user_id,
            description=f'Deleted user: {username}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({'message': 'User deleted successfully'})


class CurrentUserView(View):
    """
    Get current authenticated user info.
    GET /api/accounts/me/
    """
    
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        
        user = request.user
        return JsonResponse({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'full_name': user.get_full_name(),
            'role': user.role,
            'role_display': user.get_role_display(),
            'hemis_id': user.hemis_id,
            'department': user.department,
            'position': user.position,
            'bio': user.bio,
            'phone_number': user.phone_number,
            'permissions': {
                'can_manage_users': user.can_manage_users,
                'can_approve_portfolios': user.can_approve_portfolios,
                'can_manage_all_portfolios': user.can_manage_all_portfolios,
            },
            'is_superadmin': user.is_superadmin,
            'is_admin': user.is_admin,
            'is_teacher': user.is_teacher,
        })
    
    @method_decorator(csrf_protect)
    def put(self, request):
        """Update current user profile."""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Not authenticated'}, status=401)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        user = request.user
        
        # Only allow updating certain fields
        allowed_fields = ['first_name', 'last_name', 'bio', 'phone_number']
        
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])
        
        user.save()
        
        return JsonResponse({
            'message': 'Profile updated successfully',
            'user': {
                'id': user.id,
                'username': user.username,
                'first_name': user.first_name,
                'last_name': user.last_name,
            }
        })


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        return x_forwarded_for.split(',')[0]
    return request.META.get('REMOTE_ADDR')
