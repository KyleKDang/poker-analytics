"use client";

import { useState, useEffect } from "react";
import api from "@/services/api";
import { Loader2 } from "lucide-react";
import WinRateChart from "@/components/analytics/WinRateChart";
import PositionChart from "@/components/analytics/PositionChart";
import ActionChart from "@/components/analytics/ActionChart";
import SessionTable from "@/components/analytics/SessionTable";
import StatsCards from "@/components/analytics/StatsCards";
import StyleProfile from "@/components/analytics/StyleProfile";

interface DashboardData {
  overall: {
    total_hands: number;
    win_rate: number;
    wins: number;
    losses: number;
    ties: number;
    total_sessions: number;
    vpip: number;
    aggression_factor: number;
  };
  positions: {
    positions: Array<{
      position: string;
      total_hands: number;
      wins: number;
      losses: number;
      ties: number;
      win_rate: number;
    }>;
  };
  actions: {
    actions: Array<{
      action: string;
      total_hands: number;
      wins: number;
      losses: number;
      ties: number;
      win_rate: number;
      distribution: number;
    }>;
  };
  timeline: {
    timeline: Array<{
      hand_number: number;
      date: string;
      win_rate: number;
      cumulative_wins: number;
      cumulative_hands: number;
    }>;
  };
  style: {
    vpip: number;
    aggression_factor: number;
    fold_frequency: number;
    raise_frequency: number;
    tight_loose: string;
    passive_aggressive: string;
    style_rating: string;
  };
}

export default function AnalyticsPage() {
  const [loading, setLoading] = useState(true);
  const [dashboardData, setDashboardData] = useState<DashboardData | null>(
    null,
  );

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      const response = await api.get("/analytics/dashboard");
      setDashboardData(response.data);
    } catch (error) {
      console.error("Error fetching dashboard data:", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen p-6 bg-green-900 flex items-center justify-center">
        <Loader2 className="w-12 h-12 text-yellow-400 animate-spin" />
      </div>
    );
  }

  if (!dashboardData || dashboardData.overall.total_hands === 0) {
    return (
      <div className="min-h-screen p-6 bg-green-900">
        <div className="max-w-6xl mx-auto">
          <div className="bg-green-800/40 p-8 rounded-lg text-center">
            <p className="text-white text-xl mb-4">
              No hand data available yet
            </p>
            <p className="text-gray-400">
              Start logging hands to see your analytics and insights!
            </p>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 bg-green-900">
      <div className="max-w-7xl mx-auto space-y-6">
        {/* Stats Cards */}
        <StatsCards stats={dashboardData.overall} />

        {/* Win Rate Over Time */}
        <div className="bg-green-800/40 p-6 rounded-lg">
          <h2 className="text-2xl font-bold text-white mb-4">
            Win Rate Over Time
          </h2>
          <WinRateChart data={dashboardData.timeline.timeline} />
        </div>

        {/* Position and Action Charts */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-green-800/40 p-6 rounded-lg">
            <h2 className="text-2xl font-bold text-white mb-4">
              Win Rate by Position
            </h2>
            <PositionChart data={dashboardData.positions.positions} />
          </div>

          <div className="bg-green-800/40 p-6 rounded-lg">
            <h2 className="text-2xl font-bold text-white mb-4">
              Action Distribution
            </h2>
            <ActionChart data={dashboardData.actions.actions} />
          </div>
        </div>

        {/* Playing Style Profile */}
        <div className="bg-green-800/40 p-6 rounded-lg">
          <h2 className="text-2xl font-bold text-white mb-4">
            Playing Style Profile
          </h2>
          <StyleProfile style={dashboardData.style} />
        </div>

        {/* Session Performance Table */}
        <div className="bg-green-800/40 p-6 rounded-lg">
          <h2 className="text-2xl font-bold text-white mb-4">
            Recent Sessions
          </h2>
          <SessionTable />
        </div>
      </div>
    </div>
  );
}
