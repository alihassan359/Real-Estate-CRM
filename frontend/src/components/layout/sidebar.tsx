"""
Sidebar Component - Navigation Sidebar
"""

'use client';

import React from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { 
  BarChart3, 
  Users, 
  FileText, 
  DollarSign, 
  Settings,
  Building2,
  LogOut 
} from 'lucide-react';
import { useAuth } from '@/hooks/useAuth';
import { useAuthStore } from '@/store/authStore';

export const Sidebar: React.FC = () => {
  const pathname = usePathname();
  const { logout } = useAuth();
  const { user } = useAuthStore();

  const menuItems = [
    { href: '/dashboard', label: 'Dashboard', icon: BarChart3 },
    { href: '/dashboard/projects', label: 'Projects', icon: Building2 },
    { href: '/dashboard/clients', label: 'Clients', icon: Users },
    { href: '/dashboard/deals', label: 'Deals', icon: FileText },
    { href: '/dashboard/payments', label: 'Payments', icon: DollarSign },
    { href: '/dashboard/settings', label: 'Settings', icon: Settings },
  ];

  return (
    <div className="w-64 bg-white shadow-lg flex flex-col">
      {/* Logo */}
      <div className="p-6 border-b">
        <h1 className="text-2xl font-bold text-blue-600">RealEstate</h1>
      </div>

      {/* Navigation */}
      <nav className="flex-1 p-4">
        <ul className="space-y-2">
          {menuItems.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <li key={item.href}>
                <Link
                  href={item.href}
                  className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                    isActive
                      ? 'bg-blue-100 text-blue-600'
                      : 'text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  <Icon size={20} />
                  <span>{item.label}</span>
                </Link>
              </li>
            );
          })}
        </ul>
      </nav>

      {/* User Info & Logout */}
      <div className="p-4 border-t">
        <div className="mb-4">
          <p className="text-sm text-gray-600">Logged in as:</p>
          <p className="font-semibold text-gray-800">{user?.firstName} {user?.lastName}</p>
        </div>
        <button
          onClick={() => logout()}
          className="flex items-center space-x-2 w-full px-4 py-2 text-red-600 hover:bg-red-50 rounded-lg transition-colors"
        >
          <LogOut size={20} />
          <span>Logout</span>
        </button>
      </div>
    </div>
  );
};
