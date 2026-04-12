# ⚙️ Configuration & Environment Management

## 📋 Overview
Complete configuration strategy for multi-environment deployment.

---

## 📁 Configuration Structure

```
src/
├── config/
│   ├── __init__.py
│   ├── settings.py           (Main config)
│   ├── database.py           (DB config)
│   ├── cache.py              (Redis config)
│   ├── security.py           (JWT, passwords)
│   ├── notifications.py      (WhatsApp, Email)
│   ├── storage.py            (S3, Cloudinary)
│   └── features.py           (Feature flags)
│
└── .env                       (Environment variables)
```

---

## 🔑 Environment Variables

### .env.example
```bash
# Application
ENVIRONMENT=development
ENVIRONMENT_NAME=Development
APP_NAME=RealEstate CRM
APP_VERSION=1.0.0
DEBUG_MODE=true

# Database
DATABASE_URL=postgresql://user:password@localhost:5432/realestate
DATABASE_POOL_SIZE=20
DATABASE_MAX_OVERFLOW=10
DATABASE_ECHO_QUERIES=false

# Cache
REDIS_URL=redis://localhost:6379
REDIS_DB=0
CACHE_TTL_SECONDS=3600

# JWT
JWT_SECRET_KEY=your-secret-key-here-change-in-production
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_HOURS=1
JWT_REFRESH_TOKEN_EXPIRE_DAYS=7

# Security
CORS_ORIGINS=http://localhost:3000,https://app.example.com
CSRF_ENABLED=true
RATE_LIMIT_ENABLED=true
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD_SECONDS=60

# WhatsApp
WHATSAPP_API_URL=https://graph.instagram.com/v18.0
WHATSAPP_PHONE_NUMBER_ID=your-phone-number-id
WHATSAPP_ACCESS_TOKEN=your-access-token
WHATSAPP_BUSINESS_ACCOUNT_ID=your-business-account-id
WHATSAPP_ENABLED=true

# Email
EMAIL_SENDER_NAME=RealEstate CRM
EMAIL_SENDER_ADDRESS=noreply@realestatecr.com
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password
EMAIL_ENABLED=true

# Storage
STORAGE_TYPE=cloudinary  # cloudinary or s3
CLOUDINARY_CLOUD_NAME=your-cloud-name
CLOUDINARY_API_KEY=your-api-key
CLOUDINARY_API_SECRET=your-api-secret

# External Services
SENTRY_DSN=https://your-sentry-dsn
SENTRY_ENABLED=false

# Feature Flags
ENABLE_WHATSAPP=true
ENABLE_EMAIL=true
ENABLE_SMS=false
ENABLE_STRIPE=false
ENABLE_ANALYTICS=true
ENABLE_CRON_JOBS=true

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# API Keys (if needed)
GOOGLE_API_KEY=your-google-key
STRIPE_API_KEY=your-stripe-key
```

---

## 📝 Configuration Classes

### Main Settings
```python
# config/settings.py

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Application
    environment: str = \"development\"
    app_name: str = \"RealEstate CRM\"
    debug: bool = False
    
    # Database
    database_url: str
    database_pool_size: int = 20
    database_max_overflow: int = 10
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = \"HS256\"
    jwt_access_token_expire_hours: int = 1
    jwt_refresh_token_expire_days: int = 7
    
    # WhatsApp
    whatsapp_api_url: str
    whatsapp_phone_number_id: str
    whatsapp_access_token: str
    whatsapp_enabled: bool = True
    
    # Email
    email_sender_name: str = \"RealEstate CRM\"
    email_sender_address: str
    smtp_host: str
    smtp_port: int = 587
    email_enabled: bool = True
    
    # Storage
    storage_type: str = \"cloudinary\"
    cloudinary_cloud_name: Optional[str] = None
    
    # Feature Flags
    enable_whatsapp: bool = True
    enable_email: bool = True
    enable_sms: bool = False
    enable_cron_jobs: bool = True
    
    # Logging
    log_level: str = \"INFO\"
    
    class Config:
        env_file = \".env\"
        case_sensitive = False

settings = Settings()
```

### Database Configuration
```python
# config/database.py

from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool, QueuePool

def get_database_engine(settings):
    if settings.environment == \"testing\":
        # Use NullPool for tests
        poolclass = NullPool
    else:
        # Use QueuePool for production
        poolclass = QueuePool
    
    engine = create_engine(
        settings.database_url,
        poolclass=poolclass,
        pool_size=settings.database_pool_size,
        max_overflow=settings.database_max_overflow,
        echo=settings.debug,
        echo_pool=settings.debug
    )
    
    return engine
```

### Security Configuration
```python
# config/security.py

from passlib.context import CryptContext
from datetime import timedelta

pwd_context = CryptContext(schemes=[\"bcrypt\"], deprecated=\"auto\")

class SecurityConfig:
    ALGORITHM = \"HS256\"
    ACCESS_TOKEN_EXPIRE = timedelta(hours=1)
    REFRESH_TOKEN_EXPIRE = timedelta(days=7)
    
    # Password requirements
    PASSWORD_MIN_LENGTH = 8
    PASSWORD_REQUIRE_UPPERCASE = True
    PASSWORD_REQUIRE_LOWERCASE = True
    PASSWORD_REQUIRE_DIGIT = True
    PASSWORD_REQUIRE_SPECIAL = True
```

---

## 🌍 Environment-Specific Configs

### Development
```bash
# .env.development
ENVIRONMENT=development
DEBUG_MODE=true
LOG_LEVEL=DEBUG
DATABASE_URL=postgresql://dev_user:dev_pass@localhost:5432/realestate_dev
WHATSAPP_ENABLED=false
EMAIL_ENABLED=false
ENABLE_STRIPE=false
SENTRY_ENABLED=false
```

### Staging
```bash
# .env.staging
ENVIRONMENT=staging
DEBUG_MODE=false
LOG_LEVEL=INFO
DATABASE_URL=postgresql://stage_user:${DB_PASSWORD}@staging-db:5432/realestate_staging
WHATSAPP_ENABLED=true
EMAIL_ENABLED=true
ENABLE_STRIPE=true
SENTRY_ENABLED=true
```

### Production
```bash
# .env.production
ENVIRONMENT=production
DEBUG_MODE=false
LOG_LEVEL=WARN
DATABASE_URL=postgresql://${DB_USER}:${DB_PASSWORD}@prod-db-primary:5432/realestate
WHATSAPP_ENABLED=true
EMAIL_ENABLED=true
ENABLE_STRIPE=true
SENTRY_ENABLED=true
ENABLE_CRON_JOBS=true
RATE_LIMIT_ENABLED=true
```

---

## 🚀 Application Startup

### App Initialization
```python
# main.py

from fastapi import FastAPI
from contextlib import asynccontextmanager
from config.settings import settings
from config.database import get_database_engine
from jobs.scheduler import scheduler

# Initialize database
engine = get_database_engine(settings)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    print(f\"Starting app in {settings.environment} mode\")
    print(f\"Debug mode: {settings.debug}\")
    print(f\"Log level: {settings.log_level}\")
    
    # Start background jobs scheduler
    if settings.enable_cron_jobs:
        scheduler.start()
    
    yield
    
    # Shutdown
    if settings.enable_cron_jobs:
        scheduler.shutdown()
    
    print(\"App shutdown complete\")

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    lifespan=lifespan
)

# Include routers
app.include_router(auth_routes)
app.include_router(tenant_routes)
# ... more routers

@app.get(\"/health\")
async def health_check():
    return {
        \"status\": \"healthy\",
        \"environment\": settings.environment,
        \"version\": settings.app_version
    }
```

---

## ✅ Configuration Checklist

- [ ] .env.example created with all variables
- [ ] Settings class configured
- [ ] Database settings configured
- [ ] Security settings configured
- [ ] Notification settings configured
- [ ] Storage settings configured
- [ ] Feature flags configured
- [ ] Environment files created (.dev, .staging, .prod)
- [ ] Secrets manager integration (if applicable)
- [ ] Configuration validation
- [ ] Startup checks
- [ ] Logging configuration
- [ ] Health check endpoint
