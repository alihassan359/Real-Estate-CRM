🚨 COPILOT / AI CODING STRICT RULES (SAAS PROJECT)
🧠 1. CORE NON-NEGOTIABLE RULES
❌ NEVER DO
Never mix layers (Controller ≠ Service ≠ Repository)
Never write business logic in controllers
Never access DB directly from controllers or services
Never skip validation layer
Never hardcode configuration values
Never ignore tenant isolation (tenant_id)
Never bypass RBAC checks
Never create files >100 lines
Never create functions >20 lines
Never skip Swagger documentation
✅ ALWAYS DO
Follow MVC + Service + Repository strictly
Every API MUST have:
Controller
Service
Repository
Validator
Swagger Doc in /Docs
Always use tenant_id filtering
Always return standard response format
Always use try/catch in controllers
Always keep services business-only (NO req/res)
🏗️ 2. ARCHITECTURE RULES
Layer Responsibility
Layer	Rule
Routes	Only map endpoints
Controllers	Handle request/response only
Services	Business logic only
Repositories	DB operations only
Models	Schema only
Validators	Input validation only
🔐 3. MULTI-TENANT RULES (CRITICAL)
MUST FOLLOW:
Every DB query MUST include:
tenant_id = user.tenant_id
NEVER:
Access cross-tenant data
Forget tenant filtering
🔑 4. RBAC RULES
Before any sensitive action:

MUST check:

user role
permissions
NEVER:
Hardcode role checks in controllers
ALWAYS:

Use middleware:

authMiddleware
permissionMiddleware
📦 5. FILE SIZE RULES
Max file size: 100 lines
Max function size: 20 lines
If exceeded:
Split into helper/service/repo
📄 6. API RESPONSE FORMAT (MANDATORY)

All APIs MUST return:

{
  "success": true,
  "message": "",
  "data": {}
}

Errors:

{
  "success": false,
  "message": "",
  "error": {}
}
📚 7. SWAGGER RULES (MANDATORY)

Every endpoint MUST have:

summary
description
request body
params
responses (200/400/401/500)
security schema

📁 Location:

/Docs/{module}/{endpoint}.js
🧾 8. NAMING RULES
Files:
lowercase
descriptive
domain-based

Example:

createDealService.js
getClientController.js
paymentRepository.js
⚙️ 9. CONFIG RULES

All configs MUST be in:

/src/config/

Never hardcode:

DB URL
API keys
Secrets

Use .env only.

🔥 10. BUSINESS LOGIC RULES
Services:
ONLY business logic
NO HTTP response
NO DB schema definitions
Controllers:
ONLY:
req handling
service call
response
💰 11. PAYMENT SYSTEM RULES
Always calculate:
remaining balance
paid amount
overdue status
Never trust frontend calculations
📲 12. NOTIFICATION RULES

When triggering:

WhatsApp
Email
SMS (future)

ALWAYS:

Use service layer
Never send directly from controller
🔐 13. SECURITY RULES
Hash passwords
Never expose CNIC fully in logs
Sanitize inputs
Rate limit auth routes
Use JWT authentication
🧾 14. AUDIT RULES

Log:

deal creation
payment updates
user changes
🚫 15. FORBIDDEN PATTERNS
No inline SQL
No logic in routes
No large files
No global variables for state
No skipping validation
📁 PROJECT FOLDER STRUCTURE (SAAS READY)
src/
│
├── config/
│   ├── db.js
│   ├── env.js
│   ├── appConfig.js
│   ├── notificationConfig.js
│
├── routes/
│   ├── auth/
│   ├── tenant/
│   ├── project/
│   ├── client/
│   ├── deal/
│   ├── payment/
│
├── controllers/
│   ├── auth/
│   ├── tenant/
│   ├── project/
│   ├── client/
│   ├── deal/
│   ├── payment/
│
├── services/
│   ├── auth/
│   ├── tenant/
│   ├── project/
│   ├── client/
│   ├── deal/
│   ├── payment/
│   ├── notification/
│   ├── receipt/
│
├── repositories/
│   ├── auth/
│   ├── tenant/
│   ├── project/
│   ├── client/
│   ├── deal/
│   ├── payment/
│
├── models/
│   ├── user.model.js
│   ├── tenant.model.js
│   ├── project.model.js
│   ├── client.model.js
│   ├── deal.model.js
│   ├── payment.model.js
│   ├── receipt.model.js
│
├── validators/
│   ├── auth/
│   ├── tenant/
│   ├── project/
│   ├── client/
│   ├── deal/
│   ├── payment/
│
├── middlewares/
│   ├── authMiddleware.js
│   ├── rbacMiddleware.js
│   ├── tenantMiddleware.js
│   ├── errorHandler.js
│
├── utils/
│   ├── response.js
│   ├── logger.js
│   ├── jwt.js
│   ├── hash.js
│   ├── uniqueId.js
│
├── Docs/
│   ├── auth/
│   ├── tenant/
│   ├── project/
│   ├── client/
│   ├── deal/
│   ├── payment/
│
├── jobs/
│   ├── paymentReminder.job.js
│   ├── overdueChecker.job.js
│
├── integrations/
│   ├── whatsapp/
│   ├── email/
│   ├── sms/
│
├── app.js
├── server.js
🧠 FINAL COPILOT BEHAVIOR RULE

When Copilot generates code:

👉 It MUST behave like:

“Senior backend engineer working on enterprise SaaS with strict architecture constraints”

🚀 RESULT OF FOLLOWING THIS

If you follow these rules:

No messy code
No rework later
Easy scaling to SaaS
Easy team onboarding
Production-ready system from Day 1