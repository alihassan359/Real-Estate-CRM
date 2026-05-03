/**
 * Payment Service - API Calls for Payments
 */


import { apiClient } from './apiClient';

export interface Payment {
  id: string;
  paymentNumber: string;
  dealId: string;
  clientId: string;
  amount: number;
  paymentDate: string;
  dueDate: string;
  paymentMethod: string;
  status: 'pending' | 'paid' | 'overdue' | 'cancelled';
}

export interface CreatePaymentRequest {
  dealId: string;
  clientId: string;
  amount: number;
  dueDate: string;
  paymentMethod: string;
}

export class PaymentService {
  static async getPayments(skip = 0, limit = 10) {
    const response = await apiClient.get<{ data: Payment[] }>('/payments', {
      params: { skip, limit },
    });
    return response.data;
  }

  static async getPaymentById(id: string) {
    const response = await apiClient.get<{ data: Payment }>(`/payments/${id}`);
    return response.data;
  }

  static async createPayment(data: CreatePaymentRequest) {
    const response = await apiClient.post<{ data: Payment }>('/payments', data);
    return response.data;
  }

  static async updatePayment(id: string, data: Partial<Payment>) {
    const response = await apiClient.put<{ data: Payment }>(`/payments/${id}`, data);
    return response.data;
  }

  static async deletePayment(id: string) {
    await apiClient.delete(`/payments/${id}`);
  }

  static async getPendingPayments() {
    const response = await apiClient.get<{ data: Payment[] }>('/payments?status=pending');
    return response.data;
  }
}

// Export instance for compatibility
export const paymentService = PaymentService;

