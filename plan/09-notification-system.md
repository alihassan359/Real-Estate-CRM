# 📲 Notification System

## 📋 Overview
Multi-channel notification system sending WhatsApp, Email, and SMS to clients and stakeholders.

---

## 📡 Notification Channels

| Channel | Primary Use | Latency | Cost |
|---------|-----------|---------|------|
| **WhatsApp** | Instant updates | < 5 seconds | Low |
| **Email** | Documentation | < 1 minute | Low |
| **SMS** | Critical alerts | < 10 seconds | Higher |

---

## 🎯 Notification Triggers

### 1. On Payment Received
```yaml
trigger: Payment recorded
channels: [WHATSAPP, EMAIL]
template: payment_receipt
data:
  - deal_id
  - amount
  - remaining_balance
  - next_due_date
```

**Message Template:**
```
🎉 Payment Received: PKR {{amount}}

Deal ID: {{deal_id}}
Project: {{project_name}}
Plot: {{plot_number}}

Remaining Balance: PKR {{remaining_balance}}
Next Due: {{next_due_date}}

Thanks for the payment!
-Real Estate CRM
```

### 2. Payment Reminder (Before Due)
```yaml
trigger: 7 days before due date
channels: [WHATSAPP]
frequency: Once per installment
template: payment_reminder
```

**Message Template:**
```
📢 Payment Reminder

Your payment of PKR {{amount}} is due in 7 days.

Deal ID: {{deal_id}}
Due Date: {{due_date}}

Click to pay: [Link]

-Real Estate CRM
```

### 3. Overdue Alert (After Due)
```yaml
trigger: 1 day after due date
channels: [WHATSAPP, EMAIL]
frequency: Daily (until paid)
template: overdue_alert
```

**Message Template:**
```
⚠️ Payment Overdue

Your payment of PKR {{amount}} is now OVERDUE.

Deal ID: {{deal_id}}
Due Date: {{due_date}}
Days Overdue: {{days_overdue}}

Please contact us immediately.

-Real Estate CRM
```

### 4. Deal Created Confirmation
```yaml
trigger: Deal created
channels: [WHATSAPP, EMAIL]
template: deal_confirmation
```

---

## 📊 Notification Model

```yaml
notification:
  id: UUID
  tenant_id: UUID
  
  # Recipient
  recipient_id: UUID (user_id or client_id)
  recipient_name: String
  recipient_phone: String
  recipient_email: String
  
  # Content
  notification_type: String (PAYMENT_RECEIVED, PAYMENT_REMINDER, OVERDUE_ALERT, etc)
  title: String
  message: String
  
  # Channels
  channel: String (WHATSAPP, EMAIL, SMS)
  template_id: String
  
  # Status
  status: String (PENDING, SENT, FAILED, DELIVERED)
  sent_at: DateTime
  delivery_status: String (QUEUED, IN_PROGRESS, DELIVERED)
  
  # Tracking
  reference_id: String (API response from WhatsApp/Email)
  error_message: String (if failed)
  retry_count: Integer
  
  # Metadata
  metadata: JSON {deal_id, amount, etc}
  
  created_at: DateTime
  created_by: UUID
```

---

## 🛣️ Notification API Endpoints

### Send Manual Notification
```
POST /api/notifications/send

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "recipient_type": "CLIENT",
  "recipient_id": "client_uuid",
  "channel": "WHATSAPP",
  "template": "custom_message",
  "message": "Custom message to client",
  "metadata": {
    "deal_id": "BTM-GW-045-2026-000001"
  }
}

Response (201):
{
  "success": true,
  "message": "Notification queued",
  "data": {
    "id": "notification_uuid",
    "status": "PENDING",
    "sent_time": null
  }
}
```

### Get Notification Status
```
GET /api/notifications/{notification_id}

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "id": "notification_uuid",
    "type": "PAYMENT_RECEIVED",
    "recipient": "Ali Ahmed Khan",
    "channel": "WHATSAPP",
    "status": "DELIVERED",
    "sent_at": "2026-04-11T10:05:00Z",
    "delivery_status": "DELIVERED"
  }
}
```

### List Notifications (Audit)
```
GET /api/notifications?recipient_id=...&status=SENT&page=1&limit=20

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "notification_uuid",
      "recipient": "Ali Ahmed Khan",
      "type": "PAYMENT_RECEIVED",
      "channel": "WHATSAPP",
      "status": "DELIVERED",
      "sent_at": "2026-04-11T10:05:00Z"
    },
    ...
  ]
}
```

---

## 🧩 Notification Template System

### Template Structure
```yaml
templates:
  PAYMENT_RECEIVED:
    title: "Payment Received"
    channels: [WHATSAPP, EMAIL]
    variables: [deal_id, amount, remaining_balance, next_due]
    
  PAYMENT_REMINDER:
    title: "Payment Reminder"
    channels: [WHATSAPP]
    variables: [deal_id, amount, due_date]
    
  OVERDUE_ALERT:
    title: "Payment Overdue"
    channels: [WHATSAPP, EMAIL]
    variables: [deal_id, amount, due_date, days_overdue]
    
  DEAL_CREATED:
    title: "Deal Confirmation"
    channels: [WHATSAPP, EMAIL]
    variables: [deal_id, project, plot, amount]
```

### Custom Template
```
POST /api/admin/notification-templates

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "name": "CUSTOM_OFFER",
  "channels": ["WHATSAPP"],
  "title": "Special Offer",
  "message": "Special offer for {{client_name}}: PKR {{discount}}",
  "variables": ["client_name", "discount"]
}

Response (201):
{ ... }
```

---

## 🔌 WhatsApp Integration

### WhatsApp Business API
```python
# integrations/whatsapp/whatsapp_service.py

class WhatsAppService:
    async def send_message(phone, template_id, variables):
        # Format message with variables
        # Call WhatsApp Business API
        # Return delivery status
        
    async def track_delivery(message_id):
        # Poll WhatsApp for delivery status
        # Update notification record
        # Return status
```

### Configuration
```yaml
# config/notifications.yaml

whatsapp:
  enabled: true
  api_url: "https://graph.instagram.com/v18.0/..."
  phone_number_id: "..."
  access_token: "${WHATSAPP_API_KEY}"
  business_account_id: "..."
```

---

## 📧 Email Integration

### Email Service
```python
# integrations/email/email_service.py

class EmailService:
    async def send_email(to_email, template, variables):
        # Render template with variables
        # Create HTML email
        # Send via SMTP / SendGrid
        # Return delivery status
```

### Email Templates
```html
<!-- templates/email/payment_receipt.html -->
<html>
  <body style="font-family: Arial">
    <h2>Payment Received ✓</h2>
    <p>We received your payment of <strong>PKR {{amount}}</strong></p>
    
    <p>Deal: {{deal_id}}</p>
    <p>Project: {{project_name}}</p>
    <p>Plot: {{plot_number}}</p>
    
    <p>Remaining Balance: <strong>PKR {{remaining_balance}}</strong></p>
    <p>Next Due: <strong>{{next_due_date}}</strong></p>
    
    <p>Thank you!</p>
    <p>-Real Estate CRM</p>
  </body>
</html>
```

---

## 🔄 Notification Queue System

```python
# Background Job: Process notification queue
def process_notification_queue():
    while True:
        # Get pending notifications
        pending = Notification.filter(status='PENDING').limit(10)
        
        for notification in pending:
            try:
                # Send via channel
                if notification.channel == 'WHATSAPP':
                    whatsapp_service.send(notification)
                elif notification.channel == 'EMAIL':
                    email_service.send(notification)
                
                # Update status
                notification.status = 'SENT'
                notification.sent_at = now()
                notification.save()
                
            except Exception as e:
                notification.error_message = str(e)
                notification.retry_count += 1
                
                if notification.retry_count < 3:
                    notification.status = 'PENDING'
                else:
                    notification.status = 'FAILED'
                
                notification.save()
        
        # Wait before next batch
        sleep(5)
```

---

## ✅ Notification System Checklist

- [ ] Notification model created
- [ ] WhatsApp service integrated
- [ ] Email service integrated
- [ ] Notification templates created
- [ ] Template rendering logic
- [ ] Notification queue system
- [ ] Send manual notification endpoint
- [ ] Get notification status endpoint
- [ ] List notifications endpoint
- [ ] Template management endpoints
- [ ] Delivery tracking
- [ ] Retry logic
- [ ] Error handling
- [ ] Rate limiting per channel
- [ ] Swagger documentation
- [ ] Unit tests
- [ ] Integration tests
