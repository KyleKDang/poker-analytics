"use client";

import {
  PieChart,
  Pie,
  Cell,
  ResponsiveContainer,
  Legend,
  Tooltip,
} from "recharts";

interface ActionChartProps {
  data: Array<{
    action: string;
    total_hands: number;
    wins: number;
    losses: number;
    ties: number;
    win_rate: number;
    distribution: number;
  }>;
}

const COLORS = {
  fold: "#EF4444", // Red
  check: "#3B82F6", // Blue
  call: "#F59E0B", // Orange
  raise: "#10B981", // Green
};

export default function ActionChart({ data }: ActionChartProps) {
  if (!data || data.length === 0) {
    return (
      <div className="h-64 flex items-center justify-center text-gray-400">
        No data available
      </div>
    );
  }

  const chartData = data.map((item) => ({
    name: item.action.charAt(0).toUpperCase() + item.action.slice(1),
    value: item.distribution,
    count: item.total_hands,
  }));

  return (
    <ResponsiveContainer width="100%" height={300}>
      <PieChart>
        <Pie
          data={chartData}
          cx="50%"
          cy="50%"
          labelLine={false}
          label={({ name, value }) => `${name}: ${value.toFixed(1)}%`}
          outerRadius={80}
          fill="#8884d8"
          dataKey="value"
        >
          {chartData.map((entry, index) => (
            <Cell
              key={`cell-${index}`}
              fill={
                COLORS[data[index].action as keyof typeof COLORS] || "#6B7280"
              }
            />
          ))}
        </Pie>
        <Tooltip
          contentStyle={{
            backgroundColor: "#1F2937",
            border: "1px solid #374151",
            borderRadius: "8px",
            color: "#F3F4F6",
          }}
          formatter={(value: number, name: string, props: any) => [
            `${value.toFixed(1)}% (${props.payload.count} hands)`,
            "Distribution",
          ]}
        />
        <Legend wrapperStyle={{ color: "#F3F4F6" }} iconType="circle" />
      </PieChart>
    </ResponsiveContainer>
  );
}
