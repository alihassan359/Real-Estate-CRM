# 🔐 Authentication System Design

## 📋 Overview
Core authentication system handling user registration, login, JWT token management, and session control for multi-tenant SaaS.

---

## 🔄 Authentication Flow

```
POST /api/auth/signup
    ↓
Validate email, password, company_name
    ↓
Check duplicate email
    ↓
Hash password (bcrypt)
    ↓
Create User record
    ↓
Create Tenant record (auto-generate tenant_id)
    ↓
Generate JWT token (access + refresh)
    ↓
Return { user, tenant, token }
    ↓
POST /api/auth/login
    ↓
Validate credentials
    ↓
Issue new JWT
    ↓
Return token
```

---

## 🗂️ Data Models

### User Model
```yaml
user:
  id: UUID (Primary Key)
  tenant_id: UUID (Foreign Key → Tenant)
  email: String (Unique per tenant)
  password_hash: String (bcrypt)
  first_name: String
  last_name: String
  phone: String
  role: String (SUPER_ADMIN, PLATFORM_ADMIN, TENANT_OWNER, MANAGER, OPERATOR, ACCOUNTANT, SALESMAN)
  permissions: JSON Array
  status: String (ACTIVE, INACTIVE, SUSPENDED)
  last_login: DateTime
  created_at: DateTime
  updated_at: DateTime
  created_by: UUID
```

### Tenant Model
```yaml
tenant:
  id: UUID (Primary Key)
  tenant_code: String (Unique - BTM, GW, etc)
  company_name: String
  company_email: String
  phone: String
  address: String
  city: String
  country: String
  subscription_plan: String (FREE, BASIC, PRO, ENTERPRISE)
  paid_until: DateTime
  status: String (ACTIVE, INACTIVE, SUSPENDED)
  settings: JSON (config options)
  metadata: JSON (custom data)
  created_at: DateTime
  updated_at: DateTime
```

### JWT Token Model
```yaml
token:
  access_token: String (exp: 1 hour)
  refresh_token: String (exp: 7 days)
  token_type: Bearer
  expires_in: Integer (seconds)
  created_at: DateTime
```

---

## 🔑 JWT Payload Structure

### Access Token
```json
{
  "sub": "user_id",
  "user_email": "user@company.com",
  "tenant_id": "tenant_uuid",
  "tenant_code": "BTM",
  "role": "TENANT_OWNER",
  "permissions": ["create_deal", "add_payment", "view_reports"],
  "iat": 1704067200,
  "exp": 1704070800
}
```

### Refresh Token
```json
{
  "sub": "user_id",
  "type": "refresh",
  "iat": 1704067200,
  "exp": 1704672000
}
```

---

## 🛣️ API Endpoints

### User Registration (Signup)
```
POST /api/auth/signup

Request Body:
{
  "email": "admin@btmgroup.com",
  "password": "SecurePass123!",
  "company_name": "BTM Group",
  "company_phone": "+92-300-1234567",
  "first_name": "Ahmad",
  "last_name": "Khan"
}

Response (201):
{
  "success": true,
  "message": "User registered successfully",
  "data": {
    "user": {
      "id": "uuid",
      "email": "admin@btmgroup.com",
      "first_name": "Ahmad",
      "role": "TENANT_OWNER"
    },
    "tenant": {
      "id": "tenant_uuid",
      "tenant_code": "BTM",
      "company_name": "BTM Group"
    },
    "tokens": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "expires_in": 3600
    }
  }
}
```

### User Login
```
POST /api/auth/login

Request Body:
{
  "email": "admin@btmgroup.com",
  "password": "SecurePass123!"
}

Response (200):
{
  "success": true,
  "message": "Login successful",
  "data": {
    "user": {
      "id": "uuid",
      "email": "admin@btmgroup.com",
      "tenant_id": "tenant_uuid",
      "role": "TENANT_OWNER"
    },
    "tokens": {
      "access_token": "eyJhbGc...",
      "refresh_token": "eyJhbGc...",
      "expires_in": 3600
    }
  }
}
```

### Refresh Token
```
POST /api/auth/refresh

Request Body:
{
  "refresh_token": "eyJhbGc..."
}

Response (200):
{
  "success": true,
  "data": {
    "access_token": "eyJhbGc...",
    "expires_in": 3600
  }
}
```

### Logout
```
POST /api/auth/logout

Headers:
Authorization: Bearer access_token

Response (200):
{
  "success": true,
  "message": "Logged out successfully"
}
```

### Get Current User
```
GET /api/auth/me

Headers:
Authorization: Bearer access_token

Response (200):
{
  "success": true,
  "data": {
    "user": { ... },
    "tenant": { ... }
  }
}
```

---

## 🔒 Security Requirements

| Requirement | Implementation |
|------------|-----------------|
| Password Hashing | bcrypt (12 rounds) |
| Token Expiry | Access: 1 hour, Refresh: 7 days |
| Rate Limiting | 5 failed attempts = 15min lockout |
| HTTPS | Required in production |
| CORS | Restricted origins |
| CSRF Protection | Token validation |
| Input Validation | All fields validated |
| Password Requirements | Min 8 chars, 1 uppercase, 1 number, 1 special |

---

## 🧪 Error Handling

| Error | Status | Message |
|-------|--------|---------|
| Invalid email | 400 | "Invalid email format" |
| Email exists | 409 | "Email already registered" |
| Weak password | 400 | "Password doesn't meet requirements" |
| Invalid credentials | 401 | "Email or password incorrect" |
| Token expired | 401 | "Token expired, use refresh token" |
| Unauthorized | 401 | "Missing or invalid token" |
| Forbidden | 403 | "Insufficient permissions" |

---

## 📋 Checklist for Auth System

- [ ] User model created
- [ ] Tenant model created
- [ ] Password hashing implemented
- [ ] JWT token generation logic
- [ ] Signup endpoint
- [ ] Login endpoint
- [ ] Refresh token endpoint
- [ ] Logout endpoint
- [ ] Auth middleware created
- [ ] Rate limiting configured
- [ ] Swagger documentation
- [ ] Unit tests (80%+ coverage)
- [ ] Integration tests
