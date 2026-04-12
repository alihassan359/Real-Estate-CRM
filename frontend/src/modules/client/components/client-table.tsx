"""
Clients Table Component - Display Clients List
"""

'use client';

import React from 'react';
import { useClients } from '@/hooks/useClients';
import { LoadingSpinner } from '@/components/shared/loading';

interface UseClientsHook {
  data: { data: any[] } | undefined;
  isLoading: boolean;
  error: any;
}

export const ClientTable: React.FC = () => {
  // Note: useClients hook needs to be created
  const { data, isLoading, error } = useClients?.() || { 
    data: undefined, 
    isLoading: false, 
    error: null 
  } as UseClientsHook;

  if (isLoading) {
    return <LoadingSpinner message="Loading clients..." />;
  }

  if (error) {
    return (
      <div className="bg-red-100 text-red-700 p-4 rounded-lg">
        Error loading clients. Please try again.
      </div>
    );
  }

  const clients = data?.data || [];

  if (clients.length === 0) {
    return (
      <div className="bg-white rounded-lg shadow-md p-8 text-center text-gray-500">
        No clients found. Create your first client to get started.
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden">
      <table className="w-full">
        <thead className="bg-gray-100">
          <tr>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Name</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Email</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Phone</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">City</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Deals</th>
            <th className="px-6 py-3 text-left text-sm font-semibold text-gray-700">Actions</th>
          </tr>
        </thead>
        <tbody className="divide-y divide-gray-200">
          {clients.map((client: any) => (
            <tr key={client.id} className="hover:bg-gray-50">
              <td className="px-6 py-4 font-medium text-gray-900">{client.name}</td>
              <td className="px-6 py-4 text-sm text-gray-700">{client.email}</td>
              <td className="px-6 py-4 text-sm text-gray-700">{client.phoneNumber}</td>
              <td className="px-6 py-4 text-sm text-gray-700">{client.city}</td>
              <td className="px-6 py-4 text-sm font-semibold text-gray-900">{client.dealsCount || 0}</td>
              <td className="px-6 py-4 text-sm">
                <button className="text-blue-600 hover:underline mr-4">View</button>
                <button className="text-gray-600 hover:underline">Edit</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};
