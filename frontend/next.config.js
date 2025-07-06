/** @type {import('next').NextConfig} */
const nextConfig = {
  // Enable hot reloading in Docker
  webpack: (config, { dev }) => {
    if (dev) {
      config.watchOptions = {
        poll: 1000,
        aggregateTimeout: 300,
      };
    }
    return config;
  },
  // Modern configuration for Next.js 15+
  serverExternalPackages: [],
};

module.exports = nextConfig;
