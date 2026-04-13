/**
 * Clients Page - Client Management
 */


'use client';

import React, { useState } from 'react';
import { ClientTable } from '@/modules/client/components/client-table';
import { Plus } from 'lucide-react';

export default function ClientsPage() {
  const [showForm, setShowForm] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Clients</h1>
          <p className="text-gray-600 mt-1">Manage your real estate clients and contacts</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          <Plus size={20} />
          Add Client
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow-md p-8">
          {/* Client form will be added here */}
          <p className="text-gray-600">Client form coming soon...</p>
        </div>
      )}

      <ClientTable />
    </div>
  );
}

