# 📜 Receipt & Document System

## 📋 Overview
Receipt generation, PDF creation, storage management, and document delivery system.

---

## 📄 Document Types

| Type | Generated When | Content |
|------|----------------|---------|
| **Payment Receipt** | Payment received | Amount, date, balance |
| **Deal Agreement** | Deal created | Deal terms, plot info |
| **Payment Schedule** | Deal creation | Monthly installments |
| **Tax Invoice** | Payment (if required) | Tax details |
| **Completion Certificate** | Deal completed | Handover confirmation |

---

## 📊 Receipt Model

```yaml
receipt:
  # Primary
  id: UUID
  tenant_id: UUID
  
  # Link
  payment_id: UUID (Foreign Key)
  deal_id: UUID (Foreign Key)
  client_id: UUID (Foreign Key)
  
  # Identity
  receipt_number: String (Unique: REC-2026-000001)
  receipt_type: String (PAYMENT_RECEIPT, DEAL_AGREEMENT, etc)
  
  # Content
  title: String
  description: String
  details: JSON (amount, date, client_info, etc)
  
  # Media
  pdf_url: String (Cloudinary/AWS S3)
  original_filename: String
  file_size_bytes: Integer
  
  # Status
  status: String (GENERATED, SENT, VIEWED, PRINTED)
  sent_at: DateTime
  viewed_at: DateTime
  printed_at: DateTime
  
  # Metadata
  issue_date: DateTime
  expiry_date: DateTime (nullable)
  currency: String
  
  # Tracking
  created_at: DateTime
  created_by: UUID
  downloaded_count: Integer
```

---

## 🛣️ Receipt API Endpoints

### Generate Receipt
```
POST /api/receipts/generate

Headers:
Authorization: Bearer accountant_token

Request Body:
{
  "receipt_type": "PAYMENT_RECEIPT",
  "payment_id": "payment_uuid",
  "format": "PDF",
  "send_to_client": true
}

Response (201):
{
  "success": true,
  "message": "Receipt generated and sent",
  "data": {
    "id": "receipt_uuid",
    "receipt_number": "REC-2026-000001",
    "pdf_url": "https://...",
    "status": "SENT",
    "created_at": "2026-04-11T10:00:00Z"
  }
}
```

### Get Receipt Details
```
GET /api/receipts/{receipt_id}

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "id": "receipt_uuid",
    "receipt_number": "REC-2026-000001",
    "receipt_type": "PAYMENT_RECEIPT",
    "deal_id": "BTM-GW-045-2026-000001",
    "client_name": "Ali Ahmed Khan",
    "amount": 250000,
    "issue_date": "2026-04-11",
    "pdf_url": "https://...",
    "status": "SENT",
    "sent_at": "2026-04-11T10:05:00Z"
  }
}
```

### List Receipts
```
GET /api/receipts?receipt_type=PAYMENT_RECEIPT&deal_id=...&page=1&limit=20

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "receipt_uuid",
      "receipt_number": "REC-2026-000001",
      "deal_id": "BTM-GW-045-2026-000001",
      "amount": 250000,
      "issue_date": "2026-04-11",
      "status": "SENT"
    },
    ...
  ]
}
```

### Download Receipt
```
GET /api/receipts/{receipt_id}/download

Headers:
Authorization: Bearer token

Response: PDF Binary
{
  Header: Content-Type: application/pdf
  Body: [PDF File Stream]
}
```

### Resend Receipt to Client
```
POST /api/receipts/{receipt_id}/resend

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "email": "ali@example.com",
  "whatsapp": "+92-300-1234567"
}

Response (200):
{
  "success": true,
  "message": "Receipt resent to client",
  "data": {
    "id": "receipt_uuid",
    "sent_at": "2026-04-11T10:00:00Z"
  }
}
```

---

## 📝 Receipt Template System

### Payment Receipt Template
```html
<!DOCTYPE html>
<html>
<head>
  <style>
    body { font-family: Arial; margin: 20px; }
    .header { text-align: center; border-bottom: 2px solid #333; }
    .company-name { font-size: 24px; font-weight: bold; }
    .receipt-title { font-size: 18px; margin-top: 10px; }
    .details { margin-top: 20px; }
    .row { display: flex; justify-content: space-between; margin: 10px 0; }
    .total { font-size: 20px; font-weight: bold; border-top: 1px solid #ccc; }
  </style>
</head>
<body>
  <div class="header">
    <div class="company-name">{{tenant_name}}</div>
    <div class="receipt-title">PAYMENT RECEIPT</div>
  </div>
  
  <div class="details">
    <div class="row">
      <span>Receipt #:</span>
      <span>{{receipt_number}}</span>
    </div>
    <div class="row">
      <span>Date:</span>
      <span>{{issue_date}}</span>
    </div>
    
    <div style="margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
      <h3>Deal Information</h3>
      <div class="row">
        <span>Deal ID:</span>
        <span>{{deal_id}}</span>
      </div>
      <div class="row">
        <span>Project:</span>
        <span>{{project_name}}</span>
      </div>
      <div class="row">
        <span>Plot:</span>
        <span>{{plot_number}}</span>
      </div>
    </div>
    
    <div style="margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
      <h3>Client Information</h3>
      <div class="row">
        <span>Name:</span>
        <span>{{client_name}}</span>
      </div>
      <div class="row">
        <span>Email:</span>
        <span>{{client_email}}</span>
      </div>
      <div class="row">
        <span>Phone:</span>
        <span>{{client_phone}}</span>
      </div>
    </div>
    
    <div style="margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
      <h3>Payment Details</h3>
      <div class="row">
        <span>Amount:</span>
        <span>PKR {{amount}}</span>
      </div>
      <div class="row">
        <span>Payment Type:</span>
        <span>{{payment_type}}</span>
      </div>
      <div class="row">
        <span>Payment Date:</span>
        <span>{{payment_date}}</span>
      </div>
      <div class="row">
        <span>Payment Method:</span>
        <span>{{payment_method}}</span>
      </div>
    </div>
    
    <div style="margin-top: 30px; border-top: 1px solid #ddd; padding-top: 20px;">
      <div class="row total">
        <span>Total Paid to Date:</span>
        <span>PKR {{total_paid}}</span>
      </div>
      <div class="row">
        <span>Outstanding Balance:</span>
        <span>PKR {{outstanding_balance}}</span>
      </div>
      <div class="row">
        <span>Next Due Date:</span>
        <span>{{next_due_date}}</span>
      </div>
    </div>
  </div>
  
  <div style="margin-top: 50px; text-align: center; color: #666;">
    <p>This is an electronically generated receipt. No signature is required.</p>
    <p>Thank you for your business!</p>
  </div>
</body>
</html>
```

---

## 🛠️ PDF Generation Service

```python
# services/receipt/pdf_service.py

class PDFService:
    async def generate_receipt_pdf(data: dict):
        # Load HTML template
        template = load_template('payment_receipt.html')
        
        # Render with data
        html = template.render(data)
        
        # Convert to PDF
        pdf = html2pdf(html)
        
        # Store in cloud storage
        url = upload_to_cloudinary(pdf)
        
        return url
    
    async def generate_bulk_receipts(deals: List[str]):
        # Generate receipts for multiple deals
        # Return URLs for download
        pass
```

---

## ☁️ Cloud Storage Integration

### Cloudinary Integration
```python
# integrations/cloudinary/cloudinary_service.py

class CloudinaryService:
    async def upload_pdf(file_bytes):
        # Upload to Cloudinary
        response = cloudinary.uploader.upload(
            file_bytes,
            resource_type='raw',
            folder='receipts',
            public_id=f'receipt-{timestamp()}'
        )
        
        return response['secure_url']
    
    async def delete_pdf(public_id):
        # Delete from Cloudinary
        cloudinary.uploader.destroy(public_id)
```

---

## 📊 Receipt Audit

### Email Audit
```yaml
audit:
  - Date: 2026-04-11
    Action: Receipt generated
    Receipt #: REC-2026-000001
    User: Ahmed Hassan
    
  - Date: 2026-04-11
    Action: Receipt sent to client
    Channel: WHATSAPP
    Delivered: YES
    
  - Date: 2026-04-12
    Action: Receipt downloaded by client
    Download Time: 10:30 AM
    
  - Date: 2026-04-13
    Action: Receipt printed
    Location: Office Desk
```

---

## ✅ Receipt System Checklist

- [ ] Receipt model created
- [ ] Receipt number generation logic
- [ ] PDF generation service
- [ ] HTML template system
- [ ] Template rendering
- [ ] Cloudinary integration
- [ ] Generate receipt endpoint
- [ ] List receipts endpoint
- [ ] Get receipt details endpoint
- [ ] Download receipt endpoint
- [ ] Resend receipt endpoint
- [ ] Bulk receipt generation
- [ ] Receipt audit logging
- [ ] Email service integration
- [ ] WhatsApp sending
- [ ] Receipt templates (5+ types)
- [ ] PDF validation
- [ ] Storage cleanup (old receipts)
- [ ] Swagger documentation
- [ ] Unit tests
- [ ] Integration tests
