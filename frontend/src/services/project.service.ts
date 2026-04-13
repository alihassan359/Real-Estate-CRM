/**
 * Project Service - API Calls for Real Estate Projects
 */


import { apiClient } from './apiClient';

export interface Project {
  id: string;
  name: string;
  description?: string;
  location: string;
  city: string;
  totalPlots: number;
  availablePlots: number;
  totalArea: number;
  pricePerSqFt: number;
  status: 'active' | 'completed' | 'on_hold';
}

export interface CreateProjectRequest {
  name: string;
  location: string;
  city: string;
  totalPlots: number;
  totalArea: number;
  pricePerSqFt: number;
}

export class ProjectService {
  static async getProjects(skip = 0, limit = 10) {
    const response = await apiClient.get<{ data: Project[] }>('/projects', {
      params: { skip, limit },
    });
    return response.data;
  }

  static async getProjectById(id: string) {
    const response = await apiClient.get<{ data: Project }>(`/projects/${id}`);
    return response.data;
  }

  static async createProject(data: CreateProjectRequest) {
    const response = await apiClient.post<{ data: Project }>('/projects', data);
    return response.data;
  }

  static async updateProject(id: string, data: Partial<Project>) {
    const response = await apiClient.put<{ data: Project }>(`/projects/${id}`, data);
    return response.data;
  }

  static async deleteProject(id: string) {
    await apiClient.delete(`/projects/${id}`);
  }
}

