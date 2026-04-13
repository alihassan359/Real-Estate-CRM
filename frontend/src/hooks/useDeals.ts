/**
 * useDeals Hook - Custom Hook for Deal Management
 */


import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { DealService, CreateDealRequest } from '@/services/deal.service';

export function useDeals(skip = 0, limit = 10) {
  return useQuery({
    queryKey: ['deals', skip, limit],
    queryFn: () => DealService.getDeals(skip, limit),
  });
}

export function useDealById(id: string) {
  return useQuery({
    queryKey: ['deal', id],
    queryFn: () => DealService.getDealById(id),
    enabled: !!id,
  });
}

export function useCreateDeal() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreateDealRequest) => DealService.createDeal(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deals'] });
    },
  });
}

export function useUpdateDeal(id: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data) => DealService.updateDeal(id, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deal', id] });
      queryClient.invalidateQueries({ queryKey: ['deals'] });
    },
  });
}

export function useDeleteDeal() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (id: string) => DealService.deleteDeal(id),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['deals'] });
    },
  });
}

