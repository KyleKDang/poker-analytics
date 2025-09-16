"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import api from "@/services/api";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError(null);

    try {
      const response = await api.post("/auth/login", { username, password });
      localStorage.setItem("token", response.data.access_token);
      router.push("/");
    } catch (err: any) {
      if (err.response?.data?.detail) {
        setError(err.response.data.detail);
      } else {
        setError("Login failed. Please try again.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-gray-900 via-green-950 to-gray-900">
      <form
        onSubmit={handleSubmit}
        className="bg-gray-800/90 backdrop-blur-lg shadow-2xl rounded-2xl p-10 w-full max-w-sm border-2 border-yellow-400"
      >
        <h1 className="text-4xl font-extrabold mb-6 text-center text-yellow-400 drop-shadow-lg whitespace-nowrap">
          Hold'em Analytics
        </h1>

        {error && (
          <div className="bg-red-700 text-white p-3 rounded mb-4 text-center font-semibold shadow-md">
            {error}
          </div>
        )}

        <div className="mb-4">
          <label htmlFor="username" className="block text-sm font-semibold mb-2">
            Username
          </label>
          <input
            id="username"
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="Enter your username"
            autoFocus
            className="w-full bg-gray-700/80 p-3 rounded-lg focus:ring-2 focus:ring-yellow-400"
            required
          />
        </div>

        <div className="mb-6">
          <label htmlFor="password" className="block text-sm font-semibold mb-2">
            Password
          </label>
          <input
            id="password"
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="Enter your password"
            className="w-full bg-gray-700/80 p-3 rounded-lg focus:ring-2 focus:ring-yellow-400"
            required
          />
        </div>

        <button
          type="submit"
          disabled={loading}
          className={`w-full py-3 rounded-xl bg-yellow-400 text-gray-900 font-bold text-lg hover:scale-105 hover:brightness-110 transition-transform duration-200 ${
            loading ? "opacity-50 cursor-not-allowed" : ""
          }`}
        >
          {loading ? "Logging in..." : "Login"}
        </button>
      </form>
    </div>
  );
}
