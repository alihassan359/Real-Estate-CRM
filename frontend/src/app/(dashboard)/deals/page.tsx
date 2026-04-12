"""
Deals Page - Deals Management
"""

'use client';

import React, { useState } from 'react';
import { DealForm } from '@/modules/deal/components/deal-form';
import { DealTable } from '@/modules/deal/components/deal-table';

export default function DealsPage() {
  const [showForm, setShowForm] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Deals</h1>
          <p className="text-gray-600 mt-1">Manage your property deals and contracts</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          {showForm ? 'Cancel' : 'Create Deal'}
        </button>
      </div>

      {showForm && (
        <DealForm onSuccess={() => setShowForm(false)} />
      )}

      <DealTable />
    </div>
  );
}
