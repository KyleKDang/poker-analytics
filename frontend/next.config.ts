import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://98.93.1.240:8000/:path*/',
      },
    ];
  },
};

export default nextConfig;