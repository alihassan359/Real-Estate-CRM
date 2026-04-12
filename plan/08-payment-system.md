# 💳 Payment System (CORE)

## 📋 Overview
Core payment handling system managing installments, payments recording, ledger tracking, and payment status updates.

---

## 💰 Payment Types

| Type | When | Amount | Role |
|------|------|--------|------|
| **ADVANCE** | Deal creation | Usually 10% | ACCOUNTANT |
| **INSTALLMENT** | Monthly/Scheduled | Fixed monthly | ACCOUNTANT |
| **BUBBLE** | Mid-term | Configurable | ACCOUNTANT |
| **FINAL** | Completion | Remaining | ACCOUNTANT |
| **EXTRA** | Overpayment | Any | ACCOUNTANT |

---

## 📊 Payment Data Model

```yaml
payment:
  # Primary
  id: UUID
  tenant_id: UUID
  deal_id: UUID (Foreign Key)
  
  # Payment Details
  payment_date: DateTime
  amount: Decimal
  payment_type: String (ADVANCE, INSTALLMENT, BUBBLE, FINAL, EXTRA)
  method: String (CASH, CHECK, BANK_TRANSFER, CARD)
  
  # Reference
  installment_number: Integer (nullable)
  installment_due_date: Date (nullable)
  
  # Recording
  recorded_by: UUID (Accountant)
  reference_number: String (for BANK_TRANSFER, CHECK)
  notes: String
  
  # Status
  status: String (PENDING, PAID, CHEQUE_DEPOSITED, CHEQUE_CLEARED, FAILED)
  verification_date: DateTime (optional)
  verified_by: UUID (optional)
  
  # Auto-calculated
  balance_after_payment: Decimal
  
  # Tracking
  created_at: DateTime
  created_by: UUID
  updated_at: DateTime
  
payment_plan:
  id: UUID
  deal_id: UUID
  total_amount: Decimal
  structure_type: String (MONTHLY, CUSTOM)
  
  installments: Array
    - id: UUID
    - number: Integer
    - amount: Decimal
    - due_date: Date
    - paid_amount: Decimal
    - status: String (PENDING, PAID, OVERDUE)
    - paid_date: DateTime (optional)
```

---

## 🛣️ Payment API Endpoints

### Record Payment
```
POST /api/deals/{deal_id}/payments

Headers:
Authorization: Bearer accountant_token

Request Body:
{
  "amount": 250000,
  "payment_type": "ADVANCE",
  "payment_date": "2026-04-11",
  "method": "BANK_TRANSFER",
  "reference_number": "TRF-2026-001",
  "notes": "Advance payment received"
}

Response (201):
{
  "success": true,
  "message": "Payment recorded successfully",
  "data": {
    "id": "payment_uuid",
    "amount": 250000,
    "payment_type": "ADVANCE",
    "status": "PAID",
    "payment_date": "2026-04-11T10:00:00Z",
    "deal_balance_after": 2250000,
    "receipt_id": "receipt_uuid"
  }
}
```

### Get Payment Plan
```
GET /api/deals/{deal_id}/payment-plan

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "deal_id": "BTM-GW-045-2026-000001",
    "total_amount": 2500000,
    "structure_type": "MONTHLY",
    "breakdown": {
      "advance": 250000,
      "installments_count": 12,
      "installment_amount": 187500,
      "total_installments": 2250000
    },
    "payment_schedule": [
      {
        "id": "installment_uuid",
        "number": 1,
        "amount": 187500,
        "due_date": "2026-05-11",
        "paid_amount": 0,
        "status": "PENDING",
        "days_until_due": 30
      },
      {
        "id": "installment_uuid",
        "number": 2,
        "amount": 187500,
        "due_date": "2026-06-11",
        "paid_amount": 0,
        "status": "PENDING",
        "days_until_due": 61
      },
      ...
    ]
  }
}
```

### Get Deal Balance
```
GET /api/deals/{deal_id}/balance

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "deal_id": "BTM-GW-045-2026-000001",
    "client_name": "Ali Ahmed Khan",
    "deal_date": "2026-04-10",
    "deal_amount": 2500000,
    "paid_amount": 250000,
    "outstanding_balance": 2250000,
    "paid_percentage": 10,
    "next_due": {
      "amount": 187500,
      "due_date": "2026-05-11",
      "days_until_due": 30,
      "overdue": false
    },
    "payment_history": [
      {
        "date": "2026-04-11",
        "type": "ADVANCE",
        "amount": 250000,
        "method": "BANK_TRANSFER"
      }
    ]
  }
}
```

### Update Payment Status
```
PATCH /api/payments/{payment_id}/status

Headers:
Authorization: Bearer accountant_token

Request Body:
{
  "status": "CHEQUE_CLEARED",
  "verification_date": "2026-04-13"
}

Response (200):
{
  "success": true,
  "message": "Payment status updated",
  "data": {
    "id": "payment_uuid",
    "status": "CHEQUE_CLEARED"
  }
}
```

### List Payments (with filters)
```
GET /api/payments?deal_id=...&payment_type=INSTALLMENT&status=PENDING&page=1&limit=20

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "payment_uuid",
      "deal_id": "BTM-GW-045-2026-000001",
      "client_name": "Ali Ahmed Khan",
      "amount": 187500,
      "payment_type": "INSTALLMENT",
      "due_date": "2026-05-11",
      "status": "PENDING",
      "days_overdue": 0
    },
    ...
  ],
  "pagination": { ... }
}
```

### Get Payment Details
```
GET /api/payments/{payment_id}

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "id": "payment_uuid",
    "deal_id": "BTM-GW-045-2026-000001",
    "amount": 250000,
    "payment_type": "ADVANCE",
    "payment_date": "2026-04-11",
    "method": "BANK_TRANSFER",
    "reference_number": "TRF-2026-001",
    "status": "PAID",
    "recorded_by_name": "Ahmed Hassan",
    "notes": "Advance payment",
    "receipt": {
      "id": "receipt_uuid",
      "receipt_number": "REC-2026-000001",
      "amount": 250000,
      "date": "2026-04-11"
    }
  }
}
```

### Bulk Payment Recording (CSV Import)
```
POST /api/payments/bulk-import

Headers:
Authorization: Bearer accountant_token
Content-Type: multipart/form-data

File: payments.csv
(deal_id, amount, payment_date, method, reference_number)

Response (200):
{
  "success": true,
  "message": "25 payments recorded, 2 errors",
  "data": {
    "recorded": 25,
    "errors": 2,
    "error_details": [
      {
        "row": 5,
        "error": "Deal not found"
      }
    ]
  }
}
```

---

## 📊 Ledger (Client Perspective)

### Payment Ledger
```
GET /api/clients/{client_id}/ledger

Response:
{
  "client_id": "client_uuid",
  "client_name": "Ali Ahmed Khan",
  "summary": {
    "total_due": 2500000,
    "total_paid": 250000,
    "outstanding": 2250000,
    "overdue": 0
  },
  "deals": [
    {
      "deal_id": "BTM-GW-045-2026-000001",
      "project": "Grand View",
      "due": 2500000,
      "paid": 250000,
      "outstanding": 2250000,
      "transactions": [
        {
          "date": "2026-04-11",
          "type": "ADVANCE",
          "debit": 250000,
          "balance": 2250000
        }
      ]
    }
  ]
}
```

---

## 🔴 Late Payment Detection

```python
# Background Job: Late Detection
def check_overdue_payments():
    # Find all installments with due_date < today
    overdue = Installment.filter(
        due_date < today AND
        status = 'PENDING'
    )
    
    # Mark as OVERDUE
    for installment in overdue:
        installment.status = 'OVERDUE'
        installment.save()
        
        # Trigger notification
        send_late_payment_alert(installment)
```

---

## 📋 Payment Validators

```python
# validators/payment/record_payment_validator.py

def validate_record_payment(data, deal):
    # Validate amount > 0
    # Validate amount <= outstanding_balance (with tolerance)
    # Validate payment_date <= today
    # Validate payment_method
    # Validate reference_number (if bank transfer)
    # Check deal status (must be ACTIVE)
    # Return validated data or errors
```

---

## 🎯 Payment Processing Workflow

```
User Submits Payment
  ↓
Validate Amount & Dates
  ↓
Create Payment Record (status=PAID)
  ↓
Auto-match to Installment
  ↓
Update Deal Balance
  ↓
Generate Receipt (auto)
  ↓
Update Client Ledger
  ↓
Send WhatsApp Confirmation
  ↓
Check if Deal Complete (balance=0)
  ↓
Auto-mark Deal COMPLETED
```

---

## ✅ Payment System Checklist

- [ ] Payment model created
- [ ] Payment Plan model
- [ ] Installment model
- [ ] Record payment endpoint
- [ ] List payments endpoint
- [ ] Get payment details endpoint
- [ ] Update payment status endpoint
- [ ] Get payment plan endpoint
- [ ] Get deal balance endpoint
- [ ] Ledger calculation logic
- [ ] Balance after payment calculation
- [ ] Late payment detection job
- [ ] Bulk payment import
- [ ] Payment validators
- [ ] Payment service (business logic)
- [ ] Payment controller
- [ ] Auto-receipt generation
- [ ] Payment notifications
- [ ] Swagger documentation
- [ ] Unit tests (80%+)
- [ ] Integration tests
