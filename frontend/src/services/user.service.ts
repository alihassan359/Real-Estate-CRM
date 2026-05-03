import { apiClient } from './apiClient';

export interface CreateUserRequest {
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: string;
  password?: string;
}

export interface UserResponse {
  id: number;
  email: string;
  first_name: string;
  last_name: string;
  phone?: string;
  role: string;
  status: string;
  tenant_id: number;
  created_at: string;
  updated_at: string;
}

export class UserService {
  static async getUsers(skip = 0, limit = 20, role?: string) {
    const params: any = { skip, limit };
    if (role) params.role = role;
    const response = await apiClient.get<{ success: boolean; data: UserResponse[] }>(
      '/users',
      { params }
    );
    return response.data.data;
  }

  static async getUserById(userId: number) {
    const response = await apiClient.get<{ success: boolean; data: UserResponse }>(
      `/users/${userId}`
    );
    return response.data.data;
  }

  static async createUser(data: CreateUserRequest) {
    const response = await apiClient.post<{ success: boolean; data: UserResponse }>(
      '/users',
      data
    );
    return response.data.data;
  }

  static async updateUser(userId: number, data: Partial<CreateUserRequest>) {
    const response = await apiClient.patch<{ success: boolean; data: UserResponse }>(
      `/users/${userId}`,
      data
    );
    return response.data.data;
  }

  static async updateRole(userId: number, role: string) {
    const response = await apiClient.patch<{ success: boolean; data: UserResponse }>(
      `/users/${userId}/role`,
      { role }
    );
    return response.data.data;
  }

  static async deleteUser(userId: number) {
    await apiClient.delete(`/users/${userId}`);
  }

  static async suspendUser(userId: number) {
    const response = await apiClient.patch<{ success: boolean; data: UserResponse }>(
      `/users/${userId}/suspend`
    );
    return response.data.data;
  }

  static async enableUser(userId: number) {
    const response = await apiClient.patch<{ success: boolean; data: UserResponse }>(
      `/users/${userId}/enable`
    );
    return response.data.data;
  }
}
