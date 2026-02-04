"""
Serializers for assignments app.
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Category, Assignment, AssignmentSubmission


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    assignments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'name_uz', 'name_en', 'name_ru',
            'description', 'slug', 'icon', 'color', 'order',
            'is_active', 'assignments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_assignments_count(self, obj):
        return obj.assignments.count()


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for category lists."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'color']


class AssignmentSubmissionSerializer(serializers.ModelSerializer):
    """Serializer for AssignmentSubmission model."""
    
    submitted_by_name = serializers.CharField(
        source='submitted_by.get_full_name', 
        read_only=True
    )
    graded_by_name = serializers.CharField(
        source='graded_by.get_full_name', 
        read_only=True
    )
    
    class Meta:
        model = AssignmentSubmission
        fields = [
            'id', 'assignment', 'content', 'file',
            'submitted_by', 'submitted_by_name', 'submitted_at',
            'grade', 'feedback', 'graded_by', 'graded_by_name', 'graded_at'
        ]
        read_only_fields = [
            'submitted_by', 'submitted_at', 
            'graded_by', 'graded_at'
        ]


class AssignmentSubmissionCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating submissions."""
    
    class Meta:
        model = AssignmentSubmission
        fields = ['content', 'file']


class AssignmentSubmissionGradeSerializer(serializers.ModelSerializer):
    """Serializer for grading submissions."""
    
    class Meta:
        model = AssignmentSubmission
        fields = ['grade', 'feedback']
    
    def validate_grade(self, value):
        if value is not None and (value < 0 or value > 100):
            raise serializers.ValidationError(
                "Baho 0 dan 100 gacha bo'lishi kerak"
            )
        return value


class AssignmentListSerializer(serializers.ModelSerializer):
    """Serializer for assignment lists."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    assigned_to_name = serializers.CharField(
        source='assigned_to.get_full_name', 
        read_only=True
    )
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', 
        read_only=True
    )
    time_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'category', 'category_name',
            'assigned_to', 'assigned_to_name',
            'created_by', 'created_by_name',
            'status', 'priority', 'deadline',
            'time_remaining', 'is_overdue', 'progress_percentage',
            'created_at'
        ]
    
    def get_time_remaining(self, obj):
        return obj.time_remaining
    
    def get_is_overdue(self, obj):
        return obj.is_overdue
    
    def get_progress_percentage(self, obj):
        return obj.progress_percentage


class AssignmentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single assignment."""
    
    category = CategoryListSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        source='category',
        write_only=True
    )
    assigned_to_name = serializers.CharField(
        source='assigned_to.get_full_name', 
        read_only=True
    )
    assigned_to_email = serializers.EmailField(
        source='assigned_to.email', 
        read_only=True
    )
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', 
        read_only=True
    )
    submissions = AssignmentSubmissionSerializer(many=True, read_only=True)
    time_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    countdown = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 
            'category', 'category_id',
            'assigned_to', 'assigned_to_name', 'assigned_to_email',
            'created_by', 'created_by_name',
            'status', 'priority', 'deadline',
            'time_remaining', 'is_overdue', 'progress_percentage', 'countdown',
            'file_attachment', 'max_file_size_mb', 'allowed_file_types',
            'submissions', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_by', 'created_at', 'updated_at']
    
    def get_time_remaining(self, obj):
        return obj.time_remaining
    
    def get_is_overdue(self, obj):
        return obj.is_overdue
    
    def get_progress_percentage(self, obj):
        return obj.progress_percentage
    
    def get_countdown(self, obj):
        return obj.get_countdown()


class AssignmentCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating assignments."""
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        source='category'
    )
    
    class Meta:
        model = Assignment
        fields = [
            'title', 'description', 'category_id',
            'assigned_to', 'priority', 'deadline',
            'file_attachment', 'max_file_size_mb', 'allowed_file_types'
        ]
    
    def validate_deadline(self, value):
        if value <= timezone.now():
            raise serializers.ValidationError(
                "Muddat kelajakda bo'lishi kerak"
            )
        return value
    
    def validate_assigned_to(self, value):
        if value and value.role not in ['teacher', 'admin']:
            raise serializers.ValidationError(
                "Topshiriq faqat o'qituvchi yoki adminlarga berilishi mumkin"
            )
        return value


class AssignmentUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating assignments."""
    
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        source='category',
        required=False
    )
    
    class Meta:
        model = Assignment
        fields = [
            'title', 'description', 'category_id',
            'status', 'priority', 'deadline',
            'file_attachment', 'max_file_size_mb', 'allowed_file_types'
        ]
    
    def validate_deadline(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError(
                "Muddat kelajakda bo'lishi kerak"
            )
        return value


class AssignmentStatusUpdateSerializer(serializers.ModelSerializer):
    """Serializer for updating assignment status only."""
    
    class Meta:
        model = Assignment
        fields = ['status']
    
    def validate_status(self, value):
        current_status = self.instance.status
        valid_transitions = {
            'pending': ['in_progress', 'cancelled'],
            'in_progress': ['completed', 'pending', 'cancelled'],
            'completed': ['in_progress'],  # Can reopen
            'overdue': ['in_progress', 'completed', 'cancelled'],
            'cancelled': ['pending'],  # Can restore
        }
        
        allowed = valid_transitions.get(current_status, [])
        if value not in allowed:
            raise serializers.ValidationError(
                f"'{current_status}' holatidan '{value}' holatiga o'tish mumkin emas"
            )
        return value


class AssignmentStatisticsSerializer(serializers.Serializer):
    """Serializer for assignment statistics."""
    
    total = serializers.IntegerField()
    pending = serializers.IntegerField()
    in_progress = serializers.IntegerField()
    completed = serializers.IntegerField()
    overdue = serializers.IntegerField()
    cancelled = serializers.IntegerField()
    completion_rate = serializers.FloatField()
    average_grade = serializers.FloatField(allow_null=True)
    
    # By priority
    high_priority = serializers.IntegerField()
    medium_priority = serializers.IntegerField()
    low_priority = serializers.IntegerField()
    
    # By category
    by_category = serializers.ListField(child=serializers.DictField())
