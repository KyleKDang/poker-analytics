"use client";

interface StyleProfileProps {
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

export default function StyleProfile({ style }: StyleProfileProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
      {/* Style Rating */}
      <div className="bg-gray-800/50 p-6 rounded-lg border-2 border-yellow-400">
        <h3 className="text-xl font-bold text-yellow-400 mb-4">
          Your Playing Style
        </h3>
        <p className="text-3xl font-bold text-white mb-2">
          {style.style_rating}
        </p>
        <div className="space-y-2 mt-4">
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Tight/Loose:</span>
            <span className="text-white font-semibold">
              {style.tight_loose}
            </span>
          </div>
          <div className="flex justify-between text-sm">
            <span className="text-gray-400">Passive/Aggressive:</span>
            <span className="text-white font-semibold">
              {style.passive_aggressive}
            </span>
          </div>
        </div>
      </div>

      {/* Metrics */}
      <div className="grid grid-cols-2 gap-4">
        {/* VPIP */}
        <div className="bg-gray-800/50 p-4 rounded-lg">
          <p className="text-gray-400 text-sm mb-1">VPIP</p>
          <p className="text-2xl font-bold text-white">
            {style.vpip.toFixed(1)}%
          </p>
          <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-purple-500"
              style={{ width: `${Math.min(style.vpip, 100)}%` }}
            />
          </div>
        </div>

        {/* Aggression */}
        <div className="bg-gray-800/50 p-4 rounded-lg">
          <p className="text-gray-400 text-sm mb-1">Aggression</p>
          <p className="text-2xl font-bold text-white">
            {style.aggression_factor.toFixed(2)}
          </p>
          <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-orange-500"
              style={{
                width: `${Math.min(style.aggression_factor * 25, 100)}%`,
              }}
            />
          </div>
        </div>

        {/* Fold Frequency */}
        <div className="bg-gray-800/50 p-4 rounded-lg">
          <p className="text-gray-400 text-sm mb-1">Fold %</p>
          <p className="text-2xl font-bold text-white">
            {style.fold_frequency.toFixed(1)}%
          </p>
          <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-red-500"
              style={{ width: `${Math.min(style.fold_frequency, 100)}%` }}
            />
          </div>
        </div>

        {/* Raise Frequency */}
        <div className="bg-gray-800/50 p-4 rounded-lg">
          <p className="text-gray-400 text-sm mb-1">Raise %</p>
          <p className="text-2xl font-bold text-white">
            {style.raise_frequency.toFixed(1)}%
          </p>
          <div className="mt-2 h-2 bg-gray-700 rounded-full overflow-hidden">
            <div
              className="h-full bg-green-500"
              style={{ width: `${Math.min(style.raise_frequency, 100)}%` }}
            />
          </div>
        </div>
      </div>
    </div>
  );
}
