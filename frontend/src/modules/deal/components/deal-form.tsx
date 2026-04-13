/**
 * Deal Form Component - Create/Edit Deal Form (Multi-Step)
 */


'use client';

import React, { useState } from 'react';
import { useCreateDeal } from '@/hooks/useDeals';
import { useAuthStore } from '@/store/authStore';

interface DealFormData {
  projectId: string;
  plotId: string;
  clientId: string;
  agreementPrice: number;
  downPayment: number;
  paymentPlan: string;
}

export const DealForm: React.FC<{ onSuccess?: () => void }> = ({ onSuccess }) => {
  const createDeal = useCreateDeal();
  const { hasPermission } = useAuthStore();
  const [step, setStep] = useState(1);
  const [formData, setFormData] = useState<Partial<DealFormData>>({
    paymentPlan: 'monthly',
  });

  if (!hasPermission('create_deal')) {
    return (
      <div className="p-4 bg-red-100 text-red-700 rounded-lg">
        You don't have permission to create deals
      </div>
    );
  }

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: isNaN(Number(value)) ? value : Number(value),
    }));
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await createDeal.mutateAsync(formData as DealFormData);
      onSuccess?.();
      setFormData({ paymentPlan: 'monthly' });
      setStep(1);
    } catch (error) {
      console.error('Error creating deal:', error);
    }
  };

  const steps = [
    { number: 1, title: 'Project & Plot' },
    { number: 2, title: 'Client Info' },
    { number: 3, title: 'Payment Details' },
    { number: 4, title: 'Review' },
  ];

  return (
    <div className="bg-white rounded-lg shadow-md p-8 max-w-2xl mx-auto">
      {/* Steps */}
      <div className="flex justify-between mb-8">
        {steps.map((s) => (
          <div
            key={s.number}
            className={`flex-1 text-center ${
              s.number <= step ? 'text-blue-600' : 'text-gray-400'
            }`}
          >
            <div
              className={`mx-auto w-10 h-10 rounded-full flex items-center justify-center font-semibold mb-2 ${
                s.number <= step ? 'bg-blue-600 text-white' : 'bg-gray-200'
              }`}
            >
              {s.number}
            </div>
            <p className="text-sm">{s.title}</p>
          </div>
        ))}
      </div>

      <form onSubmit={handleSubmit}>
        {/* Step 1: Project & Plot */}
        {step === 1 && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Project</label>
              <select
                name="projectId"
                value={formData.projectId || ''}
                onChange={handleInputChange}
                required
                className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value="">Select project</option>
                <option value="1">Project A</option>
                <option value="2">Project B</option>
              </select>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Plot Number</label>
              <input
                type="text"
                name="plotId"
                value={formData.plotId || ''}
                onChange={handleInputChange}
                required
                placeholder="Enter plot number"
                className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
          </div>
        )}

        {/* Step 2: Client Info */}
        {step === 2 && (
          <div>
            <label className="block text-sm font-medium text-gray-700">Client ID</label>
            <input
              type="text"
              name="clientId"
              value={formData.clientId || ''}
              onChange={handleInputChange}
              required
              placeholder="Select or enter client"
              className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"
            />
          </div>
        )}

        {/* Step 3: Payment Details */}
        {step === 3 && (
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700">Agreement Price</label>
              <input
                type="number"
                name="agreementPrice"
                value={formData.agreementPrice || ''}
                onChange={handleInputChange}
                required
                placeholder="0.00"
                className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Down Payment</label>
              <input
                type="number"
                name="downPayment"
                value={formData.downPayment || ''}
                onChange={handleInputChange}
                required
                placeholder="0.00"
                className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700">Payment Plan</label>
              <select
                name="paymentPlan"
                value={formData.paymentPlan || 'monthly'}
                onChange={handleInputChange}
                className="mt-1 w-full px-4 py-2 border border-gray-300 rounded-lg"
              >
                <option value="monthly">Monthly</option>
                <option value="quarterly">Quarterly</option>
                <option value="semi-annual">Semi-Annual</option>
                <option value="annual">Annual</option>
              </select>
            </div>
          </div>
        )}

        {/* Step 4: Review */}
        {step === 4 && (
          <div className="space-y-2 text-sm">
            <p><strong>Project:</strong> {formData.projectId}</p>
            <p><strong>Client:</strong> {formData.clientId}</p>
            <p><strong>Agreement Price:</strong> ${formData.agreementPrice}</p>
            <p><strong>Down Payment:</strong> ${formData.downPayment}</p>
            <p><strong>Payment Plan:</strong> {formData.paymentPlan}</p>
          </div>
        )}

        {/* Navigation Buttons */}
        <div className="flex justify-between mt-8 gap-4">
          <button
            type="button"
            onClick={() => setStep(Math.max(1, step - 1))}
            disabled={step === 1}
            className="px-6 py-2 border border-gray-300 rounded-lg hover:bg-gray-50 disabled:opacity-50"
          >
            Previous
          </button>

          {step < 4 ? (
            <button
              type="button"
              onClick={() => setStep(step + 1)}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
              Next
            </button>
          ) : (
            <button
              type="submit"
              disabled={createDeal.isPending}
              className="px-6 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 disabled:opacity-50"
            >
              {createDeal.isPending ? 'Creating...' : 'Create Deal'}
            </button>
          )}
        </div>
      </form>
    </div>
  );
};

