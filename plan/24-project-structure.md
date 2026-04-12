# 📁 Project Directory Structure

## 📋 Overview
Complete directory structure for the FastAPI project.

---

## 🏗️ Full Project Structure

```
realestate-crm/
├── .github/
│   ├── workflows/
│   │   ├── ci.yml                 # CI pipeline
│   │   └── deploy.yml             # Deployment pipeline
│   └── ISSUE_TEMPLATE/
│
├── src/
│   ├── __init__.py
│   ├── main.py                    # App entry point
│   ├── server.py                  # Server startup
│   │
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py            # Main configuration
│   │   ├── database.py            # Database config
│   │   ├── security.py            # Security config
│   │   ├── notifications.py       # Notification config
│   │   ├── storage.py             # Storage config
│   │   └── features.py            # Feature flags
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   ├── router.py              # Main router
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── tenants/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── users/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── clients/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── projects/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── deals/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── payments/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── receipts/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── notifications/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   ├── dashboard/
│   │   │   ├── __init__.py
│   │   │   ├── routes.py
│   │   │   ├── controller.py
│   │   │   └── schemas.py
│   │   │
│   │   └── admin/
│   │       ├── __init__.py
│   │       ├── routes.py
│   │       ├── controller.py
│   │       └── schemas.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base.py                # Base model
│   │   ├── user.py
│   │   ├── tenant.py
│   │   ├── client.py
│   │   ├── project.py
│   │   ├── plot.py
│   │   ├── deal.py
│   │   ├── payment.py
│   │   ├── receipt.py
│   │   ├── notification.py
│   │   ├── audit_log.py
│   │   └── job_log.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth/
│   │   ├── client/
│   │   ├── deal/
│   │   ├── payment/
│   │   └── ...
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── auth_service.py
│   │   │   ├── signup_service.py
│   │   │   └── password_service.py
│   │   │
│   │   ├── tenant/
│   │   │   ├── __init__.py
│   │   │   └── tenant_service.py
│   │   │
│   │   ├── user/
│   │   │   ├── __init__.py
│   │   │   └── user_service.py
│   │   │
│   │   ├── client/
│   │   │   ├── __init__.py
│   │   │   └── client_service.py
│   │   │
│   │   ├── deal/
│   │   │   ├── __init__.py
│   │   │   ├── deal_service.py
│   │   │   └── payment_plan_service.py
│   │   │
│   │   ├── payment/
│   │   │   ├── __init__.py
│   │   │   ├── payment_service.py
│   │   │   ├── ledger_service.py
│   │   │   └── balance_service.py
│   │   │
│   │   ├── receipt/
│   │   │   ├── __init__.py
│   │   │   ├── receipt_service.py
│   │   │   ├── pdf_service.py
│   │   │   └── template_service.py
│   │   │
│   │   ├── notification/
│   │   │   ├── __init__.py
│   │   │   ├── notification_service.py
│   │   │   ├── whatsapp_service.py
│   │   │   └── email_service.py
│   │   │
│   │   ├── analytics/
│   │   │   ├── __init__.py
│   │   │   ├── analytics_service.py
│   │   │   └── kpi_service.py
│   │   │
│   │   └── backup/
│   │       ├── __init__.py
│   │       └── backup_service.py
│   │
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base_repository.py
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── user_repository.py
│   │   │   └── token_repository.py
│   │   │
│   │   ├── tenant/
│   │   │   ├── __init__.py
│   │   │   └── tenant_repository.py
│   │   │
│   │   ├── client/
│   │   │   ├── __init__.py
│   │   │   └── client_repository.py
│   │   │
│   │   ├── deal/
│   │   │   ├── __init__.py
│   │   │   └── deal_repository.py
│   │   │
│   │   ├── payment/
│   │   │   ├── __init__.py
│   │   │   └── payment_repository.py
│   │   │
│   │   ├── project/
│   │   │   ├── __init__.py
│   │   │   └── project_repository.py
│   │   │
│   │   └── notification/
│   │       ├── __init__.py
│   │       └── notification_repository.py
│   │
│   ├── validators/
│   │   ├── __init__.py
│   │   │
│   │   ├── auth/
│   │   │   ├── __init__.py
│   │   │   ├── signup_validator.py
│   │   │   └── login_validator.py
│   │   │
│   │   ├── client/
│   │   │   ├── __init__.py
│   │   │   └── client_validator.py
│   │   │
│   │   ├── deal/
│   │   │   ├── __init__.py
│   │   │   └── deal_validator.py
│   │   │
│   │   ├── payment/
│   │   │   ├── __init__.py
│   │   │   └── payment_validator.py
│   │   │
│   │   └── business_rules_validator.py
│   │
│   ├── middlewares/
│   │   ├── __init__.py
│   │   ├── auth_middleware.py
│   │   ├── rbac_middleware.py
│   │   ├── tenant_middleware.py
│   │   ├── error_handler_middleware.py
│   │   ├── request_logging_middleware.py
│   │   ├── rate_limit_middleware.py
│   │   └── cors_middleware.py
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── response.py            # Standard response
│   │   ├── logger.py              # Logging setup
│   │   ├── jwt.py                 # JWT utilities
│   │   ├── hash.py                # Hashing utilities
│   │   ├── encryption.py          # Encryption utilities
│   │   ├── validators_helpers.py  # Validation helpers
│   │   ├── date_utils.py          # Date utilities
│   │   ├── phone_formatter.py     # Phone formatting
│   │   ├── cnic_formatter.py      # CNIC formatting
│   │   └── id_generator.py        # ID generation
│   │
│   ├── jobs/
│   │   ├── __init__.py
│   │   ├── scheduler.py           # Job scheduler init
│   │   ├── payment_reminder_job.py
│   │   ├── late_payment_detection_job.py
│   │   ├── deal_completion_job.py
│   │   ├── daily_report_job.py
│   │   └── backup_job.py
│   │
│   ├── integrations/
│   │   ├── __init__.py
│   │   │
│   │   ├── whatsapp/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   └── templates.py
│   │   │
│   │   ├── email/
│   │   │   ├── __init__.py
│   │   │   ├── client.py
│   │   │   └── templates.py
│   │   │
│   │   ├── storage/
│   │   │   ├── __init__.py
│   │   │   ├── cloudinary_client.py
│   │   │   └── s3_client.py
│   │   │
│   │   └── sentry/
│   │       ├── __init__.py
│   │       └── client.py
│   │
│   ├── docs/
│   │   ├── __init__.py
│   │   ├── auth/
│   │   │   ├── signup.yaml
│   │   │   └── login.yaml
│   │   │
│   │   ├── clients/
│   │   ├── deals/
│   │   ├── payments/
│   │   └── ...
│   │
│   └── database/
│       ├── __init__.py
│       ├── session.py             # DB session
│       └── migrations/
│           ├── env.py
│           └── versions/
│               ├── 001_initial.py
│               └── ...
│
├── tests/
│   ├── __init__.py
│   │
│   ├── unit/
│   │   ├── __init__.py
│   │   ├── services/
│   │   ├── repositories/
│   │   ├── validators/
│   │   └── utils/
│   │
│   ├── integration/
│   │   ├── __init__.py
│   │   ├── auth/
│   │   ├── clients/
│   │   ├── deals/
│   │   └── ...
│   │
│   ├── e2e/
│   │   ├── __init__.py
│   │   ├── test_complete_flow.py
│   │   └── ...
│   │
│   ├── fixtures/
│   │   ├── __init__.py
│   │   ├── database.py
│   │   ├── auth.py
│   │   └── factories.py
│   │
│   └── conftest.py
│
├── docker/
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── .dockerignore
│
├── kubernetes/
│   ├── deployment.yaml
│   ├── service.yaml
│   ├── ingress.yaml
│   └── config.yaml
│
├── scripts/
│   ├── init_db.sh
│   ├── backup_db.sh
│   ├── migrate_db.sh
│   └── setup_env.sh
│
├── plan/
│   ├── 00-system-overview.md
│   ├── 01-auth-system.md
│   ├── ... (all planning documents)
│   └── INDEX.md
│
├── docs/
│   ├── API_DOCUMENTATION.md
│   ├── SETUP_GUIDE.md
│   ├── DEPLOYMENT_GUIDE.md
│   ├── DEVELOPER_GUIDE.md
│   └── ARCHITECTURE.md
│
├── logs/
│   └── app.log
│
├── .env.example
├── .env.development
├── .env.staging
├── .env.production
├── .gitignore
├── .dockerignore
├── dockerfile
├── docker-compose.yml
├── requirements.txt
├── requirements-dev.txt
├── pytest.ini
├── mypy.ini
├── .flake8
├── .pylintrc
├── README.md
├── LICENSE
├── CONTRIBUTING.md
└── Makefile                       # Development commands
```

---

## 📝 Key Files Explanation

| File | Purpose |
|------|---------|
| `main.py` | FastAPI app initialization |
| `server.py` | Server startup & configuration |
| `config/settings.py` | Environment configuration |
| `api/router.py` | Main API router |
| `models/` | SQLAlchemy models |
| `schemas/` | Pydantic request/response models |
| `services/` | Business logic |
| `repositories/` | Database operations |
| `validators/` | Input validation |
| `middlewares/` | Request/response processing |
| `jobs/` | Background jobs |
| `integrations/` | External service clients |
| `tests/` | Test suite |
| `docs/` | API documentation |

---

## ✅ Structure Checklist

- [ ] Directory structure created
- [ ] __init__.py files added to all packages
- [ ] Config files in place
- [ ] API routes organized
- [ ] Services/Repositories created
- [ ] Validators configured
- [ ] Middlewares implemented
- [ ] Tests directory structured
- [ ] Jobs scheduler setup
- [ ] Integrations clients created
- [ ] Documentation started
- [ ] Docker files created
- [ ] Kubernetes configs created
