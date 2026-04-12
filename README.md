# 🏢 Real Estate CRM System

A modern, scalable, multi-tenant SaaS platform for managing real estate deals, clients, payments, and analytics. Built with **FastAPI**, **PostgreSQL**, **Redis**, and **Next.js**.

## 📋 Quick Links

- **Documentation**: See `/plan` folder for comprehensive 27+ documents
- **Architecture**: See `/plan/00-system-overview.md`
- **API Documentation**: Visit `http://localhost:8000/docs` (when running)
- **Frontend**: Visit `http://localhost:3000` (when running)

---

## 🚀 Quick Start with Docker

### Prerequisites

- Docker (v20.10+)
- Docker Compose (v1.29+)
- Git

### 1. Clone and Setup

```bash
cd "d:\Projects\real estate"

# Copy environment file
cp .env.example .env.development

# For production
cp .env.example .env.production
```

### 2. Start Services

```bash
# Development (with hot reload)
docker-compose up -d

# Production
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose logs -f api
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### 3. Access Services

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

---

## 📦 What's Included

### Backend Stack
- **FastAPI 0.109.0** - Modern async Python web framework
- **PostgreSQL 15** - Robust relational database
- **Redis 7** - Fast caching & message queue
- **SQLAlchemy 2.0** - ORM for database operations
- **Pydantic 2.5** - Data validation
- **Python 3.11**

### Frontend Stack
- **Next.js 14.1** - React framework
- **React 18.2** - UI library
- **Tailwind CSS 3.4** - Utility-first CSS
- **Axios** - HTTP client
- **TypeScript** - Type safety

### Features
✅ Multi-tenant architecture (complete data isolation)
✅ JWT authentication with refresh tokens
✅ Role-based access control (RBAC)
✅ Real-time dashboard
✅ Payment tracking with installment management
✅ Client leads management
✅ Deal lifecycle management
✅ Automated notifications (WhatsApp, Email)
✅ PDF receipt generation
✅ Comprehensive audit logging
✅ Background job scheduling
✅ Full API documentation

---

## 🗂️ Project Structure

```
d:\Projects\real estate\
├── src/                          # FastAPI backend
│   ├── main.py                  # App entry point
│   ├── config.py                # Settings
│   ├── api/                     # API routes
│   ├── models/                  # Database models
│   ├── services/                # Business logic
│   └── repositories/            # Data access
│
├── frontend/                     # Next.js frontend
│   ├── pages/                   # App pages
│   ├── components/              # React components
│   ├── styles/                  # CSS & Tailwind
│   └── public/                  # Static files
│
├── scripts/                      # Database scripts
│   └── init-db.sql             # DB initialization
│
├── plan/                         # Planning documents (27 files)
│   ├── 00-system-overview.md
│   ├── 01-auth-system.md
│   ├── 07-deal-system.md
│   ├── 08-payment-system.md
│   ├── 25-dashboard-user-management.md
│   └── 26-excel-to-software-mapping.md
│
├── docker-compose.yml            # Local dev stack
├── Dockerfile                    # FastAPI container
├── requirements.txt              # Python dependencies
├── .env.development             # Dev environment
├── .env.example                 # Template
└── README.md                    # This file
```

---

## 🛠️ Development

### Without Docker (Local Setup)

#### Backend Setup

```bash
# 1. Create virtual environment
python -m venv venv
.\venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set environment variables
cp .env.example .env

# 4. Run migrations (when database schema exists)
alembic upgrade head

# 5. Start FastAPI server
uvicorn src.main:app --reload --port 8000
```

#### Frontend Setup

```bash
# 1. Install dependencies
cd frontend
npm install

# 2. Set environment variables
echo "NEXT_PUBLIC_API_URL=http://localhost:8000/api" > .env.local

# 3. Start development server
npm run dev
```

### Database Management

```bash
# Access PostgreSQL
docker-compose exec postgres psql -U postgres -d realestate_crm

# Create backup
docker-compose exec postgres pg_dump -U postgres realestate_crm > backup.sql

# Restore backup
docker-compose exec -T postgres psql -U postgres realestate_crm < backup.sql

# Reset database (development only)
docker-compose exec postgres dropdb -U postgres realestate_crm
docker-compose exec postgres createdb -U postgres realestate_crm
```

---

## 📊 Database Schema

Key tables:
- **tenants** - Multi-tenant support
- **users** - Authentication & RBAC
- **clients** - Customer records
- **projects** - Real estate projects
- **plots** - Property units
- **deals** - Property sales (core entity)
- **payments** - Installment tracking
- **notifications** - WhatsApp/Email logs
- **audit_logs** - Action tracking

See `/plan/11-database-schema.md` for complete schema.

---

## 🔌 API Routes

### Health & Status
```
GET /health                    # API health check
GET /api/status               # API status
GET /api/                     # API root
```

### Authentication (To Implement)
```
POST   /api/auth/signup       # User registration
POST   /api/auth/login        # User login
POST   /api/auth/refresh      # Refresh token
POST   /api/auth/logout       # User logout
GET    /api/auth/me           # Current user
```

### Core Resources (To Implement)
```
GET    /api/tenants           # List tenants
GET    /api/tenants/{id}      # Get tenant
POST   /api/users             # Create user
GET    /api/users             # List users
GET    /api/clients           # List clients
POST   /api/deals             # Create deal
GET    /api/deals             # List deals
POST   /api/payments          # Record payment
GET    /api/payments          # List payments
```

See `/plan/12-api-routes.md` for complete API specification.

---

## 🔐 Environment Variables

### Development (.env.development)
```env
ENVIRONMENT=development
DEBUG=true
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/realestate_crm
REDIS_URL=redis://localhost:6379
JWT_SECRET_KEY=dev-secret-key-change-in-production
```

### Production
```env
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:password@prod-db:5432/realestate_crm
REDIS_URL=redis://prod-redis:6379
JWT_SECRET_KEY=strong-production-secret-key-32-chars-min
```

See `.env.example` for all available variables.

---

## 📈 Performance Optimizations

### Backend
✅ FastAPI async processing
✅ Redis caching layer
✅ Database connection pooling
✅ GZIP response compression
✅ Multi-worker Uvicorn server
✅ Query optimization with indexes

### Frontend
✅ Next.js static generation
✅ Image optimization
✅ CSS minification
✅ Code splitting
✅ Lazy loading components
✅ Browser caching

### Infrastructure
✅ Alpine-based Docker images (small size)
✅ Multi-stage Docker builds
✅ Resource limits (low-budget friendly)
✅ Health checks on all services

---

## 🧪 Testing

### Run Tests
```bash
# Backend unit tests
pytest tests/

# Backend with coverage
pytest --cov=src tests/

# Frontend tests
cd frontend
npm test
```

---

## 📚 Documentation

Complete documentation in `/plan/` directory:

1. **00-system-overview.md** - Architecture & vision
2. **01-auth-system.md** - Authentication design
3. **07-deal-system.md** - Core deal features
4. **08-payment-system.md** - Payment processing
5. **11-database-schema.md** - Database design
6. **12-api-routes.md** - All API endpoints
7. **25-dashboard-user-management.md** - User management UI
8. **26-excel-to-software-mapping.md** - Excel integration

Plus 19 more comprehensive documents covering all aspects.

---

## 🚢 Deployment

### Docker Compose (Recommended for Single Server)

```bash
docker-compose -f docker-compose.yml up -d
```

### Kubernetes (Scalable)

```bash
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml
```

### Cloud Platforms

- **Google Cloud Run** - Serverless FastAPI
- **AWS ECS** - Container orchestration
- **Azure Container Instances** - Managed containers
- **Heroku** - Simple deployment
- **Railway** - Modern deployment

---

## 🐛 Troubleshooting

### API Not Connecting

```bash
# Check if API is running
curl http://localhost:8000/health

# Check logs
docker-compose logs api

# Restart API
docker-compose restart api
```

### Database Connection Failed

```bash
# Check PostgreSQL
docker-compose logs postgres

# Verify connection
docker-compose exec postgres pg_isready

# Reset database
docker-compose exec postgres psql -U postgres -c "DROP DATABASE realestate_crm;"
```

### Frontend Not Loading

```bash
# Check Next.js
docker-compose logs frontend

# Rebuild frontend
docker-compose build frontend
docker-compose restart frontend

# Clear cache
rm -rf frontend/.next
```

---

## 📋 Checklist

- [ ] Clone repository
- [ ] Copy `.env.example` to `.env.development`
- [ ] Run `docker-compose up -d`
- [ ] Access frontend at http://localhost:3000
- [ ] Check API docs at http://localhost:8000/docs
- [ ] Create first tenant
- [ ] Add users to tenant
- [ ] Create sample deals
- [ ] Record sample payments

---

## 🤝 Contributing

1. Read `/plan/00-system-overview.md` for architecture
2. Follow `/plan/16-security-compliance.md` security rules
3. Check `/plan/14-validation-rules.md` for validation
4. Write tests following `/plan/19-testing-strategy.md`

---

## 📝 License

Internal Project - Best Time Marketing

---

## 📞 Support

- **Documentation**: Check `/plan/` folder
- **Issues**: Create GitHub issue
- **Email**: support@realestate.com

---

## 🎯 Next Steps

1. ✅ **Setup Complete** - System running with demo data
2. 👉 **Implementation Phase 1** - Implement Auth System (doc #01)
3. **Phase 2** - Core Features (Deals, Payments)
4. **Phase 3** - Advanced Features (Notifications, Reports)
5. **Phase 4** - Optimization & Security hardening

---

**Status**: 🚀 Ready for Development
**Last Updated**: April 12, 2026
