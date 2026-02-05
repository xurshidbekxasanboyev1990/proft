"""
Django settings for proft project.
Professional Portfolio Management System for Teachers
"""

import os
from pathlib import Path
from decouple import config, Csv
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.redis import RedisIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', default='django-insecure-change-this-in-production')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config('DEBUG', default=False, cast=bool)

ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='localhost,127.0.0.1', cast=Csv())

# Application definition
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

THIRD_PARTY_APPS = [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'corsheaders',
    'rules',
    'django_celery_beat',
    'django_celery_results',
    'django_extensions',
    'rest_framework',
    'django_filters',
    'drf_spectacular',
]

LOCAL_APPS = [
    'apps.accounts',
    'apps.portfolios',
    'apps.hemis_auth',
    'apps.assignments',
    'apps.analytics',
    'apps.swagger',
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'allauth.account.middleware.AccountMiddleware',
    'apps.accounts.middleware.RoleBasedAccessMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

# Database - PostgreSQL
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = config('DATABASE_URL', default='postgres://postgres:password@localhost:5432/proft_db')

# Parse DATABASE_URL
import dj_database_url
DATABASES = {
    'default': dj_database_url.parse(DATABASE_URL, conn_max_age=600)
}

# Fallback if dj_database_url not available
if not DATABASES.get('default'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='proft_db'),
            'USER': config('DB_USER', default='postgres'),
            'PASSWORD': config('DB_PASSWORD', default='password'),
            'HOST': config('DB_HOST', default='db'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }

# Redis Cache Configuration
REDIS_URL = config('REDIS_URL', default='redis://localhost:6379/1')

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
            'IGNORE_EXCEPTIONS': True,
        }
    }
}

# Session Configuration - Redis Backend
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 1 week
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = not DEBUG
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_SAVE_EVERY_REQUEST = True

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'uz'
TIME_ZONE = 'Asia/Tashkent'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [BASE_DIR / 'static'] if (BASE_DIR / 'static').exists() else []
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Site framework
SITE_ID = 1

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'rules.permissions.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
    'apps.hemis_auth.backends.HemisOAuth2Backend',
]

# AllAuth Configuration
ACCOUNT_EMAIL_REQUIRED = False
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_AUTHENTICATION_METHOD = 'username'
ACCOUNT_EMAIL_VERIFICATION = 'none'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/'

# Django REST Framework Configuration
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_PARSER_CLASSES': [
        'rest_framework.parsers.JSONParser',
        'rest_framework.parsers.MultiPartParser',
        'rest_framework.parsers.FormParser',
    ],
    'DATETIME_FORMAT': '%Y-%m-%d %H:%M:%S',
    'DATE_FORMAT': '%Y-%m-%d',
    'TIME_FORMAT': '%H:%M:%S',
    # Swagger/OpenAPI Schema
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# DRF Spectacular (Swagger/OpenAPI) Configuration
SPECTACULAR_SETTINGS = {
    'TITLE': 'Portfolio Management System API',
    'DESCRIPTION': '''
## O\'qituvchilar Portfolio Boshqaruv Tizimi

Bu API Hemis OAuth 2.0 autentifikatsiya bilan ishlaydi.

### Asosiy Funksiyalar:
- 📚 **Portfoliolar** - O'qituvchilar portfoliosini boshqarish
- 📋 **Topshiriqlar** - Admin/SuperAdmin tomonidan topshiriq berish
- 📁 **Kategoriyalar** - Tezis, Esse, Maqola va boshqalar
- 📊 **Analytics** - Dashboard va hisobotlar
- 🎯 **Ball Tizimi** - Dinamik baholash

### Autentifikatsiya:
- Hemis OAuth 2.0 orqali login
- Session-based authentication
- CSRF token kerak (cookie)

### Rollar:
- **SuperAdmin** - To'liq huquq
- **Admin** - Boshqaruv huquqlari
- **Teacher** - O'qituvchi huquqlari
    ''',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    
    # Contact info
    'CONTACT': {
        'name': 'API Support',
        'email': 'support@portfolio.uz',
    },
    
    # License
    'LICENSE': {
        'name': 'MIT License',
    },
    
    # Tags
    'TAGS': [
        {'name': 'Authentication', 'description': 'Autentifikatsiya'},
        {'name': 'Users', 'description': 'Foydalanuvchilar'},
        {'name': 'Portfolios', 'description': 'Portfoliolar'},
        {'name': 'Categories', 'description': 'Kategoriyalar'},
        {'name': 'Assignments', 'description': 'Topshiriqlar'},
        {'name': 'Scoring', 'description': 'Ball tizimi'},
        {'name': 'Analytics', 'description': 'Statistika'},
        {'name': 'Reports', 'description': 'Hisobotlar'},
    ],
    
    # Schema customization
    'COMPONENT_SPLIT_REQUEST': True,
    'SCHEMA_PATH_PREFIX': r'/api/',
    
    # Authentication
    'SECURITY': [
        {'sessionAuth': []},
    ],
    
    # Enum handling
    'ENUM_NAME_OVERRIDES': {
        'StatusEnum': 'apps.assignments.models.Assignment.STATUS_CHOICES',
        'PriorityEnum': 'apps.assignments.models.Assignment.PRIORITY_CHOICES',
    },
    
    # Preprocessing/Postprocessing hooks
    'PREPROCESSING_HOOKS': ['apps.swagger.hooks.custom_preprocessing_hook'],
    'POSTPROCESSING_HOOKS': ['apps.swagger.hooks.custom_postprocessing_hook'],
}

# Hemis OAuth 2.0 Configuration
HEMIS_OAUTH2 = {
    'CLIENT_ID': config('HEMIS_CLIENT_ID', default=''),
    'CLIENT_SECRET': config('HEMIS_CLIENT_SECRET', default=''),
    'AUTHORIZATION_URL': config('HEMIS_AUTHORIZATION_URL', default='https://hemis.example.uz/oauth/authorize'),
    'TOKEN_URL': config('HEMIS_TOKEN_URL', default='https://hemis.example.uz/oauth/token'),
    'USERINFO_URL': config('HEMIS_USERINFO_URL', default='https://hemis.example.uz/oauth/userinfo'),
    'REDIRECT_URI': config('HEMIS_REDIRECT_URI', default='http://localhost:8000/auth/hemis/callback/'),
    'SCOPE': 'openid profile email',
}

# CORS Configuration (for Vue.js frontend)
CORS_ALLOWED_ORIGINS = config(
    'CORS_ALLOWED_ORIGINS',
    default='http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000',
    cast=Csv()
)
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]

# CSRF Configuration
CSRF_TRUSTED_ORIGINS = config(
    'CSRF_TRUSTED_ORIGINS',
    default='http://localhost:3000,http://localhost:5173,http://127.0.0.1:3000',
    cast=Csv()
)
CSRF_COOKIE_HTTPONLY = False  # Allow JavaScript to read CSRF token
CSRF_COOKIE_SAMESITE = 'Lax'
CSRF_COOKIE_SECURE = not DEBUG

# Security Settings (Production)
if not DEBUG:
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Celery Configuration
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_BACKEND = 'django-db'
CELERY_CACHE_BACKEND = 'default'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_TIME_LIMIT = 30 * 60  # 30 minutes
CELERY_BEAT_SCHEDULER = 'django_celery_beat.schedulers:DatabaseScheduler'

# Logging Configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'INFO',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'maxBytes': 1024 * 1024 * 5,  # 5 MB
            'backupCount': 5,
            'formatter': 'verbose',
        },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': False,
        },
        'apps': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
    },
}

# Create logs directory
LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)

# Sentry Configuration (Production)
SENTRY_DSN = config('SENTRY_DSN', default='')
if SENTRY_DSN and not DEBUG:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            CeleryIntegration(),
            RedisIntegration(),
        ],
        traces_sample_rate=0.1,
        send_default_pii=False,
        environment=config('ENVIRONMENT', default='production'),
    )
