# 🇧🇩 Funded Bangladesh - Crowdfunding Platform

A modern, full-stack crowdfunding platform built specifically for Bangladesh, featuring Django REST Framework backend and Next.js 14 frontend.

## 🎯 Project Overview

Funded Bangladesh is a comprehensive crowdfunding platform that enables:
- **Donors**: Browse campaigns, make donations (including anonymous), track contributions
- **Campaign Creators**: Submit campaigns, upload documents, track fundraising progress
- **Admins**: Review campaigns, verify users, monitor transactions, approve withdrawals

## 🏗️ Architecture

### Backend (Django)
- **Framework**: Django 5 + Django REST Framework
- **Database**: PostgreSQL with UUID primary keys
- **Cache/Sessions**: Redis
- **Background Jobs**: Celery
- **File Storage**: AWS S3 with presigned URLs
- **Authentication**: JWT (Simple JWT)
- **Payment Gateways**: bKash, Nagad

### Frontend (Next.js) - Coming Soon
- **Framework**: Next.js 14 with App Router
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **UI Components**: shadcn/ui
- **Forms**: react-hook-form + Zod validation
- **State Management**: React Context + Server Components

## 📁 Project Structure

```
funded/
├── backend/                    # Django REST API
│   ├── apps/
│   │   ├── accounts/          # Authentication & user management
│   │   ├── campaigns/         # Campaign CRUD & management
│   │   ├── donations/         # Donations & payment processing
│   │   ├── withdrawals/       # Payout management
│   │   ├── badges/            # Gamification system
│   │   └── core/              # Common utilities & base models
│   ├── config/
│   │   ├── settings/          # Split settings (base/dev/prod)
│   │   ├── urls.py
│   │   ├── celery.py
│   │   └── wsgi.py
│   ├── requirements/
│   │   ├── base.txt
│   │   ├── dev.txt
│   │   └── prod.txt
│   ├── Makefile
│   └── manage.py
├── frontend/                   # Next.js app (to be created)
├── docker-compose.yml
└── README.md
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+ (for frontend)
- PostgreSQL 14+
- Redis 7+
- Docker & Docker Compose (optional)

### Option 1: Using Docker (Recommended)

```bash
# Start all services
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# Access the API
# http://localhost:8000
```

### Option 2: Manual Setup

#### Backend Setup

```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements/dev.txt

# Copy environment file
cp .env.example .env
# Edit .env with your configuration

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

#### Start Redis & PostgreSQL

```bash
# Using Docker
docker run -d -p 5432:5432 -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=funded_db postgres:15-alpine
docker run -d -p 6379:6379 redis:7-alpine
```

#### Start Celery (in separate terminals)

```bash
# Worker
celery -A config worker -l info

# Beat scheduler
celery -A config beat -l info
```

## 📚 API Documentation

Once the backend is running:
- **Swagger UI**: http://localhost:8000/api/docs/
- **ReDoc**: http://localhost:8000/api/redoc/
- **Admin Panel**: http://localhost:8000/admin/

## 🔑 Key Features

### ✅ Implemented (Backend)

- [x] User authentication (JWT)
- [x] User registration & login
- [x] User profile management
- [x] Identity verification system
- [x] Campaign CRUD operations
- [x] Campaign categories
- [x] Campaign updates & comments
- [x] Donation processing
- [x] Payment gateway integration (structure)
- [x] Withdrawal requests
- [x] Badge/gamification system
- [x] Presigned S3 URL generation
- [x] Admin panel
- [x] API documentation

### 🚧 To Be Implemented

#### Backend
- [ ] Complete bKash integration
- [ ] Complete Nagad integration
- [ ] Email notifications
- [ ] SMS notifications
- [ ] Celery tasks for background jobs
- [ ] Advanced search & filtering
- [ ] Analytics & reporting
- [ ] Rate limiting
- [ ] Comprehensive test suite

#### Frontend
- [ ] Next.js project setup
- [ ] Authentication flow
- [ ] Campaign listing & details
- [ ] Campaign creation wizard
- [ ] Donation flow
- [ ] User dashboards (donor & creator)
- [ ] Admin dashboard
- [ ] Responsive design
- [ ] SEO optimization

## 🗄️ Database Schema

### Core Models

**User** (UUID PK)
- Email, full name, phone
- User type (donor/creator/both)
- Verification status
- Profile information

**Campaign** (UUID PK)
- Title, description, category
- Goal amount, current amount
- Timeline (start/end dates)
- Status (draft/pending/approved/active/completed)
- Creator (FK to User)

**Donation** (UUID PK)
- Donor (FK to User, nullable for anonymous)
- Campaign (FK to Campaign)
- Amount, platform fee, net amount
- Payment method, transaction ID
- Status

**Withdrawal** (UUID PK)
- Campaign (FK to Campaign)
- Creator (FK to User)
- Amount, payment details
- Status (pending/approved/completed)

## 🔐 Authentication

JWT-based authentication with access and refresh tokens.

### Endpoints
```
POST /api/v1/accounts/register/
POST /api/v1/accounts/login/
POST /api/v1/accounts/token/refresh/
POST /api/v1/accounts/logout/
GET  /api/v1/accounts/me/
```

### Usage
```bash
# Login
curl -X POST http://localhost:8000/api/v1/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{"email": "user@example.com", "password": "password"}'

# Use token
curl http://localhost:8000/api/v1/accounts/me/ \
  -H "Authorization: Bearer <access_token>"
```

## 💳 Payment Integration

### Supported Gateways
- **bKash**: Mobile financial service
- **Nagad**: Digital financial service

### Flow
1. User initiates donation
2. Backend creates donation record
3. Payment gateway URL generated
4. User completes payment
5. Webhook updates donation status
6. Campaign amount updated

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Run specific app
pytest apps/accounts/tests/
```

## 📦 Deployment

### Environment Variables

Key variables to set in production:
- `SECRET_KEY`: Strong secret key
- `DEBUG`: False
- `ALLOWED_HOSTS`: Your domain
- `DATABASE_URL`: Production database
- `REDIS_URL`: Production Redis
- `AWS_*`: S3 credentials
- `BKASH_*`: bKash credentials
- `NAGAD_*`: Nagad credentials
- `SENTRY_DSN`: Error tracking

### Production Checklist
- [ ] Set DEBUG=False
- [ ] Configure ALLOWED_HOSTS
- [ ] Use strong SECRET_KEY
- [ ] Set up production database
- [ ] Configure S3 for media files
- [ ] Set up email backend
- [ ] Configure Sentry
- [ ] Use environment variables
- [ ] Run collectstatic
- [ ] Use gunicorn/uwsgi
- [ ] Set up HTTPS
- [ ] Configure CORS properly

## 🤝 Development Workflow

1. Create feature branch
2. Implement feature with tests
3. Format code: `make format`
4. Run tests: `make test`
5. Create pull request
6. Code review
7. Merge to main

## 📝 Code Style

- **Python**: Black + isort + flake8
- **Line length**: 120 characters
- **Docstrings**: Google style
- **Type hints**: Encouraged

## 🛠️ Useful Commands

```bash
# Backend
make install          # Install dependencies
make migrate          # Run migrations
make run              # Start dev server
make celery           # Start Celery worker
make test             # Run tests
make format           # Format code
make shell            # Django shell

# Docker
docker-compose up -d              # Start all services
docker-compose logs -f backend    # View backend logs
docker-compose exec backend bash  # Access backend container
docker-compose down               # Stop all services
```

## 📖 Documentation

- [Backend README](backend/README.md)
- [API Documentation](http://localhost:8000/api/docs/)
- Frontend README (coming soon)

## 🐛 Troubleshooting

### Database connection error
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check DATABASE_URL in .env
```

### Redis connection error
```bash
# Check Redis is running
docker ps | grep redis

# Test connection
redis-cli ping
```

### Migration errors
```bash
# Reset migrations (development only!)
python manage.py migrate --fake-initial
```

## 📄 License

Proprietary - Funded Bangladesh

## 👥 Team

- Backend: Django REST Framework
- Frontend: Next.js 14
- Database: PostgreSQL
- Cache: Redis
- Queue: Celery

---

**Status**: 🟢 Backend Complete | 🟡 Frontend Pending

For questions or issues, please contact the development team.

