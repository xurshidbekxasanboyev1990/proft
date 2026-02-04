# Professional Portfolio Management System (Proft)

A Django-based backend for managing teacher portfolios with Hemis OAuth 2.0 integration.

## Features

- 🔐 **Hemis OAuth 2.0 Integration** - Single Sign-On with Hemis system
- 👥 **Role-Based Access Control** - Super Admin, Admin, Teacher roles
- 📁 **Portfolio Management** - Full CRUD operations with approval workflow
- 🔄 **Approval Workflow** - Pending → Approved/Rejected status flow
- 📊 **Activity Logging** - Track all user actions for audit
- 🐳 **Dockerized** - PostgreSQL, Redis, Celery ready
- 🚀 **Production Ready** - Gunicorn, Redis sessions, Sentry logging

## Tech Stack

- **Backend**: Python 3.11+, Django 4.2+
- **Database**: PostgreSQL 15
- **Cache/Sessions**: Redis 7
- **Task Queue**: Celery
- **Auth**: Hemis OAuth 2.0, django-allauth
- **Permissions**: django-rules

## Quick Start

### Using Docker (Recommended)

```bash
# Clone the repository
git clone <repository-url>
cd proft

# Copy environment file
cp backend/.env.example backend/.env
# Edit .env with your settings

# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser
```

### Local Development

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
cd backend
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env with your settings

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

## API Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/auth/hemis/login/` | Initiate Hemis OAuth 2.0 login |
| GET | `/auth/hemis/callback/` | OAuth callback handler |
| POST | `/auth/hemis/logout/` | Logout user |
| GET | `/auth/status/` | Check authentication status |
| GET | `/auth/csrf/` | Get CSRF token |

### Users (Super Admin Only)

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/accounts/users/` | List all users |
| POST | `/api/accounts/users/` | Create new user |
| GET | `/api/accounts/users/<id>/` | Get user details |
| PUT | `/api/accounts/users/<id>/` | Update user |
| DELETE | `/api/accounts/users/<id>/` | Delete user |
| GET | `/api/accounts/me/` | Get current user |

### Portfolios

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/portfolios/` | List portfolios |
| POST | `/api/portfolios/` | Create portfolio |
| GET | `/api/portfolios/<id>/` | Get portfolio details |
| PUT | `/api/portfolios/<id>/` | Update portfolio |
| DELETE | `/api/portfolios/<id>/` | Delete portfolio |
| POST | `/api/portfolios/<id>/approve/` | Approve portfolio |
| POST | `/api/portfolios/<id>/reject/` | Reject portfolio |
| POST | `/api/portfolios/<id>/comments/` | Add comment |
| GET | `/api/portfolios/stats/` | Get statistics |

## Roles & Permissions

| Role | Permissions |
|------|-------------|
| **Super Admin** | Full CRUD on Users, Portfolios, Reports |
| **Admin** | Approve/Reject portfolios only |
| **Teacher** | Manage own portfolios only |

## Environment Variables

```env
# Django
DEBUG=False
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DATABASE_URL=postgres://user:pass@host:5432/dbname

# Redis
REDIS_URL=redis://localhost:6379/1

# Hemis OAuth 2.0
HEMIS_CLIENT_ID=your-client-id
HEMIS_CLIENT_SECRET=your-client-secret
HEMIS_AUTHORIZATION_URL=https://hemis.example.uz/oauth/authorize
HEMIS_TOKEN_URL=https://hemis.example.uz/oauth/token
HEMIS_USERINFO_URL=https://hemis.example.uz/oauth/userinfo

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:3000

# Sentry (optional)
SENTRY_DSN=your-sentry-dsn
```

## Project Structure

```
proft/
├── docker-compose.yml
└── backend/
    ├── Dockerfile
    ├── manage.py
    ├── requirements.txt
    ├── config/
    │   ├── settings.py
    │   ├── urls.py
    │   ├── wsgi.py
    │   ├── asgi.py
    │   └── celery.py
    └── apps/
        ├── accounts/
        │   ├── models.py      # User, UserActivity
        │   ├── views.py       # User management API
        │   ├── permissions.py # Role decorators
        │   ├── rules.py       # django-rules predicates
        │   └── middleware.py  # Role-based access
        ├── portfolios/
        │   ├── models.py      # Portfolio, Attachment, Comment
        │   ├── views.py       # Portfolio CRUD & approval
        │   ├── admin.py       # Django admin
        │   └── tasks.py       # Celery tasks
        └── hemis_auth/
            ├── backends.py    # OAuth 2.0 backend
            ├── views.py       # Login/logout views
            └── urls.py        # Auth URLs
```

## Vue.js Frontend Integration

The backend is ready for Vue.js SPA frontend:

1. **Session-based auth** - No JWT needed, uses HttpOnly cookies
2. **CSRF protection** - Get token from `/auth/csrf/`
3. **CORS configured** - Add frontend URL to `CORS_ALLOWED_ORIGINS`

Example frontend auth flow:

```javascript
// Get CSRF token
const csrf = await fetch('/auth/csrf/').then(r => r.json())

// Check auth status
const status = await fetch('/auth/status/', {
  credentials: 'include'
}).then(r => r.json())

// Logout
await fetch('/auth/hemis/logout/', {
  method: 'POST',
  credentials: 'include',
  headers: { 'X-CSRFToken': csrf.csrfToken }
})
```

## License

MIT
