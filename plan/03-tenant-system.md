# 🏢 Tenant Management System

## 📋 Overview
Multi-tenant management system enabling company isolation, subscription management, and tenant-specific configuration.

---

## 🔑 Tenant Concepts

### What is a Tenant?
A tenant represents a **single company** with:
- Isolated data (no cross-tenant access)
- Independent users
- Own configuration
- Own subscription plan
- Own resources

### Tenant Hierarchy
```
Platform (SaaS)
  ├── Tenant 1 (BTM Group)
  │   ├── Users
  │   ├── Projects
  │   ├── Clients
  │   └── Deals
  │
  ├── Tenant 2 (Grand View)
  │   ├── Users
  │   ├── Projects
  │   ├── Clients
  │   └── Deals
  │
  └── Tenant N
```

---

## 📊 Tenant Data Model

```yaml
tenant:
  # Primary
  id: UUID
  tenant_code: String (Unique, 2-5 chars: BTM, GW, DHA)
  
  # Company Info
  company_name: String
  company_email: String
  phone: String
  website: String
  address: String
  city: String
  country: String
  
  # Subscription
  subscription_plan: String (FREE, BASIC, PRO, ENTERPRISE)
  subscription_start: DateTime
  paid_until: DateTime
  license_expiry: DateTime
  max_users: Integer
  max_deals: Integer
  
  # Status
  status: String (ACTIVE, INACTIVE, SUSPENDED, CANCELLED)
  
  # Configuration
  settings: JSON
    - enable_whatsapp: Boolean
    - enable_email: Boolean
    - enable_sms: Boolean
    - commission_percentage: Float
    - currency: String (PKR, USD)
    - timezone: String
    - date_format: String
  
  # Metadata
  logo_url: String
  branding_color: String
  features_enabled: JSON Array
  metadata: JSON
  
  # Tracking
  created_at: DateTime
  updated_at: DateTime
  created_by: UUID
  updated_by: UUID
```

---

## 🛣️ Tenant API Endpoints

### Create Tenant (Admin Only)
```
POST /api/tenants

Headers:
Authorization: Bearer super_admin_token

Request Body:
{
  "company_name": "New Real Estate Co",
  "company_email": "admin@newco.com",
  "phone": "+92-300-1234567",
  "subscription_plan": "BASIC"
}

Response (201):
{
  "success": true,
  "data": {
    "id": "tenant_uuid",
    "tenant_code": "NRC",
    "company_name": "New Real Estate Co",
    "subscription_plan": "BASIC",
    "status": "ACTIVE"
  }
}
```

### Get Tenant Details
```
GET /api/tenants/{tenant_id}

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "id": "tenant_uuid",
    "tenant_code": "BTM",
    "company_name": "BTM Group",
    "subscription_plan": "PRO",
    "max_users": 20,
    "current_users": 8,
    "settings": { ... },
    "status": "ACTIVE"
  }
}
```

### Update Tenant Settings
```
PATCH /api/tenants/{tenant_id}/settings

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "settings": {
    "enable_whatsapp": true,
    "commission_percentage": 5.5,
    "currency": "PKR",
    "timezone": "Asia/Karachi"
  }
}

Response (200):
{
  "success": true,
  "message": "Settings updated successfully",
  "data": { ... }
}
```

### List All Tenants (Super Admin)
```
GET /api/admin/tenants?page=1&limit=20&status=ACTIVE

Headers:
Authorization: Bearer super_admin_token

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "tenant_uuid_1",
      "tenant_code": "BTM",
      "company_name": "BTM Group",
      "subscription_plan": "PRO",
      "max_users": 20,
      "status": "ACTIVE"
    },
    ...
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 45,
    "pages": 3
  }
}
```

### Suspend Tenant (Admin)
```
POST /api/admin/tenants/{tenant_id}/suspend

Headers:
Authorization: Bearer admin_token

Request Body:
{
  "reason": "Payment overdue"
}

Response (200):
{
  "success": true,
  "message": "Tenant suspended",
  "data": {
    "id": "tenant_uuid",
    "status": "SUSPENDED"
  }
}
```

### Reactivate Tenant (Admin)
```
POST /api/admin/tenants/{tenant_id}/reactivate

Headers:
Authorization: Bearer admin_token

Response (200):
{
  "success": true,
  "message": "Tenant reactivated",
  "data": {
    "id": "tenant_uuid",
    "status": "ACTIVE"
  }
}
```

### Get Tenant Usage
```
GET /api/tenants/{tenant_id}/usage

Headers:
Authorization: Bearer owner_token

Response (200):
{
  "success": true,
  "data": {
    "current_users": 8,
    "max_users": 20,
    "current_deals": 45,
    "max_deals": 1000,
    "storage_used_mb": 256,
    "storage_limit_mb": 5120,
    "api_calls_month": 15234,
    "api_call_limit": 100000
  }
}
```

---

## 🔒 Data Isolation Rules

### Rule #1: Tenant Filter
**Every database query MUST include `tenant_id = user.tenant_id`**

```python
# ✅ CORRECT
SELECT * FROM deals WHERE tenant_id = ? AND deal_id = ?

# ❌ WRONG
SELECT * FROM deals WHERE deal_id = ?
```

### Rule #2: Middleware Enforcement
```python
@app.middleware("http")
async def add_tenant_filter(request, call_next):
    # Extract tenant_id from JWT token
    # Inject into request context
    # Middleware enforces tenant filter on all queries
```

### Rule #3: No Cross-Tenant Access
```python
# ❌ FORBIDDEN
# User from Tenant A should NEVER access Tenant B data
# Even if they guess the ID

# ✅ CORRECT
# Query: WHERE tenant_id = "user.tenant_id" AND resource_id = input
# If tenant mismatch, return 404 or 403
```

---

## 📊 Subscription Plans

| Plan | Users | Deals | Storage | Features | Price |
|------|-------|-------|---------|----------|-------|
| **FREE** | 2 | 10 | 100MB | Basic | Free |
| **BASIC** | 5 | 100 | 1GB | WhatsApp, Email | Rs 5000/mo |
| **PRO** | 20 | 1000 | 5GB | + Reports, Analytics | Rs 15000/mo |
| **ENTERPRISE** | 100+ | 10000+ | 50GB | All + Support | Custom |

---

## ⚙️ Tenant Configuration

### Default Settings
```json
{
  "enable_whatsapp": true,
  "enable_email": true,
  "enable_sms": false,
  "commission_percentage": 0,
  "currency": "PKR",
  "timezone": "Asia/Karachi",
  "date_format": "DD-MM-YYYY",
  "language": "urdu",
  "auto_receipt": true,
  "payment_reminder_days": 7,
  "late_fee_percentage": 0,
  "features": {
    "advanced_analytics": false,
    "custom_branding": false,
    "api_access": false
  }
}
```

---

## 🔄 Tenant Lifecycle

```
NEW (Just signed up)
  ↓
ACTIVE (Fully functional)
  ↓
INACTIVE (Manually disabled)
  ↓
SUSPENDED (Payment overdue / policy violation)
  ↓
CANCELLED (Deleted)
```

---

## 🛡️ Tenant Security

| Security Level | Measures |
|-----------------|----------|
| **Data Encryption** | AES-256 for sensitive fields |
| **Row-Level Security** | PostgreSQL RLS policies |
| **Audit Logging** | All tenant data changes logged |
| **Backup** | Daily backups, 30-day restore |
| **Access Control** | RBAC + Permission checks |
| **Rate Limiting** | Per-tenant API rate limits |

---

## ✅ Tenant Management Checklist

- [ ] Tenant model created
- [ ] Tenant creation endpoint
- [ ] Tenant configuration endpoint
- [ ] Tenant listing (admin)
- [ ] Tenant suspension logic
- [ ] Tenant reactivation logic
- [ ] Tenant usage calculation
- [ ] Row-level security policies
- [ ] Data isolation middleware
- [ ] Audit logging
- [ ] Swagger documentation
- [ ] Unit tests
- [ ] Integration tests
