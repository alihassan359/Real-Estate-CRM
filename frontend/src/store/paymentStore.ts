import { create } from 'zustand';

export interface Payment {
  id: number;
  deal_id: number;
  amount: number;
  payment_date: string;
  payment_method: string;
  reference_number?: string;
  receipt_number?: string;
  notes?: string;
  status: string;
  tenant_id: number;
  created_at: string;
  updated_at: string;
}

export interface PaymentState {
  payments: Payment[];
  selectedPayment: Payment | null;
  isLoading: boolean;
  error: string | null;
  filters: {
    dealId?: number;
    status?: string;
  };

  // Actions
  setPayments: (payments: Payment[]) => void;
  addPayment: (payment: Payment) => void;
  updatePayment: (payment: Payment) => void;
  removePayment: (paymentId: number) => void;
  setSelectedPayment: (payment: Payment | null) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
  setFilters: (filters: any) => void;
}

export const usePaymentStore = create<PaymentState>((set) => ({
  payments: [],
  selectedPayment: null,
  isLoading: false,
  error: null,
  filters: {},

  setPayments: (payments) => set({ payments }),
  addPayment: (payment) => set((state) => ({ payments: [...state.payments, payment] })),
  updatePayment: (payment) =>
    set((state) => ({
      payments: state.payments.map((p) => (p.id === payment.id ? payment : p)),
      selectedPayment: state.selectedPayment?.id === payment.id ? payment : state.selectedPayment,
    })),
  removePayment: (paymentId) =>
    set((state) => ({
      payments: state.payments.filter((p) => p.id !== paymentId),
      selectedPayment: state.selectedPayment?.id === paymentId ? null : state.selectedPayment,
    })),
  setSelectedPayment: (payment) => set({ selectedPayment: payment }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
  setFilters: (filters) => set({ filters }),
}));
