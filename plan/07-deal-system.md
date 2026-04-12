# 🎯 Deal Management System (CORE)

## 📋 Overview
Core deal management system handling end-to-end deal lifecycle, deal generation, and deal tracking.

---

## 🆔 Deal ID Format

```
{TENANT_CODE}-{PROJECT_CODE}-{PLOT_NUMBER}-{YEAR}-{SEQUENCE}

Examples:
BTM-GW-045-2026-000001
GW-DHA6-123-2026-000045
DHA-PH6-089-2026-000012
```

---

## 📊 Deal Data Model

```yaml
deal:
  # Primary
  id: UUID
  tenant_id: UUID (Multi-tenant)
  deal_id: String (Unique: BTM-GW-045-2026-000001)
  
  # Deal Components
  client_id: UUID (Foreign Key)
  project_id: UUID (Foreign Key)
  plot_id: UUID (Foreign Key)
  
  # People
  salesman_id: UUID (optional)
  dealer_id: UUID (optional)
  createdby_user_id: UUID
  
  # Financial
  total_amount: Decimal (plot price)
  advance_payment: Decimal (required, usually 10%)
  outstanding_balance: Decimal
  
  # Deal Structure
  deal_structure: JSON
    - advance: Decimal
    - installments: Array
      - month: Integer
      - amount: Decimal
      - due_date: Date
  
  # Status
  status: String (CREATED, ACTIVE, COMPLETED, DEFAULTED, CANCELLED)
  
  # Commission
  salesman_commission_percentage: Float
  dealer_commission_percentage: Float
  
  # Dates
  deal_date: DateTime
  signed_date: DateTime (optional)
  completion_date: DateTime (optional)
  
  # Tracking
  notes: String
  created_at: DateTime
  updated_at: DateTime
  created_by: UUID
```

---

## 🔄 Deal Creation Flow

```
POST /api/deals (Create Deal)
  ↓
Validate:
  - Client exists
  - Plot available
  - Amount = plot price
  - Advance payment >= 10%
  ↓
Create Deal record
  ↓
Generate Deal ID (BTM-GW-045-2026-000001)
  ↓
Generate Payment Plan (auto-installments)
  ↓
Transition Plot to RESERVED
  ↓
Send Confirmation Email/WhatsApp
  ↓
Return Deal + Payment Plan
```

---

## 🛣️ Deal API Endpoints

### Create Deal
```
POST /api/deals

Headers:
Authorization: Bearer operator_token

Request Body:
{
  "client_id": "client_uuid",
  "project_id": "project_uuid",
  "plot_id": "plot_uuid",
  "total_amount": 2500000,
  "advance_payment": 250000,
  "payment_plan_type": "MONTHLY",
  "installment_months": 12,
  "salesman_id": "user_uuid",
  "dealer_id": "user_uuid",
  "notes": "Discounted rate due to quick payment"
}

Response (201):
{
  "success": true,
  "message": "Deal created successfully",
  "data": {
    "id": "deal_uuid",
    "deal_id": "BTM-GW-045-2026-000001",
    "client": { ... },
    "project": { ... },
    "plot": { ... },
    "total_amount": 2500000,
    "outstanding_balance": 2250000,
    "status": "CREATED",
    "payment_plan": {
      "advance": 250000,
      "installments": [
        {
          "month": 1,
          "amount": 187500,
          "due_date": "2026-05-11"
        },
        ...
      ]
    },
    "created_at": "2026-04-11T10:00:00Z"
  }
}
```

### List Deals (with comprehensive filters)
```
GET /api/deals?status=ACTIVE&project_id=...&client_search=ali&page=1&limit=20

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "deal_uuid",
      "deal_id": "BTM-GW-045-2026-000001",
      "client_name": "Ali Ahmed Khan",
      "project": "Grand View",
      "plot_number": "045",
      "total_amount": 2500000,
      "paid_amount": 250000,
      "outstanding_balance": 2250000,
      "status": "ACTIVE",
      "created_date": "2026-04-10"
    },
    ...
  ],
  "pagination": { ... }
}
```

### Get Deal Details
```
GET /api/deals/{deal_id}

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "id": "deal_uuid",
    "deal_id": "BTM-GW-045-2026-000001",
    "client": { ... },
    "project": { ... },
    "plot": { ... },
    "total_amount": 2500000,
    "paid_amount": 250000,
    "outstanding_balance": 2250000,
    "status": "ACTIVE",
    "payment_plan": { ... },
    "payments": [array of payment records],
    "commission": {
      "salesman": { percentage: 2, amount: 50000 },
      "dealer": { percentage: 3, amount: 75000 }
    },
    "created_at": "2026-04-10T10:00:00Z"
  }
}
```

### Update Deal
```
PATCH /api/deals/{deal_id}

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "notes": "Updated notes",
  "salesman_id": "new_salesman_uuid"
}

Response (200):
{
  "success": true,
  "data": { ... }
}
```

### Complete Deal
```
POST /api/deals/{deal_id}/complete

Headers:
Authorization: Bearer accountant_token

Request Body:
{
  "completion_notes": "All payments received"
}

Response (200):
{
  "success": true,
  "message": "Deal completed",
  "data": {
    "id": "deal_uuid",
    "status": "COMPLETED",
    "completed_date": "2026-04-11T10:00:00Z"
  }
}
```

### Mark Deal as Defaulted
```
POST /api/deals/{deal_id}/default

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "reason": "Client unable to pay",
  "action": "HOLD" or "CANCEL"
}

Response (200):
{
  "success": true,
  "message": "Deal marked as defaulted",
  "data": {
    "id": "deal_uuid",
    "status": "DEFAULTED"
  }
}
```

### Get Deal Payment History
```
GET /api/deals/{deal_id}/payments

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "deal_id": "BTM-GW-045-2026-000001",
    "total_due": 2500000,
    "total_paid": 500000,
    "outstanding": 2000000,
    "payments": [
      {
        "id": "payment_uuid",
        "amount": 250000,
        "date": "2026-04-01",
        "type": "ADVANCE",
        "receipt_id": "...",
        "status": "PAID"
      },
      {
        "id": "payment_uuid",
        "amount": 250000,
        "date": "2026-05-11",
        "type": "INSTALLMENT",
        "status": "PAID"
      }
    ]
  }
}
```

### Cancel Deal
```
POST /api/deals/{deal_id}/cancel

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "reason": "Client request"
}

Response (200):
{
  "success": true,
  "message": "Deal cancelled, plot released",
  "data": {
    "id": "deal_uuid",
    "status": "CANCELLED"
  }
}
```

---

## 📊 Deal Status Lifecycle

```
CREATED (Just created, awaiting signature)
  ↓
ACTIVE (Signed, in payment)
  ↓
COMPLETED (Full payment, delivery done)
  
OR

DEFAULTED (Client unable to pay)
  ↓
CANCELLED (Deal cancelled, plot released)
```

---

## 💰 Deal Financial Summary

```json
{
  "deal_id": "BTM-GW-045-2026-000001",
  "total_amount": 2500000,
  "paid_to_date": 750000,
  "outstanding_balance": 1750000,
  "breakdown": {
    "advance": {
      "due": 250000,
      "paid": 250000,
      "status": "PAID"
    },
    "installments": {
      "due": 2250000,
      "paid": 500000,
      "pending": 1750000,
      "overdue": 0
    }
  }
}
```

---

## ✅ Deal System Checklist

- [ ] Deal model created
- [ ] Deal ID generation logic
- [ ] Deal creation validator
- [ ] Create deal endpoint
- [ ] List deals endpoint (with filters)
- [ ] Get deal details endpoint
- [ ] Update deal endpoint
- [ ] Complete deal logic
- [ ] Mark deal defaulted logic
- [ ] Cancel deal logic
- [ ] Payment plan auto-generation
- [ ] Plot reservation on deal creation
- [ ] Plot release on deal cancellation
- [ ] Deal service
- [ ] Deal controller
- [ ] Deal repository
- [ ] Swagger documentation
- [ ] Unit tests (80%+)
- [ ] Integration tests
