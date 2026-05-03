# Tenant Management System - Implementation Guide

## Overview

The Tenant Management System provides complete multi-tenant SaaS capabilities for the Real Estate CRM platform. Each tenant represents a separate company/organization with isolated data, users, and configurations.

## Architecture

### Data Model

```
Tenant (Multi-tenant root)
├── id (Primary Key)
├── tenant_code (Unique: auto-generated)
├── company_name (Unique: company identifier)
├── company_email (Email contact)
├── phone (Contact number)
├── address, city, country (Location)
├── logo_url (Company branding)
├── subscription_plan (FREE, BASIC, PRO, ENTERPRISE)
├── paid_until (Subscription expiry date)
├── status (ACTIVE, INACTIVE, SUSPENDED)
├── settings (JSON: configuration)
├── metadata_info (JSON: additional data)
├── created_at, updated_at (Timestamps)
└── users (Relationship: Users belong to Tenant)
```

### Subscription Plans

| Plan | Max Users | Max Deals | Storage | Features |
|------|-----------|-----------|---------|----------|
| FREE | 2 | 10 | 100 MB | Basic features |
| BASIC | 5 | 100 | 1 GB | Standard features |
| PRO | 20 | 1,000 | 5 GB | Advanced analytics |
| ENTERPRISE | 100 | 10,000 | 50 GB | Custom branding, API |

### Status Types

- **ACTIVE**: Tenant is active and operational
- **INACTIVE**: Tenant is inactive (can be reactivated)
- **SUSPENDED**: Tenant is suspended (due to payment or violation)

## Features

### 1. Tenant Creation
- **Endpoint**: `POST /api/tenants/`
- **Permission**: Super Admin only
- **Features**:
  - Auto-generates unique tenant code from company name
  - Enforces unique company name
  - Sets default subscription plan
  - Initializes default settings and metadata
  - Returns full tenant details

### 2. Tenant Listing
- **Endpoint**: `GET /api/tenants/`
- **Permission**: Super Admin only
- **Features**:
  - Paginated listing (skip, limit)
  - Filter by status (ACTIVE, INACTIVE, SUSPENDED)
  - Returns total count and pagination info

### 3. Tenant Details
- **Endpoint**: `GET /api/tenants/{tenant_id}`
- **Permission**: Tenant owner or Super Admin
- **Features**:
  - Returns full tenant information
  - Includes all settings
  - Includes metadata
  - Authorization checks prevent cross-tenant access

### 4. Tenant Update
- **Endpoint**: `PATCH /api/tenants/{tenant_id}`
- **Permission**: Tenant owner or Super Admin
- **Fields**:
  - company_name, company_email, phone
  - address, city, country
  - logo_url (for branding)

### 5. Settings Management
- **Endpoint**: `PATCH /api/tenants/{tenant_id}/settings`
- **Permission**: Tenant owner or Super Admin
- **Default Settings**:
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

### 6. Subscription Management
- **Endpoint**: `PATCH /api/tenants/{tenant_id}/subscription`
- **Permission**: Super Admin only
- **Features**:
  - Upgrade to different plan
  - Set subscription duration (1-36 months)
  - Automatically calculates paid_until date

### 7. Usage Statistics
- **Endpoint**: `GET /api/tenants/{tenant_id}/usage`
- **Permission**: Tenant owner, Manager, or Super Admin
- **Returns**:
  ```json
  {
    "current_users": 3,
    "max_users": 5,
    "current_deals": 45,
    "max_deals": 100,
    "storage_used_mb": 250,
    "storage_limit_mb": 1024,
    "subscription_plan": "BASIC",
    "status": "ACTIVE",
    "paid_until": "2024-12-31T00:00:00"
  }
  ```

### 8. Tenant Suspension
- **Endpoint**: `PATCH /api/tenants/{tenant_id}/suspend`
- **Permission**: Super Admin only
- **Features**:
  - Suspends tenant operations
  - Records suspension reason in metadata
  - Stores suspension timestamp

### 9. Tenant Reactivation
- **Endpoint**: `PATCH /api/tenants/{tenant_id}/reactivate`
- **Permission**: Super Admin only
- **Features**:
  - Reactivates suspended tenant
  - Updates metadata with reactivation time
  - Returns tenant to ACTIVE status

### 10. Tenant Deactivation
- **Endpoint**: `PATCH /api/tenants/{tenant_id}/deactivate`
- **Permission**: Super Admin only
- **Features**:
  - Sets status to INACTIVE
  - Tenant can be reactivated later

## API Endpoints

### Create Tenant
```
POST /api/tenants/
Authorization: Bearer <super_admin_token>

{
  "company_name": "Acme Properties",
  "company_email": "info@acme.com",
  "phone": "+1-555-0123",
  "subscription_plan": "BASIC",
  "city": "New York",
  "country": "USA"
}

Response: 201 Created
{
  "success": true,
  "message": "Tenant created successfully",
  "data": {
    "id": 1,
    "tenant_code": "AP",
    "company_name": "Acme Properties",
    "subscription_plan": "BASIC",
    "status": "ACTIVE",
    "created_at": "2024-01-15T10:30:00Z",
    ...
  }
}
```

### List Tenants
```
GET /api/admin/tenants?skip=0&limit=20&status=ACTIVE
Authorization: Bearer <super_admin_token>

Response: 200 OK
{
  "success": true,
  "data": [
    {
      "id": 1,
      "tenant_code": "AP",
      "company_name": "Acme Properties",
      ...
    }
  ],
  "pagination": {
    "skip": 0,
    "limit": 20,
    "total": 150
  }
}
```

### Get Tenant Details
```
GET /api/tenants/1
Authorization: Bearer <token>

Response: 200 OK
{
  "success": true,
  "data": {
    "id": 1,
    "tenant_code": "AP",
    "company_name": "Acme Properties",
    "settings": {
      "currency": "PKR",
      "timezone": "Asia/Karachi",
      ...
    }
  }
}
```

### Update Tenant Settings
```
PATCH /api/tenants/1/settings
Authorization: Bearer <token>

{
  "settings": {
    "currency": "USD",
    "commission_percentage": 5,
    "features": {
      "custom_branding": true,
      "api_access": true
    }
  }
}

Response: 200 OK
{
  "success": true,
  "data": {
    "id": 1,
    "settings": {
      "currency": "USD",
      ...
    }
  }
}
```

### Upgrade Subscription
```
PATCH /api/tenants/1/subscription
Authorization: Bearer <super_admin_token>

{
  "new_plan": "PRO",
  "months": 12
}

Response: 200 OK
{
  "success": true,
  "data": {
    "id": 1,
    "subscription_plan": "PRO",
    "paid_until": "2025-01-15T00:00:00Z"
  }
}
```

### Get Tenant Usage
```
GET /api/tenants/1/usage
Authorization: Bearer <token>

Response: 200 OK
{
  "current_users": 4,
  "max_users": 20,
  "current_deals": 156,
  "max_deals": 1000,
  "storage_used_mb": 512,
  "storage_limit_mb": 5120,
  "subscription_plan": "PRO",
  "status": "ACTIVE",
  "paid_until": "2025-01-15T00:00:00Z"
}
```

### Suspend Tenant
```
PATCH /api/tenants/1/suspend
Authorization: Bearer <super_admin_token>

{
  "reason": "Payment failure - invoice overdue"
}

Response: 200 OK
{
  "success": true,
  "message": "Tenant suspended successfully",
  "data": {
    "id": 1,
    "status": "SUSPENDED"
  }
}
```

### Reactivate Tenant
```
PATCH /api/tenants/1/reactivate
Authorization: Bearer <super_admin_token>

Response: 200 OK
{
  "success": true,
  "message": "Tenant reactivated successfully",
  "data": {
    "id": 1,
    "status": "ACTIVE"
  }
}
```

## Implementation Details

### File Structure
```
src/
├── models/
│   └── tenant.py              # Tenant model, enums
├── services/
│   └── tenant/
│       └── service.py         # TenantService class
├── schemas/
│   └── tenant.py              # Request/response models
├── api/
│   ├── tenants/
│   │   └── routes.py          # Tenant endpoints
│   └── admin/
│       └── routes.py          # Admin endpoints
└── database/
    └── session.py             # Tenant table initialization
```

### Service Methods

#### Create Tenant
```python
tenant = TenantService.create_tenant(
    db=db,
    company_name="Acme Properties",
    company_email="info@acme.com",
    phone="+1-555-0123",
    subscription_plan=SubscriptionPlan.BASIC,
    address="123 Main St",
    city="New York",
    country="USA"
)
```

#### Get Tenant
```python
# By ID
tenant = TenantService.get_tenant_by_id(db, tenant_id=1)

# By Code
tenant = TenantService.get_tenant_by_code(db, tenant_code="AP")
```

#### Update Tenant
```python
updated = TenantService.update_tenant(
    db=db,
    tenant_id=1,
    phone="+1-555-9999",
    city="Los Angeles"
)
```

#### Update Settings
```python
updated = TenantService.update_settings(
    db=db,
    tenant_id=1,
    settings={
        "currency": "USD",
        "commission_percentage": 5
    }
)
```

#### Manage Subscription
```python
# Upgrade
updated = TenantService.upgrade_subscription(
    db=db,
    tenant_id=1,
    new_plan=SubscriptionPlan.PRO,
    months=12
)
```

#### Manage Status
```python
# Suspend
suspended = TenantService.suspend_tenant(
    db=db,
    tenant_id=1,
    reason="Non-payment"
)

# Reactivate
reactivated = TenantService.reactivate_tenant(db=db, tenant_id=1)

# Deactivate
deactivated = TenantService.deactivate_tenant(db=db, tenant_id=1)
```

#### Get Usage
```python
usage = TenantService.get_tenant_usage(db, tenant_id=1)
```

## Authorization

### Role-Based Access

| Action | Super Admin | Platform Admin | Tenant Owner | Manager | Operator |
|--------|-------------|----------------|--------------|---------|----------|
| Create Tenant | ✅ | ❌ | ❌ | ❌ | ❌ |
| List Tenants | ✅ | ❌ | ❌ | ❌ | ❌ |
| View Tenant | ✅ | ✅ | ✅ | ✅ | ✅ |
| Update Tenant | ✅ | ✅ | ✅ | ❌ | ❌ |
| Update Settings | ✅ | ✅ | ✅ | ❌ | ❌ |
| Upgrade Plan | ✅ | ❌ | ❌ | ❌ | ❌ |
| View Usage | ✅ | ✅ | ✅ | ✅ | ❌ |
| Suspend Tenant | ✅ | ❌ | ❌ | ❌ | ❌ |
| Reactivate Tenant | ✅ | ❌ | ❌ | ❌ | ❌ |

## Error Handling

### Common Error Responses

**400 Bad Request**
```json
{
  "success": false,
  "detail": "Invalid status: UNKNOWN"
}
```

**403 Forbidden**
```json
{
  "success": false,
  "detail": "Cannot view this tenant"
}
```

**404 Not Found**
```json
{
  "success": false,
  "detail": "Tenant not found"
}
```

**409 Conflict**
```json
{
  "success": false,
  "detail": "Tenant with company name 'Acme' already exists"
}
```

## Testing

Run tenant tests:
```bash
pytest tests/test_tenant_management.py -v
```

Test coverage includes:
- Tenant CRUD operations
- Subscription management
- Status transitions
- Settings management
- Usage calculation
- Pagination and filtering
- Data integrity and constraints
- Authorization checks

## Tenant Code Generation

Tenant codes are auto-generated from company names:
- Take first letter of each word (up to 3 words)
- Convert to uppercase
- Maximum 5 characters
- Ensure uniqueness (append number if needed)

Examples:
- "Real Estate Corp" → "REC"
- "Acme" → "A"
- "Best Properties Inc" → "BPI"
- "ABC" → "ABC"

## Settings Structure

### Communication Settings
- `enable_whatsapp`: Enable WhatsApp notifications
- `enable_email`: Enable email notifications
- `enable_sms`: Enable SMS notifications

### Financial Settings
- `commission_percentage`: Default commission percentage
- `late_fee_percentage`: Late payment fee percentage

### Display Settings
- `currency`: Currency code (PKR, USD, etc.)
- `timezone`: Timezone identifier
- `date_format`: Date display format
- `language`: Default language

### Feature Flags
- `auto_receipt`: Auto-generate receipts
- `payment_reminder_days`: Days before payment due date for reminders
- `advanced_analytics`: Enable advanced analytics
- `custom_branding`: Enable custom branding
- `api_access`: Enable API access

## Database Schema

```sql
CREATE TABLE tenants (
    id SERIAL PRIMARY KEY,
    tenant_code VARCHAR(20) UNIQUE NOT NULL,
    company_name VARCHAR(255) UNIQUE NOT NULL,
    company_email VARCHAR(255),
    phone VARCHAR(20),
    address VARCHAR(500),
    city VARCHAR(100),
    country VARCHAR(100),
    logo_url VARCHAR(500),
    subscription_plan tenant_subscriptionplan NOT NULL,
    paid_until TIMESTAMP WITH TIME ZONE,
    status tenant_tenantstatus NOT NULL,
    settings TEXT,
    metadata_info TEXT,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL,
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL,
    INDEX idx_tenant_code (tenant_code),
    INDEX idx_company_name (company_name),
    INDEX idx_status (status)
);
```

## Next Steps

After tenant system is fully deployed:

1. **Client Management**: Implement client CRUD with tenant isolation
2. **Deal Management**: Implement deal tracking with commission calculations
3. **Payment System**: Implement payment processing and receipts
4. **Reporting**: Add comprehensive tenant analytics and reporting
5. **Webhooks**: Add event-based webhooks for tenant operations
6. **API Quotas**: Implement rate limiting per subscription plan

## Completion Checklist

- ✅ Tenant model created
- ✅ Tenant service layer implemented
- ✅ Request/response schemas created
- ✅ API endpoints implemented
- ✅ Admin endpoints implemented
- ✅ Authorization checks added
- ✅ Database initialization updated
- ✅ Tests created
- ✅ Documentation written
