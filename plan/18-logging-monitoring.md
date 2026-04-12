# 📝 Logging & Monitoring System

## 📋 Overview
Comprehensive logging, monitoring, and alerting system for production reliability.

---

## 🎯 Logging Levels

| Level | When | Example |
|-------|------|---------|
| **DEBUG** | Development | Variable values, function entry/exit |
| **INFO** | Normal operations | User actions, job executions |
| **WARNING** | Unusual events | Deprecated API usage, rate limit warnings |
| **ERROR** | Error conditions | Failed payments, DB errors |
| **CRITICAL** | System down | DB connection lost, OOM |

---

## 🛠️ Logging Implementation

### Configure Logging
```python
# config/logging.py

import logging
from logging.handlers import RotatingFileHandler
import json

# Structured logging formatter
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_dict = {
            'timestamp': self.formatTime(record),
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'request_id': getattr(record, 'request_id', None),
            'user_id': getattr(record, 'user_id', None),
            'tenant_id': getattr(record, 'tenant_id', None),
        }
        
        if record.exc_info:
            log_dict['exception'] = self.formatException(record.exc_info)
        
        return json.dumps(log_dict)

# Setup logger
logger = logging.getLogger('realestate-crm')
logger.setLevel(logging.INFO)

# File handler (rotating)
file_handler = RotatingFileHandler(
    'logs/app.log',
    maxBytes=10485760,  # 10MB
    backupCount=10
)
file_handler.setFormatter(JSONFormatter())
logger.addHandler(file_handler)

# Console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(JSONFormatter())
logger.addHandler(console_handler)
```

### Contextual Logging
```python
# utils/logging_context.py

import contextvars

request_id_var = contextvars.ContextVar('request_id')
user_id_var = contextvars.ContextVar('user_id')
tenant_id_var = contextvars.ContextVar('tenant_id')

# Middleware to set context
@app.middleware('http')
async def logging_middleware(request: Request, call_next):
    request_id = request.headers.get('x-request-id') or str(uuid.uuid4())
    request_id_var.set(request_id)
    
    # ... extract user & tenant from token
    
    response = await call_next(request)
    return response

# Usage in logging
logger.info('User created', extra={
    'request_id': request_id_var.get(),
    'user_id': user_id_var.get(),
    'tenant_id': tenant_id_var.get(),
})
```

### Logging Examples

#### Successful Action
```python
logger.info('Deal created', extra={
    'action': 'CREATE_DEAL',
    'deal_id': deal_id,
    'client_id': client_id,
    'amount': amount
})
```

#### Error Action
```python
logger.error('Payment recording failed', extra={
    'action': 'RECORD_PAYMENT',
    'deal_id': deal_id,
    'error_code': error.code,
    'error_message': error.message
})
```

#### Business Event
```python
logger.info('Payment reminder sent', extra={
    'action': 'PAYMENT_REMINDER',
    'installment_id': installment_id,
    'client_id': client_id,
    'amount': amount,
    'channel': 'WHATSAPP'
})
```

---

## 📊 Monitoring Metrics

### Application Metrics
```python
from prometheus_client import Counter, Histogram, Gauge

# Request metrics
request_count = Counter(
    'app_requests_total',
    'Total requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'app_request_duration_seconds',
    'Request duration',
    ['method', 'endpoint']
)

# Business metrics
deals_created = Counter(
    'deals_created_total',
    'Total deals created'
)

payments_recorded = Counter(
    'payments_recorded_total',
    'Total payments recorded'
)

# System metrics
active_connections = Gauge(
    'db_connections_active',
    'Active database connections'
)
```

### Usage
```python
@app.post('/api/deals')
async def create_deal(request):
    with request_duration.labels(method='POST', endpoint='/deals').time():
        # ... create deal
        deals_created.inc()
        request_count.labels(method='POST', endpoint='/deals', status='201').inc()
```

---

## 🔔 Alerting

### Alert Rules
```yaml
# alerts.yaml

alerts:
  - name: HighErrorRate
    condition: error_rate > 5%
    severity: CRITICAL
    action: Send Slack notification
  
  - name: DBConnectionPoolExhausted
    condition: available_connections == 0
    severity: CRITICAL
    action: Trigger PagerDuty alert
  
  - name: PaymentProcessingDelay
    condition: avg_payment_processing_time > 5s
    severity: WARNING
    action: Send email to devops
  
  - name: UnhandledExceptions
    condition: exception_count > 10/min
    severity: ERROR
    action: Send Slack notification
```

### Alert Implementation
```python
# integrations/alerting/alert_service.py

class AlertService:
    async def send_alert(level, title, message):
        if level == 'CRITICAL':
            await send_slack_critical(title, message)
            await trigger_pagerduty(title, message)
        elif level == 'ERROR':
            await send_slack_error(title, message)
            await send_email(title, message)
        elif level == 'WARNING':
            await send_slack_warning(title, message)
```

---

## 📊 Health Check

### Health Check Endpoint
```
GET /health

Response (200):
{
  "status": "HEALTHY",
  "timestamp": "2026-04-11T10:30:00Z",
  "checks": {
    "database": "HEALTHY",
    "redis": "HEALTHY",
    "external_services": "HEALTHY"
  },
  "uptime_seconds": 86400,
  "version": "1.0.0"
}
```

### Implementation
```python
# routes/health.py

@app.get('/health')
async def health_check():
    db_status = await check_database()
    redis_status = await check_redis()
    
    system_status = 'HEALTHY'
    if db_status != 'HEALTHY':
        system_status = 'UNHEALTHY'
    
    return {
        'status': system_status,
        'checks': {
            'database': db_status,
            'redis': redis_status
        }
    }
```

---

## 📈 Log Aggregation

### ELK Stack Integration
```python
# config/log_aggregation.py

from elasticapm import Client

apm_client = Client({
    'SERVICE_NAME': 'realestate-crm',
    'SERVER_URL': os.getenv('ELASTIC_APM_SERVER_URL'),
    'SECRET_TOKEN': os.getenv('ELASTIC_APM_SECRET_TOKEN'),
    'ENVIRONMENT': os.getenv('ENVIRONMENT'),
})

# Log transactions
@apm_client.trace()
async def create_deal(deal_data):
    # ... transaction executed
    pass
```

---

## 🔍 Debugging Tools

### Request/Response Logging
```python
# middlewares/debug_middleware.py

@app.middleware('http')
async def debug_middleware(request: Request, call_next):
    if os.getenv('DEBUG_MODE') == 'true':
        logger.debug(f'Request: {request.method} {request.url.path}')
        logger.debug(f'Headers: {dict(request.headers)}')
        
        response = await call_next(request)
        
        logger.debug(f'Response Status: {response.status_code}')
        return response
    
    return await call_next(request)
```

---

## ✅ Logging Checklist

- [ ] Logging framework configured
- [ ] Structured logging (JSON)
- [ ] Request ID tracking
- [ ] Contextual logging (user, tenant)
- [ ] Log levels appropriate
- [ ] Sensitive data not logged
- [ ] Rotating file handler
- [ ] Log aggregation (ELK)
- [ ] Monitoring metrics
- [ ] Health check endpoint
- [ ] Alert rules defined
- [ ] Slack integration
- [ ] Email alerts
- [ ] PagerDuty integration
- [ ] Log retention policy
- [ ] Performance monitoring
- [ ] Error tracking (Sentry)
- [ ] Debugging tools
