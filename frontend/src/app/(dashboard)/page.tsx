/**
 * Dashboard Page - Main Dashboard
 */


'use client';

import React from 'react';
import { usePendingPayments } from '@/hooks/usePayments';
import { useDeals } from '@/hooks/useDeals';
import { formatCurrency } from '@/utils/format';
import { TrendingUp, Users, FileText, DollarSign } from 'lucide-react';

export default function DashboardPage() {
  const { data: deals, isLoading: dealsLoading } = useDeals(0, 5);
  const { data: payments, isLoading: paymentsLoading } = usePendingPayments();

  const stats = [
    {
      icon: FileText,
      label: 'Active Deals',
      value: Array.isArray(deals) ? deals.length : 0,
      color: 'blue',
    },
    {
      icon: DollarSign,
      label: 'Pending Payments',
      value: Array.isArray(payments) ? payments.length : 0,
      color: 'orange',
    },
    {
      icon: Users,
      label: 'Total Clients',
      value: 127,
      color: 'green',
    },
    {
      icon: TrendingUp,
      label: 'Monthly Revenue',
      value: '$45,250',
      color: 'purple',
    },
  ];

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-1">Welcome back! Here's your business overview.</p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat) => {
          const Icon = stat.icon;
          const colorClasses = {
            blue: 'bg-blue-100 text-blue-600',
            orange: 'bg-orange-100 text-orange-600',
            green: 'bg-green-100 text-green-600',
            purple: 'bg-purple-100 text-purple-600',
          };

          return (
            <div key={stat.label} className="bg-white rounded-lg shadow-md p-6">
              <div className={`w-12 h-12 rounded-lg ${colorClasses[stat.color as keyof typeof colorClasses]} flex items-center justify-center mb-4`}>
                <Icon size={24} />
              </div>
              <p className="text-gray-600 text-sm">{stat.label}</p>
              <p className="text-3xl font-bold text-gray-900 mt-2">{stat.value}</p>
            </div>
          );
        })}
      </div>

      {/* Recent Deals & Payments */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Recent Deals */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Recent Deals</h3>
          {dealsLoading ? (
            <p className="text-gray-500">Loading...</p>
          ) : (
            <div className="space-y-4">
              {Array.isArray(deals) && deals.slice(0, 3).map((deal: any) => (
                <div key={deal.id} className="flex justify-between items-center pb-4 border-b">
                  <div>
                    <p className="font-semibold text-gray-900">{deal.deal_number}</p>
                    <p className="text-sm text-gray-600">{deal.client_id}</p>
                  </div>
                  <p className="font-semibold text-gray-900">{formatCurrency(deal.agreement_price)}</p>
                </div>
              ))}
            </div>
          )}
        </div>

        {/* Pending Payments */}
        <div className="bg-white rounded-lg shadow-md p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Pending Payments</h3>
          {paymentsLoading ? (
            <p className="text-gray-500">Loading...</p>
          ) : (
            <div className="space-y-4">
              {Array.isArray(payments) && payments.slice(0, 3).map((payment: any) => (
                <div key={payment.id} className="flex justify-between items-center pb-4 border-b">
                  <div>
                    <p className="font-semibold text-gray-900">{payment.paymentNumber}</p>
                    <p className="text-sm text-gray-600">Due: {new Date(payment.dueDate).toLocaleDateString()}</p>
                  </div>
                  <p className="font-semibold text-red-600">{formatCurrency(payment.amount)}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

