"""
REST Framework ViewSets for assignments app.
"""

from rest_framework import viewsets, status, filters
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from django.utils import timezone
from django.db.models import Count, Avg, Q

from apps.accounts.permissions import IsAdminOrSuperAdmin, IsOwnerOrAdmin
from .models import Category, Assignment, AssignmentProgress
from .serializers import (
    CategorySerializer, CategoryListSerializer,
    AssignmentListSerializer, AssignmentDetailSerializer,
    AssignmentCreateSerializer, AssignmentUpdateSerializer,
    AssignmentStatusUpdateSerializer, AssignmentStatisticsSerializer,
    AssignmentProgressSerializer, AssignmentProgressCreateSerializer,
    AssignmentProgressGradeSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Category CRUD operations.
    
    list: GET /api/assignments/categories/
    create: POST /api/assignments/categories/
    retrieve: GET /api/assignments/categories/{id}/
    update: PUT /api/assignments/categories/{id}/
    partial_update: PATCH /api/assignments/categories/{id}/
    destroy: DELETE /api/assignments/categories/{id}/
    """
    
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'name_uz', 'name_en', 'name_ru', 'description']
    ordering_fields = ['name', 'order', 'created_at']
    ordering = ['order', 'name']
    
    def get_queryset(self):
        queryset = Category.objects.all()
        
        # Show only active categories for non-admin users
        if not (self.request.user.is_superadmin or self.request.user.is_admin):
            queryset = queryset.filter(is_active=True)
        
        # Optional: filter by active status
        is_active = self.request.query_params.get('is_active')
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return CategoryListSerializer
        return CategorySerializer
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['get'])
    def assignments(self, request, pk=None):
        """Get all assignments for a category."""
        category = self.get_object()
        assignments = Assignment.objects.filter(category=category)
        
        # Filter by teacher's own assignments if not admin
        if not (request.user.is_superadmin or request.user.is_admin):
            assignments = assignments.filter(teacher=request.user)
        
        serializer = AssignmentListSerializer(assignments, many=True)
        return Response(serializer.data)


class AssignmentViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Assignment CRUD operations.
    
    list: GET /api/assignments/assignments/
    create: POST /api/assignments/assignments/
    retrieve: GET /api/assignments/assignments/{id}/
    update: PUT /api/assignments/assignments/{id}/
    partial_update: PATCH /api/assignments/assignments/{id}/
    destroy: DELETE /api/assignments/assignments/{id}/
    """
    
    queryset = Assignment.objects.all()
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'status', 'priority', 'teacher']
    search_fields = ['title', 'description']
    ordering_fields = ['deadline', 'created_at', 'priority']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = Assignment.objects.select_related(
            'category', 'teacher', 'created_by'
        ).prefetch_related('progress_items')
        
        # Teachers can only see their own assignments
        if self.request.user.role == 'teacher':
            queryset = queryset.filter(teacher=self.request.user)
        
        # Filter by status
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        
        # Filter by priority
        priority = self.request.query_params.get('priority')
        if priority:
            queryset = queryset.filter(priority=priority)
        
        # Filter overdue
        overdue = self.request.query_params.get('overdue')
        if overdue and overdue.lower() == 'true':
            queryset = queryset.filter(
                deadline__lt=timezone.now(),
                status__in=['pending', 'in_progress']
            )
        
        # Filter upcoming (deadline within 7 days)
        upcoming = self.request.query_params.get('upcoming')
        if upcoming and upcoming.lower() == 'true':
            from datetime import timedelta
            week_from_now = timezone.now() + timedelta(days=7)
            queryset = queryset.filter(
                deadline__lte=week_from_now,
                deadline__gt=timezone.now(),
                status__in=['pending', 'in_progress']
            )
        
        return queryset
    
    def get_serializer_class(self):
        if self.action == 'list':
            return AssignmentListSerializer
        elif self.action == 'create':
            return AssignmentCreateSerializer
        elif self.action in ['update', 'partial_update']:
            return AssignmentUpdateSerializer
        return AssignmentDetailSerializer
    
    def get_permissions(self):
        if self.action in ['create', 'destroy']:
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        elif self.action in ['update', 'partial_update']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
    
    @action(detail=True, methods=['patch'])
    def update_status(self, request, pk=None):
        """Update assignment status."""
        assignment = self.get_object()
        serializer = AssignmentStatusUpdateSerializer(
            assignment, 
            data=request.data, 
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Status updated successfully',
            'status': assignment.status
        })
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get assignment statistics."""
        queryset = self.get_queryset()
        
        stats = queryset.aggregate(
            total=Count('id'),
            pending=Count('id', filter=Q(status='pending')),
            in_progress=Count('id', filter=Q(status='in_progress')),
            completed=Count('id', filter=Q(status='completed')),
            overdue=Count('id', filter=Q(status='overdue')),
            cancelled=Count('id', filter=Q(status='cancelled')),
            high_priority=Count('id', filter=Q(priority='high')),
            medium_priority=Count('id', filter=Q(priority='medium')),
            low_priority=Count('id', filter=Q(priority='low')),
        )
        
        # Completion rate
        if stats['total'] > 0:
            stats['completion_rate'] = round(
                (stats['completed'] / stats['total']) * 100, 2
            )
        else:
            stats['completion_rate'] = 0
        
        # Average score
        progress_items = AssignmentProgress.objects.filter(
            assignment__in=queryset,
            raw_score__isnull=False
        )
        avg_score = progress_items.aggregate(avg=Avg('raw_score'))['avg']
        stats['average_grade'] = round(avg_score, 2) if avg_score else None
        
        # By category
        by_category = queryset.values(
            'category__name', 'category__id'
        ).annotate(count=Count('id')).order_by('-count')
        stats['by_category'] = list(by_category)
        
        return Response(stats)
    
    @action(detail=False, methods=['get'])
    def my_assignments(self, request):
        """Get current user's assignments."""
        queryset = Assignment.objects.filter(
            teacher=request.user
        ).select_related('category', 'created_by')
        
        serializer = AssignmentListSerializer(queryset, many=True)
        return Response(serializer.data)
    
    @action(detail=True, methods=['post'])
    def submit(self, request, pk=None):
        """Submit a progress to an assignment."""
        assignment = self.get_object()
        
        # Check if user is assigned to this task
        if assignment.teacher != request.user:
            return Response(
                {'error': 'Siz bu topshiriqqa javob bera olmaysiz'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        # Check if assignment is still open
        if assignment.status in ['completed', 'cancelled']:
            return Response(
                {'error': 'Bu topshiriq yakunlangan'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = AssignmentProgressCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        progress = AssignmentProgress.objects.create(
            assignment=assignment,
            **serializer.validated_data
        )
        
        # Update assignment status
        assignment.status = 'in_progress'
        assignment.save()
        
        return Response(
            AssignmentProgressSerializer(progress).data,
            status=status.HTTP_201_CREATED
        )


class AssignmentProgressViewSet(viewsets.ModelViewSet):
    """
    ViewSet for AssignmentProgress CRUD operations.
    """
    
    queryset = AssignmentProgress.objects.all()
    serializer_class = AssignmentProgressSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['assignment', 'counted']
    ordering_fields = ['created_at', 'raw_score']
    ordering = ['-created_at']
    
    def get_queryset(self):
        queryset = AssignmentProgress.objects.select_related(
            'assignment', 'portfolio', 'graded_by'
        )
        
        # Teachers can only see progress for their own assignments
        if self.request.user.role == 'teacher':
            queryset = queryset.filter(assignment__teacher=self.request.user)
        
        return queryset
    
    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update']:
            return [IsAuthenticated()]
        elif self.action == 'destroy':
            return [IsAuthenticated(), IsAdminOrSuperAdmin()]
        return [IsAuthenticated()]
    
    @action(detail=True, methods=['patch'])
    def grade(self, request, pk=None):
        """Grade a progress (Admin/SuperAdmin only)."""
        progress = self.get_object()
        
        # Check permission
        if not (request.user.is_superadmin or request.user.is_admin):
            return Response(
                {'error': 'Baholash uchun ruxsat yo\'q'},
                status=status.HTTP_403_FORBIDDEN
            )
        
        serializer = AssignmentProgressGradeSerializer(
            progress,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        
        raw_score = serializer.validated_data.get('raw_score')
        grade_note = serializer.validated_data.get('grade_note', '')
        
        # Use the model's set_score method
        progress.set_score(raw_score, graded_by=request.user, note=grade_note)
        
        return Response({
            'message': 'Baholandi',
            'raw_score': progress.raw_score,
            'final_score': progress.final_score,
            'grade_note': progress.grade_note
        })
