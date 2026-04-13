# 🚀 Frontend Integration Guide - Authentication System

---

## 📱 Quick Start for Frontend

### 1. **Install Dependencies**
```bash
npm install axios
# or
yarn add axios
```

### 2. **Create Auth Service**

Create `services/authService.ts`:

```typescript
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

interface AuthResponse {
  success: boolean;
  message: string;
  is_new_user?: boolean;
  data?: {
    user: {
      id: string;
      email: string;
      first_name: string;
      last_name: string;
      avatar_url?: string;
      role: string;
      status: string;
    };
    tenant?: {
      id: string;
      tenant_code: string;
      company_name: string;
      subscription_plan: string;
    };
    tokens: {
      access_token: string;
      refresh_token: string;
      expires_in: number;
      token_type: string;
    };
  };
}

export const authService = {
  // Tenant Signup
  tenantSignup: async (payload: {
    email: string;
    password: string;
    confirm_password: string;
    first_name: string;
    last_name: string;
    company_name: string;
    company_phone?: string;
    company_city?: string;
    accept_terms: boolean;
  }): Promise<AuthResponse> => {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/tenant/signup`,
      payload
    );
    return response.data;
  },

  // Tenant Login
  tenantLogin: async (email: string, password: string): Promise<AuthResponse> => {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/tenant/login`,
      { email, password }
    );
    return response.data;
  },

  // Admin Signup
  adminSignup: async (payload: {
    email: string;
    password: string;
    confirm_password: string;
    first_name: string;
    last_name: string;
    phone?: string;
  }): Promise<AuthResponse> => {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/admin/signup`,
      payload
    );
    return response.data;
  },

  // Admin Login
  adminLogin: async (email: string, password: string): Promise<AuthResponse> => {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/admin/login`,
      { email, password }
    );
    return response.data;
  },

  // Get Google OAuth URL
  getGoogleAuthUrl: async (): Promise<{ auth_url: string; state: string }> => {
    const response = await axios.get(
      `${API_BASE_URL}/api/auth/google/auth-url`
    );
    return response.data;
  },

  // Google OAuth Login
  googleLogin: async (idToken: string): Promise<AuthResponse> => {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/google/login`,
      { id_token: idToken }
    );
    return response.data;
  },

  // Refresh Token
  refreshToken: async (refreshToken: string): Promise<{ access_token: string; expires_in: number }> => {
    const response = await axios.post(
      `${API_BASE_URL}/api/auth/refresh`,
      { refresh_token: refreshToken }
    );
    return response.data.data;
  },

  // Get Current User
  getCurrentUser: async (accessToken: string): Promise<any> => {
    const response = await axios.get(
      `${API_BASE_URL}/api/auth/me`,
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    );
    return response.data.data;
  },

  // Logout
  logout: async (accessToken: string): Promise<void> => {
    await axios.post(
      `${API_BASE_URL}/api/auth/logout`,
      {},
      {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      }
    );
  }
};
```

---

## 🎯 Usage Examples

### **Tenant Signup Form**

```typescript
import React, { useState } from 'react';
import { authService } from './services/authService';

export const TenantSignupPage: React.FC = () => {
  const [formData, setFormData] = useState({
    email: '',
    password: '',
    confirm_password: '',
    first_name: '',
    last_name: '',
    company_name: '',
    company_phone: '',
    company_city: '',
    accept_terms: false
  });

  const handleSignup = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await authService.tenantSignup(formData);
      
      if (result.success) {
        // Store tokens
        localStorage.setItem('access_token', result.data!.tokens.access_token);
        localStorage.setItem('refresh_token', result.data!.tokens.refresh_token);
        localStorage.setItem('user', JSON.stringify(result.data!.user));
        localStorage.setItem('tenant', JSON.stringify(result.data!.tenant));
        
        // Redirect to dashboard
        window.location.href = '/dashboard';
      } else {
        alert('Signup failed: ' + result.message);
      }
    } catch (error) {
      console.error('Signup error:', error);
      alert('An error occurred during signup');
    }
  };

  return (
    <form onSubmit={handleSignup}>
      <input
        type="email"
        placeholder="Email"
        value={formData.email}
        onChange={(e) => setFormData({ ...formData, email: e.target.value })}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={formData.password}
        onChange={(e) => setFormData({ ...formData, password: e.target.value })}
        required
      />
      <input
        type="password"
        placeholder="Confirm Password"
        value={formData.confirm_password}
        onChange={(e) => setFormData({ ...formData, confirm_password: e.target.value })}
        required
      />
      <input
        type="text"
        placeholder="First Name"
        value={formData.first_name}
        onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
        required
      />
      <input
        type="text"
        placeholder="Last Name"
        value={formData.last_name}
        onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
        required
      />
      <input
        type="text"
        placeholder="Company Name"
        value={formData.company_name}
        onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
        required
      />
      <input
        type="tel"
        placeholder="Company Phone"
        value={formData.company_phone}
        onChange={(e) => setFormData({ ...formData, company_phone: e.target.value })}
      />
      <input
        type="text"
        placeholder="Company City"
        value={formData.company_city}
        onChange={(e) => setFormData({ ...formData, company_city: e.target.value })}
      />
      <label>
        <input
          type="checkbox"
          checked={formData.accept_terms}
          onChange={(e) => setFormData({ ...formData, accept_terms: e.target.checked })}
          required
        />
        I accept the terms and conditions
      </label>
      <button type="submit">Sign Up</button>
    </form>
  );
};
```

### **Login Form**

```typescript
export const LoginPage: React.FC = () => {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const result = await authService.tenantLogin(email, password);
      
      if (result.success) {
        localStorage.setItem('access_token', result.data!.tokens.access_token);
        localStorage.setItem('refresh_token', result.data!.tokens.refresh_token);
        localStorage.setItem('user', JSON.stringify(result.data!.user));
        window.location.href = '/dashboard';
      } else {
        alert('Login failed: ' + result.message);
      }
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <form onSubmit={handleLogin}>
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        required
      />
      <input
        type="password"
        placeholder="Password"
        value={password}
        onChange={(e) => setPassword(e.target.value)}
        required
      />
      <button type="submit">Login</button>
    </form>
  );
};
```

### **Google OAuth Implementation**

```typescript
import React from 'react';
import { GoogleLogin } from '@react-oauth/google';
import { authService } from './services/authService';

export const GoogleAuthButton: React.FC = () => {
  const handleGoogleSuccess = async (credentialResponse: any) => {
    try {
      const result = await authService.googleLogin(credentialResponse.credential);
      
      if (result.success) {
        localStorage.setItem('access_token', result.data!.tokens.access_token);
        localStorage.setItem('refresh_token', result.data!.tokens.refresh_token);
        localStorage.setItem('user', JSON.stringify(result.data!.user));
        
        if (result.is_new_user && result.data!.tenant) {
          localStorage.setItem('tenant', JSON.stringify(result.data!.tenant));
        }
        
        window.location.href = '/dashboard';
      }
    } catch (error) {
      console.error('Google login failed:', error);
    }
  };

  return (
    <GoogleLogin
      onSuccess={handleGoogleSuccess}
      onError={() => console.log('Login Failed')}
    />
  );
};
```

**Setup in App.tsx:**

```typescript
import { GoogleOAuthProvider } from '@react-oauth/google';

function App() {
  return (
    <GoogleOAuthProvider clientId={process.env.REACT_APP_GOOGLE_CLIENT_ID!}>
      {/* Your routes */}
    </GoogleOAuthProvider>
  );
}

export default App;
```

**.env.local:**

```env
REACT_APP_API_URL=http://localhost:8000
REACT_APP_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

---

## 🔐 Token Management

### **Axios Interceptor for Auto Token Refresh**

```typescript
import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from 'axios';
import { authService } from './authService';

const api: AxiosInstance = axios.create({
  baseURL: process.env.REACT_APP_API_URL
});

api.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      try {
        const refreshToken = localStorage.getItem('refresh_token');
        if (refreshToken) {
          const { access_token } = await authService.refreshToken(refreshToken);
          localStorage.setItem('access_token', access_token);
          
          originalRequest.headers.Authorization = `Bearer ${access_token}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Redirect to login if refresh fails
        localStorage.clear();
        window.location.href = '/login';
      }
    }

    return Promise.reject(error);
  }
);

export default api;
```

---

## 📋 Password Requirements

Passwords must contain:
- ✅ Minimum 8 characters
- ✅ At least one uppercase letter (A-Z)
- ✅ At least one lowercase letter (a-z)
- ✅ At least one digit (0-9)
- ✅ At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

Example: `SecurePass123!`

---

## 🛡️ Security Best Practices

1. **Token Storage**
   ```typescript
   // Use sessionStorage for temporary sessions
   sessionStorage.setItem('access_token', token);
   
   // Or use httpOnly cookies (recommended)
   // Let backend set cookies automatically
   ```

2. **Token Expiration**
   ```typescript
   // Access tokens expire in 1 hour
   // Use refresh tokens to get new access tokens
   const { access_token } = await authService.refreshToken(refreshToken);
   ```

3. **HTTPS in Production**
   - Always use HTTPS endpoints in production
   - TS heck `process.env.REACT_APP_API_URL` is using https://

4. **Clear Tokens on Logout**
   ```typescript
   const handleLogout = async () => {
     const token = localStorage.getItem('access_token');
     if (token) {
       await authService.logout(token);
     }
     localStorage.clear();
     window.location.href = '/login';
   };
   ```

---

## 🧪 Testing with Postman

### **Import Collection**

```json
{
  "info": {
    "name": "Real Estate CRM Auth API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Tenant Signup",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/auth/tenant/signup",
        "body": {
          "mode": "raw",
          "raw": "{\"email\": \"test@company.com\", \"password\": \"TestPass123!\", \"confirm_password\": \"TestPass123!\", \"first_name\": \"Test\", \"last_name\": \"User\", \"company_name\": \"Test Co\", \"accept_terms\": true}"
        }
      }
    },
    {
      "name": "Tenant Login",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/auth/tenant/login",
        "body": {
          "mode": "raw",
          "raw": "{\"email\": \"test@company.com\", \"password\": \"TestPass123!\"}"
        }
      }
    }
  ]
}
```

---

## ✅ Checklist Before Launch

- [ ] Backend environment variables configured
- [ ] Google OAuth credentials obtained
- [ ] Frontend auth service created
- [ ] Login/Signup components built
- [ ] Google OAuth button integrated
- [ ] Token interceptor configured
- [ ] Logout flow implemented
- [ ] Error handling added
- [ ] Testing completed
- [ ] HTTPS configured for production

---

## 📞 Support

For issues or questions:
1. Check API documentation in `AUTH_IMPLEMENTATION_COMPLETE.md`
2. Review error responses for detailed messages
3. Check backend logs for server-side issues
4. Verify environment variables are correct
