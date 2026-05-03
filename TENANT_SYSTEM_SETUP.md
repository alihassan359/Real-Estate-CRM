# Tenant System - Setup & Troubleshooting Guide

## 🔧 Installation Issues & Solutions

### Issue: "ModuleNotFoundError: No module named 'fastapi'" or Similar

**Root Cause**: Python dependencies not installed

**Solution**: Run the installation script:

```bash
pip install -r requirements.txt --no-build-isolation
```

Or install core packages manually:

```bash
pip install fastapi uvicorn pydantic sqlalchemy asyncpg python-jose pydantic-settings
pip install email-validator python-dotenv PyJWT passlib bcrypt cryptography
pip install pyotp google-auth httpx requests alembic redis pytest
```

### Issue: psycopg2 Build Error

**Error**: `pg_config executable not found`

**Solution**: Requirements.txt already uses `psycopg2-binary` which doesn't require compilation:
```bash
pip install --no-build-isolation -r requirements.txt
```

## ✅ Tenant System Status

### Routes Registered (13 total)
```
✅ POST   /api/tenants/                          - Create tenant
✅ GET    /api/tenants/                          - List tenants
✅ GET    /api/tenants/{tenant_id}               - Get tenant details
✅ PATCH  /api/tenants/{tenant_id}               - Update tenant
✅ PATCH  /api/tenants/{tenant_id}/settings      - Update settings
✅ PATCH  /api/tenants/{tenant_id}/subscription  - Upgrade plan
✅ GET    /api/tenants/{tenant_id}/usage         - Get usage stats
✅ PATCH  /api/tenants/{tenant_id}/suspend       - Suspend tenant
✅ PATCH  /api/tenants/{tenant_id}/reactivate    - Reactivate tenant
✅ PATCH  /api/tenants/{tenant_id}/deactivate    - Deactivate tenant
✅ GET    /api/admin/tenants                     - List all (admin)
✅ POST   /api/auth/tenant/signup                - Tenant signup
✅ POST   /api/auth/tenant/login                 - Tenant login
```

## Quick Start

### 1. Install Dependencies
```bash
cd f:\real-estate
pip install -r requirements.txt --no-build-isolation
```

### 2. Start the Server
```bash
python src/main.py
# or
python src/server.py
```

### 3. Access API
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Base**: http://localhost:8000/api

### 4. Test Tenant Endpoint
```bash
# Create tenant (requires Super Admin token)
curl -X POST http://localhost:8000/api/tenants/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <super_admin_token>" \
  -d '{
    "company_name": "Acme Properties",
    "subscription_plan": "BASIC",
    "city": "New York",
    "country": "USA"
  }'
```

## Verification Checklist

- ✅ Python packages installed
- ✅ Tenant routes registered (13 endpoints)
- ✅ Database connection configured
- ✅ FastAPI app starts without errors
- ✅ Service layer available
- ✅ Request/response schemas loaded
- ✅ Authorization middleware active

## Common Commands

### Run Tests
```bash
pytest tests/test_tenant_management.py -v
```

### Reset Database
```bash
python scripts/reset_db.py
```

### Validate Syntax
```bash
python -m py_compile src/services/tenant/service.py
python -m py_compile src/schemas/tenant.py
python -m py_compile src/api/tenants/routes.py
```

### Check Routes
```bash
cd src && python -c "
from main import app
for route in app.routes:
    if 'tenant' in route.path.lower():
        print(f'{route.methods or {\"GET\"}} {route.path}')
"
```

## Documentation Files

- **TENANT_SYSTEM_IMPLEMENTATION.md** - Complete implementation guide with API examples
- **TENANT_SYSTEM_COMPLETION.md** - Detailed completion summary
- **TEST_TENANT_MANAGEMENT.py** - Test suite with 19 test methods

## Support

If you encounter issues:

1. **Check dependencies**: `pip list | grep -E 'fastapi|sqlalchemy|pydantic'`
2. **Test imports**: `cd src && python -c "from api.tenants.routes import router"`
3. **Check routes**: `cd src && python -c "from main import app; print([r.path for r in app.routes if 'tenant' in r.path.lower()])"`
4. **View logs**: Check terminal output for error messages
5. **Reset DB**: `python scripts/reset_db.py` (clears and reinitializes)

## What's Next

- ✅ Tenant system is fully functional
- ⏳ Client management system
- ⏳ Deal tracking system
- ⏳ Payment processing
