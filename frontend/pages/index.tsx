import Head from 'next/head'
import { useEffect, useState } from 'react'
import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api'

export default function Home() {
  const [apiStatus, setApiStatus] = useState<string>('checking...')
  const [apiVersion, setApiVersion] = useState<string>('')

  useEffect(() => {
    // Check API health
    checkApiHealth()
  }, [])

  const checkApiHealth = async () => {
    try {
      const response = await axios.get(`${API_URL}/health`)
      setApiStatus('Connected ✅')
      setApiVersion(response.data?.version || 'unknown')
    } catch (error) {
      setApiStatus('Disconnected ❌')
      console.error('API connection failed:', error)
    }
  }

  return (
    <>
      <Head>
        <title>Real Estate CRM System</title>
        <meta name="description" content="Real Estate CRM Platform" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link rel="icon" href="/favicon.ico" />
      </Head>

      <main className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
        {/* Header */}
        <header className="bg-white shadow-sm">
          <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
            <div className="flex justify-between items-center">
              <div className="flex items-center">
                <h1 className="text-2xl font-bold text-indigo-600">
                  🏢 Real Estate CRM
                </h1>
              </div>
              <div className="flex gap-4">
                <button className="px-4 py-2 text-indigo-600 hover:text-indigo-800 font-medium">
                  Dashboard
                </button>
                <button className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700">
                  Login
                </button>
              </div>
            </div>
          </nav>
        </header>

        {/* Main Content */}
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
          {/* Welcome Section */}
          <section className="bg-white rounded-lg shadow-lg p-8 mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Welcome to Real Estate CRM
            </h2>
            <p className="text-gray-600 text-lg mb-6">
              A modern, multi-tenant SaaS platform for managing real estate deals, clients, 
              and payments with advanced features and analytics.
            </p>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <button className="bg-indigo-600 text-white px-6 py-3 rounded-lg hover:bg-indigo-700 transition">
                Get Started
              </button>
              <button className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition">
                Learn More
              </button>
              <button className="bg-gray-200 text-gray-800 px-6 py-3 rounded-lg hover:bg-gray-300 transition">
                Contact Us
              </button>
            </div>
          </section>

          {/* Status Section */}
          <section className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-8">
            {/* API Status */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">🔌 Backend API</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Status</span>
                  <span className={`font-bold ${apiStatus.includes('Connected') ? 'text-green-600' : 'text-red-600'}`}>
                    {apiStatus}
                  </span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">URL</span>
                  <span className="text-gray-900 font-mono text-sm">{API_URL}</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Framework</span>
                  <span className="text-gray-900 font-bold">FastAPI 0.109.0</span>
                </div>
              </div>
            </div>

            {/* Frontend Status */}
            <div className="bg-white rounded-lg shadow-lg p-6">
              <h3 className="text-xl font-bold text-gray-900 mb-4">⚛️ Frontend</h3>
              <div className="space-y-3">
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Status</span>
                  <span className="font-bold text-green-600">Running ✅</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">Framework</span>
                  <span className="text-gray-900 font-bold">Next.js 14.1.0</span>
                </div>
                <div className="flex justify-between items-center">
                  <span className="text-gray-600">UI Framework</span>
                  <span className="text-gray-900 font-bold">Tailwind CSS</span>
                </div>
              </div>
            </div>
          </section>

          {/* Features Section */}
          <section className="bg-white rounded-lg shadow-lg p-8">
            <h2 className="text-2xl font-bold text-gray-900 mb-6">✨ Features</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                { icon: '👥', title: 'User Management', desc: 'Dashboard-based team member invitations' },
                { icon: '🏗️', title: 'Deal Management', desc: 'Track real estate deals and projects' },
                { icon: '💰', title: 'Payment Tracking', desc: 'Installment and ledger management' },
                { icon: '📊', title: 'Analytics', desc: 'Real-time dashboards and reports' },
                { icon: '📱', title: 'Mobile Ready', desc: 'Responsive design for all devices' },
                { icon: '🔒', title: 'Security', desc: 'Multi-tenant isolation with RBAC' },
              ].map((feature, i) => (
                <div key={i} className="border border-gray-200 rounded-lg p-4">
                  <div className="text-3xl mb-2">{feature.icon}</div>
                  <h3 className="font-bold text-gray-900">{feature.title}</h3>
                  <p className="text-gray-600 text-sm">{feature.desc}</p>
                </div>
              ))}
            </div>
          </section>
        </div>
      </main>
    </>
  )
}
