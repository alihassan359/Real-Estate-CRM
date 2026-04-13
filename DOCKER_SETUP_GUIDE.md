# 🐳 Docker Setup Guide - Authentication System with Google OAuth

> **For**: Real Estate CRM with Multi-Tenant Authentication  
> **Status**: Complete Docker implementation guide

---

## 📋 Prerequisites

- Docker installed (20.10+)
- Docker Compose installed (2.0+)
- PostgreSQL running in Docker
- Redis running in Docker
- Google OAuth credentials (see setup below)

---

## 🔑 Step 1: Get Google OAuth Credentials

### **1. Create Google Cloud Project**

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project
3. Enable Google+ API:
   - Search for "Google+ API"
   - Click "Enable"

### **2. Create OAuth 2.0 Credentials**

1. Go to **Credentials** menu
2. Click **Create Credentials** → **OAuth 2.0 Client ID**
3. Choose **Web Application**
4. Add Authorized redirect URIs:
   ```
   http://localhost:8000/api/auth/google/callback
   http://localhost:3000/auth/google/callback
   http://api.yourdomain.com/api/auth/google/callback
   ```
5. Click Create
6. Copy: **Client ID** and **Client Secret**

### **3. Store Credentials Safely**
```
Client ID:     your-client-id.apps.googleusercontent.com
Client Secret: your-client-secret
```

---

## 🐳 Step 2: Update Docker Configuration

### **Update `.env` file**

Create or update `.env` in project root:

```env
# ============= EXISTING CONFIGURATION =============

# Application
ENVIRONMENT=development
DEBUG=true
PROJECT_NAME=Real Estate CRM API

# Server
HOST=0.0.0.0
PORT=8000

# Database
DB_USER=postgres
DB_PASSWORD=realestatecrm
DB_NAME=realestate_crm
DATABASE_URL=postgresql://postgres:realestatecrm@postgres:5432/realestate_crm

# Redis
REDIS_URL=redis://redis:6379

# ============= NEW: JWT CONFIGURATION =============

JWT_SECRET_KEY=your-super-secret-jwt-key-minimum-32-characters-change-in-production
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=1
JWT_REFRESH_EXPIRATION_DAYS=7

# ============= NEW: GOOGLE OAUTH CONFIGURATION =============

GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# ============= OPTIONAL: EMAIL CONFIGURATION =============

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-specific-password
SMTP_FROM_EMAIL=noreply@realestate.com

# ============= CORS CONFIGURATION =============

CORS_ORIGINS=http://localhost:3000,http://localhost:8000,http://localhost:8001
```

---

## 🚀 Step 3: Update docker-compose.yml

Replace the `api` service section in your `docker-compose.yml`:

```yaml
  # FastAPI Backend with Authentication
  api:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: realestate_api
    environment:
      # Database
      DATABASE_URL: postgresql://${DB_USER:-postgres}:${DB_PASSWORD:-postgres}@postgres:5432/${DB_NAME:-realestate_crm}
      REDIS_URL: redis://redis:6379
      
      # Application
      ENVIRONMENT: ${ENVIRONMENT:-development}
      DEBUG: ${DEBUG:-true}
      PROJECT_NAME: Real Estate CRM API
      
      # JWT Configuration (NEW)
      JWT_SECRET_KEY: ${JWT_SECRET_KEY:-your-secret-key-change-in-production}
      JWT_ALGORITHM: HS256
      JWT_EXPIRATION_HOURS: 1
      JWT_REFRESH_EXPIRATION_DAYS: 7
      
      # Google OAuth Configuration (NEW)
      GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID:-}
      GOOGLE_CLIENT_SECRET: ${GOOGLE_CLIENT_SECRET:-}
      GOOGLE_REDIRECT_URI: ${GOOGLE_REDIRECT_URI:-http://localhost:8000/api/auth/google/callback}
      
      # Email Configuration (Optional)
      SMTP_HOST: ${SMTP_HOST:-smtp.gmail.com}
      SMTP_PORT: ${SMTP_PORT:-587}
      SMTP_USER: ${SMTP_USER:-}
      SMTP_PASSWORD: ${SMTP_PASSWORD:-}
      SMTP_FROM_EMAIL: ${SMTP_FROM_EMAIL:-noreply@realestate.com}
      
      # CORS
      CORS_ORIGINS: ${CORS_ORIGINS:-http://localhost:3000,http://localhost:8000}
    
    ports:
      - "8000:8000"
    
    depends_on:
      postgres:
        condition: service_healthy
      redis:
        condition: service_healthy
    
    volumes:
      - ./src:/app  # Hot reload in development
    
    command: uvicorn main:app --host 0.0.0.0 --port 8000 --reload
    
    restart: unless-stopped
    
    networks:
      - realestate_network
    
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/auth/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

---

## 🐳 Step 4: Install Python Dependencies in Docker

Your `requirements.txt` already includes the Google OAuth packages. Verify they're there:

```
google-auth==2.27.0
google-auth-httplib2==0.2.0
google-auth-oauthlib==1.2.0
```

If not, update `requirements.txt`:

```bash
pip install google-auth google-auth-httplib2 google-auth-oauthlib

# Update requirements.txt
pip freeze > requirements.txt
```

---

## 🚀 Step 5: Start All Services with Docker

### **1. Build the Docker Image**

```bash
# Navigate to project directory
cd f:\real-estate

# Build the backend image
docker-compose build
```

### **2. Start All Services**

```bash
# Start all services (PostgreSQL, Redis, FastAPI)
docker-compose up -d
```

**Services started:**
- ✅ PostgreSQL (Port 5432)
- ✅ Redis (Port 6379)
- ✅ FastAPI Backend (Port 8000)

### **3. Verify Services Are Running**

```bash
# Check all containers
docker-compose ps

# Check API health
curl http://localhost:8000/api/auth/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "authentication",
  "version": "1.0.0"
}
```

---

## 📊 Docker Compose Architecture

```
┌─────────────────────────────────────────────────┐
│          Docker Compose Network                 │
├─────────────────────────────────────────────────┤
│                                                  │
│  ┌──────────────┐  ┌──────────────┐             │
│  │  PostgreSQL  │  │    Redis     │             │
│  │   Port 5432  │  │   Port 6379  │             │
│  └──────────────┘  └──────────────┘             │
│         ▲                  ▲                     │
│         │                  │                     │
│         └──────┬───────────┘                     │
│                │                                 │
│        ┌───────▼────────┐                       │
│        │  FastAPI API   │                       │
│        │   Port 8000    │                       │
│        │                │                       │
│        │ Authentication │                       │
│        │   - Tenant     │                       │
│        │   - Admin      │                       │
│        │   - Google     │                       │
│        └────────────────┘                       │
│             ▲                                    │
│             │                                    │
│  ┌──────────┴──────────┐                       │
│  │   Frontend/Client   │                       │
│  │   Port 3000/8001    │                       │
│  └─────────────────────┘                       │
│                                                  │
└─────────────────────────────────────────────────┘
```

---

## 🧪 Step 6: Test Endpoints with Docker

### **Test Tenant Signup**

```bash
curl -X POST http://localhost:8000/api/auth/tenant/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@company.com",
    "password": "SecurePass123!",
    "confirm_password": "SecurePass123!",
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "ABC Real Estate",
    "company_phone": "+92-300-1234567",
    "company_city": "Islamabad",
    "accept_terms": true
  }'
```

### **Test Admin Signup**

```bash
curl -X POST http://localhost:8000/api/auth/admin/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "admin@admin.com",
    "password": "AdminPass123!",
    "confirm_password": "AdminPass123!",
    "first_name": "Admin",
    "last_name": "User"
  }'
```

### **Test Tenant Login**

```bash
curl -X POST http://localhost:8000/api/auth/tenant/login \
  -H "Content-Type: application/json" \
  -d '{
    "email": "owner@company.com",
    "password": "SecurePass123!"
  }'
```

### **Get Google OAuth URL**

```bash
curl -X GET http://localhost:8000/api/auth/google/auth-url
```

---

## 🔍 Docker Management Commands

### **View Logs**

```bash
# View all logs
docker-compose logs -f

# View only API logs
docker-compose logs -f api

# View only PostgreSQL logs
docker-compose logs -f postgres
```

### **Execute Commands in Container**

```bash
# Connect to PostgreSQL container
docker-compose exec postgres psql -U postgres -d realestate_crm

# Run Python command in API container
docker-compose exec api python -c "import sys; print(sys.version)"

# List all tables in database
docker-compose exec postgres psql -U postgres -d realestate_crm -c "\dt"
```

### **Stop Services**

```bash
# Stop all services (keep data)
docker-compose stop

# Stop and remove all containers (data persists in volumes)
docker-compose down

# Stop and remove everything including volumes (DELETE DATA!)
docker-compose down -v
```

### **Restart Services**

```bash
# Restart all services
docker-compose restart

# Restart specific service
docker-compose restart api
```

### **View Container Resource Usage**

```bash
docker stats
```

---

## 🗄️ Database Setup in Docker

### **Run Migrations**

```bash
# Inside API container
docker-compose exec api alembic upgrade head
```

### **Create Tables Manually**

```bash
# Connect to PostgreSQL
docker-compose exec postgres psql -U postgres -d realestate_crm

# Run SQL commands
CREATE TABLE tenants (...);
CREATE TABLE users (...);
CREATE TABLE refresh_tokens (...);
```

---

## 🌐 Frontend Integration with Docker

### **Update Frontend Environment Variables**

Create `.env.local` in your Next.js/React frontend:

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
```

### **Run Frontend in Docker (Optional)**

Add to `docker-compose.yml`:

```yaml
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: realestate_frontend
    environment:
      NEXT_PUBLIC_API_URL: http://localhost:8000
      NEXT_PUBLIC_GOOGLE_CLIENT_ID: ${GOOGLE_CLIENT_ID}
    ports:
      - "3000:3000"
    depends_on:
      - api
    networks:
      - realestate_network
    restart: unless-stopped
```

---

## 🔐 Production Deployment (Docker)

### **Production `.env` file**

```env
ENVIRONMENT=production
DEBUG=false

DB_USER=prod_user
DB_PASSWORD=secure_password_here
DB_NAME=realestate_prod

JWT_SECRET_KEY=generate-random-32-char-key
GOOGLE_CLIENT_ID=your-prod-client-id
GOOGLE_CLIENT_SECRET=your-prod-secret
GOOGLE_REDIRECT_URI=https://api.yourdomain.com/api/auth/google/callback

CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

SMTP_USER=noreply@yourdomain.com
SMTP_PASSWORD=your-secure-password
```

### **Production docker-compose.yml Changes**

```yaml
  api:
    # ... existing config ...
    command: uvicorn main:app --host 0.0.0.0 --port 8000
    # Remove --reload for production
    restart: always
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 1G
```

---

## 📊 Common Docker Issues & Solutions

### **Issue: "Connection refused" to PostgreSQL**

```bash
# Solution: Wait for PostgreSQL to be healthy
docker-compose down
docker volume rm real-estate_postgres_data  # Remove old data if needed
docker-compose up -d --build
sleep 10  # Wait for services to start
```

### **Issue: "Port already in use"**

```bash
# Solution: Change ports in docker-compose.yml or kill existing process
# Kill process on port 8000
netstat -ano | findstr :8000  # Windows
lsof -i :8000  # Mac/Linux

# Then kill the process or change port in docker-compose.yml
```

### **Issue: "Google OAuth not working in Docker"**

```bash
# Solution: Check environment variables are passed correctly
docker-compose exec api env | grep GOOGLE

# Should show:
# GOOGLE_CLIENT_ID=your-client-id
# GOOGLE_CLIENT_SECRET=your-secret
# GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

### **Issue: "Module not found" errors**

```bash
# Solution: Rebuild Docker image
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🎯 Complete Setup Checklist

```
[ ] Google OAuth credentials obtained
[ ] .env file created with all required variables
[ ] docker-compose.yml updated with Google OAuth config
[ ] requirements.txt includes google-auth packages
[ ] Docker & Docker Compose installed
[ ] Run: docker-compose build
[ ] Run: docker-compose up -d
[ ] Verify: curl http://localhost:8000/api/auth/health
[ ] Run: docker-compose exec api alembic upgrade head
[ ] Test endpoints with curl commands
[ ] Frontend .env.local configured
[ ] Frontend running and connecting to API
[ ] Google OAuth button working
```

---

## 📱 Frontend Docker Integration

### **Test from Frontend**

```typescript
// services/authService.ts
const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const authService = {
  tenantSignup: async (payload) => {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/tenant/signup`,
      payload
    );
    return response.data;
  },

  googleLogin: async (idToken) => {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/google/login`,
      { id_token: idToken }
    );
    return response.data;
  }
};
```

---

## 🐳 Docker Compose Networking

Containers can communicate using service names:

```python
# Inside API container, to reach PostgreSQL:
DATABASE_URL = "postgresql://postgres:password@postgres:5432/realestate_crm"
# Uses 'postgres' service name, not localhost

# Inside API container, to reach Redis:
REDIS_URL = "redis://redis:6379"
# Uses 'redis' service name
```

---

## ✅ Verification Checklist

After `docker-compose up -d`:

```bash
# 1. Check all containers running
docker-compose ps

# 2. Check API health
curl http://localhost:8000/api/auth/health

# 3. Check PostgreSQL connection
docker-compose exec postgres psql -U postgres -c "SELECT 1"

# 4. Check Redis connection
docker-compose exec redis redis-cli ping

# 5. View API logs
docker-compose logs api | head -50

# 6. Test signup endpoint
curl -X POST http://localhost:8000/api/auth/tenant/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com",...}'
```

---

## 📞 Support

For issues:
1. Check Docker logs: `docker-compose logs api`
2. Verify .env variables: `docker-compose exec api env | grep JWT`
3. Verify Google credentials are correct
4. Ensure ports aren't in use
5. Check network connectivity: `docker network ls`

---

## 🎓 Useful Docker Commands Reference

```bash
# Build
docker-compose build                    # Build all images
docker-compose build --no-cache api     # Build specific service

# Start/Stop
docker-compose up -d                    # Start all in background
docker-compose down                     # Stop all services
docker-compose restart                  # Restart all services
docker-compose restart api              # Restart specific service

# Logs
docker-compose logs -f                  # Follow all logs
docker-compose logs api                 # View past logs

# Execute
docker-compose exec api bash            # Shell into container
docker-compose exec postgres psql ...   # Run PostgreSQL commands

# Cleanup
docker-compose down -v                  # Remove everything (DELETE DATA!)
docker system prune                     # Clean up unused images/volumes

# Status
docker-compose ps                       # Show running containers
docker-compose config                   # Show compose config
```

---

**Status**: ✅ Complete Docker setup guide for Authentication with Google OAuth

You're ready to deploy! 🚀
