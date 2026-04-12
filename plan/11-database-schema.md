# 🗄️ Database Schema Design

## 📋 Overview
PostgreSQL database schema with multi-tenant isolation, relationships, and indexing strategy.

---

## 🏢 Core Tables

### User Table
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  email VARCHAR(255) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  first_name VARCHAR(100),
  last_name VARCHAR(100),
  phone VARCHAR(20),
  avatar_url TEXT,
  role VARCHAR(50) NOT NULL,
  status VARCHAR(50) DEFAULT 'ACTIVE',
  email_verified BOOLEAN DEFAULT FALSE,
  last_login TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by UUID REFERENCES users(id),
  
  UNIQUE(tenant_id, email),
  INDEX idx_user_tenant (tenant_id),
  INDEX idx_user_email (email)
);
```

### Tenant Table
```sql
CREATE TABLE tenants (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_code VARCHAR(20) UNIQUE NOT NULL,
  company_name VARCHAR(255) NOT NULL,
  company_email VARCHAR(255),
  phone VARCHAR(20),
  address TEXT,
  city VARCHAR(100),
  country VARCHAR(100),
  subscription_plan VARCHAR(50) DEFAULT 'FREE',
  paid_until TIMESTAMP,
  status VARCHAR(50) DEFAULT 'ACTIVE',
  settings JSONB DEFAULT '{}',
  metadata JSONB DEFAULT '{}',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by UUID REFERENCES users(id),
  
  INDEX idx_tenant_code (tenant_code),
  INDEX idx_tenant_status (status)
);
```

### Client Table
```sql
CREATE TABLE clients (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  client_code VARCHAR(50) NOT NULL,
  full_name VARCHAR(255) NOT NULL,
  email VARCHAR(255),
  phone VARCHAR(20),
  whatsapp_phone VARCHAR(20),
  cnic VARCHAR(255),  -- Encrypted
  cnic_expiry DATE,
  passport_number VARCHAR(50),
  address TEXT,
  city VARCHAR(100),
  country VARCHAR(100),
  postal_code VARCHAR(20),
  occupation VARCHAR(100),
  company_name VARCHAR(255),
  referred_by VARCHAR(255),
  referred_by_user_id UUID,
  status VARCHAR(50) DEFAULT 'ACTIVE',
  kyc_verified BOOLEAN DEFAULT FALSE,
  kyc_document TEXT,
  total_deals INTEGER DEFAULT 0,
  total_investments DECIMAL(15,2) DEFAULT 0,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by UUID REFERENCES users(id),
  
  UNIQUE(tenant_id, client_code),
  UNIQUE(tenant_id, cnic),  -- CNIC unique per tenant
  INDEX idx_client_tenant (tenant_id),
  INDEX idx_client_phone (phone),
  INDEX idx_client_status (status)
);
```

### Project Table
```sql
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  project_code VARCHAR(50) NOT NULL,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  type VARCHAR(50),  -- RESIDENTIAL, COMMERCIAL
  category VARCHAR(50),  -- PLOT, APARTMENT
  city VARCHAR(100),
  area_name VARCHAR(100),
  address TEXT,
  coordinates JSONB,  -- {latitude, longitude}
  total_plots INTEGER,
  available_plots INTEGER,
  sold_plots INTEGER DEFAULT 0,
  base_price_per_sqft DECIMAL(10,2),
  launch_date DATE,
  expected_completion DATE,
  completion_date DATE,
  logo_url TEXT,
  brochure_url TEXT,
  images JSONB DEFAULT '[]',
  status VARCHAR(50) DEFAULT 'ACTIVE',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by UUID REFERENCES users(id),
  
  UNIQUE(tenant_id, project_code),
  INDEX idx_project_tenant (tenant_id),
  INDEX idx_project_status (status)
);
```

### Plot Table
```sql
CREATE TABLE plots (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  project_id UUID NOT NULL REFERENCES projects(id),
  plot_number VARCHAR(50) NOT NULL,
  block VARCHAR(10),
  sector VARCHAR(50),
  size_sqft DECIMAL(10,2),
  size_sqm DECIMAL(10,2),
  base_price DECIMAL(15,2),
  current_price DECIMAL(15,2),
  price_per_sqft DECIMAL(10,2),
  status VARCHAR(50) DEFAULT 'AVAILABLE',
  current_deal_id UUID,  -- REFERENCES deals(id)
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(tenant_id, project_id, plot_number),
  INDEX idx_plot_project (project_id),
  INDEX idx_plot_status (status),
  INDEX idx_plot_deal (current_deal_id)
);
```

### Deal Table
```sql
CREATE TABLE deals (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  deal_id VARCHAR(50) NOT NULL,  -- BTM-GW-045-2026-000001
  client_id UUID NOT NULL REFERENCES clients(id),
  project_id UUID NOT NULL REFERENCES projects(id),
  plot_id UUID NOT NULL REFERENCES plots(id),
  salesman_id UUID REFERENCES users(id),
  dealer_id UUID,
  total_amount DECIMAL(15,2) NOT NULL,
  advance_payment DECIMAL(15,2) NOT NULL,
  outstanding_balance DECIMAL(15,2) NOT NULL,
  deal_structure JSONB,  -- Payment plan structure
  status VARCHAR(50) DEFAULT 'CREATED',
  salesman_commission_percentage DECIMAL(5,2),
  dealer_commission_percentage DECIMAL(5,2),
  deal_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  signed_date TIMESTAMP,
  completion_date TIMESTAMP,
  notes TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by UUID REFERENCES users(id),
  
  UNIQUE(tenant_id, deal_id),
  UNIQUE(tenant_id, plot_id),  -- One deal per plot
  INDEX idx_deal_tenant (tenant_id),
  INDEX idx_deal_client (client_id),
  INDEX idx_deal_project (project_id),
  INDEX idx_deal_status (status)
);
```

### Payment Table
```sql
CREATE TABLE payments (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  deal_id UUID NOT NULL REFERENCES deals(id),
  amount DECIMAL(15,2) NOT NULL,
  payment_type VARCHAR(50) NOT NULL,  -- ADVANCE, INSTALLMENT, BUBBLE
  payment_date TIMESTAMP NOT NULL,
  method VARCHAR(50),  -- CASH, CHECK, BANK_TRANSFER
  installment_number INTEGER,
  installment_due_date DATE,
  recorded_by UUID NOT NULL REFERENCES users(id),
  reference_number VARCHAR(100),
  notes TEXT,
  status VARCHAR(50) DEFAULT 'PAID',  -- PENDING, PAID, OVERDUE
  verification_date TIMESTAMP,
  verified_by UUID REFERENCES users(id),
  balance_after_payment DECIMAL(15,2),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  INDEX idx_payment_deal (deal_id),
  INDEX idx_payment_tenant (tenant_id),
  INDEX idx_payment_date (payment_date),
  INDEX idx_payment_status (status)
);
```

### Receipt Table
```sql
CREATE TABLE receipts (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  payment_id UUID REFERENCES payments(id),
  deal_id UUID REFERENCES deals(id),
  client_id UUID REFERENCES clients(id),
  receipt_number VARCHAR(50) NOT NULL,
  receipt_type VARCHAR(50) NOT NULL,
  title VARCHAR(255),
  description TEXT,
  details JSONB,
  pdf_url TEXT,
  original_filename VARCHAR(255),
  file_size_bytes INTEGER,
  status VARCHAR(50) DEFAULT 'GENERATED',
  sent_at TIMESTAMP,
  viewed_at TIMESTAMP,
  printed_at TIMESTAMP,
  issue_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  expiry_date TIMESTAMP,
  currency VARCHAR(10),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by UUID REFERENCES users(id),
  downloaded_count INTEGER DEFAULT 0,
  
  UNIQUE(tenant_id, receipt_number),
  INDEX idx_receipt_tenant (tenant_id),
  INDEX idx_receipt_deal (deal_id),
  INDEX idx_receipt_payment (payment_id)
);
```

### Notification Table
```sql
CREATE TABLE notifications (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id UUID NOT NULL REFERENCES tenants(id),
  recipient_id UUID,
  recipient_name VARCHAR(255),
  recipient_phone VARCHAR(20),
  recipient_email VARCHAR(255),
  notification_type VARCHAR(50),
  title VARCHAR(255),
  message TEXT,
  channel VARCHAR(50),  -- WHATSAPP, EMAIL, SMS
  template_id VARCHAR(100),
  status VARCHAR(50) DEFAULT 'PENDING',
  sent_at TIMESTAMP,
  delivery_status VARCHAR(50),
  reference_id VARCHAR(255),
  error_message TEXT,
  retry_count INTEGER DEFAULT 0,
  metadata JSONB,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by UUID REFERENCES users(id),
  
  INDEX idx_notification_tenant (tenant_id),
  INDEX idx_notification_status (status),
  INDEX idx_notification_created (created_at)
);
```

---

## 🔐 Security & Indexing

### Row-Level Security Policies
```sql
-- All tables must have tenant_id filter
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

CREATE POLICY tenant_isolation ON users
  USING (tenant_id = current_tenant_id());

-- Apply same policy to all tables
```

### Key Indexes Summary
```yaml
users:
  - (tenant_id, email) UNIQUE
  - (tenant_id)
  - (email)

tenants:
  - (tenant_code) UNIQUE
  - (status)

clients:
  - (tenant_id, client_code) UNIQUE
  - (tenant_id, cnic) UNIQUE
  - (tenant_id)
  - (status)

deals:
  - (tenant_id, deal_id) UNIQUE
  - (tenant_id, plot_id) UNIQUE
  - (client_id)
  - (project_id)
  - (status)

payments:
  - (deal_id)
  - (tenant_id)
  - (payment_date)
  - (status)

receipts:
  - (tenant_id, receipt_number) UNIQUE
  - (deal_id)
  - (payment_id)
```

---

## 📊 Relationships Diagram

```
Tenant
  ├── Users
  ├── Clients
  ├── Projects
  │   └── Plots
  │       └── Deals
  │           ├── Payments
  │           │   └── Receipts
  │           └── Notifications
```

---

## ✅ Database Schema Checklist

- [ ] All tables created
- [ ] Primary keys defined
- [ ] Foreign keys defined
- [ ] Unique constraints
- [ ] Indexes created
- [ ] RLS policies enabled
- [ ] Tenant isolation enforced
- [ ] JSONB columns for flexibility
- [ ] Audit columns (created_at, updated_at)
- [ ] created_by tracking
- [ ] Encryption for sensitive fields (CNIC)
- [ ] Partitioning strategy (if needed)
- [ ] Backup strategy
- [ ] Migration scripts
