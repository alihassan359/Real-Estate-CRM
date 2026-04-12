"""
Auth Service - API Calls for Authentication
"""

import { apiClient } from './apiClient';

export interface LoginRequest {
  email: string;
  password: string;
}

export interface LoginResponse {
  success: boolean;
  data: {
    accessToken: string;
    refreshToken: string;
    user: {
      id: string;
      email: string;
      firstName: string;
      lastName: string;
      role: string;
      tenantId: string;
    };
  };
}

export interface SignupRequest {
  email: string;
  password: string;
  firstName: string;
  lastName: string;
  tenantName?: string;
}

export class AuthService {
  static async login(credentials: LoginRequest) {
    const response = await apiClient.post<LoginResponse>('/auth/login', credentials);
    return response.data;
  }

  static async signup(data: SignupRequest) {
    const response = await apiClient.post<LoginResponse>('/auth/signup', data);
    return response.data;
  }

  static async logout() {
    await apiClient.post('/auth/logout');
  }

  static async refreshToken(refreshToken: string) {
    const response = await apiClient.post<LoginResponse>('/auth/refresh', { refreshToken });
    return response.data;
  }

  static async getProfile() {
    const response = await apiClient.get('/auth/me');
    return response.data;
  }
}
