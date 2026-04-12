# 🔀 API Structure & Routes

## 📋 Overview
RESTful API routes structure for the entire SaaS platform organized by module.

---

## 🌍 API Base URL
```
Development:  http://localhost:8000/api
Production:   https://api.realestatecr.com/api
Version:      v1 (future: /api/v2)
```

---

## 🛣️ Authentication Routes

```
POST   /api/auth/signup              Create new account
POST   /api/auth/login               User login
POST   /api/auth/logout              User logout
POST   /api/auth/refresh             Refresh token
GET    /api/auth/me                  Get current user
POST   /api/auth/forgot-password     Forgot password
POST   /api/auth/reset-password      Reset password
POST   /api/auth/change-password     Change password (authenticated)
```

---

## 🛣️ Tenant Routes

```
POST   /api/tenants                  Create tenant (ADMIN)
GET    /api/tenants/{tenant_id}      Get tenant details
PATCH  /api/tenants/{tenant_id}      Update tenant
PATCH  /api/tenants/{tenant_id}/settings  Update settings
GET    /api/tenants/{tenant_id}/usage     Get usage stats

ADMIN ONLY:
GET    /api/admin/tenants            List all tenants
POST   /api/admin/tenants/{id}/suspend    Suspend tenant
POST   /api/admin/tenants/{id}/reactivate Reactivate
```

---

## 🛣️ User Routes

```
POST   /api/users                    Create user (OWNER/MANAGER)
GET    /api/users                    List users (paginated)
GET    /api/users/{user_id}          Get user details
PATCH  /api/users/{user_id}          Update user
PATCH  /api/users/{user_id}/role     Change user role
DELETE /api/users/{user_id}          Soft delete user
PATCH  /api/users/{user_id}/disable  Disable user
POST   /api/users/{user_id}/enable   Enable user
POST   /api/users/invite             Resend invitation
```

---

## 🛣️ Client Routes

```
POST   /api/clients                  Create client
GET    /api/clients                  List clients (with search/filter)
GET    /api/clients/{client_id}      Get client details
PATCH  /api/clients/{client_id}      Update client
DELETE /api/clients/{client_id}      Soft delete client
POST   /api/clients/{client_id}/verify-kyc   Verify KYC
POST   /api/clients/{client_id}/blacklist    Blacklist client
GET    /api/clients/{client_id}/ledger       Get client ledger
POST   /api/clients/import           Bulk import (CSV)
GET    /api/clients/export           Export client list
```

---

## 🛣️ Project Routes

```
POST   /api/projects                 Create project
GET    /api/projects                 List projects
GET    /api/projects/{project_id}    Get project details
PATCH  /api/projects/{project_id}    Update project
DELETE /api/projects/{project_id}    Soft delete
GET    /api/projects/{project_id}/statistics  Get stats

PLOTS:
POST   /api/projects/{project_id}/plots          Create plot
GET    /api/projects/{project_id}/plots          List plots (with filters)
GET    /api/projects/{project_id}/plots/{plot_id}  Get plot details
PATCH  /api/projects/{project_id}/plots/{plot_id}  Update plot
POST   /api/projects/{project_id}/plots/{plot_id}/reserve  Reserve plot
POST   /api/projects/{project_id}/plots/{plot_id}/release  Release plot
```

---

## 🛣️ Deal Routes

```
POST   /api/deals                    Create deal
GET    /api/deals                    List deals (with comprehensive filters)
GET    /api/deals/{deal_id}          Get deal details
PATCH  /api/deals/{deal_id}          Update deal
POST   /api/deals/{deal_id}/complete Complete deal
POST   /api/deals/{deal_id}/default  Mark as defaulted
POST   /api/deals/{deal_id}/cancel   Cancel deal

DEAL DETAILS:
GET    /api/deals/{deal_id}/payments      Get payment history
GET    /api/deals/{deal_id}/payment-plan  Get payment plan
GET    /api/deals/{deal_id}/balance       Get current balance
GET    /api/deals/{deal_id}/timeline      Get deal timeline
```

---

## 🛣️ Payment Routes

```
POST   /api/deals/{deal_id}/payments           Record payment
GET    /api/deals/{deal_id}/payments           List payments for deal
GET    /api/payments                           List all payments (filtered)
GET    /api/payments/{payment_id}              Get payment details
PATCH  /api/payments/{payment_id}/status       Update payment status
DELETE /api/payments/{payment_id}              Cancel payment

BULK:
POST   /api/payments/bulk-import               Bulk import (CSV)
GET    /api/payments/export                    Export payments

LEDGER:
GET    /api/clients/{client_id}/ledger          Client ledger
GET    /api/payments/ledger/company             Company ledger
GET    /api/payments/ledger/commission          Commission ledger
```

---

## 🛣️ Receipt Routes

```
POST   /api/receipts/generate                  Generate receipt
GET    /api/receipts                           List receipts
GET    /api/receipts/{receipt_id}              Get receipt details
GET    /api/receipts/{receipt_id}/download     Download PDF
POST   /api/receipts/{receipt_id}/resend       Resend to client
DELETE /api/receipts/{receipt_id}              Delete receipt

TEMPLATES:
POST   /api/admin/receipt-templates            Create template
GET    /api/admin/receipt-templates            List templates
PATCH  /api/admin/receipt-templates/{id}       Update template
```

---

## 🛣️ Notification Routes

```
POST   /api/notifications/send                 Send manual notification
GET    /api/notifications                      List notifications
GET    /api/notifications/{notification_id}   Get notification details
PATCH  /api/notifications/{notification_id}/status  Update status

TEMPLATES:
POST   /api/admin/notification-templates       Create template
GET    /api/admin/notification-templates       List templates
PATCH  /api/admin/notification-templates/{id}  Update template
```

---

## 🛣️ Dashboard Routes

```
GET    /api/dashboard/overview                 Dashboard summary
GET    /api/dashboard/deals                    Deals statistics
GET    /api/dashboard/payments                 Payment statistics
GET    /api/dashboard/clients                  Client statistics
GET    /api/dashboard/revenue                  Revenue analytics
GET    /api/dashboard/performance              Performance metrics
```

---

## 🛣️ Report Routes

```
GET    /api/reports/deals                      Deal report
GET    /api/reports/payments                   Payment report
GET    /api/reports/commissions                Commission report
GET    /api/reports/revenue                    Revenue report
GET    /api/reports/export/{type}              Export report (CSV/PDF)
```

---

## 🛣️ Settings Routes

```
GET    /api/settings                           Get all settings
PATCH  /api/settings/{setting_key}             Update setting
GET    /api/settings/company                   Get company settings
PATCH  /api/settings/company                   Update company settings
GET    /api/settings/features                  Get feature flags
PATCH  /api/settings/features                  Update feature flags
```

---

## 🛣️ Admin Routes

```
GET    /api/admin/audit-logs                   View audit logs
GET    /api/admin/system-health                System health
POST   /api/admin/backup                       Manual backup
GET    /api/admin/jobs                         View background jobs
POST   /api/admin/jobs/{job_id}/run            Trigger job manually
GET    /api/admin/api-logs                     API request logs
```

---

## 📊 Route Grouping Structure

```python
# FastAPI route organization

app.include_router(auth_routes, prefix="/api/auth", tags=["Authentication"])
app.include_router(tenant_routes, prefix="/api/tenants", tags=["Tenants"])
app.include_router(user_routes, prefix="/api/users", tags=["Users"])
app.include_router(client_routes, prefix="/api/clients", tags=["Clients"])
app.include_router(project_routes, prefix="/api/projects", tags=["Projects"])
app.include_router(deal_routes, prefix="/api/deals", tags=["Deals"])
app.include_router(payment_routes, prefix="/api/payments", tags=["Payments"])
app.include_router(receipt_routes, prefix="/api/receipts", tags=["Receipts"])
app.include_router(notification_routes, prefix="/api/notifications", tags=["Notifications"])
app.include_router(dashboard_routes, prefix="/api/dashboard", tags=["Dashboard"])
app.include_router(report_routes, prefix="/api/reports", tags=["Reports"])
app.include_router(settings_routes, prefix="/api/settings", tags=["Settings"])
app.include_router(admin_routes, prefix="/api/admin", tags=["Admin"])
```

---

## ✅ API Routes Checklist

- [ ] All endpoints defined
- [ ] Route parameters specified
- [ ] Query parameters documented
- [ ] Request body schemas defined
- [ ] Response schemas defined
- [ ] Error responses documented
- [ ] Authorization required specified
- [ ] Rate limiting rules
- [ ] Pagination implemented
- [ ] Sorting options
- [ ] Filtering options
- [ ] Swagger documentation
- [ ] Mock API responses
