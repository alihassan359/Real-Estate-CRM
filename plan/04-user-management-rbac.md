# 👥 User Management & RBAC System

## 📋 Overview
Role-Based Access Control (RBAC) system with hierarchical roles, permissions, and tenant-level authorization.

---

## 🎯 Role Hierarchy

### Platform Level (Global Roles)
```
SUPER_ADMIN
  ↓
PLATFORM_ADMIN
```

### Tenant Level (Company-Specific Roles)
```
TENANT_OWNER
  ├── MANAGER
  │   ├── OPERATOR
  │   ├── ACCOUNTANT
  │   └── SALESMAN
  │
  └── (Direct team members)
```

---

## 🔑 Roles & Permissions Matrix

### 1. SUPER_ADMIN
```yaml
Access: Entire Platform
Permissions:
  - manage_tenants (create, suspend, delete)
  - view_all_tenants
  - manage_platform_admins
  - view_audit_logs
  - system_configuration
  - manage_subscription_plans
```

### 2. PLATFORM_ADMIN
```yaml
Access: Limited tenant management
Permissions:
  - view_assigned_tenants
  - manage_tenant_settings
  - suspend_tenants
  - view_billing
  - support_tenants
```

### 3. TENANT_OWNER
```yaml
Access: Full tenant access
Permissions:
  - manage_users
  - manage_projects
  - manage_clients
  - create_deals
  - record_payments
  - view_all_reports
  - manage_settings
  - view_audit_logs
  - manage_integrations
```

### 4. MANAGER
```yaml
Access: Operational management
Permissions:
  - manage_operators
  - create_projects
  - create_clients
  - submit_deals (not approve)
  - view_team_performance
  - manage_comments
  - view_workflow_reports
```

### 5. OPERATOR
```yaml
Access: Data entry
Permissions:
  - create_clients
  - create_deals
  - submit_daily_reports
  - view_own_deals
  - comment_on_deals
```

### 6. ACCOUNTANT
```yaml
Access: Payment management
Permissions:
  - view_all_deals
  - record_payments
  - generate_receipts
  - view_payment_reports
  - reconcile_accounts
  - export_payment_data
```

### 7. SALESMAN
```yaml
Access: Limited deal view
Permissions:
  - view_assigned_deals
  - update_deal_status
  - view_client_info
  - comment_on_deals
```

---

## 📊 User Model

```yaml
user:
  id: UUID
  tenant_id: UUID (Foreign Key)
  email: String (Unique per tenant)
  password_hash: String
  first_name: String
  last_name: String
  phone: String
  avatar_url: String
  
  # Role & Permissions
  role: String (SUPER_ADMIN, PLATFORM_ADMIN, TENANT_OWNER, MANAGER, OPERATOR, ACCOUNTANT, SALESMAN)
  permissions: JSON Array (specific overrides)
  
  # Status
  status: String (ACTIVE, INACTIVE, SUSPENDED)
  email_verified: Boolean
  
  # Tracking
  last_login: DateTime
  created_at: DateTime
  updated_at: DateTime
  created_by: UUID
  updated_by: UUID
```

---

## 🛣️ User Management API Endpoints

### Create User (Tenant Owner or Manager)
```
POST /api/users

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "email": "operator@btmgroup.com",
  "first_name": "Ahmed",
  "last_name": "Hassan",
  "phone": "+92-300-9876543",
  "role": "OPERATOR",
  "send_invite": true
}

Response (201):
{
  "success": true,
  "message": "User created and invitation sent",
  "data": {
    "id": "user_uuid",
    "email": "operator@btmgroup.com",
    "role": "OPERATOR",
    "status": "INVITED",
    "permissions": [...]
  }
}
```

### List Users (Tenant)
```
GET /api/users?role=OPERATOR&status=ACTIVE&page=1&limit=20

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "user_uuid_1",
      "email": "operator1@btmgroup.com",
      "first_name": "Ahmed",
      "role": "OPERATOR",
      "status": "ACTIVE",
      "last_login": "2026-04-11T10:30:00Z"
    },
    ...
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 8
  }
}
```

### Get User Details
```
GET /api/users/{user_id}

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "id": "user_uuid",
    "email": "operator@btmgroup.com",
    "first_name": "Ahmed",
    "last_name": "Hassan",
    "phone": "+92-300-9876543",
    "role": "OPERATOR",
    "permissions": ["create_clients", "create_deals", ...],
    "status": "ACTIVE",
    "created_at": "2026-04-10T10:00:00Z"
  }
}
```

### Update User Role
```
PATCH /api/users/{user_id}/role

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "role": "MANAGER"
}

Response (200):
{
  "success": true,
  "message": "User role updated",
  "data": {
    "id": "user_uuid",
    "role": "MANAGER",
    "permissions": [new permissions...]
  }
}
```

### Disable User
```
PATCH /api/users/{user_id}/disable

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "reason": "Left company"
}

Response (200):
{
  "success": true,
  "message": "User disabled",
  "data": {
    "id": "user_uuid",
    "status": "INACTIVE"
  }
}
```

### Delete User (Soft Delete)
```
DELETE /api/users/{user_id}

Headers:
Authorization: Bearer owner_token

Response (200):
{
  "success": true,
  "message": "User deleted successfully"
}
```

### Update User Profile
```
PATCH /api/users/{user_id}/profile

Headers:
Authorization: Bearer token

Request Body:
{
  "first_name": "Ahmed",
  "last_name": "Hassan",
  "phone": "+92-300-9876543",
  "avatar_url": "..."
}

Response (200):
{
  "success": true,
  "data": { ... }
}
```

### Change Password
```
POST /api/users/{user_id}/change-password

Headers:
Authorization: Bearer token

Request Body:
{
  "current_password": "OldPass123!",
  "new_password": "NewPass456!"
}

Response (200):
{
  "success": true,
  "message": "Password changed successfully"
}
```

---

## 🔐 Permission Checking Middleware

```python
# middlewares/rbac_middleware.py

def check_permission(required_permission: str):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            # Get user from token
            user = get_current_user()
            
            # Get all user permissions
            user_perms = get_user_permissions(user)
            
            # Check if permission exists
            if required_permission not in user_perms:
                # Forbidden
                raise PermissionError(f"Missing: {required_permission}")
            
            return await func(*args, **kwargs)
        return wrapper
    return decorator
```

### Usage
```python
@router.post("/deals")
@check_permission("create_deal")
async def create_deal(request):
    # Only TENANT_OWNER, MANAGER, OPERATOR can access
    pass
```

---

## 📊 Permission List

```yaml
Deal Permissions:
  - create_deal
  - view_all_deals
  - view_own_deals
  - update_deal
  - delete_deal
  - approve_deal
  - reject_deal

Payment Permissions:
  - record_payment
  - view_payments
  - generate_receipt
  - reconcile_payments
  - export_payments

User Permissions:
  - create_user
  - view_users
  - edit_user
  - delete_user
  - manage_roles

Report Permissions:
  - view_reports
  - export_reports
  - view_analytics
  - view_audit_logs

System Permissions:
  - manage_tenants
  - manage_settings
  - manage_integrations
  - manage_subscription
```

---

## 🔄 Authorization Workflow

```
User Makes Request
  ↓
Extract Token
  ↓
Verify Token (auth_middleware)
  ↓
Extract User & Tenant
  ↓
Check Permission (rbac_middleware)
  ↓
Apply Tenant Filter
  ↓
All Good? Proceed
  ↓
Missing Permission? Return 403
```

---

## 🚨 Access Denial Rules

```
Scenario 1: Wrong Tenant
User from Tenant A tries to access Tenant B data
→ Return 403 Forbidden

Scenario 2: Missing Permission
Operator tries to delete user
→ Return 403 Forbidden + "Missing permission: delete_user"

Scenario 3: Expired Token
→ Return 401 Unauthorized

Scenario 4: Invalid Token
→ Return 401 Unauthorized
```

---

## ✅ User Management Checklist

- [ ] User model created
- [ ] Role enum defined
- [ ] Permissions matrix defined
- [ ] Create user endpoint
- [ ] List users endpoint
- [ ] Update user endpoint
- [ ] Delete user endpoint
- [ ] Role assignment endpoint
- [ ] Permission validation middleware
- [ ] RBAC middleware
- [ ] Permission checking on all protected routes
- [ ] Invitation system
- [ ] Email verification
- [ ] Change password flow
- [ ] User suspension logic
- [ ] Audit logging
- [ ] Swagger documentation
- [ ] Unit tests (80%+)
- [ ] Integration tests
