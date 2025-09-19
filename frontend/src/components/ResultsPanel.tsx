"use client";

import HandRankDisplay from "./HandRankDisplay";
import OddsDisplay from "./OddsDisplay";

type Odds = {
  win: number;
  tie: number;
  loss: number;
};

interface ResultsPanelProps {
  handRank?: string;
  odds: Odds | null;
}

export default function ResultsPanel({ handRank, odds }: ResultsPanelProps) {
  return (
    <div className="mt-6 p-6 border-2 border-yellow-400 rounded-2xl bg-gray-800/90 shadow-xl">
      <h2 className="text-2xl font-bold text-yellow-400 mb-4 text-center">
        Results
      </h2>
      <HandRankDisplay handRank={handRank} />
      <OddsDisplay odds={odds} />
    </div>
  );
}
