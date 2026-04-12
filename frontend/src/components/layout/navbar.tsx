"""
Navbar Component - Top Navigation Bar
"""

'use client';

import React from 'react';
import { Bell, User, Settings } from 'lucide-react';

export const Navbar: React.FC = () => {
  return (
    <div className="bg-white shadow-sm px-6 py-4 flex justify-between items-center">
      <div>
        <h2 className="text-lg font-semibold text-gray-800">Dashboard</h2>
      </div>

      {/* Right side - Actions */}
      <div className="flex items-center space-x-4">
        {/* Notifications */}
        <button className="relative p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition">
          <Bell size={20} />
          <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
        </button>

        {/* User menu */}
        <button className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition">
          <User size={20} />
        </button>

        {/* Settings */}
        <button className="p-2 text-gray-600 hover:bg-gray-100 rounded-lg transition">
          <Settings size={20} />
        </button>
      </div>
    </div>
  );
};
