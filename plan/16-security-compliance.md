# 🔐 Security & Compliance

## 📋 Overview
Comprehensive security measures, data protection, and compliance framework.

---

## 🛡️ Security Layers

```
Request
  ↓
HTTPS/TLS Encryption
  ↓
CORS Protection
  ↓
Rate Limiting
  ↓
JWT Authentication
  ↓
Authorization (RBAC)
  ↓
Input Validation & Sanitization
  ↓
SQL Prevention
  ↓
Audit Logging
```

---

## 🔑 Authentication & JWT

### JWT Implementation
```python
# utils/jwt.py

from datetime import datetime, timedelta
import jwt

class JWTService:
    SECRET_KEY = os.getenv('JWT_SECRET_KEY')
    ALGORITHM = 'HS256'
    ACCESS_TOKEN_EXPIRE_HOURS = 1
    REFRESH_TOKEN_EXPIRE_DAYS = 7
    
    @staticmethod
    def create_access_token(user_id, tenant_id, role):
        payload = {
            'sub': str(user_id),
            'user_id': str(user_id),
            'tenant_id': str(tenant_id),
            'role': role,
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def create_refresh_token(user_id):
        payload = {
            'sub': str(user_id),
            'type': 'refresh',
            'iat': datetime.utcnow(),
            'exp': datetime.utcnow() + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    @staticmethod
    def verify_token(token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.ExpiredSignatureError:
            raise Exception('Token expired')
        except jwt.InvalidTokenError:
            raise Exception('Invalid token')
```

---

## 🔒 Password Security

### Password Hashing
```python
# utils/password.py

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

class PasswordService:
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def validate_password_strength(password: str):
        errors = []
        
        if len(password) < 8:
            errors.append('Password must be at least 8 characters')
        if not any(c.isupper() for c in password):
            errors.append('Password must contain uppercase letter')
        if not any(c.islower() for c in password):
            errors.append('Password must contain lowercase letter')
        if not any(c.isdigit() for c in password):
            errors.append('Password must contain number')
        if not any(c in '!@#$%^&*' for c in password):
            errors.append('Password must contain special character')
        
        return errors if errors else None
```

---

## 🚫 Rate Limiting

### FastAPI Rate Limiting
```python
# middlewares/rate_limit_middleware.py

from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

# Apply limits
@app.post('/api/auth/login')
@limiter.limit('5/15minutes')
async def login(request):
    # Login endpoint
    pass

@app.post('/api/auth/signup')
@limiter.limit('3/hour')
async def signup(request):
    # Signup endpoint
    pass
```

---

## 🔍 Input Validation & Sanitization

### SQL Injection Prevention
```python
# All queries use parameterized queries (ORM)

# ✅ SAFE
user = await User.get(email=user_email)

# ❌ DANGEROUS
user = await db.query(f'SELECT * FROM users WHERE email = {user_email}')
```

### XSS Prevention
```python
# Input sanitization
from bleach import clean

@validator('notes')
def sanitize_notes(cls, v):
    return clean(v, tags=[], strip=True)
```

### CSRF Protection
```python
from fastapi_csrf_protect import CsrfProtect

@app.post('/api/deals')
async def create_deal(request, csrf_protect: CsrfProtect = Depends()):
    await csrf_protect.validate_csrf(request)
    # Process request
```

---

## 🔐 Data Encryption

### Sensitive Field Encryption
```python
# config/encryption.py

from cryptography.fernet import Fernet

cipher = Fernet(os.getenv('ENCRYPTION_KEY').encode())

def encrypt_field(value: str) -> str:
    return cipher.encrypt(value.encode()).decode()

def decrypt_field(encrypted: str) -> str:
    return cipher.decrypt(encrypted.encode()).decode()

# Usage in model
class Client(BaseModel):
    cnic: str
    
    def __init__(self, **data):
        super().__init__(**data)
        # Auto-encrypt CNIC
        if self.cnic:
            self.cnic = encrypt_field(self.cnic)
```

---

## 📝 Sensitive Data Handling

### Never Log Sensitive Data
```python
# ❌ WRONG
logger.info(f'User login: {user_email} with password: {password}')

# ✅ CORRECT
logger.info(f'User login: {user_id}')
logger.debug(f'Password verification for user: {user_id}')
```

### Mask Sensitive Output
```python
def mask_cnic(cnic: str) -> str:
    if len(cnic) != 15:  # CNIC length
        return '*****-*****-*'
    return f'{cnic[:5]}-****-{cnic[-1]}'

# Usage
client = await Client.get(id=client_id)
masked_cnic = mask_cnic(decrypt_field(client.cnic))
return {'cnic': masked_cnic}
```

---

## 🔐 CORS Configuration

```python
# config/cors.py

from fastapi.middleware.cors import CORSMiddleware

origins = [
    'http://localhost:3000',  # Dev
    'https://app.realestatecr.com',  # Production
    'https://admin.realestatecr.com',  # Admin
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
```

---

## 📋 Audit & Logging

### Audit Trail
```python
# models/audit_log.py

class AuditLog(BaseModel):
    id: UUID
    tenant_id: UUID
    user_id: UUID
    action: String (CREATE, UPDATE, DELETE)
    resource_type: String (DEAL, PAYMENT, CLIENT)
    resource_id: UUID
    old_values: JSON
    new_values: JSON
    ip_address: String
    user_agent: String
    created_at: DateTime

# Log all changes
async def log_audit(
    user_id, action, resource_type, resource_id, 
    old_values=None, new_values=None
):
    audit = AuditLog(
        user_id=user_id,
        action=action,
        resource_type=resource_type,
        resource_id=resource_id,
        old_values=old_values,
        new_values=new_values
    )
    await audit.save()
```

---

## 🛡️ Compliance Checklist

- [ ] HTTPS/TLS enabled (production)
- [ ] Password hashing (bcrypt)
- [ ] JWT authentication
- [ ] Token expiry enforcement
- [ ] RBAC implementation
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] CSRF protection
- [ ] Data encryption (sensitive fields)
- [ ] Audit logging
- [ ] Sensitive data masking
- [ ] No hardcoded secrets
- [ ] Environment variables secure
- [ ] Security headers (X-Frame-Options, etc)
- [ ] OWASP Top 10 compliance
- [ ] Regular security audits
- [ ] Penetration testing
