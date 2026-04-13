/**
 * Payments Page - Payment Management
 */


'use client';

import React, { useState } from 'react';
import { PaymentTable } from '@/modules/payment/components/payment-table';
import { PaymentModal } from '@/modules/payment/components/payment-modal';
import { Plus } from 'lucide-react';

export default function PaymentsPage() {
  const [showModal, setShowModal] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Payments</h1>
          <p className="text-gray-600 mt-1">Track and manage all payment transactions</p>
        </div>
        <button
          onClick={() => setShowModal(true)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          <Plus size={20} />
          Record Payment
        </button>
      </div>

      <PaymentTable />

      <PaymentModal isOpen={showModal} onClose={() => setShowModal(false)} />
    </div>
  );
}

