# 🧪 Testing Strategy

## 📋 Overview
Comprehensive testing approach including unit, integration, and end-to-end tests.

---

## 🎯 Testing Pyramid

```
        🔺
       E2E Tests (5%)
       /   \\
      Integration Tests (20%)
     /       \\
    Unit Tests (75%)
   /__________\\
```

---

## 🧪 Unit Tests

### Test Structure
```python
# tests/unit/services/test_deal_service.py

import pytest
from unittest.mock import Mock, AsyncMock, patch
from services.deal.deal_service import DealService

@pytest.fixture
def mock_client_repo():
    return AsyncMock()

@pytest.fixture
def mock_plot_repo():
    return AsyncMock()

@pytest.fixture
def deal_service(mock_client_repo, mock_plot_repo):
    return DealService(
        client_repo=mock_client_repo,
        plot_repo=mock_plot_repo
    )

class TestCreateDeal:
    @pytest.mark.asyncio
    async def test_create_deal_success(self, deal_service, mock_client_repo, mock_plot_repo):
        # Arrange
        tenant_id = 'tenant-uuid'
        deal_data = {
            'client_id': 'client-uuid',
            'plot_id': 'plot-uuid',
            'total_amount': 2500000,
            'advance_payment': 250000
        }
        
        mock_client_repo.get.return_value = Mock(id='client-uuid')
        mock_plot_repo.get.return_value = Mock(id='plot-uuid', status='AVAILABLE')
        
        # Act
        result = await deal_service.create_deal(tenant_id, deal_data)
        
        # Assert
        assert result.deal_id is not None
        assert result.status == 'CREATED'
        assert result.total_amount == 2500000
        mock_client_repo.get.assert_called_once()
        mock_plot_repo.get.assert_called_once()
    
    @pytest.mark.asyncio
    async def test_create_deal_plot_not_available(self, deal_service, mock_plot_repo):
        # Arrange
        deal_data = {'plot_id': 'plot-uuid'}
        mock_plot_repo.get.return_value = Mock(status='SOLD')
        
        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            await deal_service.create_deal('tenant-uuid', deal_data)
        
        assert 'Plot not available' in str(exc_info.value)
```

### Coverage Target
- Service layer: **90%+**
- Repository layer: **85%+**
- Controller layer: **80%+**
- Overall: **80%+**

---

## 🔗 Integration Tests

### API Integration Tests
```python
# tests/integration/test_deal_api.py

import pytest
from httpx import AsyncClient
from app import app

@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url='http://test') as client:
        yield client

@pytest.fixture
async def auth_token(client):
    # Create test user & get token
    response = await client.post(
        '/api/auth/signup',
        json={
            'email': 'test@example.com',
            'password': 'TestPass123!',
            'company_name': 'Test Company'
        }
    )
    return response.json()['data']['tokens']['access_token']

class TestDealAPI:
    @pytest.mark.asyncio
    async def test_create_deal_endpoint(self, client, auth_token):
        # Arrange
        headers = {'Authorization': f'Bearer {auth_token}'}
        deal_data = {
            'client_id': 'client-uuid',
            'plot_id': 'plot-uuid',
            'total_amount': 2500000,
            'advance_payment': 250000
        }
        
        # Act
        response = await client.post(
            '/api/deals',
            json=deal_data,
            headers=headers
        )
        
        # Assert
        assert response.status_code == 201
        assert response.json()['success'] is True
        assert response.json()['data']['deal_id'] is not None
    
    @pytest.mark.asyncio
    async def test_create_deal_unauthorized(self, client):
        # Act
        response = await client.post(
            '/api/deals',
            json={}
        )
        
        # Assert
        assert response.status_code == 401
```

---

## 🔚 End-to-End Tests

### Complete Flow Test
```python
# tests/e2e/test_complete_deal_flow.py

@pytest.mark.asyncio
async def test_complete_deal_flow(client):
    \"\"\"Test complete flow: signup → create deal → record payment → generate receipt\"\"\"
    
    # 1. Signup
    signup_resp = await client.post('/api/auth/signup', json={
        'email': 'user@example.com',
        'password': 'TestPass123!',
        'company_name': 'Test Co'
    })
    assert signup_resp.status_code == 201
    token = signup_resp.json()['data']['tokens']['access_token']
    
    # 2. Create client
    client_resp = await client.post('/api/clients', json={
        'full_name': 'Ali Khan',
        'email': 'ali@example.com',
        'phone': '+92-300-1234567',
        'cnic': '12345-6789012-3'
    }, headers={'Authorization': f'Bearer {token}'})
    assert client_resp.status_code == 201
    client_id = client_resp.json()['data']['id']
    
    # 3. Create deal
    deal_resp = await client.post('/api/deals', json={
        'client_id': client_id,
        'plot_id': 'plot-uuid',
        'total_amount': 2500000,
        'advance_payment': 250000
    }, headers={'Authorization': f'Bearer {token}'})
    assert deal_resp.status_code == 201
    deal_id = deal_resp.json()['data']['deal_id']
    
    # 4. Record payment
    payment_resp = await client.post(
        f'/api/deals/{deal_id}/payments',
        json={
            'amount': 250000,
            'payment_type': 'ADVANCE',
            'payment_date': '2026-04-11',
            'method': 'BANK_TRANSFER'
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert payment_resp.status_code == 201
    
    # 5. Generate receipt
    receipt_resp = await client.post(
        '/api/receipts/generate',
        json={
            'receipt_type': 'PAYMENT_RECEIPT',
            'deal_id': deal_id
        },
        headers={'Authorization': f'Bearer {token}'}
    )
    assert receipt_resp.status_code == 201
    assert receipt_resp.json()['data']['pdf_url'] is not None
```

---

## 📊 Test Coverage Report

```
Name                           Stmts   Miss  Cover
---------------------------------------------------
services/auth/                   150     10   93%
services/deal/                   200     20   90%
services/payment/                180     15   92%
services/client/                 120     10   92%
controllers/auth/                 80      5   94%
controllers/deal/                100     10   90%
models/                          200     15   92%
validators/                      150     12   92%
---------------------------------------------------
TOTAL                          1180    107   91%
```

---

## 🚀 Running Tests

### Run All Tests
```bash
pytest tests/ -v --cov=src --cov-report=html
```

### Run Unit Tests Only
```bash
pytest tests/unit/ -v
```

### Run Integration Tests Only
```bash
pytest tests/integration/ -v
```

### Run E2E Tests Only
```bash
pytest tests/e2e/ -v
```

### Run with Coverage
```bash
pytest tests/ --cov=src --cov-report=term-missing --cov-fail-under=80
```

---

## 🧰 Test Utilities

### Database Test Fixtures
```python
# tests/fixtures/database.py

@pytest.fixture
async def test_db():
    # Setup test database
    await create_test_db()
    yield
    # Teardown
    await drop_test_db()

@pytest.fixture
async def test_tenant(test_db):
    # Create test tenant
    tenant = await Tenant.create(
        tenant_code='TEST',
        company_name='Test Company',
        subscription_plan='PRO'
    )
    yield tenant
    await tenant.delete()
```

### Mock Data Factory
```python
# tests/factories/factory.py

class UserFactory:
    @staticmethod
    def create(tenant_id=None, **kwargs):
        return User(
            tenant_id=tenant_id or 'tenant-uuid',
            email=kwargs.get('email', 'test@example.com'),
            role=kwargs.get('role', 'OPERATOR'),
            **kwargs
        )

class DealFactory:
    @staticmethod
    def create(tenant_id=None, **kwargs):
        return Deal(
            tenant_id=tenant_id or 'tenant-uuid',
            client_id=kwargs.get('client_id', 'client-uuid'),
            plot_id=kwargs.get('plot_id', 'plot-uuid'),
            total_amount=kwargs.get('total_amount', Decimal('2500000')),
            **kwargs
        )
```

---

## ✅ Testing Checklist

- [ ] Unit tests for all services (90%+ coverage)
- [ ] Unit tests for validators (95%+ coverage)
- [ ] Integration tests for all APIs
- [ ] E2E tests for critical flows
- [ ] Authentication tests
- [ ] Authorization/RBAC tests
- [ ] Error handling tests
- [ ] Input validation tests
- [ ] Business logic tests
- [ ] Database transaction tests
- [ ] Concurrent operation tests
- [ ] Load testing setup
- [ ] Performance benchmarks
- [ ] Security tests
- [ ] Data integrity tests
- [ ] Test fixtures & factories
- [ ] Mock data generation
- [ ] Test database setup
- [ ] Test coverage reports
- [ ] CI/CD test pipeline
