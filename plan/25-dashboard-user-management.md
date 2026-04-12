# 👥 Dashboard User Management System

## 🎯 Overview

Tenant managers can add, manage, and remove users directly from the dashboard without accessing the admin panel. This provides a streamlined UX for team member onboarding.

---

## 📊 Data Structure (Based on Your Excel)

Your current Excel system tracks:

### Primary Entities from "DATA ENTRY" Sheet
```yaml
Deal (Plot Client Entry):
  Unique Deal ID: "BTM-GW-045-2026-000001"  # Auto-generated
  Project: "String (GW, DHA6, etc.)"
  Block/Dare: "String"
  Plot Number: "Integer"
  Size (Marla): "Float"
  Res/Comm: "Dropdown (Residential/Commercial)"
  Payment Type: "Dropdown (Token, Installment, etc.)"
  Per Marla Rate (PKR): "Float"
  Total Amount (PKR): "Float (auto calculated = Size * Rate)"
  Token/Advance (PKR): "Float"
  Installment Months: "Integer"
  Monthly Installment (PKR): "Float (auto calculated)"
  Bubble Payment (PKR): "Float"
  
Client Information:
  Applicant Name: "String"
  CNIC / ID: "String"
  Contact No: "Phone"
  Address: "String"
  
Additional Fields:
  Registry Status: "Dropdown (Done, Not Done, Late)"
  Payment Status: "Formula-based (Paid, Overdue, Due Soon, Upcoming)"
```

### Current Excel Sheets Mapping

| Excel Sheet | Purpose | Rows | Columns | Maps To |
|-------------|---------|------|---------|---------|
| SETTINGS | Projects & Dropdown lists | 15 | 15 | System Configuration |
| DATA ENTRY | Client bookings/deals | 203 | 48 | Deals + Clients |
| INSTALMENTS | Payment tracking | 502 | 12 | Payments Ledger |
| PAYMENT SCHEDULE | Auto-generated plans | 54 | 9 | Payment Plans |
| CLIENT COPY | Booking confirmation | 34 | 5 | Receipt/Documentation |
| DASHBOARD | Management metrics | 22 | 12 | Analytics Dashboard |

---

## 🎛️ Dashboard User Management Features

### 1. User Add Modal/Form

**Location**: Dashboard → Settings Tab → Team Members

**Access Control**:
- TENANT_OWNER: Can add all roles (except SUPER_ADMIN/PLATFORM_ADMIN)
- MANAGER: Can add OPERATOR, SALESMAN, ACCOUNTANT roles only
- OPERATOR, SALESMAN, ACCOUNTANT: No access

**Form Fields**:

```yaml
Add User Form:
  Full Name:
    type: text
    required: true
    min_length: 3
    max_length: 100
    placeholder: "e.g., Ahmed Ali"
    
  Email Address:
    type: email
    required: true
    validation: "Must be unique per tenant"
    placeholder: "user@example.com"
    
  Phone Number:
    type: tel
    required: true
    format: "+92-XXX-XXXXXXX"
    placeholder: "+92-300-1234567"
    
  Role:
    type: dropdown
    required: true
    options:
      - "MANAGER" (if TENANT_OWNER)
      - "OPERATOR" (if TENANT_OWNER or MANAGER)
      - "SALESMAN" (if TENANT_OWNER or MANAGER)
      - "ACCOUNTANT" (if TENANT_OWNER or MANAGER)
      - "DEALER" (if TENANT_OWNER)
    
  Permissions (Optional):
    type: multi-select
    depends: Selected Role
    options:
      - "create_deal"
      - "view_deals"
      - "edit_own_deals"
      - "delete_deal"
      - "record_payment"
      - "view_payments"
      - "generate_receipt"
      - "view_reports"
      - "export_data"
      - "manage_users"
      - "view_ledger"
      - "adjust_prices"
      - "approve_payments"
    
  Send Invitation Email:
    type: checkbox
    default: true
    label: "Send welcome email with login link"
    
  Activate Immediately:
    type: checkbox
    default: true
    label: "User can login after creation"
```

### 2. User List/Table in Dashboard

**Display Columns**:
```
┌─────────────────────────────────────────────────┐
│ Name     │ Email      │ Role      │ Status │ ⋯ │
├─────────────────────────────────────────────────┤
│ Ahmed    │ ahmed@...  │ SALESMAN  │ Active │ Edit Delete │
│ Fatima   │ fatima@... │ ACCOUNTANT│ Inactive│ Edit Delete │
│ Hassan   │ hassan@... │ OPERATOR  │ Active │ Edit Delete │
└─────────────────────────────────────────────────┘

Filters:
  - By Role
  - By Status (Active/Inactive)
  - Search by name/email

Bulk Actions:
  - Activate Multiple Users
  - Deactivate Multiple Users
  - Delete Multiple Users
  - Re-send Invitation Email
```

### 3. User Edit Modal

**Features**:
```yaml
Edit User:
  - Update Full Name
  - Update Phone Number
  - Change Role (with validation)
  - Modify Permissions
  - Reset Password (send link via email)
  - Deactivate/Reactivate account
  - View Last Login: "2026-04-10 14:30:22"
  - View Activity Log (last 10 actions)
```

### 4. Delete User with Confirmation

```yaml
Delete Confirmation Dialog:
  Message: "This action cannot be undone"
  Warning: "User will lose access to all deals and reports"
  Option 1: "Archive user (keep data)" - Recommended
  Option 2: "Permanently delete (remove all access)"
  
  Post-Delete:
    - User cannot login
    - User's deals assigned to: [Dropdown to select another user]
    - User's data archived (for 90 days)
    - Audit log records deletion
```

---

## 🔄 API Endpoints for Dashboard User Management

### 1. Add User

```
POST /api/users/create

Request:
{
  "full_name": "Ahmed Ali",
  "email": "ahmed@company.pk",
  "phone": "+92-300-1234567",
  "role": "SALESMAN",
  "permissions": ["create_deal", "view_deals", "record_payment"],
  "send_invitation": true,
  "activate_immediately": true
}

Response:
{
  "success": true,
  "message": "User created successfully",
  "data": {
    "user_id": "uuid-xxx",
    "email": "ahmed@company.pk",
    "role": "SALESMAN",
    "status": "ACTIVE",
    "created_at": "2026-04-11T10:30:00Z",
    "invitation_sent": true
  }
}

Errors:
  400: "EMAIL_ALREADY_EXISTS"
  400: "INVALID_ROLE_FOR_TENANT"
  401: "UNAUTHORIZED - Insufficient permissions"
  422: "VALIDATION_ERROR"
  429: "RATE_LIMIT_EXCEEDED"
```

### 2. Get Users List

```
GET /api/users?role=SALESMAN&status=ACTIVE&page=1&limit=20

Response:
{
  "success": true,
  "message": "Users retrieved",
  "data": {
    "users": [
      {
        "user_id": "uuid-xxx",
        "full_name": "Ahmed Ali",
        "email": "ahmed@company.pk",
        "phone": "+92-300-1234567",
        "role": "SALESMAN",
        "status": "ACTIVE",
        "last_login": "2026-04-10T14:30:22Z",
        "created_at": "2026-04-09T10:00:00Z"
      }
    ],
    "pagination": {
      "total": 25,
      "page": 1,
      "limit": 20,
      "pages": 2
    }
  }
}
```

### 3. Update User

```
PUT /api/users/{user_id}

Request:
{
  "full_name": "Ahmed Ali Khan",
  "phone": "+92-300-9876543",
  "role": "MANAGER",
  "permissions": ["create_deal", "view_deals", "manage_users"],
  "status": "ACTIVE"
}

Response:
{
  "success": true,
  "message": "User updated successfully",
  "data": { updated user object }
}
```

### 4. Delete User

```
DELETE /api/users/{user_id}

Request:
{
  "action": "archive",  # or "delete"
  "assign_deals_to": "uuid-another-user"  # if action is delete
}

Response:
{
  "success": true,
  "message": "User archived successfully",
  "data": {
    "user_id": "uuid-xxx",
    "status": "ARCHIVED"
  }
}
```

### 5. Resend Invitation

```
POST /api/users/{user_id}/resend-invitation

Response:
{
  "success": true,
  "message": "Invitation email sent",
  "data": {
    "user_id": "uuid-xxx",
    "email": "ahmed@company.pk",
    "invitation_sent_at": "2026-04-11T10:35:00Z"
  }
}
```

### 6. Reset User Password

```
POST /api/users/{user_id}/reset-password

Response:
{
  "success": true,
  "message": "Password reset link sent to email",
  "data": {
    "user_id": "uuid-xxx",
    "email": "ahmed@company.pk",
    "reset_link_expires": "2026-04-11T12:35:00Z"
  }
}
```

### 7. Get User Activity Log

```
GET /api/users/{user_id}/activity-log?limit=20

Response:
{
  "success": true,
  "data": {
    "activities": [
      {
        "timestamp": "2026-04-10T14:30:22Z",
        "action": "login",
        "details": "Login from 192.168.1.1",
        "ip_address": "192.168.1.1"
      },
      {
        "timestamp": "2026-04-10T14:31:05Z",
        "action": "deal_created",
        "details": "Created deal BTM-GW-045-2026-000001",
        "deal_id": "uuid-xxx"
      },
      {
        "timestamp": "2026-04-10T14:35:10Z",
        "action": "payment_recorded",
        "details": "Recorded payment of 100,000 PKR",
        "payment_id": "uuid-xxx"
      }
    ]
  }
}
```

---

## 📱 Dashboard UI Components

### User Management Card (Main View)

```html
<!-- Team Members Section in Dashboard -->
<section class="dashboard-section">
  <h2>👥 Team Members (5)</h2>
  
  <div class="controls">
    <button class="btn-primary">+ Add Team Member</button>
    <input type="search" placeholder="Search by name or email">
  </div>
  
  <table class="users-table">
    <thead>
      <tr>
        <th>Name</th>
        <th>Email</th>
        <th>Role</th>
        <th>Status</th>
        <th>Last Login</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody>
      <!-- Users list from API -->
    </tbody>
  </table>
  
  <div class="pagination">
    <!-- Pagination controls -->
  </div>
</section>
```

### Add User Modal

```html
<div class="modal" id="addUserModal">
  <div class="modal-content">
    <h3>Add Team Member</h3>
    
    <form id="addUserForm">
      <div class="form-group">
        <label>Full Name *</label>
        <input type="text" name="full_name" required>
      </div>
      
      <div class="form-group">
        <label>Email Address *</label>
        <input type="email" name="email" required>
      </div>
      
      <div class="form-group">
        <label>Phone Number *</label>
        <input type="tel" name="phone" required>
      </div>
      
      <div class="form-group">
        <label>Role *</label>
        <select name="role" id="roleSelect" required>
          <option value="">Select Role</option>
          <option value="MANAGER">Manager</option>
          <option value="OPERATOR">Operator</option>
          <option value="SALESMAN">Salesman</option>
          <option value="ACCOUNTANT">Accountant</option>
        </select>
      </div>
      
      <div class="form-group">
        <label>Permissions</label>
        <div class="permissions-list">
          <!-- Checkboxes populated based on selected role -->
        </div>
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" name="send_invitation" checked>
          Send welcome email to user
        </label>
      </div>
      
      <div class="form-group">
        <label>
          <input type="checkbox" name="activate_immediately" checked>
          Activate user immediately
        </label>
      </div>
      
      <div class="modal-actions">
        <button type="button" class="btn-secondary" onclick="closeModal()">
          Cancel
        </button>
        <button type="submit" class="btn-primary">
          Add User
        </button>
      </div>
    </form>
  </div>
</div>
```

---

## 🔐 Permission Matrix for User Creation

```
┌──────────────┬─────────┬─────────┬──────────┬────────────┐
│ Role         │ Manager │ Operator│ Salesman │ Accountant │
├──────────────┼─────────┼─────────┼──────────┼────────────┤
│ TENANT_OWNER │ ✅      │ ✅      │ ✅       │ ✅         │
│ MANAGER      │ ❌      │ ✅      │ ✅       │ ✅         │
│ OPERATOR     │ ❌      │ ❌      │ ❌       │ ❌         │
│ SALESMAN     │ ❌      │ ❌      │ ❌       │ ❌         │
│ ACCOUNTANT   │ ❌      │ ❌      │ ❌       │ ❌         │
└──────────────┴─────────┴─────────┴──────────┴────────────┘

Legend:
✅ = Can create this role
❌ = Cannot create this role
```

---

## 📧 Invitation Email Template

Subject: `Welcome to Best Time Marketing - Your Login Credentials`

```html
<h2>Welcome to Best Time Marketing CRM!</h2>

<p>Dear Ahmed,</p>

<p>Your account has been created. Here are your login details:</p>

<table>
  <tr>
    <td><strong>Email:</strong></td>
    <td>ahmed@company.pk</td>
  </tr>
  <tr>
    <td><strong>Role:</strong></td>
    <td>Salesman</td>
  </tr>
  <tr>
    <td><strong>Company:</strong></td>
    <td>Best Time Marketing</td>
  </tr>
</table>

<p>
  <a href="https://crm.example.com/setup-password?token=xyz" class="btn">
    Set Your Password
  </a>
</p>

<p>Click the button above to set your password and log in.</p>

<p>Your login link expires in 7 days.</p>

<hr>

<p><strong>Your Permissions:</strong></p>
<ul>
  <li>Create and manage deals</li>
  <li>View deal reports</li>
  <li>Record payments</li>
</ul>

<p>Need help? Contact your administrator.</p>
```

---

## 🗄️ Database Schema Updates

```sql
-- Users table (existing with new fields)
CREATE TABLE users (
  user_id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  full_name VARCHAR(100) NOT NULL,
  email VARCHAR(255) NOT NULL,
  phone VARCHAR(20),
  password_hash VARCHAR(255),
  role VARCHAR(50) NOT NULL,  -- TENANT_OWNER, MANAGER, OPERATOR, SALESMAN, ACCOUNTANT, DEALER
  status VARCHAR(20) DEFAULT 'ACTIVE',  -- ACTIVE, INACTIVE, ARCHIVED
  invitation_sent_at TIMESTAMP,
  invitation_accepted_at TIMESTAMP,
  last_login_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  created_by UUID,  -- User who created this user
  updated_at TIMESTAMP,
  updated_by UUID,
  
  UNIQUE(tenant_id, email),
  UNIQUE(tenant_id, phone),
  FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
  FOREIGN KEY (created_by) REFERENCES users(user_id),
  FOREIGN KEY (updated_by) REFERENCES users(user_id)
);

-- User permissions junction table
CREATE TABLE user_permissions (
  permission_id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  permission_name VARCHAR(100) NOT NULL,  -- create_deal, view_deals, etc.
  granted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  UNIQUE(user_id, permission_name),
  FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE
);

-- Audit log for user management actions
CREATE TABLE user_management_audit (
  audit_id UUID PRIMARY KEY,
  tenant_id UUID NOT NULL,
  actor_user_id UUID,  -- Who performed the action
  target_user_id UUID, -- Who the action was about
  action VARCHAR(50),  -- CREATE, UPDATE, DELETE, ACTIVATE, DEACTIVATE
  changes JSONB,  -- What changed
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
  FOREIGN KEY (actor_user_id) REFERENCES users(user_id),
  FOREIGN KEY (target_user_id) REFERENCES users(user_id)
);

-- Activity log for user actions
CREATE TABLE user_activity_log (
  activity_id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  tenant_id UUID NOT NULL,
  action VARCHAR(100),  -- login, deal_created, payment_recorded, etc.
  resource_type VARCHAR(50),  -- DEAL, PAYMENT, REPORT, etc.
  resource_id UUID,
  ip_address VARCHAR(15),
  user_agent TEXT,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  
  FOREIGN KEY (user_id) REFERENCES users(user_id),
  FOREIGN KEY (tenant_id) REFERENCES tenants(tenant_id),
  INDEX(user_id, created_at),
  INDEX(tenant_id, created_at)
);
```

---

## 🔄 Service Layer (Backend Logic)

```python
### File: src/services/user/user_management_service.py

class UserManagementService:
    """
    Handles user creation, updates, and management from dashboard
    Max 30 lines per method
    """
    
    async def create_user(
        self,
        tenant_id: UUID,
        current_user: User,
        user_data: CreateUserRequest
    ) -> User:
        """
        Create new user with role validation
        - Validate creator has permission
        - Validate role compatibility
        - Generate invitation token
        - Send welcome email
        """
        
    async def update_user(
        self,
        user_id: UUID,
        tenant_id: UUID,
        update_data: UpdateUserRequest
    ) -> User:
        """Update user details"""
        
    async def delete_user(
        self,
        user_id: UUID,
        tenant_id: UUID,
        action: str  # "archive" or "delete"
    ) -> None:
        """Archive or permanently delete user"""
        
    async def list_users(
        self,
        tenant_id: UUID,
        filters: Dict,
        pagination: Pagination
    ) -> List[User]:
        """List users with filters and pagination"""
        
    async def get_user_activity_log(
        self,
        user_id: UUID,
        limit: int = 20
    ) -> List[ActivityLog]:
        """Get user's activity history"""
        
    async def resend_invitation(self, user_id: UUID) -> None:
        """Resend welcome email"""
        
    async def reset_password(self, user_id: UUID) -> None:
        """Send password reset link"""
```

---

## ✅ Implementation Checklist

- [ ] Add user_permissions table
- [ ] Add user_management_audit table
- [ ] Add user_activity_log table
- [ ] Create UserManagementService
- [ ] Create user validators
- [ ] Create Dashboard API routes for user management
- [ ] Build Add User modal component
- [ ] Build Users list/table component
- [ ] Build Edit User modal
- [ ] Build Delete confirmation dialog
- [ ] Create invitation email templates
- [ ] Add permission checks to all endpoints
- [ ] Add audit logging
- [ ] Add activity tracking
- [ ] Write tests for user creation
- [ ] Write tests for permission validation
- [ ] Document all endpoints in Swagger

---

## 🚀 Integration with Your Excel Data

**Mapping to Your Excel Sheets:**

```
EXCEL SHEET                 →    CRM SYSTEM
─────────────────────────────────────────────-
SETTINGS (Projects)         →    System Config + Projects DB
DATA ENTRY (Clients/Deals)  →    Client + Deal entities
INSTALMENTS (Payments)      →    Payments + Ledger
PAYMENT SCHEDULE (Plans)    →    Payment Plans auto-generated
DASHBOARD (Metrics)         →    Dashboard analytics

NEW: User Management         →    Dashboard → Team Members
                                 (Tenant Manager can add users here)
```

---

## 📊 Example Workflow

**Scenario**: Tenant Owner adds a new Salesman

1. **Step 1**: Tenant logs into Dashboard → Settings → Team Members
2. **Step 2**: Clicks "+ Add Team Member" button
3. **Step 3**: Fills form:
   - Name: "Ahmed Ali"
   - Email: "ahmed@besttime.pk"
   - Phone: "+92-300-1234567"
   - Role: "Salesman"
   - Permissions: [create_deal, view_deals, record_payment]
4. **Step 4**: Checks "Send welcome email"
5. **Step 5**: Clicks "Add User"
6. **Backend Processing**:
   - ✅ Validate tenant owner has permission
   - ✅ Validate email is unique
   - ✅ Hash password
   - ✅ Create user record
   - ✅ Create permission records
   - ✅ Generate invitation token
   - ✅ Send welcome email
   - ✅ Log audit event
7. **Result**: 
   - User appears in team members list
   - Welcome email sent to Ahmed
   - Ahmed sets password and logs in
   - Ahmed can now create deals, record payments, etc.

---

## 📝 Notes

- All validation happens both frontend AND backend
- Permissions are checked on every API call
- Email invitations expire after 7 days
- Archived users don't appear in normal lists but data is retained
- All user management actions are audited
- Users can reset their own passwords from login page
- Tenant managers cannot exceed their subscription user limit
