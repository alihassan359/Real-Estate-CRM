/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,
  swcMinify: process.env.NODE_ENV === 'production',
  productionBrowserSourceMaps: false,
  env: {
    NEXT_PUBLIC_API_URL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api',
  },
  images: {
    unoptimized: true,
    domains: ['localhost'],
  },
  compress: process.env.NODE_ENV === 'production',
  poweredByHeader: false,
  // Fast Refresh in development
  onDemandEntries: {
    maxInactiveAge: 15 * 1000, // 15 seconds
    pagesBufferLength: 2,
  },
  // Optimization for low-budget systems
  experimental: {
    cacheMaxMemorySize: 10 * 1024 * 1024, // 10MB cache
  },
  // Webpack optimization for minimal bundle
  webpack: (config, { isServer }) => {
    if (!isServer) {
      config.optimization = {
        ...config.optimization,
        splitChunks: {
          chunks: 'all',
          cacheGroups: {
            default: false,
            vendors: false,
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: 'vendor',
              chunks: 'all',
              priority: 10,
            },
          },
        },
      };
    }
    return config;
  },
}

module.exports = nextConfig
