/**
 * usePayments Hook - Custom Hook for Payment Management
 */


import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { PaymentService, CreatePaymentRequest } from '@/services/payment.service';

export function usePayments(skip = 0, limit = 10) {
  return useQuery({
    queryKey: ['payments', skip, limit],
    queryFn: () => PaymentService.getPayments(skip, limit),
  });
}

export function usePaymentById(id: string) {
  return useQuery({
    queryKey: ['payment', id],
    queryFn: () => PaymentService.getPaymentById(id),
    enabled: !!id,
  });
}

export function useCreatePayment() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (data: CreatePaymentRequest) => PaymentService.createPayment(data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['payments'] });
    },
  });
}

export function usePendingPayments() {
  return useQuery({
    queryKey: ['payments', 'pending'],
    queryFn: () => PaymentService.getPendingPayments(),
  });
}

