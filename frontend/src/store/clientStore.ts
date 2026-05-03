import { create } from 'zustand';

export interface Client {
  id: number;
  name: string;
  email?: string;
  phone?: string;
  cnic?: string;
  address?: string;
  city?: string;
  country?: string;
  status: string;
  tenant_id: number;
  created_at: string;
  updated_at: string;
}

export interface ClientState {
  clients: Client[];
  selectedClient: Client | null;
  isLoading: boolean;
  error: string | null;

  // Actions
  setClients: (clients: Client[]) => void;
  addClient: (client: Client) => void;
  updateClient: (client: Client) => void;
  removeClient: (clientId: number) => void;
  setSelectedClient: (client: Client | null) => void;
  setLoading: (isLoading: boolean) => void;
  setError: (error: string | null) => void;
}

export const useClientStore = create<ClientState>((set) => ({
  clients: [],
  selectedClient: null,
  isLoading: false,
  error: null,

  setClients: (clients) => set({ clients }),
  addClient: (client) => set((state) => ({ clients: [...state.clients, client] })),
  updateClient: (client) =>
    set((state) => ({
      clients: state.clients.map((c) => (c.id === client.id ? client : c)),
      selectedClient: state.selectedClient?.id === client.id ? client : state.selectedClient,
    })),
  removeClient: (clientId) =>
    set((state) => ({
      clients: state.clients.filter((c) => c.id !== clientId),
      selectedClient: state.selectedClient?.id === clientId ? null : state.selectedClient,
    })),
  setSelectedClient: (client) => set({ selectedClient: client }),
  setLoading: (isLoading) => set({ isLoading }),
  setError: (error) => set({ error }),
}));
