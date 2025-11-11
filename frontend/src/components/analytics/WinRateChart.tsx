"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from "recharts";

interface WinRateChartProps {
  data: Array<{
    hand_number: number;
    date: string;
    win_rate: number;
    cumulative_wins: number;
    cumulative_hands: number;
  }>;
}

export default function WinRateChart({ data }: WinRateChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-400">
        No data available
      </div>
    );
  }

  // Sample data every N hands if too many points
  const sampledData =
    data.length > 100
      ? data.filter(
          (_, i) =>
            i % Math.ceil(data.length / 100) === 0 || i === data.length - 1,
        )
      : data;

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={sampledData}>
        <CartesianGrid strokeDasharray="3 3" stroke="#374151" />
        <XAxis
          dataKey="hand_number"
          stroke="#9CA3AF"
          label={{
            value: "Hands Played",
            position: "insideBottom",
            offset: -5,
            fill: "#9CA3AF",
          }}
        />
        <YAxis
          stroke="#9CA3AF"
          label={{
            value: "Win Rate (%)",
            angle: -90,
            position: "insideLeft",
            fill: "#9CA3AF",
          }}
          domain={[0, 100]}
        />
        <Tooltip
          contentStyle={{
            backgroundColor: "#1F2937",
            border: "1px solid #374151",
            borderRadius: "8px",
            color: "#F3F4F6",
          }}
          formatter={(value: number) => [`${value.toFixed(2)}%`, "Win Rate"]}
          labelFormatter={(label) => `Hand #${label}`}
        />
        <Line
          type="monotone"
          dataKey="win_rate"
          stroke="#FCD34D"
          strokeWidth={3}
          dot={false}
          activeDot={{ r: 6, fill: "#FCD34D" }}
        />
      </LineChart>
    </ResponsiveContainer>
  );
}
