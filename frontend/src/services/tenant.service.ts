import { apiClient } from './apiClient';

export interface CreateTenantRequest {
  company_name: string;
  company_email?: string;
  phone?: string;
  subscription_plan?: string;
  address?: string;
  city?: string;
  country?: string;
}

export interface TenantResponse {
  id: number;
  tenant_code: string;
  company_name: string;
  company_email?: string;
  phone?: string;
  address?: string;
  city?: string;
  country?: string;
  logo_url?: string;
  subscription_plan: string;
  paid_until?: string;
  status: string;
  created_at: string;
  updated_at: string;
}

export interface TenantUsage {
  current_users: number;
  max_users: number;
  current_deals: number;
  max_deals: number;
  storage_used_mb: number;
  storage_limit_mb: number;
  subscription_plan: string;
  status: string;
  paid_until?: string;
}

export class TenantService {
  static async createTenant(data: CreateTenantRequest) {
    const response = await apiClient.post<{ success: boolean; data: TenantResponse }>(
      '/tenants',
      data
    );
    return response.data.data;
  }

  static async getTenants(skip = 0, limit = 20) {
    const response = await apiClient.get<{
      success: boolean;
      data: TenantResponse[];
      pagination: { skip: number; limit: number; total: number };
    }>('/tenants', { params: { skip, limit } });
    return response.data.data;
  }

  static async getTenantById(tenantId: number) {
    const response = await apiClient.get<{ success: boolean; data: TenantResponse }>(
      `/tenants/${tenantId}`
    );
    return response.data.data;
  }

  static async updateTenant(tenantId: number, data: Partial<CreateTenantRequest>) {
    const response = await apiClient.patch<{ success: boolean; data: TenantResponse }>(
      `/tenants/${tenantId}`,
      data
    );
    return response.data.data;
  }

  static async updateSettings(tenantId: number, settings: any) {
    const response = await apiClient.patch<{ success: boolean; data: TenantResponse }>(
      `/tenants/${tenantId}/settings`,
      { settings }
    );
    return response.data.data;
  }

  static async getTenantUsage(tenantId: number) {
    const response = await apiClient.get<TenantUsage>(
      `/tenants/${tenantId}/usage`
    );
    return response.data;
  }

  static async suspendTenant(tenantId: number, reason?: string) {
    const response = await apiClient.patch<{ success: boolean; data: TenantResponse }>(
      `/tenants/${tenantId}/suspend`,
      { reason }
    );
    return response.data.data;
  }

  static async reactivateTenant(tenantId: number) {
    const response = await apiClient.patch<{ success: boolean; data: TenantResponse }>(
      `/tenants/${tenantId}/reactivate`
    );
    return response.data.data;
  }
}
