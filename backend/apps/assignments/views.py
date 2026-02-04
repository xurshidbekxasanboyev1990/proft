"""
Views for assignments and categories.
Admin/SuperAdmin can manage categories and assignments.
Teachers can view their assignments.
"""

import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.utils import timezone
from django.utils.text import slugify
from django.db.models import Q, Sum, Count
from django.core.paginator import Paginator

from apps.accounts.permissions import admin_required, superadmin_required
from apps.accounts.views import get_client_ip
from apps.accounts.models import UserActivity
from .models import Category, Assignment, AssignmentProgress


# ==================== CATEGORY VIEWS ====================

class CategoryListView(View):
    """
    List and create categories.
    GET /api/assignments/categories/ - List all categories
    POST /api/assignments/categories/ - Create new category (Admin/SuperAdmin only)
    """
    
    def get(self, request):
        """List all active categories."""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        # All authenticated users can see categories
        categories = Category.objects.filter(is_active=True).order_by('order', 'name')
        
        # For admin, show all including inactive
        if request.user.is_superadmin or request.user.is_admin:
            show_all = request.GET.get('all', 'false').lower() == 'true'
            if show_all:
                categories = Category.objects.all().order_by('order', 'name')
        
        data = [{
            'id': c.id,
            'name': c.name,
            'name_uz': c.name_uz,
            'name_ru': c.name_ru,
            'name_en': c.name_en,
            'slug': c.slug,
            'description': c.description,
            'icon': c.icon,
            'color': c.color,
            'points': c.points,
            'is_active': c.is_active,
            'order': c.order,
            'created_at': c.created_at.isoformat(),
        } for c in categories]
        
        return JsonResponse({
            'categories': data,
            'count': len(data)
        })
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def post(self, request):
        """Create new category (Admin/SuperAdmin only)."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Validation
        name = data.get('name', '').strip()
        if not name:
            return JsonResponse({'error': 'Name is required'}, status=400)
        
        # Generate slug
        slug = data.get('slug') or slugify(name)
        
        # Check uniqueness
        if Category.objects.filter(name=name).exists():
            return JsonResponse({'error': 'Category with this name already exists'}, status=400)
        
        if Category.objects.filter(slug=slug).exists():
            return JsonResponse({'error': 'Category with this slug already exists'}, status=400)
        
        # Create category
        category = Category.objects.create(
            name=name,
            name_uz=data.get('name_uz', ''),
            name_ru=data.get('name_ru', ''),
            name_en=data.get('name_en', ''),
            slug=slug,
            description=data.get('description', ''),
            icon=data.get('icon', ''),
            color=data.get('color', '#3498db'),
            points=data.get('points', 1),
            is_active=data.get('is_active', True),
            order=data.get('order', 0),
            created_by=request.user
        )
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_CREATE,
            target_model='Category',
            target_id=category.id,
            description=f'Created category: {category.name}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Category created successfully',
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
            }
        }, status=201)


class CategoryDetailView(View):
    """
    Get, update, or delete a category.
    GET/PUT/DELETE /api/assignments/categories/<category_id>/
    """
    
    def get(self, request, category_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        
        # Get assignment stats for this category
        assignment_stats = Assignment.objects.filter(category=category).aggregate(
            total=Count('id'),
            active=Count('id', filter=Q(status='active')),
            completed=Count('id', filter=Q(status='completed'))
        )
        
        return JsonResponse({
            'id': category.id,
            'name': category.name,
            'name_uz': category.name_uz,
            'name_ru': category.name_ru,
            'name_en': category.name_en,
            'slug': category.slug,
            'description': category.description,
            'icon': category.icon,
            'color': category.color,
            'points': category.points,
            'is_active': category.is_active,
            'order': category.order,
            'created_at': category.created_at.isoformat(),
            'updated_at': category.updated_at.isoformat(),
            'stats': assignment_stats
        })
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def put(self, request, category_id):
        """Update category (Admin/SuperAdmin only)."""
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Update fields
        updatable_fields = [
            'name', 'name_uz', 'name_ru', 'name_en', 'slug',
            'description', 'icon', 'color', 'points', 'is_active', 'order'
        ]
        
        for field in updatable_fields:
            if field in data:
                setattr(category, field, data[field])
        
        # Check uniqueness if name/slug changed
        if 'name' in data:
            if Category.objects.filter(name=data['name']).exclude(id=category_id).exists():
                return JsonResponse({'error': 'Category with this name already exists'}, status=400)
        
        if 'slug' in data:
            if Category.objects.filter(slug=data['slug']).exclude(id=category_id).exists():
                return JsonResponse({'error': 'Category with this slug already exists'}, status=400)
        
        category.save()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_UPDATE,
            target_model='Category',
            target_id=category.id,
            description=f'Updated category: {category.name}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Category updated successfully',
            'category': {
                'id': category.id,
                'name': category.name,
                'slug': category.slug,
            }
        })
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def delete(self, request, category_id):
        """Delete category (Admin/SuperAdmin only)."""
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        
        # Check if category has assignments
        if Assignment.objects.filter(category=category).exists():
            return JsonResponse({
                'error': 'Cannot delete category with existing assignments. Deactivate it instead.'
            }, status=400)
        
        name = category.name
        category_id_saved = category.id
        category.delete()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_DELETE,
            target_model='Category',
            target_id=category_id_saved,
            description=f'Deleted category: {name}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({'message': 'Category deleted successfully'})


# ==================== ASSIGNMENT VIEWS ====================

class AssignmentListView(View):
    """
    List and create assignments.
    GET /api/assignments/ - List assignments
    POST /api/assignments/ - Create new assignment (Admin/SuperAdmin only)
    """
    
    def get(self, request):
        """List assignments based on user role."""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        user = request.user
        
        # Base queryset based on role
        if user.is_superadmin or user.is_admin:
            queryset = Assignment.objects.all()
        else:  # Teacher
            queryset = Assignment.objects.filter(teacher=user)
        
        # Filters
        status = request.GET.get('status')
        if status and status in ['active', 'completed', 'overdue', 'cancelled']:
            queryset = queryset.filter(status=status)
        
        category_id = request.GET.get('category_id')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        
        teacher_id = request.GET.get('teacher_id')
        if teacher_id and (user.is_superadmin or user.is_admin):
            queryset = queryset.filter(teacher_id=teacher_id)
        
        priority = request.GET.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Check and update overdue status
        now = timezone.now()
        queryset.filter(
            status='active',
            deadline__lt=now
        ).update(status='overdue')
        
        # Ordering
        ordering = request.GET.get('ordering', '-created_at')
        if ordering in ['created_at', '-created_at', 'deadline', '-deadline', 'priority']:
            queryset = queryset.order_by(ordering)
        
        # Pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        paginator = Paginator(queryset.select_related('teacher', 'category', 'assigned_by'), page_size)
        page_obj = paginator.get_page(page)
        
        assignments = []
        for a in page_obj:
            assignments.append({
                'id': a.id,
                'title': a.title or f"{a.category.name} topshiriq",
                'description': a.description,
                'teacher': {
                    'id': a.teacher.id,
                    'username': a.teacher.username,
                    'full_name': a.teacher.get_full_name(),
                },
                'category': {
                    'id': a.category.id,
                    'name': a.category.name,
                    'color': a.category.color,
                },
                'required_quantity': a.required_quantity,
                'completed_quantity': a.completed_quantity,
                'remaining_quantity': a.remaining_quantity,
                'progress_percentage': a.progress_percentage,
                'deadline': a.deadline.isoformat(),
                'time_remaining': a.time_remaining_display,
                'days_remaining': a.days_remaining,
                'status': a.status,
                'status_display': a.get_status_display(),
                'priority': a.priority,
                'priority_display': a.get_priority_display(),
                'is_overdue': a.is_overdue,
                'assigned_by': {
                    'id': a.assigned_by.id,
                    'username': a.assigned_by.username,
                } if a.assigned_by else None,
                'created_at': a.created_at.isoformat(),
            })
        
        return JsonResponse({
            'assignments': assignments,
            'pagination': {
                'page': page,
                'page_size': page_size,
                'total_pages': paginator.num_pages,
                'total_count': paginator.count,
                'has_next': page_obj.has_next(),
                'has_previous': page_obj.has_previous(),
            }
        })
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def post(self, request):
        """Create new assignment (Admin/SuperAdmin only)."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Validation
        required_fields = ['teacher_id', 'category_id', 'required_quantity', 'deadline']
        for field in required_fields:
            if field not in data:
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Validate teacher
        from apps.accounts.models import User
        try:
            teacher = User.objects.get(id=data['teacher_id'], role='teacher')
        except User.DoesNotExist:
            return JsonResponse({'error': 'Teacher not found'}, status=404)
        
        # Validate category
        try:
            category = Category.objects.get(id=data['category_id'], is_active=True)
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        
        # Parse deadline
        from django.utils.dateparse import parse_datetime
        deadline = parse_datetime(data['deadline'])
        if not deadline:
            return JsonResponse({'error': 'Invalid deadline format. Use ISO 8601.'}, status=400)
        
        # Make deadline timezone aware if not
        if timezone.is_naive(deadline):
            deadline = timezone.make_aware(deadline)
        
        # Create assignment
        assignment = Assignment.objects.create(
            teacher=teacher,
            category=category,
            required_quantity=int(data['required_quantity']),
            deadline=deadline,
            title=data.get('title', ''),
            description=data.get('description', ''),
            priority=data.get('priority', 'medium'),
            assigned_by=request.user
        )
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_CREATE,
            target_model='Assignment',
            target_id=assignment.id,
            description=f'Created assignment for {teacher.get_full_name()}: {category.name} x{assignment.required_quantity}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Assignment created successfully',
            'assignment': {
                'id': assignment.id,
                'teacher': teacher.get_full_name(),
                'category': category.name,
                'required_quantity': assignment.required_quantity,
                'deadline': assignment.deadline.isoformat(),
            }
        }, status=201)


class AssignmentDetailView(View):
    """
    Get, update, or delete an assignment.
    GET/PUT/DELETE /api/assignments/<assignment_id>/
    """
    
    def get(self, request, assignment_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            assignment = Assignment.objects.select_related(
                'teacher', 'category', 'assigned_by'
            ).get(id=assignment_id)
        except Assignment.DoesNotExist:
            return JsonResponse({'error': 'Assignment not found'}, status=404)
        
        # Check permission
        user = request.user
        if not (user.is_superadmin or user.is_admin or assignment.teacher_id == user.id):
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Get progress items
        progress_items = [{
            'id': p.id,
            'portfolio_id': p.portfolio_id,
            'portfolio_title': p.portfolio.title if p.portfolio else None,
            'note': p.note,
            'counted': p.counted,
            'created_at': p.created_at.isoformat(),
        } for p in assignment.progress_items.select_related('portfolio').all()]
        
        return JsonResponse({
            'id': assignment.id,
            'title': assignment.title or f"{assignment.category.name} topshiriq",
            'description': assignment.description,
            'teacher': {
                'id': assignment.teacher.id,
                'username': assignment.teacher.username,
                'full_name': assignment.teacher.get_full_name(),
                'department': assignment.teacher.department,
            },
            'category': {
                'id': assignment.category.id,
                'name': assignment.category.name,
                'name_uz': assignment.category.name_uz,
                'color': assignment.category.color,
                'icon': assignment.category.icon,
                'points': assignment.category.points,
            },
            'required_quantity': assignment.required_quantity,
            'completed_quantity': assignment.completed_quantity,
            'remaining_quantity': assignment.remaining_quantity,
            'progress_percentage': assignment.progress_percentage,
            'deadline': assignment.deadline.isoformat(),
            'time_remaining': assignment.time_remaining_display,
            'days_remaining': assignment.days_remaining,
            'status': assignment.status,
            'status_display': assignment.get_status_display(),
            'priority': assignment.priority,
            'priority_display': assignment.get_priority_display(),
            'is_overdue': assignment.is_overdue,
            'assigned_by': {
                'id': assignment.assigned_by.id,
                'username': assignment.assigned_by.username,
                'full_name': assignment.assigned_by.get_full_name(),
            } if assignment.assigned_by else None,
            'progress_items': progress_items,
            'created_at': assignment.created_at.isoformat(),
            'updated_at': assignment.updated_at.isoformat(),
            'completed_at': assignment.completed_at.isoformat() if assignment.completed_at else None,
        })
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def put(self, request, assignment_id):
        """Update assignment (Admin/SuperAdmin only)."""
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            return JsonResponse({'error': 'Assignment not found'}, status=404)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Update fields
        if 'required_quantity' in data:
            assignment.required_quantity = int(data['required_quantity'])
        
        if 'deadline' in data:
            from django.utils.dateparse import parse_datetime
            deadline = parse_datetime(data['deadline'])
            if deadline:
                if timezone.is_naive(deadline):
                    deadline = timezone.make_aware(deadline)
                assignment.deadline = deadline
        
        if 'title' in data:
            assignment.title = data['title']
        
        if 'description' in data:
            assignment.description = data['description']
        
        if 'priority' in data:
            assignment.priority = data['priority']
        
        if 'status' in data and data['status'] in ['active', 'completed', 'overdue', 'cancelled']:
            assignment.status = data['status']
            if data['status'] == 'completed':
                assignment.completed_at = timezone.now()
        
        assignment.save()
        assignment.check_and_update_status()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_UPDATE,
            target_model='Assignment',
            target_id=assignment.id,
            description=f'Updated assignment: {assignment}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Assignment updated successfully',
            'assignment': {
                'id': assignment.id,
                'status': assignment.status,
                'deadline': assignment.deadline.isoformat(),
            }
        })
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def delete(self, request, assignment_id):
        """Delete assignment (Admin/SuperAdmin only)."""
        try:
            assignment = Assignment.objects.get(id=assignment_id)
        except Assignment.DoesNotExist:
            return JsonResponse({'error': 'Assignment not found'}, status=404)
        
        assignment_str = str(assignment)
        assignment_id_saved = assignment.id
        assignment.delete()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_DELETE,
            target_model='Assignment',
            target_id=assignment_id_saved,
            description=f'Deleted assignment: {assignment_str}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({'message': 'Assignment deleted successfully'})


class BulkAssignmentView(View):
    """
    Create multiple assignments at once.
    POST /api/assignments/bulk/
    """
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def post(self, request):
        """Create multiple assignments."""
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        teacher_id = data.get('teacher_id')
        assignments_data = data.get('assignments', [])
        
        if not teacher_id:
            return JsonResponse({'error': 'teacher_id is required'}, status=400)
        
        if not assignments_data:
            return JsonResponse({'error': 'assignments array is required'}, status=400)
        
        # Validate teacher
        from apps.accounts.models import User
        try:
            teacher = User.objects.get(id=teacher_id, role='teacher')
        except User.DoesNotExist:
            return JsonResponse({'error': 'Teacher not found'}, status=404)
        
        created_assignments = []
        errors = []
        
        for idx, item in enumerate(assignments_data):
            try:
                category = Category.objects.get(id=item['category_id'], is_active=True)
                
                from django.utils.dateparse import parse_datetime
                deadline = parse_datetime(item['deadline'])
                if timezone.is_naive(deadline):
                    deadline = timezone.make_aware(deadline)
                
                assignment = Assignment.objects.create(
                    teacher=teacher,
                    category=category,
                    required_quantity=int(item['required_quantity']),
                    deadline=deadline,
                    title=item.get('title', ''),
                    description=item.get('description', ''),
                    priority=item.get('priority', 'medium'),
                    assigned_by=request.user
                )
                
                created_assignments.append({
                    'id': assignment.id,
                    'category': category.name,
                    'required_quantity': assignment.required_quantity,
                })
                
            except Exception as e:
                errors.append({
                    'index': idx,
                    'error': str(e)
                })
        
        # Log activity
        if created_assignments:
            UserActivity.objects.create(
                user=request.user,
                action=UserActivity.ACTION_CREATE,
                target_model='Assignment',
                description=f'Bulk created {len(created_assignments)} assignments for {teacher.get_full_name()}',
                ip_address=get_client_ip(request),
                user_agent=request.META.get('HTTP_USER_AGENT', '')
            )
        
        return JsonResponse({
            'message': f'Created {len(created_assignments)} assignments',
            'created': created_assignments,
            'errors': errors
        }, status=201 if created_assignments else 400)


class TeacherAssignmentDashboardView(View):
    """
    Teacher's assignment dashboard with summary and deadlines.
    GET /api/assignments/my-dashboard/
    """
    
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        user = request.user
        
        if not user.is_teacher:
            return JsonResponse({'error': 'This endpoint is for teachers only'}, status=403)
        
        # Update overdue assignments
        now = timezone.now()
        Assignment.objects.filter(
            teacher=user,
            status='active',
            deadline__lt=now
        ).update(status='overdue')
        
        # Get assignments
        assignments = Assignment.objects.filter(teacher=user).select_related('category')
        
        # Stats
        total = assignments.count()
        active = assignments.filter(status='active').count()
        completed = assignments.filter(status='completed').count()
        overdue = assignments.filter(status='overdue').count()
        
        # Urgent (deadline within 7 days)
        week_later = now + timezone.timedelta(days=7)
        urgent = assignments.filter(
            status='active',
            deadline__lte=week_later
        ).order_by('deadline')
        
        urgent_list = [{
            'id': a.id,
            'title': a.title or f"{a.category.name} topshiriq",
            'category': {
                'name': a.category.name,
                'color': a.category.color,
            },
            'required_quantity': a.required_quantity,
            'completed_quantity': a.completed_quantity,
            'remaining_quantity': a.remaining_quantity,
            'progress_percentage': a.progress_percentage,
            'deadline': a.deadline.isoformat(),
            'time_remaining': a.time_remaining_display,
            'days_remaining': a.days_remaining,
            'priority': a.priority,
        } for a in urgent[:10]]
        
        # By category summary
        category_summary = assignments.filter(
            status__in=['active', 'overdue']
        ).values(
            'category__id', 'category__name', 'category__color'
        ).annotate(
            total_required=Sum('required_quantity'),
            total_completed=Sum('completed_quantity'),
            count=Count('id')
        )
        
        category_list = [{
            'category_id': c['category__id'],
            'category_name': c['category__name'],
            'category_color': c['category__color'],
            'total_required': c['total_required'] or 0,
            'total_completed': c['total_completed'] or 0,
            'remaining': (c['total_required'] or 0) - (c['total_completed'] or 0),
            'assignment_count': c['count'],
        } for c in category_summary]
        
        # Overall progress
        total_required = sum(c['total_required'] for c in category_list)
        total_completed_items = sum(c['total_completed'] for c in category_list)
        overall_progress = int((total_completed_items / total_required * 100)) if total_required > 0 else 0
        
        return JsonResponse({
            'summary': {
                'total_assignments': total,
                'active': active,
                'completed': completed,
                'overdue': overdue,
                'total_required_items': total_required,
                'total_completed_items': total_completed_items,
                'overall_progress': overall_progress,
            },
            'urgent_assignments': urgent_list,
            'by_category': category_list,
            'current_time': now.isoformat(),
        })


class AssignmentStatsView(View):
    """
    Assignment statistics for Admin/SuperAdmin.
    GET /api/assignments/stats/
    """
    
    @method_decorator(admin_required)
    def get(self, request):
        # Update overdue
        now = timezone.now()
        Assignment.objects.filter(
            status='active',
            deadline__lt=now
        ).update(status='overdue')
        
        # Overall stats
        total = Assignment.objects.count()
        active = Assignment.objects.filter(status='active').count()
        completed = Assignment.objects.filter(status='completed').count()
        overdue = Assignment.objects.filter(status='overdue').count()
        
        # By category
        by_category = list(Assignment.objects.values(
            'category__id', 'category__name'
        ).annotate(
            count=Count('id'),
            total_required=Sum('required_quantity'),
            total_completed=Sum('completed_quantity')
        ))
        
        # By teacher (top 10 with most assignments)
        by_teacher = list(Assignment.objects.values(
            'teacher__id', 'teacher__username', 'teacher__first_name', 'teacher__last_name'
        ).annotate(
            count=Count('id'),
            completed=Count('id', filter=Q(status='completed')),
            overdue=Count('id', filter=Q(status='overdue'))
        ).order_by('-count')[:10])
        
        # Recent assignments
        recent = Assignment.objects.select_related('teacher', 'category').order_by('-created_at')[:10]
        recent_list = [{
            'id': a.id,
            'teacher': a.teacher.get_full_name(),
            'category': a.category.name,
            'status': a.status,
            'created_at': a.created_at.isoformat(),
        } for a in recent]
        
        return JsonResponse({
            'summary': {
                'total': total,
                'active': active,
                'completed': completed,
                'overdue': overdue,
            },
            'by_category': by_category,
            'by_teacher': by_teacher,
            'recent': recent_list,
        })
