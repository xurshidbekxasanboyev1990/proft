# HEMIS OAuth 2.0 Integratsiya

## Umumiy ma'lumot

HEMIS Universitet tizimi bilan OAuth 2.0 integratsiya. Bu integratsiya orqali foydalanuvchilar HEMIS Universitet tizimidagi hodim yoki talaba akkaunti yordamida Portfolio tizimiga kirish imkoniyatiga ega bo'ladilar.

**OAuth standarti:** OAuth 2.0 (Authorization Code Flow)

---

## 📋 Klient sozlamalari (HEMIS tomonida)

### 1. HEMIS boshqaruv panelida klient yaratish

1. HEMIS Universitet tizimi boshqaruv paneliga kiring
2. **Tizim → oAuth klientlar** sahifasiga o'ting
3. Yangi klient yarating:
   - **Klient nomi:** Portfolio Tizimi
   - **Redirect URI:** `http://your-domain.com/auth/hemis/callback/`
   - **Hodim URL:** `https://univer.hemis.uz` (hodimlar uchun)
   - **Talaba URL:** `https://student.hemis.uz` (talabalar uchun)

4. Saqlangach quyidagi ma'lumotlar hosil bo'ladi:
   - **Client ID** (masalan: `8`)
   - **Client Secret** (masalan: `Vt5dnZtzK_v3vzs0ycsV2uLzrh7zicZUrz4TEiOI`)

> ⚠️ **Eslatma:** Bir nechta Redirect URI vergul orqali kiritiladi. Production va development uchun alohida URI'lar ko'rsating.

---

## 🔧 Backend Sozlamalari (Django)

### 1. Environment Variables (.env)

```env
# HEMIS OAuth 2.0 Configuration
HEMIS_CLIENT_ID=8
HEMIS_CLIENT_SECRET=Vt5dnZtzK_v3vzs0ycsV2uLzrh7zicZUrz4TEiOI
HEMIS_REDIRECT_URI=http://localhost:8000/auth/hemis/callback/

# HEMIS URLs - Hodimlar uchun (Employee)
HEMIS_AUTHORIZATION_URL=https://univer.hemis.uz/oauth/authorize
HEMIS_TOKEN_URL=https://univer.hemis.uz/oauth/access-token
HEMIS_USERINFO_URL=https://univer.hemis.uz/oauth/api/user

# Yoki Talabalar uchun (Student)
# HEMIS_AUTHORIZATION_URL=https://student.hemis.uz/oauth/authorize
# HEMIS_TOKEN_URL=https://student.hemis.uz/oauth/access-token
# HEMIS_USERINFO_URL=https://student.hemis.uz/oauth/api/user
```

### 2. Django Settings (settings.py)

```python
# HEMIS OAuth 2.0 Configuration
HEMIS_OAUTH2 = {
    'CLIENT_ID': os.environ.get('HEMIS_CLIENT_ID', ''),
    'CLIENT_SECRET': os.environ.get('HEMIS_CLIENT_SECRET', ''),
    'REDIRECT_URI': os.environ.get('HEMIS_REDIRECT_URI', 'http://localhost:8000/auth/hemis/callback/'),
    
    # Hodimlar uchun (Employee Portal)
    'AUTHORIZATION_URL': os.environ.get('HEMIS_AUTHORIZATION_URL', 'https://univer.hemis.uz/oauth/authorize'),
    'TOKEN_URL': os.environ.get('HEMIS_TOKEN_URL', 'https://univer.hemis.uz/oauth/access-token'),
    'USERINFO_URL': os.environ.get('HEMIS_USERINFO_URL', 'https://univer.hemis.uz/oauth/api/user'),
    
    # Talabalar uchun (Student Portal) - agar kerak bo'lsa
    # 'AUTHORIZATION_URL': 'https://student.hemis.uz/oauth/authorize',
    # 'TOKEN_URL': 'https://student.hemis.uz/oauth/access-token',
    # 'USERINFO_URL': 'https://student.hemis.uz/oauth/api/user',
    
    # User info so'rovida olinadigan maydonlar
    'USER_FIELDS': 'id,uuid,type,name,firstname,surname,patronymic,login,picture,email,university_id,phone,birth_date',
    
    # Scope
    'SCOPE': 'openid profile email',
}

# Authentication Backends
AUTHENTICATION_BACKENDS = [
    'apps.hemis_auth.backends.HemisOAuth2Backend',  # HEMIS OAuth
    'django.contrib.auth.backends.ModelBackend',     # Default Django auth
]
```

---

## 🔄 OAuth 2.0 Flow

### Authorization Code Flow diagrammasi

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Frontend  │     │   Backend   │     │    HEMIS    │
│   (Vue.js)  │     │  (Django)   │     │   Server    │
└──────┬──────┘     └──────┬──────┘     └──────┬──────┘
       │                   │                   │
       │  1. Login click   │                   │
       │──────────────────>│                   │
       │                   │                   │
       │  2. Redirect to   │                   │
       │     HEMIS         │                   │
       │<──────────────────│                   │
       │                   │                   │
       │  3. User login    │                   │
       │───────────────────────────────────────>
       │                   │                   │
       │  4. Redirect with │                   │
       │     auth code     │                   │
       │<───────────────────────────────────────
       │                   │                   │
       │  5. Callback with │                   │
       │     code & state  │                   │
       │──────────────────>│                   │
       │                   │                   │
       │                   │  6. Exchange code │
       │                   │     for token     │
       │                   │──────────────────>│
       │                   │                   │
       │                   │  7. Access token  │
       │                   │<──────────────────│
       │                   │                   │
       │                   │  8. Get user info │
       │                   │──────────────────>│
       │                   │                   │
       │                   │  9. User data     │
       │                   │<──────────────────│
       │                   │                   │
       │  10. Set session  │                   │
       │      & redirect   │                   │
       │<──────────────────│                   │
       │                   │                   │
```

---

## 🛣️ API Endpoints

### Backend URLs (Django)

| Endpoint | Method | Tavsif |
|----------|--------|--------|
| `/auth/hemis/login/` | GET | HEMIS OAuth loginni boshlash |
| `/auth/hemis/callback/` | GET | HEMIS OAuth callback |
| `/auth/logout/` | POST | Tizimdan chiqish |
| `/auth/me/` | GET | Joriy foydalanuvchi ma'lumotlari |
| `/auth/refresh-token/` | POST | Access tokenni yangilash |

### Development Endpoint (faqat DEBUG=True)

| Endpoint | Method | Tavsif |
|----------|--------|--------|
| `/auth/dev-login/` | POST | Development login (test uchun) |

---

## 📁 Fayl tuzilishi

```
backend/
├── apps/
│   └── hemis_auth/
│       ├── __init__.py
│       ├── admin.py
│       ├── apps.py
│       ├── backends.py      # OAuth backend & client
│       ├── urls.py          # Auth URLs
│       └── views.py         # Auth views
├── config/
│   └── settings.py          # HEMIS_OAUTH2 config
└── .env                     # Environment variables
```

---

## 💻 Backend Kod (Python/Django)

### 1. OAuth Client (`apps/hemis_auth/backends.py`)

```python
"""
HEMIS OAuth 2.0 Client - PHP dan Python/Django ga moslashtirish
"""

import requests
import logging
from urllib.parse import urlencode
from django.conf import settings

logger = logging.getLogger(__name__)


class HemisOAuth2Client:
    """
    HEMIS OAuth 2.0 API uchun client.
    PHP dagi League\OAuth2\Client\Provider\GenericProvider ning analogi.
    """
    
    def __init__(self):
        """
        PHP:
        $provider = new GenericProvider([
            'clientId' => '8',
            'clientSecret' => 'xxx',
            'redirectUri' => 'http://...',
            'urlAuthorize' => 'https://univer.hemis.uz/oauth/authorize',
            'urlAccessToken' => 'https://univer.hemis.uz/oauth/access-token',
            'urlResourceOwnerDetails' => 'https://univer.hemis.uz/oauth/api/user'
        ]);
        """
        self.config = settings.HEMIS_OAUTH2
        self.client_id = self.config['CLIENT_ID']
        self.client_secret = self.config['CLIENT_SECRET']
        self.redirect_uri = self.config['REDIRECT_URI']
        self.authorization_url = self.config['AUTHORIZATION_URL']
        self.token_url = self.config['TOKEN_URL']
        self.userinfo_url = self.config['USERINFO_URL']
        self.user_fields = self.config.get('USER_FIELDS', 'id,uuid,type,name,login,picture,email,university_id,phone')
    
    def get_authorization_url(self, state=None):
        """
        Authorization URL yaratish.
        
        PHP:
        $authorizationUrl = $provider->getAuthorizationUrl();
        $_SESSION['oauth2state'] = $provider->getState();
        header('Location: ' . $authorizationUrl);
        """
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'response_type': 'code',
            'scope': self.config.get('SCOPE', 'openid profile email'),
        }
        
        if state:
            params['state'] = state
        
        return f"{self.authorization_url}?{urlencode(params)}"
    
    def exchange_code_for_token(self, code):
        """
        Authorization code ni access token ga almashtirish.
        
        PHP:
        $accessToken = $provider->getAccessToken('authorization_code', [
            'code' => $_GET['code']
        ]);
        """
        try:
            response = requests.post(
                self.token_url,
                data={
                    'grant_type': 'authorization_code',
                    'code': code,
                    'redirect_uri': self.redirect_uri,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                },
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                timeout=30
            )
            
            if response.status_code == 200:
                token_data = response.json()
                logger.info(f"Token exchange successful")
                return token_data
            else:
                logger.error(f"Token exchange failed: {response.status_code} - {response.text}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Token exchange request error: {e}")
            return None
    
    def refresh_access_token(self, refresh_token):
        """
        Access token ni refresh token orqali yangilash.
        
        PHP:
        $newAccessToken = $provider->getAccessToken('refresh_token', [
            'refresh_token' => $existingAccessToken->getRefreshToken()
        ]);
        """
        try:
            response = requests.post(
                self.token_url,
                data={
                    'grant_type': 'refresh_token',
                    'refresh_token': refresh_token,
                    'client_id': self.client_id,
                    'client_secret': self.client_secret,
                },
                headers={
                    'Accept': 'application/json',
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(f"Token refresh failed: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Token refresh error: {e}")
            return None
    
    def get_user_info(self, access_token):
        """
        Foydalanuvchi ma'lumotlarini olish.
        
        PHP:
        $resourceOwner = $provider->getResourceOwner($accessToken);
        foreach ($resourceOwner->toArray() as $key => $value) {
            echo "<p>$key: <b>$value</b></p>";
        }
        
        HEMIS API Response:
        {
            "id": "123",
            "uuid": "xxx-xxx-xxx",
            "type": "employee",
            "name": "Ism Familiya",
            "firstname": "Ism",
            "surname": "Familiya",
            "patronymic": "Otasining ismi",
            "login": "username",
            "picture": "https://...",
            "email": "user@example.com",
            "university_id": "456",
            "phone": "+998901234567",
            "birth_date": "1990-01-01"
        }
        """
        try:
            # User fields qo'shish
            url = f"{self.userinfo_url}?fields={self.user_fields}"
            
            response = requests.get(
                url,
                headers={
                    'Authorization': f'Bearer {access_token}',
                    'Accept': 'application/json',
                },
                timeout=30
            )
            
            if response.status_code == 200:
                user_data = response.json()
                logger.info(f"User info retrieved successfully")
                return user_data
            else:
                logger.error(f"User info request failed: {response.status_code}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"User info request error: {e}")
            return None
```

### 2. Authentication Backend (`apps/hemis_auth/backends.py`)

```python
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import BaseBackend
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class HemisOAuth2Backend(BaseBackend):
    """
    Django authentication backend for HEMIS OAuth 2.0.
    """
    
    def authenticate(self, request, hemis_id=None, access_token=None, user_data=None, **kwargs):
        """
        HEMIS OAuth orqali foydalanuvchini autentifikatsiya qilish.
        """
        if not hemis_id:
            return None
        
        try:
            # Mavjud foydalanuvchini topish
            user = User.objects.get(hemis_id=hemis_id)
            
            # Tokenlarni yangilash
            if access_token:
                user.hemis_access_token = access_token
                user.hemis_token_expires_at = timezone.now() + timedelta(hours=1)
            
            # Ma'lumotlarni yangilash
            if user_data:
                self._update_user_from_hemis(user, user_data)
            
            user.save()
            return user
            
        except User.DoesNotExist:
            # Yangi foydalanuvchi yaratish
            if not user_data:
                return None
            
            return self._create_user_from_hemis(hemis_id, access_token, user_data)
    
    def _create_user_from_hemis(self, hemis_id, access_token, user_data):
        """
        HEMIS ma'lumotlaridan yangi foydalanuvchi yaratish.
        
        HEMIS user_data maydonlari:
        - id: HEMIS ID
        - uuid: Unique identifier
        - type: "employee" yoki "student"
        - name: To'liq ism
        - firstname: Ism
        - surname: Familiya
        - patronymic: Otasining ismi
        - login: Username
        - picture: Profil rasmi URL
        - email: Email manzil
        - university_id: Universitet ID
        - phone: Telefon raqami
        - birth_date: Tug'ilgan sana
        """
        # Username aniqlash
        username = (
            user_data.get('login') or 
            user_data.get('username') or 
            f"hemis_{hemis_id}"
        )
        
        # Unique username ta'minlash
        base_username = username
        counter = 1
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{counter}"
            counter += 1
        
        # Foydalanuvchi yaratish
        user = User.objects.create(
            username=username,
            email=user_data.get('email', ''),
            hemis_id=hemis_id,
            hemis_access_token=access_token,
            hemis_token_expires_at=timezone.now() + timedelta(hours=1),
            
            # Rol aniqlash - HEMIS type ga qarab
            role='teacher' if user_data.get('type') == 'employee' else 'teacher',
            
            # Shaxsiy ma'lumotlar
            first_name=user_data.get('firstname', user_data.get('first_name', '')),
            last_name=user_data.get('surname', user_data.get('last_name', '')),
            middle_name=user_data.get('patronymic', ''),
            phone=user_data.get('phone', ''),
            
            # Qo'shimcha ma'lumotlar
            avatar=user_data.get('picture', ''),
        )
        
        user.set_unusable_password()
        user.save()
        
        return user
    
    def _update_user_from_hemis(self, user, user_data):
        """Mavjud foydalanuvchi ma'lumotlarini yangilash."""
        if user_data.get('email'):
            user.email = user_data['email']
        if user_data.get('firstname'):
            user.first_name = user_data['firstname']
        if user_data.get('surname'):
            user.last_name = user_data['surname']
        if user_data.get('patronymic'):
            user.middle_name = user_data['patronymic']
        if user_data.get('phone'):
            user.phone = user_data['phone']
        if user_data.get('picture'):
            user.avatar = user_data['picture']
    
    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
```

### 3. Views (`apps/hemis_auth/views.py`)

```python
import secrets
import logging
from django.http import JsonResponse
from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import login, logout, authenticate
from django.conf import settings

from .backends import HemisOAuth2Client

logger = logging.getLogger(__name__)


class HemisLoginView(View):
    """
    HEMIS OAuth login boshlash.
    GET /auth/hemis/login/
    
    PHP analogi:
    if (!isset($_GET['code'])) {
        if (isset($_GET['start'])) {
            $authorizationUrl = $provider->getAuthorizationUrl();
            $_SESSION['oauth2state'] = $provider->getState();
            header('Location: ' . $authorizationUrl);
            exit;
        }
    }
    """
    
    def get(self, request):
        # State yaratish (CSRF himoyasi)
        state = secrets.token_urlsafe(32)
        request.session['hemis_oauth_state'] = state
        
        # Next URL saqlash
        next_url = request.GET.get('next', '/dashboard/')
        request.session['hemis_oauth_next'] = next_url
        
        # Authorization URL olish
        client = HemisOAuth2Client()
        auth_url = client.get_authorization_url(state=state)
        
        logger.info(f"Redirecting to HEMIS OAuth: {auth_url}")
        
        return redirect(auth_url)


class HemisCallbackView(View):
    """
    HEMIS OAuth callback.
    GET /auth/hemis/callback/?code=xxx&state=yyy
    
    PHP analogi:
    } else if (empty($_GET['state']) || $_GET['state'] !== $_SESSION['oauth2state']) {
        exit('Invalid state');
    } else {
        $accessToken = $provider->getAccessToken('authorization_code', ['code' => $_GET['code']]);
        $resourceOwner = $provider->getResourceOwner($accessToken);
    }
    """
    
    def get(self, request):
        # Xatolikni tekshirish
        error = request.GET.get('error')
        if error:
            error_description = request.GET.get('error_description', 'Unknown error')
            logger.error(f"HEMIS OAuth error: {error} - {error_description}")
            return self._error_response(error, error_description)
        
        # Authorization code olish
        code = request.GET.get('code')
        if not code:
            return self._error_response('missing_code', 'No authorization code provided')
        
        # State tekshirish (CSRF himoyasi)
        state = request.GET.get('state')
        stored_state = request.session.get('hemis_oauth_state')
        
        if not state or state != stored_state:
            logger.warning("Invalid OAuth state parameter")
            return self._error_response('invalid_state', 'Invalid state parameter')
        
        # State ni o'chirish
        del request.session['hemis_oauth_state']
        
        # Code ni token ga almashtirish
        client = HemisOAuth2Client()
        token_response = client.exchange_code_for_token(code)
        
        if not token_response:
            return self._error_response('token_error', 'Failed to exchange code for token')
        
        access_token = token_response.get('access_token')
        refresh_token = token_response.get('refresh_token')
        
        if not access_token:
            return self._error_response('no_token', 'No access token in response')
        
        # Foydalanuvchi ma'lumotlarini olish
        user_info = client.get_user_info(access_token)
        
        if not user_info:
            return self._error_response('userinfo_error', 'Failed to get user info')
        
        # HEMIS ID olish
        hemis_id = user_info.get('id') or user_info.get('uuid')
        
        if not hemis_id:
            logger.error(f"No hemis_id in user info: {user_info}")
            return self._error_response('no_user_id', 'No user ID in response')
        
        # Foydalanuvchini autentifikatsiya qilish
        user = authenticate(
            request,
            hemis_id=str(hemis_id),
            access_token=access_token,
            user_data=user_info
        )
        
        if not user:
            return self._error_response('auth_failed', 'Authentication failed')
        
        # Refresh token saqlash
        if refresh_token:
            user.hemis_refresh_token = refresh_token
            user.save()
        
        # Login qilish
        login(request, user, backend='apps.hemis_auth.backends.HemisOAuth2Backend')
        
        logger.info(f"User {user.username} logged in via HEMIS OAuth")
        
        # Frontend ga redirect
        next_url = request.session.pop('hemis_oauth_next', '/dashboard/')
        frontend_url = settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:3000'
        
        # Token bilan redirect (SPA uchun)
        from rest_framework_simplejwt.tokens import RefreshToken
        tokens = RefreshToken.for_user(user)
        
        redirect_url = f"{frontend_url}/auth/callback?access={tokens.access_token}&refresh={tokens}&next={next_url}"
        
        return redirect(redirect_url)
    
    def _error_response(self, error, description):
        """Xatolik response."""
        frontend_url = settings.FRONTEND_URL if hasattr(settings, 'FRONTEND_URL') else 'http://localhost:3000'
        return redirect(f"{frontend_url}/auth/error?error={error}&description={description}")
```

### 4. URLs (`apps/hemis_auth/urls.py`)

```python
from django.urls import path
from . import views

app_name = 'hemis_auth'

urlpatterns = [
    # HEMIS OAuth 2.0
    path('hemis/login/', views.HemisLoginView.as_view(), name='hemis-login'),
    path('hemis/callback/', views.HemisCallbackView.as_view(), name='hemis-callback'),
    
    # Auth endpoints
    path('me/', views.CurrentUserView.as_view(), name='current-user'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('refresh-token/', views.RefreshTokenView.as_view(), name='refresh-token'),
    
    # Development only
    path('dev-login/', views.DevLoginView.as_view(), name='dev-login'),
]
```

---

## 🖥️ Frontend Kod (Vue.js)

### 1. Auth Service (`src/services/authService.js`)

```javascript
import api from './api'

const AUTH_TOKEN_KEY = 'access_token'
const REFRESH_TOKEN_KEY = 'refresh_token'

export default {
  /**
   * HEMIS OAuth login URL olish
   */
  getHemisLoginUrl(nextUrl = '/dashboard') {
    const baseUrl = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'
    return `${baseUrl}/auth/hemis/login/?next=${encodeURIComponent(nextUrl)}`
  },

  /**
   * HEMIS OAuth callback dan tokenlarni saqlash
   */
  handleOAuthCallback() {
    const params = new URLSearchParams(window.location.search)
    const accessToken = params.get('access')
    const refreshToken = params.get('refresh')
    const next = params.get('next') || '/dashboard'

    if (accessToken && refreshToken) {
      this.setTokens(accessToken, refreshToken)
      return { success: true, next }
    }

    return { success: false, error: params.get('error') }
  },

  /**
   * Tokenlarni saqlash
   */
  setTokens(accessToken, refreshToken) {
    localStorage.setItem(AUTH_TOKEN_KEY, accessToken)
    localStorage.setItem(REFRESH_TOKEN_KEY, refreshToken)
  },

  /**
   * Access token olish
   */
  getAccessToken() {
    return localStorage.getItem(AUTH_TOKEN_KEY)
  },

  /**
   * Refresh token olish
   */
  getRefreshToken() {
    return localStorage.getItem(REFRESH_TOKEN_KEY)
  },

  /**
   * Tokenlarni o'chirish
   */
  clearTokens() {
    localStorage.removeItem(AUTH_TOKEN_KEY)
    localStorage.removeItem(REFRESH_TOKEN_KEY)
  },

  /**
   * Foydalanuvchi login holatini tekshirish
   */
  isAuthenticated() {
    return !!this.getAccessToken()
  },

  /**
   * Joriy foydalanuvchi ma'lumotlarini olish
   */
  async getCurrentUser() {
    const response = await api.get('/auth/me/')
    return response.data
  },

  /**
   * Logout
   */
  async logout() {
    try {
      await api.post('/auth/logout/')
    } finally {
      this.clearTokens()
    }
  },

  /**
   * Token yangilash
   */
  async refreshAccessToken() {
    const refreshToken = this.getRefreshToken()
    if (!refreshToken) {
      throw new Error('No refresh token')
    }

    const response = await api.post('/auth/refresh-token/', {
      refresh: refreshToken
    })

    const { access } = response.data
    localStorage.setItem(AUTH_TOKEN_KEY, access)
    return access
  },

  /**
   * Development login (faqat test uchun)
   */
  async devLogin(username, password) {
    const response = await api.post('/auth/dev-login/', { username, password })
    const { access, refresh } = response.data
    this.setTokens(access, refresh)
    return response.data
  }
}
```

### 2. Login View (`src/views/auth/LoginView.vue`)

```vue
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50 py-12 px-4">
    <div class="max-w-md w-full space-y-8">
      <div>
        <h2 class="mt-6 text-center text-3xl font-extrabold text-gray-900">
          Portfolio Tizimi
        </h2>
        <p class="mt-2 text-center text-sm text-gray-600">
          HEMIS tizimi orqali kiring
        </p>
      </div>

      <!-- HEMIS OAuth Login Button -->
      <div class="mt-8 space-y-6">
        <a
          :href="hemisLoginUrl"
          class="group relative w-full flex justify-center py-3 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
        >
          <span class="absolute left-0 inset-y-0 flex items-center pl-3">
            <!-- HEMIS Icon -->
            <svg class="h-5 w-5 text-blue-500 group-hover:text-blue-400" fill="currentColor" viewBox="0 0 20 20">
              <path fill-rule="evenodd" d="M5 9V7a5 5 0 0110 0v2a2 2 0 012 2v5a2 2 0 01-2 2H5a2 2 0 01-2-2v-5a2 2 0 012-2zm8-2v2H7V7a3 3 0 016 0z" clip-rule="evenodd" />
            </svg>
          </span>
          HEMIS orqali kirish
        </a>
      </div>

      <!-- Development Login (faqat dev mode da) -->
      <div v-if="isDevelopment" class="mt-8">
        <div class="relative">
          <div class="absolute inset-0 flex items-center">
            <div class="w-full border-t border-gray-300"></div>
          </div>
          <div class="relative flex justify-center text-sm">
            <span class="px-2 bg-gray-50 text-gray-500">Yoki (development)</span>
          </div>
        </div>

        <form @submit.prevent="handleDevLogin" class="mt-6 space-y-4">
          <div>
            <label for="username" class="sr-only">Username</label>
            <input
              id="username"
              v-model="devForm.username"
              type="text"
              required
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Username"
            />
          </div>
          <div>
            <label for="password" class="sr-only">Password</label>
            <input
              id="password"
              v-model="devForm.password"
              type="password"
              required
              class="appearance-none rounded-md relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
              placeholder="Password"
            />
          </div>
          <button
            type="submit"
            :disabled="loading"
            class="w-full flex justify-center py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
          >
            {{ loading ? 'Kirish...' : 'Dev Login' }}
          </button>
        </form>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="mt-4 p-4 bg-red-50 border border-red-200 rounded-md">
        <p class="text-sm text-red-600">{{ error }}</p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'

const router = useRouter()

const loading = ref(false)
const error = ref('')
const devForm = ref({
  username: '',
  password: ''
})

const isDevelopment = computed(() => {
  return import.meta.env.DEV || import.meta.env.VITE_DEV_MODE === 'true'
})

const hemisLoginUrl = computed(() => {
  return authService.getHemisLoginUrl('/dashboard')
})

const handleDevLogin = async () => {
  loading.value = true
  error.value = ''

  try {
    await authService.devLogin(devForm.value.username, devForm.value.password)
    router.push('/dashboard')
  } catch (e) {
    error.value = e.response?.data?.error || 'Login failed'
  } finally {
    loading.value = false
  }
}
</script>
```

### 3. OAuth Callback View (`src/views/auth/OAuthCallback.vue`)

```vue
<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="text-center">
      <div v-if="loading" class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
      <p class="mt-4 text-gray-600">{{ message }}</p>
      
      <div v-if="error" class="mt-4">
        <p class="text-red-600">{{ error }}</p>
        <router-link to="/login" class="mt-4 inline-block text-blue-600 hover:text-blue-800">
          Qaytadan kirish
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import authService from '@/services/authService'

const router = useRouter()

const loading = ref(true)
const message = ref('Avtorizatsiya tekshirilmoqda...')
const error = ref('')

onMounted(() => {
  const result = authService.handleOAuthCallback()

  if (result.success) {
    message.value = 'Muvaffaqiyatli! Yo\'naltirilmoqda...'
    setTimeout(() => {
      router.push(result.next)
    }, 500)
  } else {
    loading.value = false
    error.value = result.error || 'Avtorizatsiya xatosi'
  }
})
</script>
```

### 4. Router (`src/router/index.js`)

```javascript
import { createRouter, createWebHistory } from 'vue-router'
import authService from '@/services/authService'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/auth/LoginView.vue'),
    meta: { guest: true }
  },
  {
    path: '/auth/callback',
    name: 'OAuthCallback',
    component: () => import('@/views/auth/OAuthCallback.vue'),
    meta: { guest: true }
  },
  {
    path: '/auth/error',
    name: 'AuthError',
    component: () => import('@/views/auth/AuthError.vue'),
    meta: { guest: true }
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: () => import('@/views/DashboardView.vue'),
    meta: { requiresAuth: true }
  },
  // ... boshqa routes
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const isAuthenticated = authService.isAuthenticated()

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login')
  } else if (to.meta.guest && isAuthenticated) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
```

---

## 🔐 HEMIS User Fields

HEMIS OAuth userinfo endpoint qaytaradigan maydonlar:

| Field | Tavsif | Misol |
|-------|--------|-------|
| `id` | HEMIS ID | `"12345"` |
| `uuid` | Unique identifier | `"550e8400-e29b-41d4-a716-446655440000"` |
| `type` | Foydalanuvchi turi | `"employee"` yoki `"student"` |
| `name` | To'liq ism | `"Ism Familiya Otasining ismi"` |
| `firstname` | Ism | `"Ism"` |
| `surname` | Familiya | `"Familiya"` |
| `patronymic` | Otasining ismi | `"Otasining ismi"` |
| `login` | Username | `"username123"` |
| `picture` | Profil rasmi URL | `"https://hemis.uz/avatar/123.jpg"` |
| `email` | Email manzil | `"user@example.com"` |
| `university_id` | Universitet ID | `"789"` |
| `phone` | Telefon raqami | `"+998901234567"` |
| `birth_date` | Tug'ilgan sana | `"1990-01-01"` |

---

## 🧪 Test qilish

### 1. Development mode da test

```bash
# Backend ishga tushirish
cd backend
python manage.py runserver

# Frontend ishga tushirish (boshqa terminalda)
cd frontend
npm run dev
```

### 2. Test foydalanuvchilari yaratish

```bash
python manage.py shell -c "
from apps.accounts.models import User

# Admin yaratish
User.objects.create_superuser(
    'admin', 
    'admin@test.com', 
    'admin123',
    role='superadmin',
    first_name='Super',
    last_name='Admin'
)

# Teacher yaratish
User.objects.create_user(
    'teacher',
    'teacher@test.com',
    'teacher123',
    role='teacher',
    first_name='Test',
    last_name='Teacher'
)

print('Test users created!')
"
```

### 3. API test (curl)

```bash
# Dev login
curl -X POST http://localhost:8000/auth/dev-login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "admin123"}'

# Response:
# {"access": "eyJ...", "refresh": "eyJ...", "user": {...}}
```

---

## 🚀 Production Deployment

### 1. Environment variables

```env
# Production .env
DEBUG=False
SECRET_KEY=your-very-secret-key

# HEMIS OAuth
HEMIS_CLIENT_ID=your-client-id
HEMIS_CLIENT_SECRET=your-client-secret
HEMIS_REDIRECT_URI=https://your-domain.com/auth/hemis/callback/
HEMIS_AUTHORIZATION_URL=https://univer.hemis.uz/oauth/authorize
HEMIS_TOKEN_URL=https://univer.hemis.uz/oauth/access-token
HEMIS_USERINFO_URL=https://univer.hemis.uz/oauth/api/user

# Frontend
FRONTEND_URL=https://your-domain.com
```

### 2. CORS sozlamalari

```python
# settings.py
CORS_ALLOWED_ORIGINS = [
    "https://your-domain.com",
]

CSRF_TRUSTED_ORIGINS = [
    "https://your-domain.com",
]
```

---

## 📞 Yordam

Muammolar uchun:
- HEMIS texnik yordam: support@hemis.uz
- GitHub Issues: https://github.com/xurshidbekxasanboyev1990/proft/issues

---

## 📝 PHP vs Python/Django Taqqoslash

| PHP (League OAuth2) | Python/Django |
|---------------------|---------------|
| `$provider = new GenericProvider([...])` | `client = HemisOAuth2Client()` |
| `$provider->getAuthorizationUrl()` | `client.get_authorization_url()` |
| `$_SESSION['oauth2state']` | `request.session['hemis_oauth_state']` |
| `$provider->getAccessToken('authorization_code', [...])` | `client.exchange_code_for_token(code)` |
| `$provider->getResourceOwner($accessToken)` | `client.get_user_info(access_token)` |
| `$resourceOwner->toArray()` | `user_info` (dict) |
