/**
 * Deal Table Component - Display Deals in Table Format
 */


'use client';

import React from 'react';
import { useDeals } from '@/hooks/useDeals';
import { formatCurrency, formatDate } from '@/utils/format';

export const DealTable: React.FC = () => {
  const { data, isLoading, error } = useDeals();

  if (isLoading) {
    return <div className="text-center py-8">Loading deals...</div>;
  }

  if (error) {
    return <div className="text-center py-8 text-red-600">Error loading deals</div>;
  }

  const deals = data?.data || [];

  if (deals.length === 0) {
    return <div className="text-center py-8 text-gray-500">No deals found</div>;
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Deal #</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Client</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Project</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Price</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Status</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Date</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {deals.map((deal: any) => (
            <tr key={deal.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 text-sm text-gray-700">{deal.dealNumber}</td>
              <td className="px-6 py-4 text-sm text-gray-700">{deal.clientId}</td>
              <td className="px-6 py-4 text-sm text-gray-700">{deal.projectId}</td>
              <td className="px-6 py-4 text-sm font-semibold text-gray-900">
                {formatCurrency(deal.agreementPrice)}
              </td>
              <td className="px-6 py-4 text-sm">
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    deal.status === 'active'
                      ? 'bg-green-100 text-green-700'
                      : deal.status === 'completed'
                      ? 'bg-blue-100 text-blue-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {deal.status}
                </span>
              </td>
              <td className="px-6 py-4 text-sm text-gray-700">{formatDate(deal.contractDate)}</td>
              <td className="px-6 py-4 text-sm text-blue-600 hover:underline cursor-pointer">
                View
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

