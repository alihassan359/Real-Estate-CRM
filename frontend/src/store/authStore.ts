/**
 * Auth Store - Zustand Store for
 Authentication State
 */


import { create } from 'zustand';
import { jwtDecode } from 'jwt-decode';

export interface User {
  id: string;
  email: string;
  firstName: string;
  lastName: string;
  role: 'admin' | 'manager' | 'operator';
  tenantId: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;

  // Actions
  setUser: (user: User) => void;
  setToken: (token: string) => void;
  logout: () => void;
  isTokenValid: () => boolean;
  hasRole: (role: string | string[]) => boolean;
  hasPermission: (permission: string) => boolean;
}

export const useAuthStore = create<AuthState>((set, get) => {
  // Initialize token from localStorage
  const initialToken = typeof window !== 'undefined' ? localStorage.getItem('token') : null;
  
  return {
    user: null,
    token: initialToken,
    isAuthenticated: !!initialToken,
    isLoading: false,

    setUser: (user) => set({ user, isAuthenticated: true }),
    
    setToken: (token) => {
      if (typeof window !== 'undefined') {
        localStorage.setItem('token', token);
      }
      set({ token, isAuthenticated: true });
    },

  logout: () => {
    if (typeof window !== 'undefined') {
      localStorage.removeItem('token');
    }
    set({ user: null, token: null, isAuthenticated: false });
  },

  isTokenValid: () => {
    const { token } = get();
    if (!token) return false;
    try {
      const decoded = jwtDecode(token);
      return decoded.exp ? decoded.exp > Date.now() / 1000 : false;
    } catch {
      return false;
    }
  },

  hasRole: (role) => {
    const { user } = get();
    if (!user) return false;
    return Array.isArray(role) ? role.includes(user.role) : role === user.role;
  },

  hasPermission: (permission) => {
    const { user } = get();
    if (!user) return false;
    
    const rolePermissions: Record<string, string[]> = {
      admin: ['create_deal', 'edit_deal', 'delete_deal', 'view_payments', 'create_payment', 'manage_users'],
      manager: ['create_deal', 'edit_deal', 'view_payments', 'create_payment'],
      operator: ['create_deal', 'view_payments'],
    };

    return rolePermissions[user.role]?.includes(permission) ?? false;
  },
  };
});

