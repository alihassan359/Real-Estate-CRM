/**
 * Types - Core Application Types
 */


export interface ApiResponse<T = unknown> {
  success: boolean;
  message: string;
  data?: T;
  error?: Record<string, unknown>;
}

export interface PaginationType {
  skip: number;
  limit: number;
  total: number;
}

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'admin' | 'manager' | 'operator';
  tenantId: string;
}

export interface Auth {
  accessToken: string;
  refreshToken: string;
  user: User;
}

