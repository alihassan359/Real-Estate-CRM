"""
Reports Page - Analytics & Reports
"""

'use client';

import React from 'react';
import { BarChart3, TrendingUp, PieChart } from 'lucide-react';

export default function ReportsPage() {
  const reportCards = [
    {
      icon: TrendingUp,
      title: 'Sales Performance',
      description: 'Monthly and yearly sales trends',
    },
    {
      icon: PieChart,
      title: 'Deal Distribution',
      description: 'Deal breakdown by status and agent',
    },
    {
      icon: BarChart3,
      title: 'Revenue Analysis',
      description: 'Revenue trends and forecasts',
    },
  ];

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Reports</h1>
        <p className="text-gray-600 mt-1">Business analytics and performance metrics</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {reportCards.map((card) => {
          const Icon = card.icon;
          return (
            <button
              key={card.title}
              className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition text-left"
            >
              <Icon className="text-blue-600 mb-4" size={28} />
              <h3 className="text-lg font-semibold text-gray-900">{card.title}</h3>
              <p className="text-sm text-gray-600 mt-2">{card.description}</p>
            </button>
          );
        })}
      </div>

      <div className="bg-white rounded-lg shadow-md p-8">
        <p className="text-center text-gray-500">Reports coming soon...</p>
      </div>
    </div>
  );
}
