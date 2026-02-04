"""
Analytics services - Business logic for generating statistics and reports.
"""

from django.db.models import Count, Avg, Sum, Q, F
from django.db.models.functions import TruncMonth, TruncWeek, TruncDay
from django.utils import timezone
from django.contrib.auth import get_user_model
from datetime import timedelta
from typing import Dict, Any, Optional
from collections import defaultdict

User = get_user_model()


class AnalyticsService:
    """Main analytics service class"""
    
    @staticmethod
    def get_overview_stats() -> Dict[str, Any]:
        """Get general overview statistics for dashboard"""
        from apps.accounts.models import User
        from apps.portfolios.models import Portfolio
        from apps.assignments.models import Assignment, Category
        
        now = timezone.now()
        month_ago = now - timedelta(days=30)
        week_ago = now - timedelta(days=7)
        
        # User stats
        total_users = User.objects.count()
        total_teachers = User.objects.filter(role='teacher').count()
        total_admins = User.objects.filter(role__in=['admin', 'superadmin']).count()
        new_users_month = User.objects.filter(date_joined__gte=month_ago).count()
        active_users_week = User.objects.filter(last_login__gte=week_ago).count()
        
        # Portfolio stats
        total_portfolios = Portfolio.objects.count()
        approved_portfolios = Portfolio.objects.filter(status='approved').count()
        pending_portfolios = Portfolio.objects.filter(status='pending').count()
        rejected_portfolios = Portfolio.objects.filter(status='rejected').count()
        
        # Assignment stats
        total_assignments = Assignment.objects.count()
        completed_assignments = Assignment.objects.filter(status='completed').count()
        pending_assignments = Assignment.objects.filter(status='pending').count()
        overdue_assignments = Assignment.objects.filter(
            status__in=['pending', 'in_progress'],
            deadline__lt=now
        ).count()
        
        # Category stats
        total_categories = Category.objects.filter(is_active=True).count()
        
        # Completion rates
        portfolio_approval_rate = (approved_portfolios / total_portfolios * 100) if total_portfolios > 0 else 0
        assignment_completion_rate = (completed_assignments / total_assignments * 100) if total_assignments > 0 else 0
        
        return {
            'users': {
                'total': total_users,
                'teachers': total_teachers,
                'admins': total_admins,
                'new_this_month': new_users_month,
                'active_this_week': active_users_week,
            },
            'portfolios': {
                'total': total_portfolios,
                'approved': approved_portfolios,
                'pending': pending_portfolios,
                'rejected': rejected_portfolios,
                'approval_rate': round(portfolio_approval_rate, 1),
            },
            'assignments': {
                'total': total_assignments,
                'completed': completed_assignments,
                'pending': pending_assignments,
                'overdue': overdue_assignments,
                'completion_rate': round(assignment_completion_rate, 1),
            },
            'categories': {
                'total': total_categories,
            },
            'generated_at': now.isoformat(),
        }
    
    @staticmethod
    def get_portfolio_analytics(
        date_from: Optional[timezone.datetime] = None,
        date_to: Optional[timezone.datetime] = None
    ) -> Dict[str, Any]:
        """Get detailed portfolio analytics"""
        from apps.portfolios.models import Portfolio
        
        queryset = Portfolio.objects.all()
        
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        # Status distribution
        status_distribution = list(
            queryset.values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )
        
        # Monthly trend
        monthly_trend = list(
            queryset.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(
                total=Count('id'),
                approved=Count('id', filter=Q(status='approved')),
                rejected=Count('id', filter=Q(status='rejected'))
            )
            .order_by('month')
        )
        
        # By teacher
        by_teacher = list(
            queryset.values('user__first_name', 'user__last_name', 'user__id')
            .annotate(
                count=Count('id'),
                approved=Count('id', filter=Q(status='approved'))
            )
            .order_by('-count')[:10]
        )
        
        # Average processing time (from submission to approval)
        approved = queryset.filter(status='approved', approved_at__isnull=False)
        if approved.exists():
            processing_times = [
                (p.approved_at - p.created_at).total_seconds() / 3600
                for p in approved
                if p.approved_at and p.created_at
            ]
            avg_processing_hours = sum(processing_times) / len(processing_times) if processing_times else 0
        else:
            avg_processing_hours = 0
        
        return {
            'status_distribution': status_distribution,
            'monthly_trend': [
                {
                    'month': item['month'].strftime('%Y-%m') if item['month'] else None,
                    'total': item['total'],
                    'approved': item['approved'],
                    'rejected': item['rejected'],
                }
                for item in monthly_trend
            ],
            'top_teachers': [
                {
                    'id': item['user__id'],
                    'name': f"{item['user__first_name']} {item['user__last_name']}".strip(),
                    'total': item['count'],
                    'approved': item['approved'],
                }
                for item in by_teacher
            ],
            'average_processing_hours': round(avg_processing_hours, 1),
        }
    
    @staticmethod
    def get_assignment_analytics(
        date_from: Optional[timezone.datetime] = None,
        date_to: Optional[timezone.datetime] = None
    ) -> Dict[str, Any]:
        """Get detailed assignment analytics"""
        from apps.assignments.models import Assignment, AssignmentSubmission, Category
        
        queryset = Assignment.objects.all()
        
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        # Status distribution
        status_distribution = list(
            queryset.values('status')
            .annotate(count=Count('id'))
            .order_by('status')
        )
        
        # Priority distribution
        priority_distribution = list(
            queryset.values('priority')
            .annotate(count=Count('id'))
            .order_by('priority')
        )
        
        # By category
        by_category = list(
            queryset.values('category__name', 'category__id', 'category__color')
            .annotate(
                count=Count('id'),
                completed=Count('id', filter=Q(status='completed'))
            )
            .order_by('-count')
        )
        
        # Monthly trend
        monthly_trend = list(
            queryset.annotate(month=TruncMonth('created_at'))
            .values('month')
            .annotate(
                total=Count('id'),
                completed=Count('id', filter=Q(status='completed')),
                overdue=Count('id', filter=Q(status='overdue'))
            )
            .order_by('month')
        )
        
        # Average grade
        submissions_with_grade = AssignmentSubmission.objects.filter(
            grade__isnull=False
        )
        if date_from:
            submissions_with_grade = submissions_with_grade.filter(submitted_at__gte=date_from)
        if date_to:
            submissions_with_grade = submissions_with_grade.filter(submitted_at__lte=date_to)
        
        avg_grade = submissions_with_grade.aggregate(avg=Avg('grade'))['avg']
        
        # Grade distribution
        grade_distribution = {
            'excellent': submissions_with_grade.filter(grade__gte=90).count(),  # A
            'good': submissions_with_grade.filter(grade__gte=75, grade__lt=90).count(),  # B
            'satisfactory': submissions_with_grade.filter(grade__gte=60, grade__lt=75).count(),  # C
            'poor': submissions_with_grade.filter(grade__lt=60).count(),  # D/F
        }
        
        return {
            'status_distribution': status_distribution,
            'priority_distribution': priority_distribution,
            'by_category': [
                {
                    'id': item['category__id'],
                    'name': item['category__name'],
                    'color': item['category__color'],
                    'total': item['count'],
                    'completed': item['completed'],
                }
                for item in by_category
            ],
            'monthly_trend': [
                {
                    'month': item['month'].strftime('%Y-%m') if item['month'] else None,
                    'total': item['total'],
                    'completed': item['completed'],
                    'overdue': item['overdue'],
                }
                for item in monthly_trend
            ],
            'grades': {
                'average': round(avg_grade, 1) if avg_grade else None,
                'distribution': grade_distribution,
            },
        }
    
    @staticmethod
    def get_teacher_performance(
        teacher_id: Optional[int] = None,
        date_from: Optional[timezone.datetime] = None,
        date_to: Optional[timezone.datetime] = None
    ) -> Dict[str, Any]:
        """Get teacher performance analytics"""
        from apps.portfolios.models import Portfolio
        from apps.assignments.models import Assignment, AssignmentSubmission
        
        filters = {}
        if teacher_id:
            filters['user_id'] = teacher_id
        if date_from:
            filters['created_at__gte'] = date_from
        if date_to:
            filters['created_at__lte'] = date_to
        
        # Portfolio stats per teacher
        portfolio_stats = User.objects.filter(role='teacher').annotate(
            total_portfolios=Count('portfolios', filter=Q(**{
                k.replace('user_id', 'user__id'): v 
                for k, v in filters.items() 
                if k != 'user_id'
            }) if filters else Q()),
            approved_portfolios=Count(
                'portfolios', 
                filter=Q(portfolios__status='approved')
            )
        ).values('id', 'first_name', 'last_name', 'total_portfolios', 'approved_portfolios')
        
        # Assignment stats per teacher
        assignment_filters = {}
        if teacher_id:
            assignment_filters['assigned_to_id'] = teacher_id
        if date_from:
            assignment_filters['created_at__gte'] = date_from
        if date_to:
            assignment_filters['created_at__lte'] = date_to
        
        assignment_stats = User.objects.filter(role='teacher').annotate(
            total_assignments=Count(
                'assigned_assignments',
                filter=Q(**{
                    k.replace('assigned_to_id', 'assigned_assignments__assigned_to__id'): v
                    for k, v in assignment_filters.items()
                    if k != 'assigned_to_id'
                }) if assignment_filters else Q()
            ),
            completed_assignments=Count(
                'assigned_assignments',
                filter=Q(assigned_assignments__status='completed')
            ),
            overdue_assignments=Count(
                'assigned_assignments',
                filter=Q(assigned_assignments__status='overdue')
            )
        ).values(
            'id', 'first_name', 'last_name', 
            'total_assignments', 'completed_assignments', 'overdue_assignments'
        )
        
        # Combine and format
        teachers_data = {}
        for p in portfolio_stats:
            tid = p['id']
            teachers_data[tid] = {
                'id': tid,
                'name': f"{p['first_name']} {p['last_name']}".strip(),
                'portfolios': {
                    'total': p['total_portfolios'],
                    'approved': p['approved_portfolios'],
                },
                'assignments': {'total': 0, 'completed': 0, 'overdue': 0},
            }
        
        for a in assignment_stats:
            tid = a['id']
            if tid in teachers_data:
                teachers_data[tid]['assignments'] = {
                    'total': a['total_assignments'],
                    'completed': a['completed_assignments'],
                    'overdue': a['overdue_assignments'],
                }
        
        # Calculate performance scores
        for tid, data in teachers_data.items():
            portfolio_rate = (
                data['portfolios']['approved'] / data['portfolios']['total'] * 100
                if data['portfolios']['total'] > 0 else 0
            )
            assignment_rate = (
                data['assignments']['completed'] / data['assignments']['total'] * 100
                if data['assignments']['total'] > 0 else 0
            )
            data['performance_score'] = round((portfolio_rate + assignment_rate) / 2, 1)
        
        # Sort by performance
        sorted_teachers = sorted(
            teachers_data.values(),
            key=lambda x: x['performance_score'],
            reverse=True
        )
        
        if teacher_id:
            return teachers_data.get(teacher_id, {})
        
        return {
            'teachers': sorted_teachers,
            'top_performers': sorted_teachers[:5],
            'needs_attention': [t for t in sorted_teachers if t['performance_score'] < 50][-5:],
        }
    
    @staticmethod
    def get_chart_data(chart_type: str, period: str = 'month') -> Dict[str, Any]:
        """Get data formatted for charts"""
        from apps.portfolios.models import Portfolio
        from apps.assignments.models import Assignment
        
        now = timezone.now()
        
        if period == 'week':
            start_date = now - timedelta(days=7)
            trunc_func = TruncDay
            date_format = '%Y-%m-%d'
        elif period == 'month':
            start_date = now - timedelta(days=30)
            trunc_func = TruncDay
            date_format = '%Y-%m-%d'
        elif period == 'year':
            start_date = now - timedelta(days=365)
            trunc_func = TruncMonth
            date_format = '%Y-%m'
        else:
            start_date = now - timedelta(days=30)
            trunc_func = TruncDay
            date_format = '%Y-%m-%d'
        
        if chart_type == 'portfolio_trend':
            data = list(
                Portfolio.objects.filter(created_at__gte=start_date)
                .annotate(date=trunc_func('created_at'))
                .values('date')
                .annotate(count=Count('id'))
                .order_by('date')
            )
            return {
                'labels': [d['date'].strftime(date_format) for d in data],
                'datasets': [{
                    'label': 'Portfoliolar',
                    'data': [d['count'] for d in data],
                }]
            }
        
        elif chart_type == 'assignment_status':
            data = list(
                Assignment.objects.filter(created_at__gte=start_date)
                .values('status')
                .annotate(count=Count('id'))
            )
            status_labels = {
                'pending': 'Kutilmoqda',
                'in_progress': 'Jarayonda',
                'completed': 'Bajarildi',
                'overdue': 'Muddati o\'tgan',
                'cancelled': 'Bekor qilingan',
            }
            return {
                'labels': [status_labels.get(d['status'], d['status']) for d in data],
                'datasets': [{
                    'data': [d['count'] for d in data],
                }]
            }
        
        elif chart_type == 'category_distribution':
            from apps.assignments.models import Category
            data = list(
                Assignment.objects.filter(created_at__gte=start_date)
                .values('category__name', 'category__color')
                .annotate(count=Count('id'))
                .order_by('-count')
            )
            return {
                'labels': [d['category__name'] for d in data],
                'datasets': [{
                    'data': [d['count'] for d in data],
                    'backgroundColor': [d['category__color'] for d in data],
                }]
            }
        
        return {'labels': [], 'datasets': []}
