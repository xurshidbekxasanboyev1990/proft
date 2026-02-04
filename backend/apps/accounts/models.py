"""
Custom User model for the portfolio management system.
Supports role-based access control with Hemis OAuth 2.0 integration.
"""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    """Custom user manager for User model."""
    
    def create_user(self, username, email=None, password=None, **extra_fields):
        """Create and save a regular User with the given username and password."""
        if not username:
            raise ValueError(_('The Username must be set'))
        
        email = self.normalize_email(email) if email else None
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        """Create and save a SuperUser with the given username and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('role', User.ROLE_SUPERADMIN)
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom User model with role-based access control.
    
    Roles:
    - superadmin: Full CRUD, manage all users, portfolios, reports
    - admin: Only approve/reject teachers' portfolios
    - teacher: Only manage their own portfolios
    """
    
    ROLE_SUPERADMIN = 'superadmin'
    ROLE_ADMIN = 'admin'
    ROLE_TEACHER = 'teacher'
    
    ROLE_CHOICES = [
        (ROLE_SUPERADMIN, _('Super Admin')),
        (ROLE_ADMIN, _('Admin')),
        (ROLE_TEACHER, _('Teacher')),
    ]
    
    # Role field
    role = models.CharField(
        _('role'),
        max_length=20,
        choices=ROLE_CHOICES,
        default=ROLE_TEACHER,
        db_index=True
    )
    
    # Hemis OAuth 2.0 fields
    hemis_id = models.CharField(
        _('Hemis ID'),
        max_length=100,
        unique=True,
        null=True,
        blank=True,
        db_index=True
    )
    hemis_access_token = models.TextField(
        _('Hemis Access Token'),
        blank=True,
        null=True
    )
    hemis_refresh_token = models.TextField(
        _('Hemis Refresh Token'),
        blank=True,
        null=True
    )
    hemis_token_expires_at = models.DateTimeField(
        _('Hemis Token Expires At'),
        null=True,
        blank=True
    )
    
    # Profile fields
    avatar = models.ImageField(
        _('avatar'),
        upload_to='avatars/',
        null=True,
        blank=True
    )
    phone_number = models.CharField(
        _('phone number'),
        max_length=20,
        blank=True,
        null=True
    )
    department = models.CharField(
        _('department'),
        max_length=255,
        blank=True,
        null=True
    )
    position = models.CharField(
        _('position'),
        max_length=255,
        blank=True,
        null=True
    )
    bio = models.TextField(
        _('biography'),
        blank=True,
        null=True
    )
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    objects = UserManager()
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['role']),
            models.Index(fields=['hemis_id']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.get_full_name() or self.username} ({self.get_role_display()})"
    
    # Role check properties
    @property
    def is_superadmin(self):
        """Check if user is a super admin."""
        return self.role == self.ROLE_SUPERADMIN
    
    @property
    def is_admin(self):
        """Check if user is an admin."""
        return self.role == self.ROLE_ADMIN
    
    @property
    def is_teacher(self):
        """Check if user is a teacher."""
        return self.role == self.ROLE_TEACHER
    
    @property
    def can_manage_users(self):
        """Check if user can manage other users."""
        return self.is_superadmin
    
    @property
    def can_approve_portfolios(self):
        """Check if user can approve/reject portfolios."""
        return self.is_superadmin or self.is_admin
    
    @property
    def can_manage_all_portfolios(self):
        """Check if user can manage all portfolios (full CRUD)."""
        return self.is_superadmin
    
    def get_managed_portfolios_queryset(self):
        """Get the queryset of portfolios this user can manage."""
        from apps.portfolios.models import Portfolio
        
        if self.is_superadmin:
            return Portfolio.objects.all()
        elif self.is_admin:
            return Portfolio.objects.filter(status='pending')
        else:
            return Portfolio.objects.filter(teacher=self)


class UserActivity(models.Model):
    """Track user activities for audit purposes."""
    
    ACTION_LOGIN = 'login'
    ACTION_LOGOUT = 'logout'
    ACTION_CREATE = 'create'
    ACTION_UPDATE = 'update'
    ACTION_DELETE = 'delete'
    ACTION_APPROVE = 'approve'
    ACTION_REJECT = 'reject'
    
    ACTION_CHOICES = [
        (ACTION_LOGIN, _('Login')),
        (ACTION_LOGOUT, _('Logout')),
        (ACTION_CREATE, _('Create')),
        (ACTION_UPDATE, _('Update')),
        (ACTION_DELETE, _('Delete')),
        (ACTION_APPROVE, _('Approve')),
        (ACTION_REJECT, _('Reject')),
    ]
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='activities'
    )
    action = models.CharField(
        max_length=20,
        choices=ACTION_CHOICES
    )
    target_model = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )
    target_id = models.PositiveIntegerField(
        null=True,
        blank=True
    )
    description = models.TextField(
        blank=True,
        null=True
    )
    ip_address = models.GenericIPAddressField(
        null=True,
        blank=True
    )
    user_agent = models.TextField(
        blank=True,
        null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = _('user activity')
        verbose_name_plural = _('user activities')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.action} - {self.created_at}"
