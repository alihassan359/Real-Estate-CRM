/**
 * Projects Page - Real Estate Projects Management
 */


'use client';

import React, { useState } from 'react';
import { Plus } from 'lucide-react';

export default function ProjectsPage() {
  const [showForm, setShowForm] = useState(false);

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Projects</h1>
          <p className="text-gray-600 mt-1">Manage your real estate development projects</p>
        </div>
        <button
          onClick={() => setShowForm(!showForm)}
          className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition"
        >
          <Plus size={20} />
          New Project
        </button>
      </div>

      {showForm && (
        <div className="bg-white rounded-lg shadow-md p-8">
          <p className="text-gray-600">Project form coming soon...</p>
        </div>
      )}

      <div className="bg-white rounded-lg shadow-md p-8 text-center text-gray-500">
        <p>No projects yet. Create your first project to get started.</p>
      </div>
    </div>
  );
}

