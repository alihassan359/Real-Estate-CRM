# 📊 Dashboard & Analytics System

## 📋 Overview
Comprehensive dashboard and analytics system for business intelligence and performance tracking.

---

## 🎯 Dashboard Types

| Dashboard | Audience | Purpose |
|-----------|----------|---------|
| **Admin Dashboard** | Company Owner | Full business overview |
| **Sales Dashboard** | Salesmen/Dealers | Deal performance |
| **Financial Dashboard** | Accountants | Payment tracking |
| **Manager Dashboard** | Managers | Team performance |

---

## 🏠 Admin Dashboard Overview

### Key Metrics
```yaml
metrics:
  # Deal Summary
  total_deals: Integer
  active_deals: Integer
  completed_deals: Integer
  defaulted_deals: Integer
  
  # Financial Summary
  total_deal_value: Decimal (PKR)
  total_paid: Decimal (PKR)
  total_due: Decimal (PKR)
  pending_amount: Decimal (PKR)
  overdue_amount: Decimal (PKR)
  
  # Client Summary
  total_clients: Integer
  kyc_verified: Integer
  kyc_pending: Integer
  
  # Payment Summary
  this_month_payments: Decimal (PKR)
  this_month_installments_due: Integer
  on_time_rate: Float (percentage)
  
  # Plot Summary
  total_plots: Integer
  available_plots: Integer
  reserved_plots: Integer
  sold_plots: Integer
  
  # Team Summary
  total_users: Integer
  active_users: Integer
  sales_team_size: Integer
```

---

## 🛣️ Dashboard API Endpoints

### Get Admin Dashboard Overview
```
GET /api/dashboard/overview

Headers:
Authorization: Bearer owner_token

Query Params:
- date_range: LAST_30_DAYS | LAST_90_DAYS | THIS_YEAR | CUSTOM
- start_date: 2026-04-01
- end_date: 2026-04-11

Response (200):
{
  "success": true,
  "data": {
    "summary": {
      "total_deals": 45,
      "active_deals": 35,
      "completed_deals": 8,
      "defaulted_deals": 2,
      
      "total_deal_value": 112500000,
      "total_paid": 33750000,
      "total_due": 78750000,
      "overdue_amount": 5000000,
      
      "on_time_rate": 92.5
    },
    
    "charts": {
      "deals_by_status": {
        "labels": ["ACTIVE", "COMPLETED", "DEFAULTED"],
        "values": [35, 8, 2]
      },
      
      "revenue_by_month": {
        "labels": ["Jan", "Feb", "Mar", "Apr"],
        "values": [2000000, 2500000, 3100000, 2150000]
      },
      
      "payment_status": {
        "labels": ["PAID", "PENDING", "OVERDUE"],
        "values": [250, 200, 15]
      }
    },
    
    "recent_deals": [
      {
        "deal_id": "BTM-GW-045-2026-000001",
        "client_name": "Ali Ahmed Khan",
        "amount": 2500000,
        "status": "ACTIVE",
        "created_date": "2026-04-10"
      },
      ...
    ],
    
    "pending_payments": [
      {
        "client_name": "Ali Ahmed Khan",
        "amount_due": 250000,
        "due_date": "2026-05-11",
        "days_until_due": 30
      },
      ...
    ]
  }
}
```

### Get Financial Analytics
```
GET /api/dashboard/financial

Query Params:
- date_range: LAST_30_DAYS
- project_id: optional

Response (200):
{
  "success": true,
  "data": {
    "summary": {
      "total_revenue": 11500000,
      "received_revenue": 3500000,
      "pending_revenue": 8000000,
      "overdue_revenue": 500000
    },
    
    "breakdown_by_project": [
      {
        "project_name": "Grand View",
        "total_potential": 6000000,
        "received": 2000000,
        "pending": 4000000,
        "overdue": 200000
      },
      ...
    ],
    
    "breakdown_by_payment_type": {
      "ADVANCE": 3500000,
      "INSTALLMENT": 8000000,
      "BUBBLE": 0
    },
    
    "monthly_cash_flow": [
      {
        "month": "April",
        "inflow": 2500000,
        "outflow": 800000,
        "net": 1700000
      },
      ...
    ]
  }
}
```

### Get Sales Analytics
```
GET /api/dashboard/sales

Query Params:
- date_range: LAST_90_DAYS
- salesman_id: optional

Response (200):
{
  "success": true,
  "data": {
    "summary": {
      "total_deals_created": 15,
      "total_deal_value": 37500000,
      "average_deal_size": 2500000,
      "completion_rate": 80
    },
    
    "by_salesman": [
      {
        "salesman_name": "Ahmed Hassan",
        "deals_created": 8,
        "total_value": 20000000,
        "earned_commission": 400000
      },
      {
        "salesman_name": "Fatima Khan",
        "deals_created": 7,
        "total_value": 17500000,
        "earned_commission": 350000
      }
    ],
    
    "by_project": [
      {
        "project_name": "Grand View",
        "deals_created": 10,
        "total_value": 25000000,
        "completion_rate": 85
      },
      ...
    ],
    
    "top_performers": [
      {
        "salesman_name": "Ahmed Hassan",
        "ranking": 1,
        "deals": 8,
        "value": 20000000
      },
      ...
    ]
  }
}
```

### Get Client Analytics
```
GET /api/dashboard/clients

Query Params:
- date_range: LAST_30_DAYS

Response (200):
{
  "success": true,
  "data": {
    "summary": {
      "total_clients": 156,
      "new_clients": 12,
      "kyc_verified": 140,
      "kyc_pending": 16,
      "blacklisted": 0
    },
    
    "by_status": {
      "ACTIVE": 150,
      "INACTIVE": 5,
      "BLACKLISTED": 0
    },
    
    "by_city": [
      {
        "city": "Islamabad",
        "count": 85,
        "total_investment": 50000000
      },
      {
        "city": "Lahore",
        "count": 45,
        "total_investment": 30000000
      },
      ...
    ],
    
    "client_acquisition": [
      {
        "month": "April",
        "new_clients": 5,
        "with_deals": 3
      },
      ...
    ]
  }
}
```

### Get Performance Metrics
```
GET /api/dashboard/performance

Response (200):
{
  "success": true,
  "data": {
    "kpis": {
      "payment_on_time_rate": 92.5,
      "average_deal_completion_time": 45,  // days
      "client_satisfaction_score": 4.5,  // out of 5
      "average_response_time": 2  // hours
    },
    
    "trends": {
      "deals_created_trend": [10, 12, 11, 15],  // Last 4 weeks
      "revenue_trend": [2000000, 2300000, 2100000, 2500000],
      "client_acquisition_trend": [3, 4, 3, 5]
    },
    
    "health_check": {
      "system_status": "HEALTHY",
      "api_uptime": 99.9,
      "database_status": "HEALTHY",
      "notification_delivery_rate": 98.5
    }
  }
}
```

---

## 📊 Chart Types

### Deal Status Distribution
```json
{
  "type": "pie",
  "labels": ["ACTIVE", "COMPLETED", "DEFAULTED", "CANCELLED"],
  "values": [50, 30, 15, 5],
  "colors": ["green", "blue", "red", "grey"]
}
```

### Revenue Over Time
```json
{
  "type": "line",
  "labels": ["Jan", "Feb", "Mar", "Apr"],
  "datasets": [
    {
      "label": "Received",
      "values": [500000, 750000, 1000000, 1200000]
    },
    {
      "label": "Due",
      "values": [2000000, 1800000, 1600000, 1400000]
    }
  ]
}
```

### Payment Breakdown
```json
{
  "type": "bar",
  "labels": ["On Time", "Late", "Overdue"],
  "values": [200, 30, 5]
}
```

---

## 🛠️ Analytics Service

```python
# services/analytics/analytics_service.py

class AnalyticsService:
    async def get_dashboard_overview(tenant_id, date_range):
        # Calculate all metrics
        # Get recent deals
        # Get pending payments
        # Return dashboard data
    
    async def get_financial_analytics(tenant_id, date_range):
        # Calculate revenue metrics
        # Group by project
        # Calculate cash flow
        # Return financial data
    
    async def get_sales_analytics(tenant_id, salesman_id=None):
        # Calculate sales metrics
        # Rank salesmen
        # Calculate commissions
        # Return sales data
    
    async def calculate_kpis(tenant_id):
        # Calculate on-time payment rate
        # Calculate average deal size
        # Calculate completion rate
        # Return KPIs
```

---

## 🔌 Real-time Updates (Optional)

```python
# WebSocket for real-time dashboard updates
# When payment recorded -> update dashboard
# When deal completed -> update dashboard
# When overdue detected -> send alert

from fastapi import WebSocket

@app.websocket("/ws/dashboard/{tenant_id}")
async def websocket_dashboard(websocket: WebSocket, tenant_id: str):
    await websocket.accept()
    
    # Subscribe to real-time events
    # Send updates as they happen
    # Close connection on disconnect
```

---

## ✅ Dashboard Checklist

- [ ] Admin dashboard overview
- [ ] Financial dashboard
- [ ] Sales dashboard
- [ ] Client dashboard
- [ ] Dashboard API endpoints
- [ ] Chart generation logic
- [ ] Date range filtering
- [ ] Export functionality
- [ ] Real-time updates (optional)
- [ ] Performance optimizations
- [ ] Caching strategy
- [ ] Swagger documentation
- [ ] Unit tests
- [ ] UI mockups
