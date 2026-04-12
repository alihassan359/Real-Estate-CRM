# 🤝 Client Management System

## 📋 Overview
Complete client management system for tracking real estate clients, their contact information, transaction history, and compliance data.

---

## 📊 Client Data Model

```yaml
client:
  # Primary
  id: UUID
  tenant_id: UUID (Multi-tenant isolation)
  client_code: String (Auto-generated: BTM-CLIENT-0001)
  
  # Personal Information
  full_name: String
  email: String
  phone: String
  whatsapp_phone: String (optional)
  
  # Identity
  cnic: String (Pakistan ID, validated, never logged fully)
  cnic_expiry: Date
  passport_number: String (optional)
  
  # Address
  address: String
  city: String
  country: String
  postal_code: String
  
  # Professional
  occupation: String
  company_name: String (optional)
  
  # Relationship
  referred_by: String (optional)
  referred_by_user_id: UUID (optional)
  primary_contact: String (phone or email)
  
  # Status
  status: String (ACTIVE, INACTIVE, BLACKLISTED)
  kyc_verified: Boolean
  kyc_document: String (URL)
  
  # Tracking
  total_deals: Integer (calculated)
  total_investments: Decimal (calculated)
  created_at: DateTime
  updated_at: DateTime
  created_by: UUID
  updated_by: UUID
```

---

## 🛣️ Client API Endpoints

### Create Client
```
POST /api/clients

Headers:
Authorization: Bearer token

Request Body:
{
  "full_name": "Ali Ahmed Khan",
  "email": "ali@example.com",
  "phone": "+92-300-1234567",
  "whatsapp_phone": "+92-300-1234567",
  "cnic": "12345-6789012-3",
  "cnic_expiry": "2030-12-31",
  "city": "Islamabad",
  "country": "Pakistan",
  "occupation": "Software Engineer",
  "company_name": "Tech Company",
  "referred_by": "Ahmed Hassan"
}

Response (201):
{
  "success": true,
  "message": "Client created successfully",
  "data": {
    "id": "client_uuid",
    "client_code": "BTM-CLIENT-0001",
    "full_name": "Ali Ahmed Khan",
    "email": "ali@example.com",
    "status": "ACTIVE",
    "created_at": "2026-04-11T10:00:00Z"
  }
}
```

### List Clients (with filters)
```
GET /api/clients?page=1&limit=20&status=ACTIVE&search=ali

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "client_uuid",
      "client_code": "BTM-CLIENT-0001",
      "full_name": "Ali Ahmed Khan",
      "email": "ali@example.com",
      "phone": "+92-300-1234567",
      "city": "Islamabad",
      "status": "ACTIVE",
      "kyc_verified": true,
      "total_deals": 3,
      "total_investments": 2500000
    },
    ...
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 156
  }
}
```

### Get Client Details
```
GET /api/clients/{client_id}

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "id": "client_uuid",
    "client_code": "BTM-CLIENT-0001",
    "full_name": "Ali Ahmed Khan",
    "email": "ali@example.com",
    "phone": "+92-300-1234567",
    "cnic": "12345-****-3",  // Masked
    "city": "Islamabad",
    "status": "ACTIVE",
    "total_deals": 3,
    "total_investments": 2500000,
    "created_at": "2026-03-15T10:00:00Z",
    "deals": [
      {
        "id": "deal_uuid",
        "deal_id": "BTM-GW-045-2026-000001",
        "project_name": "Grand View",
        "plot_number": "045",
        "amount": 1000000,
        "status": "ACTIVE"
      }
    ]
  }
}
```

### Update Client
```
PATCH /api/clients/{client_id}

Headers:
Authorization: Bearer token

Request Body:
{
  "phone": "+92-300-9876543",
  "whatsapp_phone": "+92-300-9876543",
  "city": "Lahore"
}

Response (200):
{
  "success": true,
  "message": "Client updated successfully",
  "data": { ... }
}
```

### Verify KYC
```
POST /api/clients/{client_id}/verify-kyc

Headers:
Authorization: Bearer accountant_token

Request Body:
{
  "document_url": "https://...",
  "verified_by": "user_uuid"
}

Response (200):
{
  "success": true,
  "message": "KYC verified",
  "data": {
    "id": "client_uuid",
    "kyc_verified": true,
    "kyc_document": "https://..."
  }
}
```

### Blacklist Client
```
POST /api/clients/{client_id}/blacklist

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "reason": "Payment default"
}

Response (200):
{
  "success": true,
  "message": "Client blacklisted",
  "data": {
    "id": "client_uuid",
    "status": "BLACKLISTED"
  }
}
```

### Get Client Ledger
```
GET /api/clients/{client_id}/ledger

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "client_id": "client_uuid",
    "full_name": "Ali Ahmed Khan",
    "total_due": 500000,
    "total_paid": 2000000,
    "transactions": [
      {
        "date": "2026-04-10",
        "type": "PAYMENT",
        "amount": 100000,
        "description": "Deal BTM-GW-045-2026-000001 Installment",
        "balance": 500000
      },
      ...
    ]
  }
}
```

### Bulk Import Clients (CSV)
```
POST /api/clients/import

Headers:
Authorization: Bearer owner_token
Content-Type: multipart/form-data

File: clients.csv
(full_name,email,phone,city,cnic)

Response (200):
{
  "success": true,
  "message": "50 clients imported, 2 errors",
  "data": {
    "imported": 50,
    "errors": 2,
    "error_details": [
      {
        "row": 3,
        "error": "Invalid email format"
      }
    ]
  }
}
```

---

## 🔒 CNIC Security Rules

| Rule | Implementation |
|------|-----------------|
| Never Log Fully | Always mask: 12345-****-3 |
| Encrypt in DB | AES-256 encryption |
| Validate Format | Pakistan CNIC format |
| Check Expiry | Validate expiry date |
| PII Protection | Limited access (ACCOUNTANT, OWNER) |

---

## 📋 Client Validators

```python
# validators/client/create_client_validator.py

def validate_create_client(data):
    # Validate full_name (required, 5-100 chars)
    # Validate email format
    # Validate phone format
    # Validate CNIC format & uniqueness
    # Validate city
    # Validate country
    return validated_data or errors
```

---

## 🛠️ Client Service

```python
# services/client/client_service.py

class ClientService:
    async def create_client(tenant_id, data):
        # Validate input
        # Check CNIC uniqueness in tenant
        # Generate client_code
        # Create client record
        # Return client
    
    async def update_client(tenant_id, client_id, data):
        # Validate tenant access
        # Update fields
        # Log changes (audit)
        # Return updated client
    
    async def list_clients(tenant_id, filters):
        # Build query with tenant filter
        # Apply search/status filters
        # Return paginated results
    
    async def get_client_ledger(tenant_id, client_id):
        # Get all deals for client
        # Get all payments
        # Calculate balance
        # Return ledger
```

---

## 📊 Client Status Lifecycle

```
ACTIVE
  ↓
INACTIVE (No new deals)
  ↓
BLACKLISTED (Blocked from deals)
```

---

## ✅ Client Management Checklist

- [ ] Client model created
- [ ] Client code generation logic
- [ ] Create client endpoint
- [ ] List clients endpoint
- [ ] Get client details endpoint
- [ ] Update client endpoint
- [ ] Delete client (soft)
- [ ] Blacklist client endpoint
- [ ] KYC verification logic
- [ ] Client ledger calculation
- [ ] Bulk import functionality
- [ ] CNIC encryption
- [ ] CNIC masking in responses
- [ ] Client validators
- [ ] Client service
- [ ] Client controller
- [ ] Swagger documentation
- [ ] Unit tests (80%+)
- [ ] Integration tests
