/**
 * Tenant Store - Zustand Store for Multi-Tenant State
 */


import { create } from 'zustand';

export interface Tenant {
  id: string;
  name: string;
  slug: string;
  logo: string;
  plan: 'free' | 'pro' | 'enterprise';
}

export interface TenantState {
  currentTenant: Tenant | null;
  tenants: Tenant[];

  // Actions
  setCurrentTenant: (tenant: Tenant) => void;
  setTenants: (tenants: Tenant[]) => void;
  switchTenant: (tenantId: string) => void;
}

export const useTenantStore = create<TenantState>((set, get) => ({
  currentTenant: null,
  tenants: [],

  setCurrentTenant: (tenant) => set({ currentTenant: tenant }),
  
  setTenants: (tenants) => set({ tenants }),

  switchTenant: (tenantId) => {
    const { tenants } = get();
    const tenant = tenants.find(t => t.id === tenantId);
    if (tenant) {
      set({ currentTenant: tenant });
      if (typeof window !== 'undefined') {
        localStorage.setItem('tenantId', tenantId);
      }
    }
  },
}));

