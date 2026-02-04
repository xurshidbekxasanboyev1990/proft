"""
Views for portfolios app.
"""

import json
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.db.models import Q
from django.utils import timezone
from django.core.paginator import Paginator
import rules

from apps.accounts.permissions import role_required, admin_required, superadmin_required
from apps.accounts.models import UserActivity
from apps.accounts.views import get_client_ip
from .models import Portfolio, PortfolioAttachment, PortfolioComment, PortfolioHistory


class PortfolioListView(View):
    """
    List portfolios based on user role.
    GET /api/portfolios/
    
    - Super Admin: See all portfolios
    - Admin: See all portfolios (for approval)
    - Teacher: See only their own portfolios
    """
    
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        user = request.user
        
        # Base queryset based on role
        if user.is_superadmin:
            queryset = Portfolio.objects.all()
        elif user.is_admin:
            queryset = Portfolio.objects.all()
        else:  # Teacher
            queryset = Portfolio.objects.filter(teacher=user)
        
        # Filters
        status = request.GET.get('status')
        if status and status in ['pending', 'approved', 'rejected']:
            queryset = queryset.filter(status=status)
        
        category = request.GET.get('category')
        if category:
            queryset = queryset.filter(category=category)
        
        teacher_id = request.GET.get('teacher_id')
        if teacher_id and (user.is_superadmin or user.is_admin):
            queryset = queryset.filter(teacher_id=teacher_id)
        
        # Search
        search = request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(description__icontains=search)
            )
        
        # Ordering
        ordering = request.GET.get('ordering', '-created_at')
        if ordering in ['created_at', '-created_at', 'title', '-title', 'status', '-status']:
            queryset = queryset.order_by(ordering)
        
        # Pagination
        page = int(request.GET.get('page', 1))
        page_size = int(request.GET.get('page_size', 20))
        paginator = Paginator(queryset, page_size)
        page_obj = paginator.get_page(page)
        
        portfolios = []
        for p in page_obj:
            portfolios.append({
                'id': p.id,
                'title': p.title,
                'description': p.description[:200] + '...' if len(p.description) > 200 else p.description,
                'category': p.category,
                'category_display': p.get_category_display(),
                'status': p.status,
                'status_display': p.get_status_display(),
                'is_public': p.is_public,
                'teacher': {
                    'id': p.teacher.id,
                    'username': p.teacher.username,
                    'full_name': p.teacher.get_full_name(),
                },
                'reviewed_by': {
                    'id': p.reviewed_by.id,
                    'username': p.reviewed_by.username,
                } if p.reviewed_by else None,
                'reviewed_at': p.reviewed_at.isoformat() if p.reviewed_at else None,
                'created_at': p.created_at.isoformat(),
                'updated_at': p.updated_at.isoformat(),
            })
        
        return JsonResponse({
            'portfolios': portfolios,
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
    def post(self, request):
        """
        Create a new portfolio.
        Only teachers and superadmins can create portfolios.
        """
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        if not (request.user.is_teacher or request.user.is_superadmin):
            return JsonResponse({'error': 'Only teachers can create portfolios'}, status=403)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Validation
        required_fields = ['title', 'description']
        for field in required_fields:
            if field not in data or not data[field]:
                return JsonResponse({'error': f'{field} is required'}, status=400)
        
        # Create portfolio
        portfolio = Portfolio.objects.create(
            teacher=request.user,
            title=data['title'],
            description=data['description'],
            category=data.get('category', 'other'),
            meta_data=data.get('meta_data', {}),
            is_public=data.get('is_public', False),
            status='pending'
        )
        
        # Create history entry
        PortfolioHistory.objects.create(
            portfolio=portfolio,
            changed_by=request.user,
            old_status=None,
            new_status='pending',
            comment='Portfolio created'
        )
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_CREATE,
            target_model='Portfolio',
            target_id=portfolio.id,
            description=f'Created portfolio: {portfolio.title}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Portfolio created successfully',
            'portfolio': {
                'id': portfolio.id,
                'title': portfolio.title,
                'status': portfolio.status,
            }
        }, status=201)


class PortfolioDetailView(View):
    """
    Get, update, or delete a specific portfolio.
    GET/PUT/DELETE /api/portfolios/<portfolio_id>/
    """
    
    def get(self, request, portfolio_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            portfolio = Portfolio.objects.select_related('teacher', 'reviewed_by').get(id=portfolio_id)
        except Portfolio.DoesNotExist:
            return JsonResponse({'error': 'Portfolio not found'}, status=404)
        
        # Check permission
        if not rules.has_perm('portfolios.view_portfolio', request.user, portfolio):
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        # Get attachments
        attachments = [{
            'id': a.id,
            'title': a.title,
            'file': a.file.url if a.file else None,
            'file_type': a.file_type,
            'file_size': a.file_size,
            'created_at': a.created_at.isoformat(),
        } for a in portfolio.attachments.all()]
        
        # Get comments
        comments = [{
            'id': c.id,
            'author': {
                'id': c.author.id,
                'username': c.author.username,
                'full_name': c.author.get_full_name(),
            },
            'content': c.content,
            'created_at': c.created_at.isoformat(),
        } for c in portfolio.comments.filter(parent__isnull=True)]
        
        # Get history
        history = [{
            'id': h.id,
            'changed_by': h.changed_by.username if h.changed_by else None,
            'old_status': h.old_status,
            'new_status': h.new_status,
            'comment': h.comment,
            'created_at': h.created_at.isoformat(),
        } for h in portfolio.history.all()[:10]]
        
        return JsonResponse({
            'id': portfolio.id,
            'title': portfolio.title,
            'description': portfolio.description,
            'category': portfolio.category,
            'category_display': portfolio.get_category_display(),
            'status': portfolio.status,
            'status_display': portfolio.get_status_display(),
            'is_public': portfolio.is_public,
            'meta_data': portfolio.meta_data,
            'teacher': {
                'id': portfolio.teacher.id,
                'username': portfolio.teacher.username,
                'full_name': portfolio.teacher.get_full_name(),
                'department': portfolio.teacher.department,
                'position': portfolio.teacher.position,
            },
            'reviewed_by': {
                'id': portfolio.reviewed_by.id,
                'username': portfolio.reviewed_by.username,
                'full_name': portfolio.reviewed_by.get_full_name(),
            } if portfolio.reviewed_by else None,
            'reviewed_at': portfolio.reviewed_at.isoformat() if portfolio.reviewed_at else None,
            'review_comment': portfolio.review_comment,
            'attachments': attachments,
            'comments': comments,
            'history': history,
            'created_at': portfolio.created_at.isoformat(),
            'updated_at': portfolio.updated_at.isoformat(),
            'permissions': {
                'can_edit': rules.has_perm('portfolios.change_portfolio', request.user, portfolio),
                'can_delete': rules.has_perm('portfolios.delete_portfolio', request.user, portfolio),
                'can_approve': rules.has_perm('portfolios.approve_portfolio', request.user, portfolio),
            }
        })
    
    @method_decorator(csrf_protect)
    def put(self, request, portfolio_id):
        """Update a portfolio."""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
        except Portfolio.DoesNotExist:
            return JsonResponse({'error': 'Portfolio not found'}, status=404)
        
        # Check permission
        if not rules.has_perm('portfolios.change_portfolio', request.user, portfolio):
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        # Update fields
        updatable_fields = ['title', 'description', 'category', 'meta_data', 'is_public']
        for field in updatable_fields:
            if field in data:
                setattr(portfolio, field, data[field])
        
        # If teacher updates, reset to pending (optional behavior)
        if request.user.is_teacher and portfolio.status != 'pending':
            old_status = portfolio.status
            portfolio.status = 'pending'
            portfolio.reviewed_by = None
            portfolio.reviewed_at = None
            portfolio.review_comment = None
            
            PortfolioHistory.objects.create(
                portfolio=portfolio,
                changed_by=request.user,
                old_status=old_status,
                new_status='pending',
                comment='Portfolio updated by teacher, reset to pending'
            )
        
        portfolio.save()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_UPDATE,
            target_model='Portfolio',
            target_id=portfolio.id,
            description=f'Updated portfolio: {portfolio.title}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Portfolio updated successfully',
            'portfolio': {
                'id': portfolio.id,
                'title': portfolio.title,
                'status': portfolio.status,
            }
        })
    
    @method_decorator(csrf_protect)
    def delete(self, request, portfolio_id):
        """Delete a portfolio."""
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
        except Portfolio.DoesNotExist:
            return JsonResponse({'error': 'Portfolio not found'}, status=404)
        
        # Check permission
        if not rules.has_perm('portfolios.delete_portfolio', request.user, portfolio):
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        title = portfolio.title
        portfolio_id_saved = portfolio.id
        portfolio.delete()
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_DELETE,
            target_model='Portfolio',
            target_id=portfolio_id_saved,
            description=f'Deleted portfolio: {title}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({'message': 'Portfolio deleted successfully'})


class PortfolioApproveView(View):
    """
    Approve a portfolio.
    POST /api/portfolios/<portfolio_id>/approve/
    """
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def post(self, request, portfolio_id):
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
        except Portfolio.DoesNotExist:
            return JsonResponse({'error': 'Portfolio not found'}, status=404)
        
        if portfolio.status == 'approved':
            return JsonResponse({'error': 'Portfolio is already approved'}, status=400)
        
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            data = {}
        
        comment = data.get('comment', '')
        old_status = portfolio.status
        
        # Approve
        portfolio.approve(request.user, comment)
        
        # Create history
        PortfolioHistory.objects.create(
            portfolio=portfolio,
            changed_by=request.user,
            old_status=old_status,
            new_status='approved',
            comment=comment or 'Portfolio approved'
        )
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_APPROVE,
            target_model='Portfolio',
            target_id=portfolio.id,
            description=f'Approved portfolio: {portfolio.title}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Portfolio approved successfully',
            'portfolio': {
                'id': portfolio.id,
                'title': portfolio.title,
                'status': portfolio.status,
            }
        })


class PortfolioRejectView(View):
    """
    Reject a portfolio.
    POST /api/portfolios/<portfolio_id>/reject/
    """
    
    @method_decorator(csrf_protect)
    @method_decorator(admin_required)
    def post(self, request, portfolio_id):
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
        except Portfolio.DoesNotExist:
            return JsonResponse({'error': 'Portfolio not found'}, status=404)
        
        if portfolio.status == 'rejected':
            return JsonResponse({'error': 'Portfolio is already rejected'}, status=400)
        
        try:
            data = json.loads(request.body) if request.body else {}
        except json.JSONDecodeError:
            data = {}
        
        comment = data.get('comment', '')
        if not comment:
            return JsonResponse({'error': 'Rejection comment is required'}, status=400)
        
        old_status = portfolio.status
        
        # Reject
        portfolio.reject(request.user, comment)
        
        # Create history
        PortfolioHistory.objects.create(
            portfolio=portfolio,
            changed_by=request.user,
            old_status=old_status,
            new_status='rejected',
            comment=comment
        )
        
        # Log activity
        UserActivity.objects.create(
            user=request.user,
            action=UserActivity.ACTION_REJECT,
            target_model='Portfolio',
            target_id=portfolio.id,
            description=f'Rejected portfolio: {portfolio.title}',
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
        
        return JsonResponse({
            'message': 'Portfolio rejected successfully',
            'portfolio': {
                'id': portfolio.id,
                'title': portfolio.title,
                'status': portfolio.status,
            }
        })


class PortfolioStatsView(View):
    """
    Get portfolio statistics.
    GET /api/portfolios/stats/
    """
    
    def get(self, request):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        user = request.user
        
        if user.is_superadmin or user.is_admin:
            # Stats for all portfolios
            total = Portfolio.objects.count()
            pending = Portfolio.objects.filter(status='pending').count()
            approved = Portfolio.objects.filter(status='approved').count()
            rejected = Portfolio.objects.filter(status='rejected').count()
            
            # Category breakdown
            from django.db.models import Count
            by_category = dict(
                Portfolio.objects.values('category')
                .annotate(count=Count('id'))
                .values_list('category', 'count')
            )
            
            # Recent activity
            recent = Portfolio.objects.order_by('-updated_at')[:5].values(
                'id', 'title', 'status', 'updated_at'
            )
        else:
            # Stats for teacher's own portfolios
            queryset = Portfolio.objects.filter(teacher=user)
            total = queryset.count()
            pending = queryset.filter(status='pending').count()
            approved = queryset.filter(status='approved').count()
            rejected = queryset.filter(status='rejected').count()
            by_category = {}
            recent = queryset.order_by('-updated_at')[:5].values(
                'id', 'title', 'status', 'updated_at'
            )
        
        return JsonResponse({
            'total': total,
            'pending': pending,
            'approved': approved,
            'rejected': rejected,
            'by_category': by_category,
            'recent': list(recent),
        })


class PortfolioCommentView(View):
    """
    Add comment to a portfolio.
    POST /api/portfolios/<portfolio_id>/comments/
    """
    
    @method_decorator(csrf_protect)
    def post(self, request, portfolio_id):
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=401)
        
        try:
            portfolio = Portfolio.objects.get(id=portfolio_id)
        except Portfolio.DoesNotExist:
            return JsonResponse({'error': 'Portfolio not found'}, status=404)
        
        # Check permission to view (commenting requires at least view permission)
        if not rules.has_perm('portfolios.view_portfolio', request.user, portfolio):
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        
        content = data.get('content', '').strip()
        if not content:
            return JsonResponse({'error': 'Comment content is required'}, status=400)
        
        parent_id = data.get('parent_id')
        parent = None
        if parent_id:
            try:
                parent = PortfolioComment.objects.get(id=parent_id, portfolio=portfolio)
            except PortfolioComment.DoesNotExist:
                return JsonResponse({'error': 'Parent comment not found'}, status=404)
        
        comment = PortfolioComment.objects.create(
            portfolio=portfolio,
            author=request.user,
            content=content,
            parent=parent
        )
        
        return JsonResponse({
            'message': 'Comment added successfully',
            'comment': {
                'id': comment.id,
                'author': {
                    'id': comment.author.id,
                    'username': comment.author.username,
                },
                'content': comment.content,
                'created_at': comment.created_at.isoformat(),
            }
        }, status=201)
