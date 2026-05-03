/**
 * Deal Service - API Calls for Deals/Contracts
 */

import { apiClient } from './apiClient';

export interface Deal {
  id: number;
  deal_number: string;
  client_id: number;
  project_id: number;
  plot_id?: number;
  agreement_date: string;
  agreement_price: number;
  down_payment: number;
  remaining_balance: number;
  payment_plan: string;
  commission_percentage: number;
  status: string;
  tenant_id: number;
  created_at: string;
  updated_at: string;
}

export interface CreateDealRequest {
  client_id: number;
  project_id: number;
  plot_id?: number;
  agreement_date: string;
  agreement_price: number;
  down_payment: number;
  payment_plan: string;
  commission_percentage?: number;
}

export class DealService {
  static async getDeals(skip = 0, limit = 20, status?: string, client_id?: number) {
    const params: any = { skip, limit };
    if (status) params.status = status;
    if (client_id) params.client_id = client_id;
    
    const response = await apiClient.get<{
      success: boolean;
      data: Deal[];
      pagination: { skip: number; limit: number; total: number };
    }>('/deals', { params });
    return response.data.data;
  }

  static async getDealById(id: number) {
    const response = await apiClient.get<{ success: boolean; data: Deal }>(
      `/deals/${id}`
    );
    return response.data.data;
  }

  static async createDeal(data: CreateDealRequest) {
    const response = await apiClient.post<{ success: boolean; data: Deal }>(
      '/deals',
      data
    );
    return response.data.data;
  }

  static async updateDeal(id: number, data: Partial<CreateDealRequest>) {
    const response = await apiClient.patch<{ success: boolean; data: Deal }>(
      `/deals/${id}`,
      data
    );
    return response.data.data;
  }

  static async updateStatus(id: number, status: string) {
    const response = await apiClient.patch<{ success: boolean; data: Deal }>(
      `/deals/${id}/status`,
      { status }
    );
    return response.data.data;
  }

  static async deleteDeal(id: number) {
    await apiClient.delete(`/deals/${id}`);
  }

  static async getDealStats() {
    const response = await apiClient.get<any>('/deals/stats');
    return response.data;
  }
}

// Export instance for compatibility
export const dealService = DealService;


