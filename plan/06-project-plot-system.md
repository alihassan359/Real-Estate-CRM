# 🏗️ Project & Plot Management System

## 📋 Overview
Real estate project management system for tracking development projects and individual plots.

---

## 📊 Project Data Model

```yaml
project:
  # Primary
  id: UUID
  tenant_id: UUID
  project_code: String (Unique per tenant: GW, DHA, BTM-CITY)
  
  # Project Details
  name: String (Grand View, DHA Phase 6, etc)
  description: String
  type: String (RESIDENTIAL, COMMERCIAL, MIXED)
  category: String (PLOT, APARTMENT, HOUSE)
  
  # Location
  city: String
  area_name: String
  address: String
  coordinates: JSON (latitude, longitude)
  
  # Financial
  total_plots: Integer
  available_plots: Integer
  sold_plots: Integer
  base_price_per_sqft: Decimal
  
  # Timeline
  launch_date: Date
  expected_completion: Date
  completion_date: Date (nullable)
  
  # Media
  logo_url: String
  brochure_url: String
  images: Array (URLs)
  
  # Status
  status: String (PLANNING, ACTIVE, COMPLETED, ON_HOLD, CANCELLED)
  
  # Tracking
  created_at: DateTime
  updated_at: DateTime
  created_by: UUID
  updated_by: UUID
```

---

## 📊 Plot Data Model

```yaml
plot:
  # Primary
  id: UUID
  tenant_id: UUID
  project_id: UUID (Foreign Key)
  
  # Plot Details
  plot_number: String (unique within project)
  block: String (A, B, C, etc)
  sector: String
  size_sqft: Decimal
  size_sqm: Decimal
  
  # Financial
  base_price: Decimal
  current_price: Decimal (may increase over time)
  price_per_sqft: Decimal
  
  # Status
  status: String (AVAILABLE, RESERVED, SOLD, CANCELLED)
  
  # Deal Reference
  current_deal_id: UUID (Foreign Key, nullable)
  
  # Tracking
  created_at: DateTime
  updated_at: DateTime
```

---

## 🛣️ Project API Endpoints

### Create Project
```
POST /api/projects

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "name": "Grand View",
  "description": "Luxury residential project",
  "type": "RESIDENTIAL",
  "category": "PLOT",
  "city": "Islamabad",
  "area_name": "DHA Phase 6",
  "total_plots": 500,
  "base_price_per_sqft": 5000,
  "launch_date": "2026-04-01",
  "expected_completion": "2029-12-31"
}

Response (201):
{
  "success": true,
  "data": {
    "id": "project_uuid",
    "project_code": "GW",
    "name": "Grand View",
    "status": "ACTIVE",
    "total_plots": 500,
    "available_plots": 500
  }
}
```

### List Projects
```
GET /api/projects?status=ACTIVE&page=1&limit=20

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "project_uuid",
      "project_code": "GW",
      "name": "Grand View",
      "city": "Islamabad",
      "total_plots": 500,
      "available_plots": 250,
      "sold_plots": 250,
      "status": "ACTIVE"
    },
    ...
  ],
  "pagination": { ... }
}
```

### Get Project Details
```
GET /api/projects/{project_id}

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "id": "project_uuid",
    "name": "Grand View",
    "city": "Islamabad",
    "total_plots": 500,
    "available_plots": 250,
    "status": "ACTIVE",
    "plots": [array of plots],
    "statistics": {
      "sold_percentage": 50,
      "total_revenue": 2500000000,
      "pending_revenue": 1500000000
    }
  }
}
```

### Update Project
```
PATCH /api/projects/{project_id}

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "status": "COMPLETED",
  "completion_date": "2029-12-15"
}

Response (200):
{
  "success": true,
  "data": { ... }
}
```

---

## 🛣️ Plot API Endpoints

### Create Plot
```
POST /api/projects/{project_id}/plots

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "plot_number": "045",
  "block": "A",
  "sector": "1",
  "size_sqft": 5000,
  "size_sqm": 464.5
}

Response (201):
{
  "success": true,
  "data": {
    "id": "plot_uuid",
    "plot_number": "045",
    "block": "A",
    "status": "AVAILABLE",
    "price": 25000000
  }
}
```

### List Plots (with filters)
```
GET /api/projects/{project_id}/plots?status=AVAILABLE&block=A

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "plot_uuid",
      "plot_number": "045",
      "block": "A",
      "size_sqft": 5000,
      "current_price": 25000000,
      "status": "AVAILABLE"
    },
    ...
  ]
}
```

### Get Plot Details
```
GET /api/projects/{project_id}/plots/{plot_id}

Headers:
Authorization: Bearer token

Response (200):
{
  "success": true,
  "data": {
    "id": "plot_uuid",
    "plot_number": "045",
    "project_code": "GW",
    "size_sqft": 5000,
    "current_price": 25000000,
    "status": "SOLD",
    "current_deal": {
      "deal_id": "BTM-GW-045-2026-000001",
      "client_name": "Ali Ahmed Khan",
      "deal_amount": 25000000
    }
  }
}
```

### Reserve Plot (for deal)
```
POST /api/projects/{project_id}/plots/{plot_id}/reserve

Headers:
Authorization: Bearer operator_token

Request Body:
{
  "deal_id": "deal_uuid",
  "client_id": "client_uuid"
}

Response (200):
{
  "success": true,
  "message": "Plot reserved for deal",
  "data": {
    "plot_id": "plot_uuid",
    "status": "RESERVED",
    "reserved_until": "2026-05-11"
  }
}
```

### Release Plot
```
POST /api/projects/{project_id}/plots/{plot_id}/release

Headers:
Authorization: Bearer owner_token

Request Body:
{
  "reason": "Deal cancelled",
  "deal_id": "deal_uuid"
}

Response (200):
{
  "success": true,
  "message": "Plot released to AVAILABLE",
  "data": {
    "plot_id": "plot_uuid",
    "status": "AVAILABLE"
  }
}
```

---

## 📊 Project Status Lifecycle

```
PLANNING (Pre-launch)
  ↓
ACTIVE (Selling phase)
  ↓
ON_HOLD (Temporary pause)
  ↓
COMPLETED (Project finished)
  ↓
CANCELLED (Project cancelled)
```

---

## 📊 Plot Status Lifecycle

```
AVAILABLE (Can be sold)
  ↓
RESERVED (Reserved for 30 days)
  ↓
SOLD (Deal created, in payment)
  ↓
COMPLETED (Full payment made)
  OR
CANCELLED (Deal cancelled, back to AVAILABLE)
```

---

## 📈 Project Statistics

```yaml
statistics:
  total_plots: 500
  available_plots: 200
  reserved_plots: 50
  sold_plots: 250
  
  financial:
    total_potential_revenue: 12500000000  # 500 plots × 25M
    realized_revenue: 6250000000          # 250 sold × 25M
    pending_revenue: 3125000000           # 125 reserved × 25M
    pending_payments: 1875000000          # Expected from active deals
  
  timeline:
    launch_date: "2026-04-01"
    expected_completion: "2029-12-31"
    actual_completion: null
```

---

## ✅ Project & Plot Checklist

- [ ] Project model created
- [ ] Plot model created
- [ ] Project code generation
- [ ] Plot number generation
- [ ] Create project endpoint
- [ ] List projects endpoint
- [ ] Get project details endpoint
- [ ] Update project endpoint
- [ ] Create plot endpoint
- [ ] List plots endpoint
- [ ] Get plot details endpoint
- [ ] Reserve plot logic
- [ ] Release plot logic
- [ ] Plot status transitions
- [ ] Project statistics calculation
- [ ] Project validators
- [ ] Project service
- [ ] Project controller
- [ ] Swagger documentation
- [ ] Unit tests
- [ ] Integration tests
