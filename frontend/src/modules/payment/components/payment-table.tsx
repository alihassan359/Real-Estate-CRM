/**
 * Payment Table Component - Display Payments List
 */


'use client';

import React from 'react';
import { usePayments } from '@/hooks/usePayments';
import { formatCurrency, formatDate } from '@/utils/format';
import { LoadingSpinner } from '@/components/shared/loading';

export const PaymentTable: React.FC = () => {
  const { data, isLoading, error } = usePayments(0, 10);

  if (isLoading) {
    return <LoadingSpinner message="Loading payments..." />;
  }

  if (error) {
    return (
      <div className="bg-red-100 text-red-700 p-4 rounded-lg">
        Error loading payments. Please try again.
      </div>
    );
  }

  const payments = data?.data || [];

  if (payments.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center text-gray-500">
        No payments found
      </div>
    );
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'paid':
        return 'bg-green-100 text-green-700';
      case 'pending':
        return 'bg-yellow-100 text-yellow-700';
      case 'overdue':
        return 'bg-red-100 text-red-700';
      default:
        return 'bg-gray-100 text-gray-700';
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Payment #</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Deal</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Amount</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Due Date</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Status</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Method</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {payments.map((payment: any) => (
            <tr key={payment.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 text-sm font-medium text-gray-700">{payment.paymentNumber}</td>
              <td className="px-6 py-4 text-sm text-gray-700">{payment.dealId}</td>
              <td className="px-6 py-4 text-sm font-semibold text-gray-900">
                {formatCurrency(payment.amount)}
              </td>
              <td className="px-6 py-4 text-sm text-gray-700">
                {formatDate(payment.dueDate)}
              </td>
              <td className="px-6 py-4 text-sm">
                <span className={`px-3 py-1 rounded-full text-xs font-semibold ${getStatusColor(payment.status)}`}>
                  {payment.status}
                </span>
              </td>
              <td className="px-6 py-4 text-sm text-gray-700">{payment.paymentMethod}</td>
              <td className="px-6 py-4 text-sm">
                <button className="text-blue-600 hover:underline">View Receipt</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

