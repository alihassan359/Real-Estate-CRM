// API Response Types
export interface ApiResponse<T> {
  success: boolean;
  message?: string;
  data?: T;
  detail?: string;
  pagination?: {
    skip: number;
    limit: number;
    total: number;
  };
}

// Auth Types
export interface LoginCredentials {
  email: string;
  password: string;
}

export interface SignupCredentials {
  company_name: string;
  email: string;
  password: string;
  first_name: string;
  last_name: string;
  phone?: string;
}

export interface AuthUser {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  tenant_id: number;
  status: string;
}

// Tenant Types
export interface Tenant {
  id: number;
  tenant_code: string;
  company_name: string;
  subscription_plan: string;
  status: string;
  created_at: string;
}

// Deal Types
export interface Deal {
  id: number;
  deal_number: string;
  client_id: number;
  project_id: number;
  agreement_price: number;
  down_payment: number;
  remaining_balance: number;
  payment_plan: string;
  status: string;
}

// Client Types
export interface Client {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  cnic?: string;
  address?: string;
  status: string;
}

// Payment Types
export interface Payment {
  id: number;
  deal_id: number;
  amount: number;
  payment_date: string;
  payment_method: string;
  status: string;
}

// User Types
export interface User {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  role: string;
  status: string;
}
