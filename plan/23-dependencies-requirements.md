# 📦 Dependencies & Requirements

## 📋 Overview
Complete list of Python dependencies and their purposes.

---

## 🐍 Python Requirements

### requirements.txt
```
# Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
python-multipart==0.0.6

# Database
sqlalchemy==2.0.25
asyncpg==0.29.0
alembic==1.13.1

# ORM/Schema
pydantic==2.5.3
pydantic-settings==2.1.0

# Authentication & Security
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
bcrypt==4.1.2
cryptography==41.0.7
python-jwt==1.3.0

# Data Validation
email-validator==2.1.0
phonenumbers==8.13.0

# HTTP Client
httpx==0.27.0
requests==2.31.0

# External Services Integration
boto3==1.34.20  # AWS S3
cloudinary==1.36.0

# Background Jobs
apscheduler==3.10.4
celery==5.3.4  # Optional: for distributed tasks
redis==5.0.1

# PDF Generation
reportlab==4.0.9
weasyprint==59.3

# Email
python-dotenv==1.0.0
python-multipart==0.0.6

# Monitoring & Logging
sentry-sdk==1.39.2
python-json-logger==2.0.7

# Testing
pytest==7.4.4
pytest-asyncio==0.23.2
pytest-cov==4.1.0
httpx[cli]==0.27.0
faker==22.0.0

# Code Quality
black==23.12.1
flake8==6.1.0
isort==5.13.2
mypy==1.8.0
pylint==3.0.3

# Documentation
mkdocs==1.5.3
mkdocs-material==9.5.3

# Utilities
python-dateutil==2.8.2
pytz==2023.3.post1
pydantic-extra-types==2.1.0

# Performance
orjson==3.9.13
ujson==5.9.0

# Rate Limiting
slowapi==0.1.9

# CORS
fastapi-cors==0.0.8

# Debug & Development
ipython==8.20.0
python-decouple==3.8
```

---

## 📌 Dependency Details

### Core Framework
| Package | Version | Purpose |
|---------|---------|---------|
| `fastapi` | 0.109.0 | Web framework |
| `uvicorn` | 0.27.0 | ASGI server |
| `starlette` | 0.36.3 | Underlying framework |

### Database
| Package | Version | Purpose |
|---------|---------|---------|
| `sqlalchemy` | 2.0.25 | ORM |
| `asyncpg` | 0.29.0 | PostgreSQL async driver |
| `alembic` | 1.13.1 | Database migrations |

### Authentication
| Package | Version | Purpose |
|---------|---------|---------|
| `python-jose` | 3.3.0 | JWT handling |
| `passlib` | 1.7.4 | Password hashing |
| `bcrypt` | 4.1.2 | Bcrypt implementation |

### Data Validation
| Package | Version | Purpose |
|---------|---------|---------|
| `pydantic` | 2.5.3 | Data validation |
| `email-validator` | 2.1.0 | Email validation |
| `phonenumbers` | 8.13.0 | Phone validation |

### External Services
| Package | Version | Purpose |
|---------|---------|---------|
| `cloudinary` | 1.36.0 | File storage |
| `boto3` | 1.34.20 | AWS S3 |
| `requests` | 2.31.0 | HTTP requests |
| `httpx` | 0.27.0 | Async HTTP |

### Background Jobs
| Package | Version | Purpose |
|---------|---------|---------|
| `apscheduler` | 3.10.4 | Job scheduling |
| `celery` | 5.3.4 | Distributed tasks (optional) |
| `redis` | 5.0.1 | Cache & message broker |

### Document Generation
| Package | Version | Purpose |
|---------|---------|---------|
| `reportlab` | 4.0.9 | PDF generation |
| `weasyprint` | 59.3 | HTML to PDF |

### Monitoring
| Package | Version | Purpose |
|---------|---------|---------|
| `sentry-sdk` | 1.39.2 | Error tracking |
| `prometheus-client` | Latest | Metrics |

### Testing
| Package | Version | Purpose |
|---------|---------|---------|
| `pytest` | 7.4.4 | Testing framework |
| `pytest-asyncio` | 0.23.2 | Async test support |
| `pytest-cov` | 4.1.0 | Coverage analysis |
| `faker` | 22.0.0 | Fake data generation |

### Code Quality
| Package | Version | Purpose |
|---------|---------|---------|
| `black` | 23.12.1 | Code formatter |
| `flake8` | 6.1.0 | Linter |
| `isort` | 5.13.2 | Import sorter |
| `mypy` | 1.8.0 | Type checker |

---

## 📝 setup.py (Alternative)

```python
from setuptools import setup, find_packages

setup(
    name=\"realestate-crm\",
    version=\"1.0.0\",
    description=\"Multi-Tenant Real Estate CRM SaaS\",
    author=\"Your Name\",
    author_email=\"your-email@example.com\",
    packages=find_packages(),
    python_requires=\">=3.11\",
    install_requires=[
        \"fastapi==0.109.0\",
        \"uvicorn[standard]==0.27.0\",
        \"sqlalchemy==2.0.25\",
        \"asyncpg==0.29.0\",
        # ... more dependencies
    ],
    extras_require={
        \"dev\": [
            \"pytest==7.4.4\",
            \"pytest-asyncio==0.23.2\",
            \"black==23.12.1\",
            \"flake8==6.1.0\",
        ],
        \"prod\": [
            \"sentry-sdk==1.39.2\",
            \"prometheus-client==0.19.0\",
        ],
    },
)
```

---

## 🔒 Security Dependencies Notes

```yaml
cryptography:
  version: \"41.0.7\"
  critical: true
  purpose: \"Encryption, JWT signing\"
  security_update: \"Always keep updated\"

passlib:
  version: \"1.7.4\"
  critical: true
  purpose: \"Password hashing\"
  security_update: \"Always keep updated\"

bcrypt:
  version: \"4.1.2\"
  critical: true
  purpose: \"Bcrypt implementation\"
  notes: \"Install from PyPI, don't compile from source\"
```

---

## 🚀 Installation

### Create Virtual Environment
```bash
python3.11 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

### Install Development Dependencies
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

### Update Dependencies
```bash
pip install --upgrade -r requirements.txt
```

---

## ✅ Dependency Checklist

- [ ] All core dependencies listed
- [ ] All optional dependencies documented
- [ ] Version pinning strategy defined
- [ ] Security vulnerabilities checked
- [ ] Licenses reviewed (compatibility)
- [ ] Size optimization considered
- [ ] Startup time impact assessed
- [ ] Testing dependencies added
- [ ] Development dependencies separated
- [ ] Installation tested
- [ ] Requirements documentation
- [ ] Upgrade path documented
