"use client";

import { TrendingUp, Target, Activity, Zap } from "lucide-react";

interface StatsCardsProps {
  stats: {
    total_hands: number;
    win_rate: number;
    wins: number;
    losses: number;
    ties: number;
    total_sessions: number;
    vpip: number;
    aggression_factor: number;
  };
}

export default function StatsCards({ stats }: StatsCardsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
      {/* Win Rate Card */}
      <div className="bg-gradient-to-br from-green-600 to-green-700 p-6 rounded-lg shadow-lg">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-white font-semibold">Win Rate</h3>
          <TrendingUp className="w-6 h-6 text-green-200" />
        </div>
        <p className="text-4xl font-bold text-white">
          {stats.win_rate.toFixed(1)}%
        </p>
        <p className="text-green-200 text-sm mt-2">
          {stats.wins}W - {stats.losses}L - {stats.ties}T
        </p>
      </div>

      {/* Total Hands Card */}
      <div className="bg-gradient-to-br from-blue-600 to-blue-700 p-6 rounded-lg shadow-lg">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-white font-semibold">Hands Played</h3>
          <Target className="w-6 h-6 text-blue-200" />
        </div>
        <p className="text-4xl font-bold text-white">{stats.total_hands}</p>
        <p className="text-blue-200 text-sm mt-2">
          Across {stats.total_sessions} sessions
        </p>
      </div>

      {/* VPIP Card */}
      <div className="bg-gradient-to-br from-purple-600 to-purple-700 p-6 rounded-lg shadow-lg">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-white font-semibold">VPIP</h3>
          <Activity className="w-6 h-6 text-purple-200" />
        </div>
        <p className="text-4xl font-bold text-white">
          {stats.vpip.toFixed(1)}%
        </p>
        <p className="text-purple-200 text-sm mt-2">
          {stats.vpip < 20 ? "Tight" : stats.vpip < 35 ? "Balanced" : "Loose"}
        </p>
      </div>

      {/* Aggression Card */}
      <div className="bg-gradient-to-br from-orange-600 to-orange-700 p-6 rounded-lg shadow-lg">
        <div className="flex items-center justify-between mb-2">
          <h3 className="text-white font-semibold">Aggression</h3>
          <Zap className="w-6 h-6 text-orange-200" />
        </div>
        <p className="text-4xl font-bold text-white">
          {stats.aggression_factor.toFixed(2)}
        </p>
        <p className="text-orange-200 text-sm mt-2">
          {stats.aggression_factor < 1
            ? "Passive"
            : stats.aggression_factor < 2
              ? "Balanced"
              : "Aggressive"}
        </p>
      </div>
    </div>
  );
}
