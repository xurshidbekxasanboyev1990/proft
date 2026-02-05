# 📋 CHANGELOG - O'zgarishlar Tarixi

> Portfolio Management System uchun barcha o'zgarishlar tarixi

---

## [2026-02-04] - Swagger/OpenAPI + Ball Tizimi (Scoring System)

**Commit:** `pending` - feat: Add Swagger/OpenAPI docs and dynamic scoring system

### ✨ Yangi Funksiyalar

#### 📚 Swagger/OpenAPI Documentation
- **drf-spectacular** integratsiyasi
- Interactive API documentation
- Schema download (JSON/YAML)
- ReDoc alternative view

#### 🎯 Ball (Score) Tizimi

##### Kategoriya uchun standart ball
- `default_score` - standart maksimal ball (masalan: esse=10)
- `min_score` - minimal qabul qilinadigan ball
- `score_weight` - kategoriya vazni (1.0 default)

##### Topshiriq uchun maxsus ball
- `use_custom_score` - maxsus ball ishlatish
- `custom_max_score` - maxsus maksimal ball (admin o'zgartirishi mumkin, masalan: esse=20)
- `custom_min_score` - maxsus minimal ball
- `score_multiplier` - ball ko'paytiruvchi (2x bonus uchun)
- `score_note` - ball haqida izoh

##### Ball hisoblash
```
final_score = raw_score × category.score_weight × assignment.score_multiplier
```

##### Progress baholash
- `raw_score` - xom ball (baholovchi kiradi)
- `final_score` - hisoblangan yakuniy ball
- `grade_note` - baholash izohi
- `graded_by` / `graded_at` - kim va qachon baholadi

##### Ball tarixi (ScoreHistory)
- Barcha ball o'zgarishlarini kuzatish
- Kim, qachon, nima o'zgartirdi

### 📡 API Endpoints

#### Swagger URLs
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/docs/` | Swagger UI |
| GET | `/api/docs/schema/` | OpenAPI schema (JSON) |
| GET | `/api/docs/schema/?format=yaml` | OpenAPI schema (YAML) |
| GET | `/api/docs/redoc/` | ReDoc documentation |

#### Ball Tizimi APIs
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET/PUT | `/api/assignments/{id}/score/` | Topshiriq ball sozlamalarini olish/yangilash |
| GET | `/api/assignments/{id}/score-history/` | Topshiriq ball tarixi |
| PUT | `/api/assignments/progress/{id}/grade/` | Progress baholash |
| GET | `/api/assignments/score-history/` | Barcha ball tarixi |
| POST | `/api/assignments/bulk-score-update/` | Bulk ball yangilash |
| PUT | `/api/assignments/categories/{id}/score/` | Kategoriya ball sozlamalarini yangilash |

#### Ball Tizimi Request Examples

**Topshiriq uchun maxsus ball sozlash:**
```json
PUT /api/assignments/123/score/
{
  "use_custom_score": true,
  "custom_max_score": 20,      // esse 10 emas, 20 ball
  "score_multiplier": 1.5,     // 1.5x bonus
  "score_note": "A'lo ish uchun qo'shimcha ball"
}
```

**Progress baholash:**
```json
PUT /api/assignments/progress/456/grade/
{
  "raw_score": 18,
  "grade_note": "Juda yaxshi bajarilgan"
}
```
Response: `{ "raw_score": 18, "final_score": 27.0 }` (18 × 1.5)

**Bulk ball yangilash:**
```json
POST /api/assignments/bulk-score-update/
{
  "assignment_ids": ["uuid1", "uuid2", "uuid3"],
  "custom_max_score": 25,
  "score_multiplier": 2.0,
  "score_note": "2x bonus barcha uchun"
}
```

### 📁 Yangi/O'zgartirilgan Fayllar

#### Yangi
```
backend/apps/swagger/
├── __init__.py
├── apps.py           # SwaggerConfig
├── urls.py           # Swagger URLs
├── extensions.py     # Custom auth schemes
└── hooks.py          # Schema pre/post processing
```

#### O'zgartirilgan
```
backend/apps/assignments/
├── models.py         # Category, Assignment, AssignmentProgress, ScoreHistory (yangi)
├── admin.py          # Ball tizimi admin
├── serializers.py    # Ball tizimi serializers
├── views.py          # Ball tizimi views
└── urls.py           # Ball tizimi URLs

backend/config/
├── settings.py       # SPECTACULAR_SETTINGS
└── urls.py           # Swagger URLs

backend/requirements.txt  # drf-spectacular
```

### 📦 Yangi Dependencies
```
drf-spectacular>=0.27.0        # OpenAPI 3.0 schema generator
drf-spectacular-sidecar>=2024.1.1  # Swagger UI assets
```

### 🔧 Admin Panel

#### CategoryAdmin
- `score_display` - standart ball ko'rsatish
- `weight_display` - vazn ko'rsatish
- Ball sozlamalari fieldset

#### AssignmentAdmin
- `score_info_display` - ball info
- Maxsus ball fieldset
- Bulk actions: "2x bonus", "Reset to default"

#### AssignmentProgressAdmin
- `score_display` - ball va foiz
- Baholash fieldset

#### ScoreHistoryAdmin
- Read-only tarix

---

## [2026-02-04] - Analytics & Reports App qo'shildi

**Commit:** `545064e` - feat: Add analytics app with dashboard, reports, and export

### ✨ Yangi Funksiyalar

#### 📊 Dashboard Overview
- Umumiy statistika (foydalanuvchilar, portfoliolar, topshiriqlar)
- Real-time ma'lumotlar (5 daqiqada yangilanadi)
- Role-based widgetlar
- Chart.js uchun ma'lumotlar

#### 📈 Analytics APIs
- Portfolio analytics (status distribution, monthly trend, top teachers)
- Assignment analytics (by category, by status, grade distribution)
- Teacher performance (performance score, rankings)

#### 📁 Export Funksiyalari
- **Excel** - openpyxl bilan professional formatda
- **PDF** - reportlab bilan chiroyli hisobotlar
- **CSV** - oddiy jadval formatda
- **JSON** - API uchun

#### 📋 Report Generation
- Async report generation (Celery bilan)
- Automatic monthly/yearly reports
- Report history and download

#### ⏰ Scheduled Tasks
- Dashboard cache refresh (5 daqiqada)
- Expired cache cleanup (kunlik)
- Old reports cleanup (haftalik)
- Monthly/Yearly auto-reports

### 📡 API Endpoints

#### Dashboard APIs
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/analytics/dashboard/overview/` | Umumiy statistika |
| GET | `/api/analytics/dashboard/widgets/` | Dashboard widgetlar |

#### Chart APIs
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/analytics/charts/portfolio_trend/` | Portfolio trend grafigi |
| GET | `/api/analytics/charts/assignment_status/` | Topshiriq status pie chart |
| GET | `/api/analytics/charts/category_distribution/` | Kategoriya distribution |

**Query params:** `?period=week|month|year`

#### Analytics APIs
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/analytics/portfolios/` | Portfolio analytics |
| GET | `/api/analytics/assignments/` | Assignment analytics |
| GET | `/api/analytics/teachers/` | Barcha o'qituvchilar performance |
| GET | `/api/analytics/teachers/{id}/` | Bitta o'qituvchi performance |

**Query params:** `?date_from=YYYY-MM-DD&date_to=YYYY-MM-DD`

#### Report APIs
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/analytics/reports/` | Hisobotlar ro'yxati |
| POST | `/api/analytics/reports/` | Yangi hisobot yaratish |
| GET | `/api/analytics/reports/{id}/` | Hisobot tafsilotlari |
| DELETE | `/api/analytics/reports/{id}/` | Hisobotni o'chirish |
| GET | `/api/analytics/reports/{id}/download/` | Hisobotni yuklab olish |

#### Export API
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| POST | `/api/analytics/export/` | Tezkor export (fayl saqlamaydi) |

**Request body:**
```json
{
  "type": "overview|portfolios|assignments|teachers",
  "format": "excel|pdf|csv|json",
  "date_from": "2026-01-01",
  "date_to": "2026-01-31"
}
```

#### Cache Management (SuperAdmin)
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| DELETE | `/api/analytics/cache/` | Keshni tozalash |

**Query params:** `?pattern=dashboard` - faqat dashboard keshini tozalash

### 📁 Yangi Fayllar
```
backend/apps/analytics/
├── __init__.py
├── admin.py          # Admin panel (Report, Widget, Cache)
├── apps.py           # App config
├── exporters.py      # CSV, Excel, PDF, JSON exporters
├── models.py         # Report, DashboardWidget, AnalyticsCache
├── services.py       # AnalyticsService - business logic
├── tasks.py          # Celery tasks (reports, cache, cleanup)
├── urls.py           # URL patterns
└── views.py          # API views
```

### 📦 Yangi Dependencies
```
openpyxl>=3.1.2       # Excel export
reportlab>=4.0.7      # PDF export
xlsxwriter>=3.1.9     # Advanced Excel
```

---

## [2026-02-04] - Assignments App qo'shildi

**Commit:** `a3c6616` - feat: Add assignments app with categories and task management

### ✨ Yangi Funksiyalar

#### 📁 Kategoriyalar (Categories)
Admin va SuperAdmin dinamik kategoriyalar yaratishi mumkin:
- Tezis
- Esse  
- Ilmiy maqola
- Loyiha
- Hisobot
- Boshqalar...

#### 📋 Topshiriqlar (Assignments)
- O'qituvchilarga topshiriq berish
- Deadline (muddat) belgilash
- Countdown - qolgan vaqtni hisoblash
- Progress - bajarilish foizi
- Priority - low, medium, high

#### 📤 Javoblar (Submissions)
- O'qituvchi topshiriqga javob yuborish
- Fayl biriktirish
- Admin baholash (0-100)

#### 🔔 Bildirishnomalar
- Yangi topshiriq - email
- Muddat yaqinlashganda (24 soat) - email
- Baholanganda - email

#### ⏰ Celery Tasks
- Har soatda deadline reminder
- Har 30 daqiqada overdue status yangilash

### 🔧 Texnik O'zgarishlar
- Django REST Framework qo'shildi
- django-filter qo'shildi
- Celery Beat schedule sozlandi
- TIME_ZONE: `Asia/Tashkent`

### 📡 API Endpoints

#### Categories API
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/assignments/v2/categories/` | Barcha kategoriyalar |
| POST | `/api/assignments/v2/categories/` | Yangi kategoriya (Admin) |
| GET | `/api/assignments/v2/categories/{id}/` | Bitta kategoriya |
| PUT | `/api/assignments/v2/categories/{id}/` | Kategoriya tahrirlash |
| DELETE | `/api/assignments/v2/categories/{id}/` | Kategoriya o'chirish |
| GET | `/api/assignments/v2/categories/{id}/assignments/` | Kategoriya topshiriqlari |

#### Assignments API
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/assignments/v2/assignments/` | Barcha topshiriqlar |
| POST | `/api/assignments/v2/assignments/` | Yangi topshiriq (Admin) |
| GET | `/api/assignments/v2/assignments/{id}/` | Bitta topshiriq |
| PUT | `/api/assignments/v2/assignments/{id}/` | Topshiriq tahrirlash |
| DELETE | `/api/assignments/v2/assignments/{id}/` | Topshiriq o'chirish |
| PATCH | `/api/assignments/v2/assignments/{id}/update_status/` | Status yangilash |
| GET | `/api/assignments/v2/assignments/statistics/` | Statistika |
| GET | `/api/assignments/v2/assignments/my_assignments/` | Mening topshiriqlarim |
| POST | `/api/assignments/v2/assignments/{id}/submit/` | Javob yuborish |

#### Submissions API
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/assignments/v2/submissions/` | Barcha javoblar |
| POST | `/api/assignments/v2/submissions/` | Yangi javob |
| GET | `/api/assignments/v2/submissions/{id}/` | Bitta javob |
| PATCH | `/api/assignments/v2/submissions/{id}/grade/` | Baholash (Admin) |

#### Query Parameters
```
# Filterlash
?status=pending|in_progress|completed|overdue|cancelled
?priority=low|medium|high
?category={category_id}
?assigned_to={user_id}

# Maxsus filterlar
?overdue=true          # Muddati o'tganlar
?upcoming=true         # 7 kun ichida muddati tugaydiganlar

# Qidiruv
?search=keyword

# Tartiblash
?ordering=deadline|-deadline|created_at|-created_at|priority
```

### 📁 Yangi Fayllar
```
backend/apps/assignments/
├── __init__.py
├── admin.py          # Admin panel konfiguratsiyasi
├── api_views.py      # DRF ViewSets
├── apps.py           # App config
├── models.py         # Category, Assignment, Submission
├── serializers.py    # DRF Serializers
├── signals.py        # Email notifications
├── tasks.py          # Celery tasks
├── urls.py           # URL patterns
└── views.py          # Legacy views
```

### 📝 O'zgartirilgan Fayllar
- `backend/config/settings.py` - DRF, django-filter, assignments app
- `backend/config/urls.py` - assignments URLs
- `backend/config/celery.py` - Beat schedule
- `backend/requirements.txt` - djangorestframework, django-filter
- `backend/apps/accounts/permissions.py` - DRF permission classes

---

## [2026-02-04] - Initial Release

**Commit:** `6edf040` - Initial commit with full backend

### ✨ Asosiy Funksiyalar
- Django 4.2+ project structure
- Docker + Docker Compose
- PostgreSQL 15 database
- Redis 7 caching
- Hemis OAuth 2.0 authentication
- User roles: SuperAdmin, Admin, Teacher
- Portfolio management with approval workflow
- Session-based authentication

### 📡 Core API Endpoints

#### Authentication
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/auth/hemis/login/` | Hemis OAuth login |
| GET | `/auth/hemis/callback/` | OAuth callback |
| POST | `/auth/hemis/logout/` | Logout |
| GET | `/auth/hemis/me/` | Current user info |

#### Accounts
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/accounts/profile/` | User profile |
| PUT | `/api/accounts/profile/` | Update profile |
| GET | `/api/accounts/users/` | Users list (Admin) |
| GET | `/api/accounts/users/{id}/` | User detail |

#### Portfolios
| Method | Endpoint | Tavsif |
|--------|----------|--------|
| GET | `/api/portfolios/` | Portfolios list |
| POST | `/api/portfolios/` | Create portfolio |
| GET | `/api/portfolios/{id}/` | Portfolio detail |
| PUT | `/api/portfolios/{id}/` | Update portfolio |
| DELETE | `/api/portfolios/{id}/` | Delete portfolio |
| POST | `/api/portfolios/{id}/approve/` | Approve (Admin) |
| POST | `/api/portfolios/{id}/reject/` | Reject (Admin) |

---

## 📌 Kelgusi Rejalar

- [ ] Portfolio fayl yuklash optimization
- [ ] Real-time notifications (WebSocket)
- [ ] Export to PDF/Excel
- [ ] Advanced analytics dashboard
- [ ] Mobile API optimization

---

> 📅 Oxirgi yangilanish: 2026-02-04
