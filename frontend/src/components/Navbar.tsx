"use client";

import { useRouter, usePathname } from "next/navigation";
import Link from "next/link";
import { LogOut, User, BarChart3 } from "lucide-react";
import { useEffect, useState } from "react";

export default function Navbar() {
  const router = useRouter();
  const pathname = usePathname();
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  useEffect(() => {
    setIsLoggedIn(!!localStorage.getItem("token"));
  }, [pathname]);

  const handleLogout = () => {
    localStorage.removeItem("token");
    setIsLoggedIn(false);
    router.push("/login");
  };

  return (
    <nav className="bg-gray-800/90 backdrop-blur-lg border-b-2 border-yellow-400 sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-6 py-4">
        <div className="flex items-center justify-between">
          <Link href="/" className="flex items-center gap-2 group">
            <BarChart3 className="w-8 h-8 text-yellow-400" />
            <span className="text-2xl font-extrabold text-yellow-400 group-hover:brightness-110 transition-all">
              Hold&apos;Em Analytics
            </span>
          </Link>

          <div className="flex items-center gap-6">
            <Link
              href="/"
              className={`text-lg font-semibold transition-colors ${
                pathname === "/"
                  ? "text-yellow-400"
                  : "text-gray-300 hover:text-yellow-400"
              }`}
            >
              Analyzer
            </Link>

            {isLoggedIn && (
              <Link
                href="/sessions"
                className={`text-lg font-semibold transition-colors ${
                  pathname === "/sessions"
                    ? "text-yellow-400"
                    : "text-gray-300 hover:text-yellow-400"
                }`}
              >
                Sessions
              </Link>
            )}

            {isLoggedIn && (
              <Link
                href="/analytics"
                className={`text-lg font-semibold transition-colors ${
                  pathname === "/analytics"
                    ? "text-yellow-400"
                    : "text-gray-300 hover:text-yellow-400"
                }`}
              >
                Dashboard
              </Link>
            )}

            {isLoggedIn ? (
              <button
                onClick={handleLogout}
                className="flex items-center gap-2 px-4 py-2 bg-red-600 text-white font-semibold rounded-lg hover:brightness-110 transition-all"
              >
                <LogOut className="w-4 h-4" />
                Logout
              </button>
            ) : (
              <div className="flex items-center gap-3">
                <Link
                  href="/login"
                  className="px-4 py-2 text-white font-semibold rounded-lg hover:bg-gray-700/50 transition-all"
                >
                  Login
                </Link>
                <Link
                  href="/register"
                  className="flex items-center gap-2 px-4 py-2 bg-yellow-400 text-gray-900 font-semibold rounded-lg hover:brightness-110 transition-all"
                >
                  <User className="w-4 h-4" />
                  Sign Up
                </Link>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
