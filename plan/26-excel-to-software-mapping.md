# 📊 Excel to Software Mapping Guide

## 🎯 Purpose

This document maps your existing **BestTimeMarketing_CRM_v2.xlsx** Excel workbook to the new Real Estate CRM Software system. Understanding this mapping helps with data migration and feature planning.

---

## 📁 Excel Sheet Structure Analysis

### Sheet 1: SETTINGS

**Current Purpose**: Projects list, master data, configuration

**Current Data**:
```
✓ Project Codes (GW, DHA6, BTM, etc.)
✓ Project Names
✓ Locations
✓ Total Units per project
✓ Dropdown lists for status values:
  - Registry Status: Done, Not Done, Late
  - Custom dropdown lists
```

**Maps To Software**:
```
Database Table: projects + settings

Entities:
  - projects table (project_code, project_name, location, total_units)
  - system_settings table (dropdown_values, configuration)
  - registry_statuses (enum: DONE, NOT_DONE, LATE)

API Endpoints:
  - GET /api/projects (list all projects)
  - POST /api/projects (admin only)
  - GET /api/settings/dropdowns
```

**Dashboard Location**: 
- Admin Panel → Projects
- Settings → Dropdown Customization

---

### Sheet 2: DATA ENTRY (203 rows × 48 columns) 🎯 CORE SHEET

**Current Purpose**: Client booking data, deal information, payment details

**Current Data Structure**:

```yaml
Row Headers (Key Columns):
  A. Row #                    → Auto incrementing identifier
  B. Unique Deal ID           → Formula: BTM-GW-045-2026-000001
  C. Project                  → Lookup from SETTINGS
  D. Dare / Block             → Location identifier
  E. Plot No.                 → Plot number
  F. Size (Marla)             → Land size in Marla units
  G. Res / Comm               → Dropdown: Residential / Commercial
  H. Payment Type             → Dropdown: Token, Installment, etc.
  I. Per Marla Rate (PKR)     → Unit price
  J. Total Amount (PKR)       → Formula: F × I
  K. Token/Advance (PKR)      → Down payment
  L. Installment Months       → Number of monthly payments
  M. Monthly Instalment (PKR) → Formula: (J - K) / L
  N. Bubble Payment (PKR)     → Mid-term payment
  
  + Additional Columns:
    - Applicant Name
    - CNIC
    - Phone
    - Address
    - Email
    - Nationality
    - Payment Options
    - Registry Status
    - Notes
    - Reference source
```

**Actual Sample Deal (from Excel)**:
```
Row 4 (First data row):
  Unique Deal ID: = IF(C4="","",IF(E4="","",IFERROR("BTM-"&LEFT(C4,3)&"-"&E4&"-"&TEXT(TODAY(),"YY")&"-"&TEXT(A4,"000"),"")))
  Format: {TENANT}-{PROJECT_CODE}-{PLOT_NO}-{YEAR}-{SEQUENCE}
  
  Example: BTM-GW-045-2026-0001
  (Best Time Marketing, GW Project, Plot 045, Year 2026, Deal #0001)
```

**Maps To Software**:

```
Primary Database Tables:
  1. deals
  2. clients  
  3. plots
  4. payment_plans
  5. payments (recorded later in INSTALMENTS sheet)

Deal Table Schema:
  deal_id (UUID) ← Primary key
  tenant_id (UUID) ← Multi-tenant
  deal_code (String) ← Excel: "BTM-GW-045-2026-0001"
  client_id (FK)
  project_id (FK)
  plot_id (FK)
  size_marla (Float) ← Excel column F
  property_type (String) ← Excel column G: Residential/Commercial
  payment_type (String) ← Excel column H: Token/Installment/etc.
  rate_per_marla (Float) ← Excel column I
  total_amount (Float) ← Excel column J (auto-calculated)
  advance_payment (Float) ← Excel column K
  num_installments (Int) ← Excel column L
  monthly_installment (Float) ← Excel column M (auto-calculated)
  bubble_payment (Float) ← Excel column N
  status (String) ← ACTIVE, COMPLETED, DEFAULTED, CANCELLED
  registry_status (String) ← Excel column from SETTINGS: Done/Not Done/Late
  
Client Table (extracted from DATA ENTRY):
  client_id (UUID)
  tenant_id (UUID)
  full_name (String) ← Excel: Applicant Name
  cnic (String encrypted) ← Excel: CNIC
  phone (String) ← Excel: Phone
  email (String) ← Excel: Email
  address (String) ← Excel: Address
  nationality (String) ← Excel: Nationality
  kyc_verified (Boolean)
  
Plot Table (extracted from DATA ENTRY):
  plot_id (UUID)
  project_id (FK)
  plot_number (String) ← Excel: Plot No.
  block_section (String) ← Excel: Dare/Block
  size_marla (Float) ← Excel: Size (Marla)
  property_type (String) ← Excel: Res/Comm
  status (String) ← AVAILABLE, RESERVED, SOLD, COMPLETED
  current_price (Float) ← From SETTINGS projects
```

**Software API Mapping**:

```
DATA ENTRY Sheet ↔ Software APIs

CREATE DEAL:
  POST /api/deals
  Body: {
    "project_code": "GW",           ← Excel column C
    "plot_number": "045",            ← Excel column E
    "client_name": "Ahmed Ali",      ← Excel: Applicant Name
    "cnic": "12345-1234567-8",      ← Excel: CNIC
    "phone": "+92-300-1234567",      ← Excel: Phone
    "size_marla": 5.5,               ← Excel column F
    "property_type": "RESIDENTIAL",  ← Excel column G
    "payment_type": "INSTALLMENT",   ← Excel column H
    "rate_per_marla": 200000,        ← Excel column I
    "advance_payment": 100000,       ← Excel column K
    "num_installments": 12,          ← Excel column L
    "bubble_payment": 150000         ← Excel column N
  }
  
  Response: {
    "deal_code": "BTM-GW-045-2026-0001",  ← Auto-generated like Excel
    "total_amount": 1100000,               ← Auto-calculated (5.5 × 200000)
    "monthly_installment": 75000,          ← Auto-calculated
    "status": "ACTIVE"
  }

RETRIEVE DEAL:
  GET /api/deals/BTM-GW-045-2026-0001
  → Returns full deal details matching Excel row

UPDATE DEAL (Registry Status):
  PATCH /api/deals/{deal_id}
  Body: {
    "registry_status": "DONE"  ← From Excel SETTINGS dropdown
  }

LIST DEALS (Like viewing all of DATA ENTRY):
  GET /api/deals?tenant_id=xxx&project=GW&status=ACTIVE
```

**Dashboard Location**: 
- Sales Dashboard → View All Deals
- Sales Dashboard → New Deal (creates new row in Excel)
- Edit Deal → Modify existing deal
- TenantManager Dashboard → Add Team Members (NEW)

---

### Sheet 3: INSTALMENTS (502 rows × 12 columns)

**Current Purpose**: Track each installment payment for each deal

**Current Structure**:

```yaml
Column Headers:
  A. Inst. #                  → Installment number (1, 2, 3, ...)
  B. Month                    → Due month
  C. Deal ID                  → Lookup to DATA ENTRY sheet B
  D. Applicant Name           → Auto-lookup from DATA ENTRY
  E. Project                  → Auto-lookup from DATA ENTRY
  F. Plot No.                 → Auto-lookup from DATA ENTRY
  G. Due Date                 → Payment due date
  H. Amount Due (PKR)         → Monthly installment amount
  I. Amount Paid (PKR)        → Actual amount paid
  J. Payment Date             → Date payment received
  K. Shortfall (PKR)          → Formula: H - I
  L. Status                   → Formula-based:
                                ✅ Paid (if I >= H)
                                🔴 Overdue (if J < TODAY())
                                🟡 Due Soon (if J <= TODAY()+90)
                                ⬜ Upcoming
```

**Example Row**:
```
Deal: BTM-GW-045-2026-0001
  Installment 1: Due 2026-04-25, Amount 75000 PKR
  Installment 2: Due 2026-05-25, Amount 75000 PKR
  Installment 3: Due 2026-06-25, Amount 75000 PKR
  ... (x12 months)
```

**Maps To Software**:

```
Primary Database Tables:
  1. payments
  2. payment_schedules
  3. client_ledger

Payment Table Schema:
  payment_id (UUID)
  deal_id (FK) ← Excel column C (Deal ID)
  payment_number (Int) ← Excel column A (Inst. #)
  payment_type (String) ← INSTALLMENT, ADVANCE, BUBBLE, FINAL
  due_date (Date) ← Excel column G
  amount_due (Float) ← Excel column H
  amount_paid (Float) ← Excel column I
  payment_date (Date) ← Excel column J
  balance_due (Float) ← Excel column K (H - I)
  status (String) ← PENDING, PAID, OVERDUE, LATE, DEFAULTED
  payment_method (String) ← CASH, BANK_TRANSFER, CHEQUE, etc.
  reference_no (String) ← Cheque no, receipt no, etc.
  notes (Text)
  created_at (Timestamp)
  updated_at (Timestamp)

Client Ledger Table (Summary):
  ledger_id (UUID)
  client_id (FK)
  deal_id (FK)
  total_amount (Float)
  total_paid (Float)
  outstanding_balance (Float) ← Formula like Excel
  paid_percentage (Int)
  default_status (Boolean) ← If any payment is 90+ days late
```

**Software API Mapping**:

```
INSTALMENTS Sheet ↔ Software APIs

RECORD PAYMENT:
  POST /api/payments
  Body: {
    "deal_id": "BTM-GW-045-2026-0001",
    "payment_number": 1,
    "amount_paid": 75000,
    "payment_date": "2026-04-22",
    "payment_method": "BANK_TRANSFER",
    "reference_no": "TRF-202604-001",
    "status": "PAID"
  }
  
  After API call:
    - Row populated in INSTALMENTS sheet (if Excel integrated)
    - Status auto-calculated
    - Shortfall calculated
    - Client ledger updated
    - Receipt generated

GET PAYMENT SCHEDULE:
  GET /api/deals/{deal_id}/payment-schedule
  → Returns all rows for this deal from INSTALMENTS

GET INSTALLMENT DUE:
  GET /api/payments?status=OVERDUE&tenant_id=xxx
  → Returns all overdue payments (🔴 Status from Excel)

GET CLIENT LEDGER:
  GET /api/clients/{client_id}/ledger
  → Returns summary matching Excel totals

Daily Job (like Excel formulas):
  - APScheduler checks all payments daily
  - Updates status based on due date
  - Marks OVERDUE if today > due_date and amount_paid < amount_due
  - Sends reminder notifications
```

**Dashboard Location**: 
- Payment Tracking → View All Payments
- Client Dashboard → Payment Schedule (pull all rows f or a client)
- Reports → Overdue Payments
- Notifications → Payment Reminders

---

### Sheet 4: PAYMENT SCHEDULE

**Current Purpose**: Generate full payment plan for a single deal

**Structure**:
```
Header: "📅 PAYMENT SCHEDULE GENERATOR — Type a Deal ID in B4 to auto-generate full schedule"

Input: Deal ID (from DATA ENTRY sheet)
Output: Monthly schedule with all installments, due dates, amounts
```

**Maps To Software**:

```
Function: PaymentPlanGenerator
  Input: deal_id
  Process:
    1. Fetch deal from database
    2. Calculate payment schedule based on:
       - num_installments (from deals table)
       - monthly_installment amount (from deals table)
       - start_date (deal creation date)
       - payment_type (INSTALLMENT, ADVANCE, BUBBLE, FINAL)
    3. Generate 12 rows (or as per installment count)
    4. Set due dates (same day each month)
    5. Create payment_schedule records
  Output: List of payment objects

API Endpoint:
  POST /api/deals/{deal_id}/generate-payment-schedule
  → Creates all payment records for a deal
  
  OR
  
  GET /api/deals/{deal_id}/payment-schedule
  → Returns pre-generated schedule
```

**Dashboard Location**: 
- Deal Creation → Auto-generate payment schedule
- Deal Management → View/Edit payment schedule

---

### Sheet 5: CLIENT COPY

**Current Purpose**: Official booking confirmation document

**Structure**:
```
Header: "🏢 BEST TIME MARKETING - OFFICIAL BOOKING CONFIRMATION"
Input: Enter Deal ID in cell C4
Output: Auto-filled form with:
  - Deal details
  - Client details
  - Payment schedule
  - Terms & conditions
  - Signature area
```

**Maps To Software**:

```
Function: Generate Booking Receipt/Confirmation
  Input: deal_id
  Process:
    1. Fetch deal + client + project details
    2. Render HTML template (like Excel template)
    3. Fill in all values
    4. Generate PDF
    5. Store in Cloudinary/S3
  Output: PDF file

API Endpoint:
  GET /api/deals/{deal_id}/confirmation
  → Returns PDF for download
  
  OR
  
  POST /api/deals/{deal_id}/send-confirmation
  → Sends PDF via WhatsApp/Email to client

Service:
  class ReceiptService:
    def generate_booking_confirmation(deal_id):
      → Generates PDF like Excel sheet
      
  class NotificationService:
    def send_confirmation_to_client(deal_id, client_phone, client_email):
      → Sends PDF via WhatsApp + Email

Template (HTML/CSS):
  <div class="confirmation">
    <h1>BOOKING CONFIRMATION</h1>
    <table>
      <tr><td>Deal ID:</td><td>{deal_code}</td></tr>
      <tr><td>Client:</td><td>{client_name}</td></tr>
      <tr><td>CNIC:</td><td>{cnic_masked}</td></tr>
      <tr><td>Project:</td><td>{project_name}</td></tr>
      <tr><td>Plot No:</td><td>{plot_number}</td></tr>
      ...
    </table>
  </div>
```

**Dashboard Location**: 
- Deal View → Download Confirmation
- Deal View → Send Confirmation to Client

---

### Sheet 6: DASHBOARD (22 rows × 12 columns)

**Current Purpose**: Management dashboard with KPIs

**Current Metrics**:
```
✓ TOTAL DEALS (formula-based count)
✓ TOTAL REVENUE (PKR) (sum of all deal amounts)
✓ TOTAL RECEIVED (PKR) (sum of all payments made)
✓ BALANCE DUE (PKR) (Total Revenue - Total Received)
✓ Visual charts and trends
```

**Maps To Software**:

```
Software Dashboard with same metrics:

GET /api/dashboard/metrics
Response: {
  "total_deals": 45,
  "active_deals": 42,
  "completed_deals": 3,
  "total_revenue": 50000000,        ← Sum of all deal amounts (like Excel)
  "total_received": 35000000,       ← Sum of all payments
  "balance_due": 15000000,          ← Calculated (revenue - received)
  "overdue_amount": 2500000,        ← New KPI
  "average_deal_value": 1111111,
  "deals_by_status": {
    "ACTIVE": 42,
    "COMPLETED": 3,
    "DEFAULTED": 0
  },
  "sales_by_month": [...],  ← Charts
  "payment_trends": [...],  ← Charts
}

Also new to Software (not in current Excel):
  - Sales team performance
  - Top performing salesmen
  - Client satisfaction
  - KYC verification status
  - Late payment details
  - Receipt pending list
```

**Software Dashboard Has**:
```
Different views based on role:
  1. Admin Dashboard: All company overview
  2. Sales Dashboard: Deal performance, sales targets
  3. Finance Dashboard: Payment collection, ledger, cash flow
  4. Manager Dashboard: Team performance, assignments

Each dashboard auto-updates from database
Charts generated in real-time (vs manual Excel)
```

**Dashboard Location**: 
- Main Dashboard → Overview
- Sales Dashboard → Sales metrics
- Finance Dashboard → Payment metrics
- Manager Dashboard → Team metrics

---

## 🔄 Data Migration Plan

### Phase 1: Preparation

```sql
-- Create all database tables
CREATE TABLE clients (...)
CREATE TABLE projects (...)
CREATE TABLE plots (...)
CREATE TABLE deals (...)
CREATE TABLE payments (...)
CREATE TABLE receipts (...)
...
```

### Phase 2: Data Mapping

```python
# Example data migration script
def migrate_deals_from_excel():
    """
    Read DATA ENTRY sheet
    For each data row:
      1. Extract client info → Create client record
      2. Extract deal info → Create deal record
      3. Auto-generate deal_code (BTM-GW-045-2026-0001)
      4. Store in PostgreSQL deals table
    """

def migrate_payments_from_excel():
    """
    Read INSTALMENTS sheet
    For each row:
      1. Lookup deal by deal_id
      2. Extract payment info → Create payment record
      3. Calculate status (Paid, Overdue, etc.)
      4. Store in PostgreSQL payments table
    """
```

### Phase 3: Validation

```
✓ All deal codes match Excel
✓ All client info migrated
✓ Payment calculations match
✓ Ledger balances correct
✓ Registry status preserved
```

---

## 📊 Excel vs Software Feature Comparison

| Feature | Excel | Software |
|---------|-------|----------|
| Deal Creation | Manual rows | API + Dashboard form |
| Deal ID Generation | Formula | Auto-generated API |
| Payment Tracking | Manual rows | Automatic with notifications |
| Payment Calculation | Formulas | Database + APIs |
| Status Updates | Manual formula | Auto-updated via jobs |
| Client Lookup | VLOOKUP | Database join + API |
| Reports | Manual pivot tables | Real-time dashboards |
| Notifications | Manual | Automatic WhatsApp/Email |
| Receipts | Manual copy/paste | Auto-generated PDFs |
| Multi-user | Limited (shared file) | Full RBAC system |
| Accessibility | Desktop only | Web + Mobile ready |
| Data Backup | Manual | Automatic daily |
| Scalability | 500 rows max | Unlimited |
| Real-time Updates | No | Yes |
| Mobile Access | No | Yes |
| Permission Control | No | Yes (RBAC) |
| Audit Trail | No | Yes (all actions logged) |
| Dashboard Metrics | Static | Dynamic in real-time |
| User Management | Not possible | Full system + Dashboard |

---

## ✨ New Features (Not in Excel)

### 1. User Management (Dashboard)
```
NEW: Tenant manager can add users from Dashboard
  - Add Team Members dialog
  - User list with status
  - Edit/Delete users
  - Permission control
  - Invitation emails
```

### 2. Real-time Notifications
```
NEW: Automatic alerts
  - Payment reminders
  - Overdue alerts
  - Deal confirmations
  - Receipt notifications
```

### 3. Mobile App
```
NEW: Sales team can view/create deals on mobile
  - View assigned deals
  - Record payments
  - Generate receipts
  - View payment schedule
```

### 4. Detailed Ledger
```
NEW: Per-client financial summary
  - Payment history
  - Outstanding balance
  - Due installments
  - Commission tracking (for salesmen)
```

### 5. Analytics & Reports
```
NEW: Advanced reporting
  - Sales by region
  - Top performing plots
  - Client payment patterns
  - Salesman performance
  - Commission calculations
```

---

## 📝 Implementation Checklist

- [ ] Create database schema for all tables
- [ ] Create data migration scripts from Excel
- [ ] Migrate existing clients from Excel
- [ ] Migrate existing deals from Excel
- [ ] Migrate payment history from Excel
- [ ] Validate all data integrity
- [ ] Create test deals in new system
- [ ] Compare calculations (total, balance, etc.)
- [ ] Train team on new system
- [ ] Set cutover date for live migration
- [ ] Archive Excel file (keep as backup)
- [ ] Decommission Excel system

---

## 🎯 Mapping Summary Table

```
┌─────────────────────────────────────────────────────────┐
│  EXCEL SHEET  →  DATABASE/API  →  SOFTWARE FEATURE     │
├─────────────────────────────────────────────────────────┤
│ SETTINGS      →  projects, settings  →  Admin Config   │
│ DATA ENTRY    →  clients, deals      →  Deal Management│
│ INSTALMENTS   →  payments            →  Payment Track  │
│ PAYMENT SCH   →  payment_schedules   →  Auto Generate  │
│ CLIENT COPY   →  receipts            →  PDF Receipt    │
│ DASHBOARD     →  analytics, reports  →  Dashboard      │
│               →  users               →  Team Members   │
└─────────────────────────────────────────────────────────┘
```

---

## 🚀 Next Steps

1. **Review** this mapping with Excel users
2. **Extract** current data from Excel
3. **Prepare** database structure
4. **Migrate** data in phases (Clients → Deals → Payments)
5. **Validate** all calculations
6. **Train** team on new system
7. **Go Live** with cutover date

---

**Generated**: April 11, 2026
**Excel File**: BestTimeMarketing_CRM_v2.xlsx
**Status**: Mapping Complete ✅

