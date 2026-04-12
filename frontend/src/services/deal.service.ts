"""
Deal Service - API Calls for Deals/Contracts
"""

import { apiClient } from './apiClient';

export interface Deal {
  id: string;
  dealNumber: string;
  clientId: string;
  projectId: string;
  plotId: string;
  contractDate: string;
  agreementPrice: number;
  downPayment: number;
  remainingBalance: number;
  paymentPlan: string;
  status: 'active' | 'completed' | 'cancelled';
}

export interface CreateDealRequest {
  clientId: string;
  projectId: string;
  plotId: string;
  agreementPrice: number;
  downPayment: number;
  paymentPlan: string;
}

export class DealService {
  static async getDeals(skip = 0, limit = 10) {
    const response = await apiClient.get<{ data: Deal[] }>('/deals', {
      params: { skip, limit },
    });
    return response.data;
  }

  static async getDealById(id: string) {
    const response = await apiClient.get<{ data: Deal }>(`/deals/${id}`);
    return response.data;
  }

  static async createDeal(data: CreateDealRequest) {
    const response = await apiClient.post<{ data: Deal }>('/deals', data);
    return response.data;
  }

  static async updateDeal(id: string, data: Partial<Deal>) {
    const response = await apiClient.put<{ data: Deal }>(`/deals/${id}`, data);
    return response.data;
  }

  static async deleteDeal(id: string) {
    await apiClient.delete(`/deals/${id}`);
  }
}
