# 🐳 Docker Quick Reference Card - Real Estate CRM

**Complete setup & troubleshooting for Google OAuth authentication in Docker**

---

## 🚀 5-Minute Quick Start

### **Step 1: Copy Example .env**
```bash
copy .env.docker .env
# Then edit .env and add:
# GOOGLE_CLIENT_ID=your-id
# GOOGLE_CLIENT_SECRET=your-secret
```

### **Step 2: Build & Start**
```bash
# Windows PowerShell:
.\docker-start.ps1

# Linux/Mac:
bash docker-start.sh

# Or manual:
docker-compose build
docker-compose up -d
```

### **Step 3: Verify & Test**
```bash
# Check all running:
docker-compose ps

# Test API:
curl http://localhost:8000/api/auth/health

# Test signup:
curl -X POST http://localhost:8000/api/auth/tenant/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"test@test.com","password":"TestPass123!","confirm_password":"TestPass123!","first_name":"Test","last_name":"User","company_name":"Test Co","accept_terms":true}'
```

---

## 🔑 Google OAuth Setup (3 Steps)

### **1. Create Google Cloud Project**
- Go to [console.cloud.google.com](https://console.cloud.google.com)
- Create new project
- Enable Google+ API

### **2. Create OAuth Credentials**
- Go to Credentials → Create Credentials → OAuth 2.0 Client ID
- Select "Web Application"
- Add redirect URIs:
  - `http://localhost:8000/api/auth/google/callback`
  - `http://localhost:3000/auth/google/callback`

### **3. Add to .env**
```env
GOOGLE_CLIENT_ID=your-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-client-secret
GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback
```

---

## 📦 What's in Docker

```
PostgreSQL:5432    - Database
Redis:6379         - Cache
FastAPI:8000       - API (11 endpoints)

Services:
✅ Tenant signup/login
✅ Admin signup/login  
✅ Google OAuth
✅ JWT tokens
✅ Multi-tenant isolation
```

---

## 🛠️ Common Tasks

| Task | Command |
|------|---------|
| **Start All** | `docker-compose up -d` |
| **Stop All** | `docker-compose stop` |
| **View Logs** | `docker-compose logs -f api` |
| **DB Shell** | `docker-compose exec postgres psql -U postgres` |
| **API Shell** | `docker-compose exec api bash` |
| **Run Migration** | `docker-compose exec api alembic upgrade head` |
| **Restart API** | `docker-compose restart api` |
| **Rebuild** | `docker-compose build --no-cache` |
| **Full Reset** | `docker-compose down -v && docker-compose up -d` |

---

## 🔴 10 Minute Troubleshoot

| Problem | Fix |
|---------|-----|
| **Connection refused** | Wait 30s, check `docker-compose ps`, restart: `docker-compose restart` |
| **Google auth fails** | Check `.env`, verify `GOOGLE_CLIENT_ID`, restart: `docker-compose restart api` |
| **DB connection error** | Check `DATABASE_URL=postgresql://postgres:realestatecrm@postgres:5432/realestate_crm` (use "postgres" not localhost) |
| **Port in use** | `netstat -ano \| findstr :8000` then kill, or use port 8001 |
| **Module not found** | Rebuild: `docker-compose build --no-cache && docker-compose up -d` |
| **API crashes** | Check logs: `docker-compose logs api \| tail -50` |
| **Migrations fail** | Run: `docker-compose exec api alembic upgrade head` |
| **No permission** | Restart: `docker-compose restart` |
| **Email config** | Optional, set `SMTP_*` variables in `.env` |
| **CORS issues** | Update `.env`: `CORS_ORIGINS=http://localhost:3000,http://localhost:8000` |

---

## 📋 Checklist Before Launch

```
[ ] .env file created with all variables
[ ] Google OAuth credentials obtained
[ ] docker-compose build succeeds
[ ] docker-compose up -d works
[ ] curl http://localhost:8000/api/auth/health returns 200
[ ] docker-compose ps shows all services "Up"
[ ] Database migrations complete
[ ] Test signup works
[ ] Test login works
[ ] Google OAuth button functional
[ ] Frontend can reach API
```

---

## 🔑 Required .env Variables

```env
# Essential:
DATABASE_URL=postgresql://postgres:realestatecrm@postgres:5432/realestate_crm
JWT_SECRET_KEY=your-32-char-secret-key-minimum
GOOGLE_CLIENT_ID=your-id-here
GOOGLE_CLIENT_SECRET=your-secret-here

# Optional:
ENVIRONMENT=development
DEBUG=true
CORS_ORIGINS=http://localhost:3000,http://localhost:8000
SMTP_HOST=smtp.gmail.com
SMTP_USER=your@email.com
```

---

## 📊 Architecture

```
User → Frontend (React/Next) → FastAPI API (8000) → PostgreSQL (5432)
                                    ↓
                                 Redis (6379)
                                    ↓
                         Google OAuth Verification
```

---

## 🧪 Test Commands

### **Create Tenant**
```bash
curl -X POST http://localhost:8000/api/auth/tenant/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"owner@test.com","password":"TestPass123!","confirm_password":"TestPass123!","first_name":"John","last_name":"Doe","company_name":"Test Co","accept_terms":true}'
```

### **Login**
```bash
curl -X POST http://localhost:8000/api/auth/tenant/login \
  -H "Content-Type: application/json" \
  -d '{"email":"owner@test.com","password":"TestPass123!"}'
```

### **Create Admin**
```bash
curl -X POST http://localhost:8000/api/auth/admin/signup \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@admin.com","password":"AdminPass123!","confirm_password":"AdminPass123!","first_name":"Admin","last_name":"User"}'
```

### **Get Google Auth URL**
```bash
curl http://localhost:8000/api/auth/google/auth-url
```

---

## 📁 Important Files

| File | Purpose |
|------|---------|
| `.env` | Environment configuration (copy from `.env.docker`) |
| `docker-compose.yml` | Service definitions |
| `Dockerfile` | Build image |
| `requirements.txt` | Python dependencies |
| `src/main.py` | FastAPI app entry |
| `DOCKER_SETUP_GUIDE.md` | Complete Docker guide |
| `DOCKER_TROUBLESHOOTING.md` | Issue solutions |

---

## 🚀 Production Deployment

### **1. Update .env**
```env
ENVIRONMENT=production
DEBUG=false
JWT_SECRET_KEY=generate-strong-key
CORS_ORIGINS=https://yourdomain.com
```

### **2. Update docker-compose.yml**
```yaml
command: uvicorn main:app --host 0.0.0.0 --port 8000
# Remove --reload for production
```

### **3. Deploy**
```bash
docker-compose build --no-cache
docker-compose up -d
```

---

## 🛡️ Security Checklist

```
[ ] JWT_SECRET_KEY is 32+ characters
[ ] GOOGLE_CLIENT_SECRET is not exposed
[ ] Database password is strong
[ ] CORS_ORIGINS only includes your domains
[ ] DEBUG=false in production
[ ] HTTPS enabled on production
[ ] Rate limiting configured (optional)
[ ] Audit logging enabled (optional)
```

---

## 📞 API Endpoints Summary

### **Public (No Auth)**
- `POST /api/auth/tenant/signup` - Company registration
- `POST /api/auth/tenant/login` - User login
- `POST /api/auth/admin/signup` - Admin registration
- `POST /api/auth/admin/login` - Admin login
- `GET /api/auth/google/auth-url` - Google OAuth URL
- `POST /api/auth/google/signup` - Google signup
- `POST /api/auth/google/login` - Google login

### **Protected (Needs Token)**
- `POST /api/auth/refresh` - Get new access token
- `POST /api/auth/logout` - Logout
- `GET /api/auth/me` - Current user info

---

## 🎯 Next Steps After Setup

1. ✅ Docker running with all services
2. ✅ Auth endpoints working
3. ✅ Google OAuth configured
4. ⏳ Setup frontend (see FRONTEND_AUTH_INTEGRATION_GUIDE.md)
5. ⏳ Email verification (next phase)
6. ⏳ Password reset (next phase)
7. ⏳ User management (next phase)

---

## 📚 Full Documentation

- **DOCKER_SETUP_GUIDE.md** - Complete setup instructions
- **DOCKER_TROUBLESHOOTING.md** - Detailed troubleshooting
- **AUTH_IMPLEMENTATION_COMPLETE.md** - API documentation
- **FRONTEND_AUTH_INTEGRATION_GUIDE.md** - Frontend setup
- **IMPLEMENTATION_STATUS.md** - Feature overview

---

## 💡 Pro Tips

```bash
# Tip 1: Keep logs open while coding
docker-compose logs -f api

# Tip 2: Quickly test all endpoints
./test-api.sh  # Run all tests

# Tip 3: Reset database only (keep containers)
docker-compose exec postgres psql -U postgres -c "DROP DATABASE realestate_crm; CREATE DATABASE realestate_crm;"

# Tip 4: Check what env your API has
docker-compose exec api env | grep -E "JWT|GOOGLE|DATABASE"

# Tip 5: Port forward from Docker to host
# Add to docker-compose.yml:
# ports:
#   - "127.0.0.1:8000:8000"
```

---

**Last Updated**: April 12, 2026  
**Status**: ✅ Production Ready

**Quick Start**: Copy `.env.docker` → Edit with Google OAuth → Run `docker-compose up -d` → Done! 🚀
