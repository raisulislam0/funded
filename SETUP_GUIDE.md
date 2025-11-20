# 🚀 Setup Guide - Funded Bangladesh

Complete step-by-step guide to set up the development environment.

## 📋 Prerequisites Checklist

Before starting, ensure you have:
- [ ] Python 3.11 or higher installed
- [ ] PostgreSQL 14+ installed (or Docker)
- [ ] Redis 7+ installed (or Docker)
- [ ] Git installed
- [ ] Code editor (VS Code recommended)

## 🔧 Step 1: Clone and Setup Backend

### 1.1 Navigate to Backend Directory
```bash
cd backend
```

### 1.2 Create Virtual Environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 1.3 Install Dependencies
```bash
pip install -r requirements/dev.txt
```

## 🗄️ Step 2: Database Setup

### Option A: Using Docker (Recommended)
```bash
# Start PostgreSQL
docker run -d \
  --name funded_postgres \
  -e POSTGRES_DB=funded_db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -p 5432:5432 \
  postgres:15-alpine

# Start Redis
docker run -d \
  --name funded_redis \
  -p 6379:6379 \
  redis:7-alpine
```

### Option B: Local Installation
Install PostgreSQL and Redis locally and create database:
```sql
CREATE DATABASE funded_db;
CREATE USER postgres WITH PASSWORD 'postgres';
GRANT ALL PRIVILEGES ON DATABASE funded_db TO postgres;
```

## ⚙️ Step 3: Environment Configuration

### 3.1 Copy Environment File
```bash
cp .env.example .env
```

### 3.2 Edit .env File
Open `.env` and configure:

**Required Settings:**
```env
DJANGO_SETTINGS_MODULE=config.settings.dev
SECRET_KEY=your-secret-key-here-change-this
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

DATABASE_URL=postgresql://postgres:postgres@localhost:5432/funded_db
REDIS_URL=redis://localhost:6379/0
CELERY_BROKER_URL=redis://localhost:6379/1
```

**Optional (for development):**
```env
USE_S3=False
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend
```

## 🔄 Step 4: Database Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Verify migrations
python manage.py showmigrations
```

Expected output: All migrations should have [X] marks.

## 👤 Step 5: Create Superuser

```bash
python manage.py createsuperuser
```

Enter:
- Email: admin@funded.bd
- Full name: Admin User
- Password: (choose a strong password)

## 🎯 Step 6: Load Initial Data (Optional)

### Create Categories
```bash
python manage.py shell
```

```python
from apps.campaigns.models import Category

categories = [
    {'name': 'Medical', 'slug': 'medical', 'description': 'Medical emergencies and treatments', 'icon': '🏥'},
    {'name': 'Education', 'slug': 'education', 'description': 'Educational support and scholarships', 'icon': '📚'},
    {'name': 'Emergency', 'slug': 'emergency', 'description': 'Emergency relief and disaster support', 'icon': '🚨'},
    {'name': 'Community', 'slug': 'community', 'description': 'Community development projects', 'icon': '🏘️'},
    {'name': 'Business', 'slug': 'business', 'description': 'Small business and entrepreneurship', 'icon': '💼'},
]

for cat in categories:
    Category.objects.get_or_create(**cat)

print("Categories created successfully!")
exit()
```

## 🚀 Step 7: Run Development Server

### Terminal 1: Django Server
```bash
python manage.py runserver
```

### Terminal 2: Celery Worker (Optional)
```bash
celery -A config worker -l info
```

### Terminal 3: Celery Beat (Optional)
```bash
celery -A config beat -l info
```

## ✅ Step 8: Verify Installation

### 8.1 Check API is Running
Open browser and visit:
- API Root: http://localhost:8000/
- Admin Panel: http://localhost:8000/admin/
- API Docs: http://localhost:8000/api/docs/

### 8.2 Login to Admin Panel
- URL: http://localhost:8000/admin/
- Email: admin@funded.bd
- Password: (your superuser password)

### 8.3 Test API Endpoints

**Register a User:**
```bash
curl -X POST http://localhost:8000/api/v1/accounts/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "full_name": "Test User",
    "phone": "+8801712345678",
    "user_type": "donor",
    "password": "testpass123",
    "password_confirm": "testpass123"
  }'
```

**Login:**
```bash
curl -X POST http://localhost:8000/api/v1/accounts/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "test@example.com",
    "password": "testpass123"
  }'
```

**Get Categories:**
```bash
curl http://localhost:8000/api/v1/campaigns/categories/
```

## 🐳 Alternative: Using Docker Compose

If you prefer to use Docker for everything:

```bash
# From project root
docker-compose up -d

# Run migrations
docker-compose exec backend python manage.py migrate

# Create superuser
docker-compose exec backend python manage.py createsuperuser

# View logs
docker-compose logs -f backend

# Stop services
docker-compose down
```

## 🧪 Step 9: Run Tests

```bash
# Install test dependencies (already in dev.txt)
pytest

# Run with coverage
pytest --cov=apps --cov-report=html

# Open coverage report
# Open htmlcov/index.html in browser
```

## 🛠️ Development Tools

### Using Makefile
```bash
make install          # Install dependencies
make migrate          # Run migrations
make run              # Start server
make celery           # Start Celery
make test             # Run tests
make format           # Format code
make lint             # Lint code
make shell            # Django shell
make superuser        # Create superuser
```

### Django Extensions
```bash
# Enhanced shell with auto-imports
python manage.py shell_plus

# Show URLs
python manage.py show_urls

# Generate ER diagram (requires graphviz)
python manage.py graph_models -a -o models.png
```

## 🔍 Troubleshooting

### Issue: "No module named 'apps'"
**Solution:** Make sure you're in the `backend` directory and virtual environment is activated.

### Issue: Database connection refused
**Solution:** 
```bash
# Check if PostgreSQL is running
docker ps | grep postgres

# Or check local PostgreSQL service
# Windows: services.msc -> PostgreSQL
# Linux: sudo systemctl status postgresql
```

### Issue: Redis connection error
**Solution:**
```bash
# Check if Redis is running
docker ps | grep redis

# Test Redis connection
redis-cli ping
# Should return: PONG
```

### Issue: Migration conflicts
**Solution:**
```bash
# Reset migrations (DEVELOPMENT ONLY!)
python manage.py migrate --fake-initial

# Or delete db and start fresh
dropdb funded_db
createdb funded_db
python manage.py migrate
```

### Issue: Port already in use
**Solution:**
```bash
# Find process using port 8000
# Windows
netstat -ano | findstr :8000

# Linux/Mac
lsof -i :8000

# Kill the process or use different port
python manage.py runserver 8001
```

## 📚 Next Steps

1. ✅ Backend is now running!
2. 📖 Read the [API Documentation](http://localhost:8000/api/docs/)
3. 🎨 Set up the Next.js frontend (coming soon)
4. 💳 Configure payment gateways (bKash, Nagad)
5. 📧 Set up email service
6. ☁️ Configure AWS S3 for file uploads

## 🎓 Learning Resources

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Celery Documentation](https://docs.celeryproject.org/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)

## 💡 Tips

1. **Use Django Debug Toolbar**: Already installed in dev mode, visit any page to see the toolbar
2. **API Documentation**: Use Swagger UI for interactive API testing
3. **Database GUI**: Use pgAdmin or DBeaver to visualize database
4. **Redis GUI**: Use RedisInsight to monitor Redis
5. **Code Formatting**: Run `make format` before committing

## ✨ You're All Set!

Your development environment is ready. Start building amazing features! 🚀

For questions or issues, refer to:
- [Main README](README.md)
- [Backend README](backend/README.md)
- API Documentation at http://localhost:8000/api/docs/

