# Funded Bangladesh - Backend API

Django REST API for the Funded Bangladesh crowdfunding platform.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- PostgreSQL 14+
- Redis 7+

### Installation

1. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. **Install dependencies**
```bash
cd backend
pip install -r requirements/dev.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. **Run database migrations**
```bash
python manage.py migrate
```

5. **Create superuser**
```bash
python manage.py createsuperuser
```

6. **Run development server**
```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`

### Using Makefile

```bash
# Install dependencies
make install

# Run migrations
make migrate

# Run development server
make run

# Run Celery worker
make celery

# Run tests
make test

# Format code
make format
```

## 📁 Project Structure

```
backend/
├── apps/
│   ├── accounts/       # User authentication & profiles
│   ├── campaigns/      # Campaign management
│   ├── donations/      # Donations & transactions
│   ├── withdrawals/    # Payout management
│   ├── badges/         # Gamification
│   └── core/           # Common utilities
├── config/
│   ├── settings/       # Settings (base, dev, prod)
│   ├── urls.py
│   ├── wsgi.py
│   ├── asgi.py
│   └── celery.py
├── requirements/
│   ├── base.txt
│   ├── dev.txt
│   └── prod.txt
└── manage.py
```

## 🔧 Configuration

### Environment Variables

See `.env.example` for all available configuration options.

Key variables:
- `DJANGO_SETTINGS_MODULE`: Settings module to use (default: `config.settings.dev`)
- `DATABASE_URL`: PostgreSQL connection string
- `REDIS_URL`: Redis connection string
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)

### Settings

- **Development**: `config.settings.dev`
- **Production**: `config.settings.prod`

## 📚 API Documentation

Once the server is running, visit:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`
- OpenAPI Schema: `http://localhost:8000/api/schema/`

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=apps

# Run specific app tests
pytest apps/accounts/tests/
```

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Endpoints:
- `POST /api/v1/accounts/register/` - Register new user
- `POST /api/v1/accounts/login/` - Login and get tokens
- `POST /api/v1/accounts/token/refresh/` - Refresh access token
- `POST /api/v1/accounts/logout/` - Logout (blacklist token)

### Usage:
Include the access token in the Authorization header:
```
Authorization: Bearer <access_token>
```

## 📦 Apps

### Accounts
- User registration and authentication
- User profiles
- Identity verification
- Presigned URL generation for S3 uploads

### Campaigns
- Campaign CRUD operations
- Campaign categories
- Campaign updates
- Comments
- Document and image management

### Donations
- Donation processing
- Payment gateway integration (bKash, Nagad)
- Transaction management
- Webhook handling

### Withdrawals
- Withdrawal requests
- Admin approval workflow
- Payout processing

### Badges
- Badge definitions
- User badge awards
- Gamification logic

## 🔄 Background Tasks (Celery)

Start Celery worker:
```bash
celery -A config worker -l info
```

Start Celery beat (for scheduled tasks):
```bash
celery -A config beat -l info
```

## 🗄️ Database

### Migrations

```bash
# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Show migrations
python manage.py showmigrations
```

### Models

All models use UUID as primary key for better security and scalability.

## 🚢 Deployment

### Production Checklist

1. Set `DEBUG=False`
2. Configure `ALLOWED_HOSTS`
3. Set strong `SECRET_KEY`
4. Configure production database
5. Set up S3 for media files
6. Configure email backend
7. Set up Sentry for error tracking
8. Use environment variables for all secrets
9. Run `python manage.py collectstatic`
10. Use gunicorn as WSGI server

### Running with Gunicorn

```bash
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 4
```

## 📝 Code Quality

```bash
# Format code
black apps/ config/
isort apps/ config/

# Lint code
flake8 apps/ config/
pylint apps/ config/

# Type checking
mypy apps/
```

## 🤝 Contributing

1. Follow Django best practices
2. Write tests for new features
3. Format code with black and isort
4. Update documentation
5. Create meaningful commit messages

## 📄 License

Proprietary - Funded Bangladesh

