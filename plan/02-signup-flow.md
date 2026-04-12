# 📝 User Registration & Signup Flow

## 🎯 Overview
Complete signup flow for new companies registering on the SaaS platform. Creates user, tenant, and initializes subscription.

---

## 🔄 Signup Process

### Step 1: Validation
```yaml
Validate:
  - Email format (RFC 5322)
  - Email uniqueness (global check)
  - Password strength (8+ chars, uppercase, number, special)
  - Company name (not empty, < 100 chars)
  - Phone format
  - Terms acceptance
```

### Step 2: Tenant Creation
```yaml
Generate:
  - tenant_id (UUID)
  - tenant_code (auto from company name: BTM, GW, etc)
  
Create Tenant:
  - tenant_id
  - tenant_code
  - company_name
  - subscription_plan: "FREE" (default)
  - paid_until: null
  - status: "ACTIVE"
```

### Step 3: User Creation
```yaml
Create User:
  - user_id (UUID)
  - tenant_id (link to tenant)
  - email
  - password_hash (bcrypt)
  - role: "TENANT_OWNER" (auto)
  - permissions: [all permissions]
  - status: "ACTIVE"
```

### Step 4: Generate Tokens
```yaml
Create Tokens:
  - access_token (1 hour)
  - refresh_token (7 days)
  - Store refresh token in database
```

### Step 5: Send Welcome Email
```yaml
Email Template:
  - Subject: "Welcome to Real Estate CRM"
  - Body: Company info, setup instructions
  - CTA: Go to dashboard
```

---

## 📊 Signup API Endpoint

###  POST /api/auth/signup

#### Request Body
```json
{
  "email": "admin@btmgroup.com",
  "password": "SecurePass123!",
  "confirm_password": "SecurePass123!",
  "first_name": "Ahmad",
  "last_name": "Khan",
  "company_name": "BTM Group",
  "company_phone": "+92-300-1234567",
  "company_city": "Islamabad",
  "accept_terms": true
}
```

#### Validation Rules
```yaml
email:
  - Required
  - Valid format
  - Unique globally
  - Max 255 chars

password:
  - Required
  - Min 8 characters
  - Max 50 characters
  - Must contain: uppercase, lowercase, number, special char
  - Cannot be common passwords

first_name:
  - Required
  - Min 2, Max 50

last_name:
  - Required
  - Min 2, Max 50

company_name:
  - Required
  - Min 3, Max 100
  - Not duplicate tenant name

company_phone:
  - Optional
  - Valid phone format

accept_terms:
  - Must be true
```

#### Success Response (201)
```json
{
  "success": true,
  "message": "Registration successful. Welcome to Real Estate CRM!",
  "data": {
    "user": {
      "id": "550e8400-e29b-41d4-a716-446655440000",
      "email": "admin@btmgroup.com",
      "first_name": "Ahmad",
      "last_name": "Khan",
      "role": "TENANT_OWNER",
      "status": "ACTIVE",
      "created_at": "2026-04-11T10:00:00Z"
    },
    "tenant": {
      "id": "660e8400-e29b-41d4-a716-446655440000",
      "tenant_code": "BTM",
      "company_name": "BTM Group",
      "subscription_plan": "FREE",
      "status": "ACTIVE"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
      "expires_in": 3600,
      "token_type": "Bearer"
    }
  }
}
```

---

## ❌ Error Responses

### Email Already Exists (409)
```json
{
  "success": false,
  "message": "Email already registered",
  "error": {
    "field": "email",
    "code": "DUPLICATE_EMAIL",
    "details": "This email is already in use"
  }
}
```

### Weak Password (400)
```json
{
  "success": false,
  "message": "Password doesn't meet requirements",
  "error": {
    "field": "password",
    "code": "WEAK_PASSWORD",
    "details": "Must contain uppercase, lowercase, number, and special character"
  }
}
```

### Validation Failed (400)
```json
{
  "success": false,
  "message": "Validation failed",
  "error": {
    "fields": [
      {
        "field": "first_name",
        "message": "Must be at least 2 characters"
      },
      {
        "field": "company_name",
        "message": "Company name is required"
      }
    ]
  }
}
```

### Terms Not Accepted (400)
```json
{
  "success": false,
  "message": "You must accept terms and conditions",
  "error": {
    "field": "accept_terms",
    "code": "TERMS_REQUIRED"
  }
}
```

---

## 🛠️ Implementation Components

### 1. Signup Validator
```python
# validators/auth/signup_validator.py
def validate_signup(data):
    # Email validation
    # Password strength check
    # Company name validation
    # Phone validation
    # Terms acceptance
    # Return validated data or errors
```

### 2. Signup Service
```python
# services/auth/signup_service.py
class SignupService:
    def register_user(data):
        # Validate input
        # Create tenant
        # Create user
        # Hash password
        # Generate tokens
        # Send welcome email
        # Return user + tokens
```

### 3. Signup Controller
```python
# controllers/auth/signup_controller.py
@router.post("/signup")
async def signup(request: SignupRequest):
    # Validate input
    # Try: register user via service
    # Catch: handle errors
    # Return response
```

### 4. Auth Middleware
```python
# middlewares/auth_middleware.py
def verify_token(token):
    # Decode JWT
    # Check expiry
    # Extract claims
    # Return user info
```

---

## 📧 Welcome Email Template

```html
Subject: Welcome to Real Estate CRM! 🎉

Dear {{first_name}},

Your account has been successfully created!

Company Name: {{company_name}}
Email: {{email}}
Tenant Code: {{tenant_code}}

Next Steps:
1. Verify your email address
2. Complete company profile
3. Add team members
4. Create your first deal

Get Started: [Button: Go to Dashboard]

Questions? Contact support@realestatecr.com

Best regards,
Real Estate CRM Team
```

---

## 🔒 Security Considerations

| Point | Implementation |
|-------|-----------------|
| Password Storage | bcrypt 12 rounds |
| Email Verification | OTP or magic link |
| Brute Force | Rate limiting (5 attempts / 15 min) |
| SQL Injection | Parameterized queries |
| CSRF | Token validation |
| XSS | Input sanitization |
| Token Security | HttpOnly cookies |

---

## ✅ Signup Checklist

- [ ] Signup validator implemented
- [ ] Signup service implemented
- [ ] Signup controller implemented
- [ ] Email validation logic
- [ ] Password strength validation
- [ ] Duplicate email check
- [ ] Tenant creation logic
- [ ] User creation logic
- [ ] Token generation
- [ ] Welcome email sending
- [ ] Error handling
- [ ] Rate limiting
- [ ] Swagger documentation
- [ ] Unit tests (80%+ coverage)
- [ ] Integration tests
- [ ] Load testing
