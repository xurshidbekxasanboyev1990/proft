"""
Serializers for assignments app.
"""

from rest_framework import serializers
from django.utils import timezone
from .models import Category, Assignment, AssignmentProgress, ScoreHistory


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for Category model."""
    
    assignments_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'name', 'name_uz', 'name_en', 'name_ru',
            'description', 'slug', 'icon', 'color', 'order',
            'default_score', 'min_score', 'score_weight',
            'is_active', 'assignments_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['slug', 'created_at', 'updated_at']
    
    def get_assignments_count(self, obj):
        return obj.assignments.count()


class CategoryListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for category lists."""
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'color', 'default_score', 'score_weight']


class AssignmentProgressSerializer(serializers.ModelSerializer):
    """Serializer for AssignmentProgress model."""
    
    graded_by_name = serializers.CharField(
        source='graded_by.get_full_name', 
        read_only=True
    )
    
    class Meta:
        model = AssignmentProgress
        fields = [
            'id', 'assignment', 'portfolio', 'note',
            'counted', 'raw_score', 'final_score',
            'graded_by', 'graded_by_name', 'graded_at', 'grade_note',
            'created_at'
        ]
        read_only_fields = [
            'final_score', 'graded_by', 'graded_at', 'created_at'
        ]


class AssignmentProgressCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating progress."""
    
    class Meta:
        model = AssignmentProgress
        fields = ['portfolio', 'note']


class AssignmentProgressGradeSerializer(serializers.ModelSerializer):
    """Serializer for grading progress."""
    
    class Meta:
        model = AssignmentProgress
        fields = ['raw_score', 'grade_note']
    
    def validate_raw_score(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Ball 0 dan kichik bo'lishi mumkin emas"
            )
        return value


class AssignmentListSerializer(serializers.ModelSerializer):
    """Serializer for assignment lists."""
    
    category_name = serializers.CharField(source='category.name', read_only=True)
    teacher_name = serializers.CharField(
        source='teacher.get_full_name', 
        read_only=True
    )
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', 
        read_only=True
    )
    time_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    
    # Score fields
    max_score = serializers.SerializerMethodField()
    min_score_value = serializers.SerializerMethodField()
    has_custom_score = serializers.BooleanField(source='use_custom_score', read_only=True)
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'category', 'category_name',
            'teacher', 'teacher_name',
            'created_by', 'created_by_name',
            'status', 'priority', 'deadline',
            'time_remaining', 'is_overdue', 'progress_percentage',
            'max_score', 'min_score_value', 'has_custom_score',
            'created_at'
        ]
    
    def get_time_remaining(self, obj):
        return obj.time_remaining
    
    def get_is_overdue(self, obj):
        return obj.is_overdue
    
    def get_progress_percentage(self, obj):
        return obj.progress_percentage
    
    def get_max_score(self, obj):
        return obj.max_score
    
    def get_min_score_value(self, obj):
        return obj.min_score_value


class AssignmentDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer for single assignment."""
    
    category = CategoryListSerializer(read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.filter(is_active=True),
        source='category',
        write_only=True
    )
    teacher_name = serializers.CharField(
        source='teacher.get_full_name', 
        read_only=True
    )
    teacher_email = serializers.EmailField(
        source='teacher.email', 
        read_only=True
    )
    created_by_name = serializers.CharField(
        source='created_by.get_full_name', 
        read_only=True
    )
    progress_items = AssignmentProgressSerializer(many=True, read_only=True)
    time_remaining = serializers.SerializerMethodField()
    is_overdue = serializers.SerializerMethodField()
    progress_percentage = serializers.SerializerMethodField()
    countdown = serializers.SerializerMethodField()
    
    # Score fields
    max_score = serializers.SerializerMethodField()
    min_score_value = serializers.SerializerMethodField()
    effective_weight = serializers.SerializerMethodField()
    score_info = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignment
        fields = [
            'id', 'title', 'description', 
            'category', 'category_id',
            'teacher', 'teacher_name', 'teacher_email',
            'created_by', 'created_by_name',
            'status', 'priority', 'deadline',
            'time_remaining', 'is_overdue', 'progress_percentage', 'countdown',
            'file_attachment', 'max_file_size_mb', 'allowed_file_types',
            # Score fields
            'use_custom_score', 'custom_max_score', 'custom_min_score',
            'score_multiplier', 'score_note',
            'max_score', 'min_score_value', 'effective_weight', 'score_info',
            'progress_items', 'created_at', 'updated_at'
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
    
    def get_max_score(self, obj):
        return obj.max_score
    
    def get_min_score_value(self, obj):
        return obj.min_score_value
    
    def get_effective_weight(self, obj):
        return obj.effective_weight
    
    def get_score_info(self, obj):
        """Return detailed score configuration info."""
        return {
            'category_default': obj.category.default_score,
            'category_min': obj.category.min_score,
            'category_weight': float(obj.category.score_weight),
            'is_custom': obj.use_custom_score,
            'effective_max': obj.max_score,
            'effective_min': obj.min_score_value,
            'multiplier': float(obj.score_multiplier),
            'note': obj.score_note or None,
        }


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
            'teacher', 'priority', 'deadline',
            'file_attachment', 'max_file_size_mb', 'allowed_file_types'
        ]
    
    def validate_deadline(self, value):
        if value and value <= timezone.now():
            raise serializers.ValidationError(
                "Muddat kelajakda bo'lishi kerak"
            )
        return value
    
    def validate_teacher(self, value):
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


# =============================================
# Ball (Score) Tizimi Serializers
# =============================================

class AssignmentScoreUpdateSerializer(serializers.Serializer):
    """Serializer for updating assignment custom score settings."""
    
    use_custom_score = serializers.BooleanField(required=False)
    custom_max_score = serializers.IntegerField(
        required=False, 
        min_value=1, 
        max_value=1000,
        help_text="Maxsus maksimal ball (1-1000)"
    )
    custom_min_score = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=500,
        help_text="Maxsus minimal ball"
    )
    score_multiplier = serializers.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=2,
        min_value=0.1,
        max_value=10.0,
        help_text="Ball ko'paytiruvchi (0.1-10.0)"
    )
    score_note = serializers.CharField(
        required=False,
        max_length=500,
        allow_blank=True,
        help_text="Ball o'zgarishi haqida izoh"
    )
    
    def validate(self, data):
        custom_max = data.get('custom_max_score')
        custom_min = data.get('custom_min_score')
        
        if custom_max and custom_min and custom_min >= custom_max:
            raise serializers.ValidationError({
                'custom_min_score': "Minimal ball maksimal balldan kichik bo'lishi kerak"
            })
        return data


class AssignmentProgressScoreSerializer(serializers.ModelSerializer):
    """Serializer for assignment progress with scoring."""
    
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    max_score = serializers.SerializerMethodField()
    score_percentage = serializers.SerializerMethodField()
    graded_by_name = serializers.CharField(source='graded_by.get_full_name', read_only=True)
    
    class Meta:
        model = AssignmentProgress
        fields = [
            'id', 'assignment', 'assignment_title', 'portfolio',
            'raw_score', 'final_score', 'max_score', 'score_percentage',
            'grade_note', 'graded_by', 'graded_by_name', 'graded_at',
            'counted', 'note', 'created_at'
        ]
        read_only_fields = ['final_score', 'graded_by', 'graded_at', 'created_at']
    
    def get_max_score(self, obj):
        return obj.assignment.max_score
    
    def get_score_percentage(self, obj):
        return obj.score_percentage


class GradeAssignmentSerializer(serializers.Serializer):
    """Serializer for grading an assignment progress."""
    
    raw_score = serializers.IntegerField(
        min_value=0,
        help_text="Xom ball (0 dan maksimal ballgacha)"
    )
    grade_note = serializers.CharField(
        required=False,
        max_length=500,
        allow_blank=True,
        help_text="Baholash haqida izoh"
    )
    
    def validate_raw_score(self, value):
        # Will validate against assignment max_score in view
        return value


class ScoreHistorySerializer(serializers.ModelSerializer):
    """Serializer for score history records."""
    
    assignment_title = serializers.CharField(source='assignment.title', read_only=True)
    changed_by_name = serializers.CharField(source='changed_by.get_full_name', read_only=True)
    action_display = serializers.SerializerMethodField()
    
    class Meta:
        model = ScoreHistory
        fields = [
            'id', 'assignment', 'assignment_title', 'progress',
            'action', 'action_display', 'old_value', 'new_value',
            'note', 'changed_by', 'changed_by_name', 'created_at'
        ]
        read_only_fields = '__all__'
    
    def get_action_display(self, obj):
        return obj.get_action_display()


class CategoryScoreUpdateSerializer(serializers.Serializer):
    """Serializer for updating category default scores."""
    
    default_score = serializers.IntegerField(
        min_value=1,
        max_value=1000,
        help_text="Standart ball (1-1000)"
    )
    min_score = serializers.IntegerField(
        min_value=0,
        max_value=500,
        help_text="Minimal ball"
    )
    score_weight = serializers.DecimalField(
        max_digits=4,
        decimal_places=2,
        min_value=0.1,
        max_value=10.0,
        help_text="Ball vazni (0.1-10.0)"
    )
    
    def validate(self, data):
        if data.get('min_score', 0) >= data.get('default_score', 100):
            raise serializers.ValidationError({
                'min_score': "Minimal ball standart balldan kichik bo'lishi kerak"
            })
        return data


class BulkScoreUpdateSerializer(serializers.Serializer):
    """Serializer for bulk updating scores on multiple assignments."""
    
    assignment_ids = serializers.ListField(
        child=serializers.UUIDField(),
        min_length=1,
        help_text="Topshiriq ID lari ro'yxati"
    )
    use_custom_score = serializers.BooleanField(default=True)
    custom_max_score = serializers.IntegerField(
        min_value=1,
        max_value=1000,
        help_text="Barcha tanlangan topshiriqlar uchun maxsus ball"
    )
    score_multiplier = serializers.DecimalField(
        required=False,
        max_digits=4,
        decimal_places=2,
        default=1.0,
        help_text="Ball ko'paytiruvchi"
    )
    score_note = serializers.CharField(
        required=False,
        max_length=500,
        allow_blank=True,
        help_text="Izoh"
    )
