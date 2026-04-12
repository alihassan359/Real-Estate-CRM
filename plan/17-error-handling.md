# 🆘 Error Handling & Status Codes

## 📋 Overview
Comprehensive error handling strategy with consistent error responses and HTTP status codes.

---

## ✅ HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| **200** | OK | Successful GET/PATCH |
| **201** | Created | Successful POST |
| **204** | No Content | Successful DELETE |
| **400** | Bad Request | Invalid input data |
| **401** | Unauthorized | Missing/invalid token |
| **403** | Forbidden | Missing permissions |
| **404** | Not Found | Resource doesn't exist |
| **409** | Conflict | Duplicate email/CNIC |
| **422** | Unprocessable | Validation failed |
| **429** | Too Many Requests | Rate limit exceeded |
| **500** | Server Error | Unexpected error |
| **503** | Service Unavailable | DB down, etc |

---

## 📊 Error Response Format

### Standard Error Response
```json
{
  "success": false,
  "message": "Human-readable error message",
  "error": {
    "code": "ERROR_CODE",
    "type": "ERROR_TYPE",
    "details": {}
  }
}
```

### Validation Error (400)
```json
{
  "success": false,
  "message": "Validation failed",
  "error": {
    "type": "VALIDATION_ERROR",
    "fields": [
      {
        "field": "email",
        "message": "Email is required",
        "code": "REQUIRED_FIELD"
      },
      {
        "field": "password",
        "message": "Password must be at least 8 characters",
        "code": "MIN_LENGTH"
      }
    ]
  }
}
```

### Authentication Error (401)
```json
{
  "success": false,
  "message": "Unauthorized",
  "error": {
    "code": "AUTH_FAILED",
    "type": "AUTHENTICATION_ERROR",
    "details": {
      "reason": "Invalid credentials"
    }
  }
}
```

### Permission Error (403)
```json
{
  "success": false,
  "message": "Forbidden",
  "error": {
    "code": "PERMISSION_DENIED",
    "type": "AUTHORIZATION_ERROR",
    "details": {
      "required_permission": "create_deal",
      "user_role": "OPERATOR"
    }
  }
}
```

### Not Found Error (404)
```json
{
  "success": false,
  "message": "Resource not found",
  "error": {
    "code": "NOT_FOUND",
    "type": "RESOURCE_ERROR",
    "details": {
      "resource_type": "client",
      "resource_id": "uuid"
    }
  }
}
```

### Conflict Error (409)
```json
{
  "success": false,
  "message": "Email already registered",
  "error": {
    "code": "DUPLICATE_EMAIL",
    "type": "CONSTRAINT_ERROR",
    "details": {
      "field": "email",
      "value": "user@example.com"
    }
  }
}
```

### Rate Limit Error (429)
```json
{
  "success": false,
  "message": "Too many requests",
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "type": "RATE_LIMIT_ERROR",
    "details": {
      "retry_after": 900,
      "limit": 5,
      "window": "15 minutes"
    }
  }
}
```

### Server Error (500)
```json
{
  "success": false,
  "message": "Internal server error",
  "error": {
    "code": "INTERNAL_ERROR",
    "type": "SERVER_ERROR",
    "details": {
      "request_id": "req-uuid",
      "timestamp": "2026-04-11T10:30:00Z"
    }
  }
}
```

---

## 🛠️ Error Handling Implementation

### Global Exception Handler
```python
# middlewares/exception_handler.py

from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            'success': False,
            'message': 'Internal server error',
            'error': {
                'code': 'INTERNAL_ERROR',
                'request_id': request.headers.get('request-id'),
            }
        }
    )
```

### Custom Exception Classes
```python
# exceptions.py

class AppException(Exception):
    def __init__(self, message, code, status_code, details=None):
        self.message = message
        self.code = code
        self.status_code = status_code
        self.details = details or {}

class ValidationException(AppException):
    def __init__(self, message, fields=None):
        super().__init__(
            message=message,
            code='VALIDATION_ERROR',
            status_code=400,
            details={'fields': fields}
        )

class AuthenticationException(AppException):
    def __init__(self, message='Unauthorized'):
        super().__init__(
            message=message,
            code='AUTH_FAILED',
            status_code=401
        )

class AuthorizationException(AppException):
    def __init__(self, message='Forbidden', perm=None):
        super().__init__(
            message=message,
            code='PERMISSION_DENIED',
            status_code=403,
            details={'required_permission': perm}
        )

class NotFoundException(AppException):
    def __init__(self, resource_type, resource_id):
        super().__init__(
            message=f'{resource_type} not found',
            code='NOT_FOUND',
            status_code=404,
            details={'resource_type': resource_type, 'resource_id': resource_id}
        )

class DuplicateException(AppException):
    def __init__(self, field, value):
        super().__init__(
            message=f'{field} already exists',
            code=f'DUPLICATE_{field.upper()}',
            status_code=409,
            details={'field': field, 'value': value}
        )
```

### Usage in Controllers
```python
# controllers/auth/signup_controller.py

@router.post('/signup')
async def signup(request: SignupRequest):
    try:
        # Validate email uniqueness
        existing = await User.get(email=request.email)
        if existing:
            raise DuplicateException('email', request.email)
        
        # Validate password strength
        pwd_errors = PasswordService.validate_password_strength(request.password)
        if pwd_errors:
            raise ValidationException(
                'Password validation failed',
                fields=[{'field': 'password', 'message': err} for err in pwd_errors]
            )
        
        # Process signup
        user = await signup_service.register_user(request)
        
        return {
            'success': True,
            'message': 'Registration successful',
            'data': user
        }
        
    except DuplicateException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                'success': False,
                'message': e.message,
                'error': {'code': e.code, 'details': e.details}
            }
        )
```

---

## 📝 Error Codes Reference

| Code | HTTP | Description | Action |
|------|------|-------------|--------|
| `VALIDATION_ERROR` | 400 | Input validation failed | Retry with correct data |
| `AUTH_FAILED` | 401 | Authentication failed | Login again |
| `TOKEN_EXPIRED` | 401 | JWT token expired | Use refresh token |
| `PERMISSION_DENIED` | 403 | Insufficient permissions | Admin action needed |
| `NOT_FOUND` | 404 | Resource not found | Check resource ID |
| `DUPLICATE_EMAIL` | 409 | Email already exists | Use different email |
| `DUPLICATE_CNIC` | 409 | CNIC already exists | Contact support |
| `PLOT_NOT_AVAILABLE` | 409 | Plot already sold | Choose different plot |
| `INSUFFICIENT_BALANCE` | 400 | Payment exceeds balance | Check deal balance |
| `RATE_LIMIT_EXCEEDED` | 429 | Too many requests | Retry after timeout |
| `DATABASE_ERROR` | 500 | Database operation failed | Retry later |
| `EXTERNAL_SERVICE_ERROR` | 503 | Third-party service error | Retry later |
| `INTERNAL_ERROR` | 500 | Unexpected error | Contact support |

---

## 🔍 Request Tracing

```python
# middlewares/request_tracing.py

import uuid
from fastapi import Request

@app.middleware('http')
async def add_request_id(request: Request, call_next):
    request_id = request.headers.get('x-request-id') or str(uuid.uuid4())
    
    # Log request
    logger.info(f'Request: {request_id} {request.method} {request.url.path}')
    
    try:
        response = await call_next(request)
        response.headers['x-request-id'] = request_id
        
        # Log response
        logger.info(f'Response: {request_id} {response.status_code}')
        return response
        
    except Exception as e:
        logger.error(f'Error: {request_id} {str(e)}')
        raise
```

---

## ✅ Error Handling Checklist

- [ ] Global exception handler
- [ ] Custom exception classes
- [ ] HTTP status codes documented
- [ ] Error response format consistent
- [ ] Error codes standardized
- [ ] Validation error formatting
- [ ] Authentication error handling
- [ ] Authorization error handling
- [ ] Not found error handling
- [ ] Duplicate error handling
- [ ] Rate limit error handling
- [ ] Server error handling
- [ ] Request tracing/logging
- [ ] Error logging without sensitive data
- [ ] Error recovery mechanisms
- [ ] Client-friendly error messages
- [ ] Swagger error documentation
- [ ] Error unit tests
