# ✅ Input Validation & Data Integrity

## 📋 Overview
Comprehensive validation system for all input data, business rules enforcement, and data integrity.

---

## 🎯 Validation Layers

```
Request
  ↓
Route Parameter Validation (FastAPI)
  ↓
Request Body Schema Validation (Pydantic)
  ↓
Business Logic Validation (Validator Service)
  ↓
Database Constraints
  ↓
Response
```

---

## 📊 Validation Examples

### Signup Validation
```python
# validators/auth/signup_validator.py

from pydantic import BaseModel, validator, EmailStr
import re

class SignupRequest(BaseModel):
    email: EmailStr  # Auto-validates email format
    password: str
    confirm_password: str
    first_name: str
    last_name: str
    company_name: str
    company_phone: str
    
    @validator('password')
    def validate_password(cls, v):
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain uppercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain number')
        if not re.search(r'[!@#$%^&*]', v):
            raise ValueError('Password must contain special character')
        return v
    
    @validator('confirm_password')
    def passwords_match(cls, v, values):
        if 'password' in values and v != values['password']:
            raise ValueError('Passwords do not match')
        return v
    
    @validator('first_name', 'last_name')
    def name_length(cls, v):
        if len(v) < 2:
            raise ValueError('Name must be at least 2 characters')
        if len(v) > 50:
            raise ValueError('Name must not exceed 50 characters')
        return v
    
    @validator('company_name')
    def company_name_length(cls, v):
        if len(v) < 3:
            raise ValueError('Company name must be at least 3 characters')
        if len(v) > 100:
            raise ValueError('Company name must not exceed 100 characters')
        return v
```

### Client Validation
```python
# validators/client/create_client_validator.py

class CreateClientRequest(BaseModel):
    full_name: str
    email: EmailStr
    phone: str
    whatsapp_phone: Optional[str]
    cnic: str
    cnic_expiry: date
    city: str
    country: str
    occupation: Optional[str]
    
    @validator('full_name')
    def validate_full_name(cls, v):
        if len(v) < 5:
            raise ValueError('Full name must be at least 5 characters')
        return v
    
    @validator('phone', 'whatsapp_phone')
    def validate_phone(cls, v):
        if not re.match(r'^\+92-\d{3}-\d{7}$', v or ''):
            if v:
                raise ValueError('Phone must be in format: +92-300-1234567')
        return v
    
    @validator('cnic')
    def validate_cnic(cls, v):
        # CNIC format: 12345-6789012-3
        if not re.match(r'^\d{5}-\d{7}-\d{1}$', v):
            raise ValueError('Invalid CNIC format')
        return v
    
    @validator('cnic_expiry')
    def validate_cnic_expiry(cls, v):
        if v < date.today():
            raise ValueError('CNIC must not be expired')
        return v
```

### Deal Validation
```python
# validators/deal/create_deal_validator.py

class CreateDealRequest(BaseModel):
    client_id: UUID
    project_id: UUID
    plot_id: UUID
    total_amount: Decimal
    advance_payment: Decimal
    payment_plan_type: str
    installment_months: int
    
    @validator('total_amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v
    
    @validator('advance_payment')
    def validate_advance(cls, v, values):
        if v <= 0:
            raise ValueError('Advance payment must be greater than 0')
        
        if 'total_amount' in values:
            min_advance = values['total_amount'] * Decimal('0.1')  # 10% minimum
            if v < min_advance:
                raise ValueError(f'Advance must be at least 10% (PKR {min_advance})')
        
        return v
    
    @validator('installment_months')
    def validate_months(cls, v):
        if v < 1 or v > 60:
            raise ValueError('Installment months must be between 1 and 60')
        return v
```

### Payment Validation
```python
# validators/payment/record_payment_validator.py

class RecordPaymentRequest(BaseModel):
    amount: Decimal
    payment_type: str
    payment_date: datetime
    method: str
    reference_number: Optional[str]
    notes: Optional[str]
    
    @validator('amount')
    def validate_amount(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v
    
    @validator('payment_type')
    def validate_type(cls, v):
        valid_types = ['ADVANCE', 'INSTALLMENT', 'BUBBLE', 'FINAL', 'EXTRA']
        if v not in valid_types:
            raise ValueError(f'Payment type must be one of: {valid_types}')
        return v
    
    @validator('method')
    def validate_method(cls, v):
        valid_methods = ['CASH', 'CHECK', 'BANK_TRANSFER', 'CARD']
        if v not in valid_methods:
            raise ValueError(f'Payment method must be one of: {valid_methods}')
        return v
    
    @validator('payment_date')
    def validate_date(cls, v):
        if v > datetime.now():
            raise ValueError('Payment date cannot be in the future')
        return v
    
    @validator('reference_number')
    def validate_reference(cls, v, values):
        if values.get('method') == 'BANK_TRANSFER' and not v:
            raise ValueError('Reference number required for bank transfer')
        return v
```

---

## 🧪 Business Rule Validators

```python
# validators/business_rules_validator.py

class BusinessRulesValidator:
    @staticmethod
    async def validate_client_exists(tenant_id, client_id):
        client = await Client.get(id=client_id, tenant_id=tenant_id)
        if not client:
            raise ValueError('Client not found')
        return client
    
    @staticmethod
    async def validate_plot_available(tenant_id, plot_id):
        plot = await Plot.get(id=plot_id, tenant_id=tenant_id)
        if not plot:
            raise ValueError('Plot not found')
        if plot.status != 'AVAILABLE':
            raise ValueError(f'Plot is not available (Status: {plot.status})')
        return plot
    
    @staticmethod
    async def validate_deal_amount(total_amount, plot_price):
        # Deal amount should match plot price (with 5% tolerance)
        tolerance = plot_price * Decimal('0.05')
        if abs(total_amount - plot_price) > tolerance:
            raise ValueError(
                f'Deal amount must be within 5% of plot price: {plot_price}'
            )
    
    @staticmethod
    async def validate_payment_not_exceeds_balance(deal):
        # Validate payment doesn't exceed outstanding balance
        if deal.outstanding_balance <= 0:
            raise ValueError('All payments for this deal have been made')
    
    @staticmethod
    async def validate_user_permission(user, required_permission):
        if required_permission not in user.permissions:
            raise PermissionError(f'Missing permission: {required_permission}')
    
    @staticmethod
    async def validate_tenant_isolation(user_tenant_id, resource_tenant_id):
        if user_tenant_id != resource_tenant_id:
            raise PermissionError('Cross-tenant access denied')
```

---

## 🔍 Data Integrity Checks

```python
# validators/data_integrity_validator.py

class DataIntegrityValidator:
    @staticmethod
    async def validate_deal_financial_balance(deal):
        # Total paid + outstanding should equal deal amount
        total_checked = deal.paid_amount + deal.outstanding_balance
        
        if abs(total_checked - deal.total_amount) > Decimal('0.01'):
            raise ValueError('Deal financial balance mismatch')
    
    @staticmethod
    async def validate_payment_plan_consistency(payment_plan):
        # Installments total should equal payment plan total
        installment_total = sum(inst.amount for inst in payment_plan.installments)
        advance_total = payment_plan.advance
        
        if abs(installment_total + advance_total - payment_plan.total_amount) > Decimal('0.01'):
            raise ValueError('Payment plan total mismatch')
    
    @staticmethod
    async def validate_no_duplicate_cnic(tenant_id, cnic, exclude_client_id=None):
        query = Client.filter(tenant_id=tenant_id, cnic=cnic)
        
        if exclude_client_id:
            query = query.exclude(id=exclude_client_id)
        
        existing = await query.first()
        if existing:
            raise ValueError('CNIC already registered')
```

---

## 🛡️ Error Response Format

```python
# utils/error_response.py

class ValidationError(Exception):
    def __init__(self, message, errors=None, fields=None):
        self.message = message
        self.errors = errors
        self.fields = fields

# Response format:
{
  "success": false,
  "message": "Validation failed",
  "error": {
    "type": "VALIDATION_ERROR",
    "fields": [
      {
        "field": "email",
        "message": "Email already exists",
        "code": "DUPLICATE_EMAIL"
      },
      {
        "field": "password",
        "message": "Password must contain uppercase letter",
        "code": "WEAK_PASSWORD"
      }
    ]
  }
}
```

---

## ✅ Validation Checklist

- [ ] Pydantic schemas for all requests
- [ ] Email validation
- [ ] Password strength validation
- [ ] Phone format validation
- [ ] CNIC format validation
- [ ] Currency/Amount validation
- [ ] Date validation
- [ ] Enum validation
- [ ] Unique constraint validation
- [ ] Cross-field validation
- [ ] Business rule validation
- [ ] Data integrity checks
- [ ] Tenant isolation validation
- [ ] Permission validation
- [ ] Error handling & formatting
- [ ] Input sanitization
- [ ] SQL injection prevention
- [ ] XSS prevention
- [ ] Unit tests for validators
