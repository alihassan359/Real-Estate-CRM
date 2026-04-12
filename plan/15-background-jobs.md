# 🔄 Background Jobs & Automation

## 📋 Overview
Background job system for automated tasks like payment reminders, late detection, and report generation.

---

## 🎯 Background Jobs

### 1. Payment Reminder Job
```yaml
job_name: payment_reminder
schedule: \"0 9 * * *\"  # 9 AM daily
frequency: Once per due date per deal
purpose: Send reminder 7 days before payment due
actions:
  - Query all installments with due_date = today + 7 days
  - Filter by status = PENDING
  - Send WhatsApp/Email to client
  - Log notification sent
```

### 2. Late Payment Detection Job
```yaml
job_name: late_payment_detection
schedule: \"0 0 * * *\"  # Midnight daily
frequency: Check all overdue payments
purpose: Detect and mark overdue payments
actions:
  - Query all payments with due_date < today
  - Filter by status = PENDING
  - Update status to OVERDUE
  - Send alert to accountant
  - Update client's overdue amount
  - Record audit log
```

### 3. Deal Completion Check
```yaml
job_name: deal_completion_check
schedule: \"*/30 * * * *\"  # Every 30 minutes
frequency: Check if deals are completed
purpose: Auto-mark deals as COMPLETED when fully paid
actions:
  - Query all deals with status = ACTIVE
  - Check outstanding_balance = 0
  - Auto-update status to COMPLETED
  - Send completion email
  - Generate completion certificate
```

### 4. Report Generation Job
```yaml
job_name: daily_report_generation
schedule: \"0 20 * * *\"  # 8 PM daily
frequency: Daily
purpose: Generate daily reports
actions:
  - Calculate daily revenue
  - Count new deals
  - Count new payments
  - Generate PDF report
  - Email to owner
  - Store in database
```

### 5. Backup Job
```yaml
job_name: database_backup
schedule: \"0 2 * * *\"  # 2 AM daily
frequency: Daily
purpose: Backup database
actions:
  - Export database
  - Compress backup
  - Upload to cloud storage
  - Keep 30-day rolling backup
  - Log backup status
```

---

## 🛠️ Job Implementation

### Job Scheduler Setup
```python
# jobs/scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime

scheduler = BackgroundScheduler()

# Register all jobs
scheduler.add_job(
    payment_reminder_job,
    trigger='cron',
    hour=9,
    minute=0,
    id='payment_reminder'
)

scheduler.add_job(
    late_payment_detection_job,
    trigger='cron',
    hour=0,
    minute=0,
    id='late_payment_detection'
)

scheduler.add_job(
    deal_completion_check_job,
    trigger='interval',
    minutes=30,
    id='deal_completion_check'
)

scheduler.add_job(
    daily_report_generation_job,
    trigger='cron',
    hour=20,
    minute=0,
    id='daily_report_generation'
)

scheduler.add_job(
    database_backup_job,
    trigger='cron',
    hour=2,
    minute=0,
    id='database_backup'
)

# Start scheduler on app startup
scheduler.start()
```

### Payment Reminder Job
```python
# jobs/payment_reminder_job.py

async def payment_reminder_job():
    try:
        # Get all tenants
        tenants = await Tenant.all()
        
        for tenant in tenants:
            # Get all installments due 7 days from now
            target_date = date.today() + timedelta(days=7)
            
            installments = await Installment.filter(
                tenant_id=tenant.id,
                due_date=target_date,
                status='PENDING'
            ).all()
            
            for installment in installments:
                deal = await Deal.get(id=installment.deal_id)
                client = await Client.get(id=deal.client_id)
                
                # Send WhatsApp reminder
                await notification_service.send_payment_reminder(
                    client=client,
                    deal=deal,
                    amount=installment.amount,
                    due_date=installment.due_date,
                    channels=['WHATSAPP']
                )
                
                # Log job execution
                await Job.create(
                    tenant_id=tenant.id,
                    job_name='payment_reminder',
                    status='SENT',
                    target_id=installment.id
                )
        
        logger.info('Payment reminder job completed')
        
    except Exception as e:
        logger.error(f'Payment reminder job failed: {str(e)}')
```

### Late Payment Detection Job
```python
# jobs/late_payment_detection_job.py

async def late_payment_detection_job():
    try:
        today = date.today()
        tenants = await Tenant.all()
        
        for tenant in tenants:
            # Get all overdue installments
            overdue_installments = await Installment.filter(
                tenant_id=tenant.id,
                due_date__lt=today,
                status='PENDING'
            ).all()
            
            for installment in overdue_installments:
                print(f'Processing overdue installment: {installment.id}')
                
                # Mark as overdue
                installment.status = 'OVERDUE'
                await installment.save()
                
                # Update deal's overdue amount
                deal = await Deal.get(id=installment.deal_id)
                deal.overdue_amount = (deal.overdue_amount or Decimal('0')) + installment.amount
                await deal.save()
                
                # Update client's overdue amount
                client = await Client.get(id=deal.client_id)
                client.overdue_amount = (client.overdue_amount or Decimal('0')) + installment.amount
                await client.save()
                
                # Send alert to accountant
                accountants = await User.filter(
                    tenant_id=tenant.id,
                    role='ACCOUNTANT'
                ).all()
                
                for accountant in accountants:
                    await notification_service.send_overdue_alert(
                        recipient=accountant,
                        deal=deal,
                        client=client,
                        amount=installment.amount,
                        days_overdue=(today - installment.due_date).days
                    )
        
        logger.info('Late payment detection job completed')
        
    except Exception as e:
        logger.error(f'Late payment detection job failed: {str(e)}')
```

### Deal Completion Check Job
```python
# jobs/deal_completion_check_job.py

async def deal_completion_check_job():
    try:
        tenants = await Tenant.all()
        
        for tenant in tenants:
            # Get all active deals
            active_deals = await Deal.filter(
                tenant_id=tenant.id,
                status='ACTIVE'
            ).all()
            
            for deal in active_deals:
                # Check if fully paid
                if deal.outstanding_balance <= 0:
                    print(f'Completing deal: {deal.deal_id}')
                    
                    # Update deal status
                    deal.status = 'COMPLETED'
                    deal.completion_date = datetime.now()
                    await deal.save()
                    
                    # Update plot status
                    plot = await Plot.get(id=deal.plot_id)
                    if plot:
                        plot.status = 'COMPLETED'
                        await plot.save()
                    
                    # Generate completion certificate
                    await receipt_service.generate_completion_certificate(deal)
                    
                    # Send completion email
                    client = await Client.get(id=deal.client_id)
                    await notification_service.send_completion_email(
                        client=client,
                        deal=deal
                    )
        
        logger.info('Deal completion check job completed')
        
    except Exception as e:
        logger.error(f'Deal completion check job failed: {str(e)}')
```

---

## 📊 Job Monitoring

### Job Execution Logging
```python
# models/job.py

class Job(BaseModel):
    id: UUID
    tenant_id: UUID
    job_name: String
    status: String (PENDING, EXECUTING, COMPLETED, FAILED)
    target_id: UUID (optional)
    error_message: String (optional)
    execution_time_ms: Integer
    started_at: DateTime
    completed_at: DateTime
    retry_count: Integer
```

### Job Status Endpoint
```
GET /api/admin/jobs?page=1&limit=20

Response:
{
  "success": true,
  "data": [
    {
      "job_name": "payment_reminder",
      "status": "COMPLETED",
      "last_execution": "2026-04-11T09:00:00Z",
      "next_execution": "2026-04-12T09:00:00Z",
      "execution_time_ms": 1250,
      "processed_items": 15,
      "failed_items": 0
    },
    ...
  ]
}
```

### Trigger Manual Job
```
POST /api/admin/jobs/{job_name}/run

Response:
{
  "success": true,
  "message": "Job triggered manually",
  "data": {
    "job_name": "payment_reminder",
    "started_at": "2026-04-11T10:30:00Z"
  }
}
```

---

## ⚠️ Error Handling in Jobs

```python
# All jobs must have try/catch

async def sample_job():
    try:
        # Job logic here
        pass
    except Exception as e:
        # Log error
        logger.error(f'Job failed: {str(e)}')
        
        # Record failure
        await Job.create(
            tenant_id=tenant_id,
            job_name='sample_job',
            status='FAILED',
            error_message=str(e)
        )
        
        # Optionally send alert
        await send_admin_alert(f'Job failed: sample_job')
```

---

## ✅ Background Jobs Checklist

- [ ] Job scheduler setup (APScheduler)
- [ ] Payment reminder job
- [ ] Late payment detection job
- [ ] Deal completion check job
- [ ] Daily report generation job
- [ ] Database backup job
- [ ] Job execution logging
- [ ] Job monitoring endpoint
- [ ] Manual job trigger endpoint
- [ ] Error handling & alerts
- [ ] Retry logic
- [ ] Job status dashboard
- [ ] Swagger documentation
- [ ] Unit tests
