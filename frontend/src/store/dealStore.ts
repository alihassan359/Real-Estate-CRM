import { create } from 'zustand';

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

export interface DealState {
  deals: Deal[];
  selectedDeal: Deal | null;
  isLoading: boolean;
  error: string | null;
  filters: {
    status?: string;
    clientId?: number;
    projectId?: number;
  };

  // Actions
  setDeals: (deals: Deal[]) => void;
  addDeal: (deal: Deal) => void;
  updateDeal: (deal: Deal) => void;
  removeDeal: (dealId: number) => void;
  setSelectedDeal: (deal: Deal | null) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  setFilters: (filters: any) => void;
}

export const useDealStore = create<DealState>((set) => ({
  deals: [],
  selectedDeal: null,
  isLoading: false,
  error: null,
  filters: {},

  setDeals: (deals) => set({ deals }),
  addDeal: (deal) => set((state) => ({ deals: [...state.deals, deal] })),
  updateDeal: (deal) =>
    set((state) => ({
      deals: state.deals.map((d) => (d.id === deal.id ? deal : d)),
      selectedDeal: state.selectedDeal?.id === deal.id ? deal : state.selectedDeal,
    })),
  removeDeal: (dealId) =>
    set((state) => ({
      deals: state.deals.filter((d) => d.id !== dealId),
      selectedDeal: state.selectedDeal?.id === dealId ? null : state.selectedDeal,
    })),
  setSelectedDeal: (deal) => set({ selectedDeal: deal }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  setFilters: (filters) => set({ filters }),
}));
