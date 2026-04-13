# 🐳 Docker Troubleshooting Guide - Google OAuth & Authentication

---

## 🔴 Common Issues & Solutions

### **Issue 1: "Connection refused" when accessing http://localhost:8000**

**Symptoms:**
```
curl: (7) Failed to connect to localhost port 8000: Connection refused
```

**Causes & Solutions:**

```bash
# 1. Check if containers are running
docker-compose ps

# Expected output should show all containers as "Up"
# If not, start them:
docker-compose up -d

# 2. Wait for services to be healthy (takes 30-40 seconds)
# Check if API is ready:
docker-compose logs api | tail -20

# 3. If still not working, rebuild:
docker-compose down
docker-compose build --no-cache
docker-compose up -d
sleep 10
curl http://localhost:8000/api/auth/health
```

---

### **Issue 2: Google OAuth credentials not working**

**Symptoms:**
```json
{
  "success": false,
  "message": "Invalid token",
  "status_code": 401
}
```

**Causes & Solutions:**

```bash
# 1. Check if environment variables are set correctly
docker-compose exec api env | grep GOOGLE

# Expected output:
# GOOGLE_CLIENT_ID=your-client-id
# GOOGLE_CLIENT_SECRET=your-secret
# GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# 2. If not showing, update .env file:
nano .env  # or edit in your editor

# Add/update these lines:
# GOOGLE_CLIENT_ID=your-actual-client-id
# GOOGLE_CLIENT_SECRET=your-actual-secret
# GOOGLE_REDIRECT_URI=http://localhost:8000/api/auth/google/callback

# 3. Restart API container:
docker-compose restart api

# 4. Verify environment again:
docker-compose exec api env | grep GOOGLE

# 5. Check Google Cloud Console:
# - Go to https://console.cloud.google.com/
# - Select your project
# - Go to APIs & Services → Credentials
# - Verify Client ID and Secret match
# - Check authorized redirect URIs includes:
#   http://localhost:8000/api/auth/google/callback

# 6. If still not working, test directly:
docker-compose exec api python -c "
from services.auth.google_oauth_service import GoogleOAuthService
import os
print(f'Client ID: {os.getenv(\"GOOGLE_CLIENT_ID\")}')
print(f'Client Secret: {os.getenv(\"GOOGLE_CLIENT_SECRET\")}')
print(f'Redirect URI: {os.getenv(\"GOOGLE_REDIRECT_URI\")}')
"
```

---

### **Issue 3: Database connection errors**

**Symptoms:**
```
sqlalchemy.exc.OperationalError: (psycopg2.OperationalError) could not connect to server
```

**Causes & Solutions:**

```bash
# 1. Check PostgreSQL is running:
docker-compose ps postgres

# 2. Check database URL in .env:
cat .env | grep DATABASE_URL

# Should be:
# DATABASE_URL=postgresql://postgres:realestatecrm@postgres:5432/realestate_crm
#                                                  ^^^^^^^^-- Use service name!

# NOT:
# DATABASE_URL=postgresql://postgres:realestatecrm@localhost:5432/realestate_crm

# 3. Restart PostgreSQL:
docker-compose restart postgres
sleep 5

# 4. Check PostgreSQL logs:
docker-compose logs postgres | tail -20

# 5. Test connection directly:
docker-compose exec postgres psql -U postgres -c "SELECT 1"

# 6. If still failing, restart everything:
docker-compose down
rm -rf postgres_data volume  # WARNING: Deletes data!
docker-compose up -d postgres
sleep 10
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE realestate_crm"
```

---

### **Issue 4: Port already in use**

**Symptoms:**
```
Error response from daemon: Ports are not available: exposing port TCP 0.0.0.0:8000 -> 0.0.0.0:0: listen tcp 0.0.0.0:8000: bind: address already in use
```

**Causes & Solutions:**

**Windows:**
```powershell
# 1. Find process using port 8000:
netstat -ano | findstr :8000

# 2. Kill the process (replace PID with actual number):
taskkill /PID <PID> /F

# 3. Or change port in docker-compose.yml:
# Change "8000:8000" to "8001:8000"
```

**Mac/Linux:**
```bash
# 1. Find process using port 8000:
lsof -i :8000

# 2. Kill the process:
kill -9 <PID>

# 3. Or change port in docker-compose.yml
```

---

### **Issue 5: "Module not found" errors**

**Symptoms:**
```
ModuleNotFoundError: No module named 'google'
ModuleNotFoundError: No module named 'services.auth.google_oauth_service'
```

**Causes & Solutions:**

```bash
# 1. Rebuild Docker image:
docker-compose down
docker-compose build --no-cache

# 2. Verify requirements.txt has Google OAuth packages:
grep -i google requirements.txt

# Should show:
# google-auth==2.27.0
# google-auth-httplib2==0.2.0
# google-auth-oauthlib==1.2.0

# 3. If missing, add them:
pip install google-auth google-auth-httplib2 google-auth-oauthlib
pip freeze > requirements.txt

# 4. Rebuild and restart:
docker-compose build --no-cache
docker-compose up -d
```

---

### **Issue 6: Permission denied errors**

**Symptoms:**
```
PermissionError: [Errno 13] Permission denied: '/app/...'
```

**Causes & Solutions:**

```bash
# This happens when running with non-root user
# The Dockerfile creates 'appuser' with UID 1000

# 1. Docker Compose should handle this automatically
# If you're still getting errors:

# 2. Check running user:
docker-compose exec api whoami
# Should output: appuser

# 3. If it says root, rebuild:
docker-compose build --no-cache

# 4. In extreme cases, modify Dockerfile temporarily:
# Comment out this line:
# RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
# USER appuser
# Then rebuild and test
```

---

### **Issue 7: Authentication endpoints returning 400 errors**

**Symptoms:**
```json
{
  "success": false,
  "message": "Email already registered",
  "status_code": 400
}
```

**Causes & Solutions:**

```bash
# 1. Check if user already exists:
docker-compose exec postgres psql -U postgres -d realestate_crm -c "SELECT * FROM users WHERE email='test@test.com';"

# 2. Clean test data:
docker-compose exec postgres psql -U postgres -d realestate_crm -c "DELETE FROM users WHERE email='test@test.com';"

# 3. Test signup with different email:
curl -X POST http://localhost:8000/api/auth/tenant/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "newuser-'$(date +%s)'@test.com",
    "password": "TestPass123!",
    "confirm_password": "TestPass123!",
    "first_name": "Test",
    "last_name": "User",
    "company_name": "Test Company",
    "accept_terms": true
  }'

# 4. If you need to reset database:
docker-compose down
docker volume rm realestate_postgres_data
docker-compose up -d postgres
sleep 5
docker-compose exec postgres psql -U postgres -c "CREATE DATABASE realestate_crm;"
docker-compose up -d
docker-compose exec api alembic upgrade head
```

---

### **Issue 8: Migrations failing or not running**

**Symptoms:**
```
alembic.util.exc.CommandError: Can't locate revision identified by 'abc123'
```

**Causes & Solutions:**

```bash
# 1. Check migration status:
docker-compose exec api alembic current

# 2. View all migrations:
docker-compose exec api alembic history

# 3. Upgrade to latest:
docker-compose exec api alembic upgrade head

# 4. If specific revision is failing:
# Check migrations directory:
docker-compose exec api ls -la alembic/versions/

# 5. Downgrade then retry:
docker-compose exec api alembic downgrade -1
docker-compose exec api alembic upgrade head

# 6. Reset database and reinit migrations:
docker-compose down
docker volume rm realestate_postgres_data
docker-compose up -d
docker-compose exec api alembic upgrade head
```

---

### **Issue 9: API container keeps restarting**

**Symptoms:**
```
docker-compose ps
# STATUS showing "Restarting (1) ... " or "Exited (1) ..."
```

**Causes & Solutions:**

```bash
# 1. Check why it's failing:
docker-compose logs api

# 2. Common causes:
# - Database connection failed (wait longer, DB needs time to start)
# - Port already in use
# - Missing environment variables
# - Python module import errors

# 3. Wait longer and check logs:
sleep 15
docker-compose logs api | tail -50

# 4. Check all environment variables are passed:
docker-compose exec api env

# 5. Try running Python directly to find issue:
docker-compose exec api python -c "from main import app; print('OK')"

# 6. If still issues, rebuild and start fresh:
docker-compose down
docker-compose build --no-cache
docker-compose up -d
sleep 15
docker-compose logs api
```

---

### **Issue 10: Cannot reach API from frontend (localhost:3000)**

**Symptoms:**
```
CORS error: Access-Control-Allow-Origin header is missing
Connection refused to http://localhost:8000
```

**Causes & Solutions:**

```bash
# 1. Check CORS origins in .env:
grep CORS .env

# Should include:
# CORS_ORIGINS=http://localhost:3000,http://localhost:8000

# 2. Restart API with updated CORS:
docker-compose restart api

# 3. Verify frontend can reach API:
# From your frontend code:
const response = await fetch('http://localhost:8000/api/auth/health');

# 4. If still failing, check Docker network:
docker network ls
docker network inspect realestate_network

# 5. Make sure both containers are on same network:
docker-compose ps --services

# 6. If frontend is also in Docker:
# Update docker-compose.yml to include frontend service
# And ensure networks are configured correctly
```

---

## 🔍 Debugging Commands Reference

```bash
# View logs
docker-compose logs -f api              # Follow API logs in real-time
docker-compose logs api --tail=50       # Last 50 lines
docker-compose logs postgres            # PostgreSQL logs

# Execute commands in containers
docker-compose exec api bash            # Interactive shell
docker-compose exec api python -c "..."  # Run Python code
docker-compose exec postgres psql ...   # PostgreSQL commands

# Check environment
docker-compose exec api env             # View all env variables
docker-compose exec api env | grep GOOGLE  # Check Google OAuth

# Check files
docker-compose exec api ls -la src/     # List files
docker-compose exec api cat .env        # View .env (if copied)

# Database inspection
docker-compose exec postgres psql -U postgres -d realestate_crm -c "SELECT * FROM users;"
docker-compose exec postgres psql -U postgres -l  # List databases

# Resource usage
docker stats                             # Memory/CPU usage

# Clean up
docker-compose down -v                  # Stop and remove volumes (DELETE DATA!)
docker system prune                     # Clean unused images
```

---

## 📋 Pre-Launch Checklist

Before going to production:

```
[ ] Docker build succeeds without errors
[ ] All services healthy: docker-compose ps
[ ] Database migrations run: docker-compose exec api alembic current
[ ] API responds to health check: curl http://localhost:8000/api/auth/health
[ ] Google OAuth credentials are correct
[ ] Environment variables exported properly
[ ] All JWT_SECRET_KEY is strong (32+ characters)
[ ] Database connection tested
[ ] Signup endpoint works: test with curl
[ ] Login endpoint works: test with curl
[ ] Google OAuth flow tested
[ ] Frontend can reach backend
[ ] No sensitive data in logs
[ ] No containers keep restarting
[ ] Proper error handling implemented
[ ] Rate limiting configured (if needed)
```

---

## 🆘 Emergency Procedures

### **Complete Reset (Deletes all data!)**

```bash
# Windows PowerShell:
docker-compose down -v
docker volume prune -f
docker-compose build --no-cache
docker-compose up -d
docker-compose exec api alembic upgrade head

# Linux/Mac:
docker-compose down -v
docker volume prune -f
docker-compose build --no-cache
docker-compose up -d
docker-compose exec api alembic upgrade head
```

### **Emergency Restart**

```bash
# When everything seems stuck:
docker-compose restart
sleep 10
docker-compose logs api | tail -20
```

### **Get Emergency Shell Access**

```bash
# If container won't start properly:
docker-compose run --rm api bash
# Then manually check imports, configs, etc.
```

---

## 📞 When to Check

| Symptom | Check This First |
|---------|-----------------|
| API won't start | `docker-compose logs api` |
| DB connection error | `docker-compose ps postgres` + check DATABASE_URL |
| Google OAuth not working | Check .env has GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET |
| Port already in use | `netstat -ano` (Windows) or `lsof -i` (Mac/Linux) |
| Permissions denied | Check Dockerfile USER line |
| Migrations failing | `docker-compose exec api alembic current` |
| Services crashing | Check all environment variables with `docker-compose exec api env` |
| Nothing responds | `docker-compose ps` - is everything running? |

---

## 🎯 Quick Recovery Commands

```bash
# Fast recovery script:
docker-compose restart              # Restart all
sleep 10
docker-compose logs api | tail -30   # Check logs
curl http://localhost:8000/api/auth/health  # Test

# If that doesn't work:
docker-compose down
docker-compose up -d
sleep 15
docker-compose logs api | tail -50
```

---

**Remember**: Most issues are fixed by:
1. Waiting for services to start (30-40 seconds)
2. Checking environment variables
3. Restarting containers
4. Rebuilding images

Good luck! 🚀
