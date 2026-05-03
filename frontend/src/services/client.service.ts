/**
 * Client Service - API Calls for Clients
 */


import { apiClient } from './apiClient';

export interface Client {
  id: string;
  name: string;
  email: string;
  phone: string;
  cnic?: string;
  address?: string;
  city: string;
  province?: string;
}

export interface CreateClientRequest {
  name: string;
  email: string;
  phone: string;
  cnic?: string;
  city: string;
}

export class ClientService {
  static async getClients(skip = 0, limit = 10) {
    const response = await apiClient.get<{ data: Client[] }>('/clients', {
      params: { skip, limit },
    });
    return response.data;
  }

  static async getClientById(id: string) {
    const response = await apiClient.get<{ data: Client }>(`/clients/${id}`);
    return response.data;
  }

  static async createClient(data: CreateClientRequest) {
    const response = await apiClient.post<{ data: Client }>('/clients', data);
    return response.data;
  }

  static async updateClient(id: string, data: Partial<Client>) {
    const response = await apiClient.put<{ data: Client }>(`/clients/${id}`, data);
    return response.data;
  }

  static async deleteClient(id: string) {
    await apiClient.delete(`/clients/${id}`);
  }
}

// Export instance for compatibility
export const clientService = ClientService;

