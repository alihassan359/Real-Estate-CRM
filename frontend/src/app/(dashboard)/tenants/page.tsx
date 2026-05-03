'use client';

import { useEffect, useState } from 'react';
import { useTenantStore } from '@/store/tenantStore';
import { TenantService, TenantResponse } from '@/services/tenant.service';

export default function TenantsPage() {
  const setTenants = useTenantStore((state) => state.setTenants);
  const [tenants, setLocalTenants] = useState<TenantResponse[]>([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({ company_name: '', subscription_plan: 'BASIC' });

  useEffect(() => {
    loadTenants();
  }, []);

  const loadTenants = async () => {
    try {
      setLoading(true);
      const data = await TenantService.getTenants();
      setLocalTenants(data);
      setTenants(
        data.map((t) => ({
          id: String(t.id),
          name: t.company_name,
          slug: t.tenant_code,
          logo: t.logo_url || '',
          plan: t.subscription_plan.toLowerCase() as any,
        }))
      );
    } catch (error) {
      console.error('Failed to load tenants:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      await TenantService.createTenant(formData);
      setFormData({ company_name: '', subscription_plan: 'BASIC' });
      setShowForm(false);
      loadTenants();
    } catch (error) {
      console.error('Failed to create tenant:', error);
    }
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <h1 className="text-3xl font-bold text-gray-900">Tenants Management</h1>
        <button
          onClick={() => setShowForm(!showForm)}
          className="px-4 py-2 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition"
        >
          {showForm ? 'Cancel' : 'New Tenant'}
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow p-6">
          <form onSubmit={handleCreate} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Company Name</label>
              <input
                type="text"
                required
                value={formData.company_name}
                onChange={(e) => setFormData({ ...formData, company_name: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Plan</label>
              <select
                value={formData.subscription_plan}
                onChange={(e) => setFormData({ ...formData, subscription_plan: e.target.value })}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option>FREE</option>
                <option>BASIC</option>
                <option>PRO</option>
                <option>ENTERPRISE</option>
              </select>
            </div>
            <button
              type="submit"
              className="w-full px-4 py-2 bg-green-600 hover:bg-green-700 text-white rounded-lg transition"
            >
              Create Tenant
            </button>
          </form>
        </div>
      )}

      {loading ? (
        <div className="text-center py-8">Loading...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {tenants.map((tenant) => (
            <div key={tenant.id} className="bg-white rounded-lg shadow p-6">
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-bold text-lg text-gray-900">{tenant.company_name}</h3>
                  <p className="text-xs text-gray-500">Code: {tenant.tenant_code}</p>
                </div>
                <span
                  className={`px-3 py-1 rounded-full text-xs font-semibold ${
                    tenant.status === 'ACTIVE'
                      ? 'bg-green-100 text-green-800'
                      : 'bg-red-100 text-red-800'
                  }`}
                >
                  {tenant.status}
                </span>
              </div>
              <div className="space-y-2 text-sm text-gray-600">
                <p>📋 Plan: {tenant.subscription_plan}</p>
                {tenant.company_email && <p>📧 {tenant.company_email}</p>}
                {tenant.phone && <p>📱 {tenant.phone}</p>}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
