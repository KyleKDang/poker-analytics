"use client";

import { Loader2 } from "lucide-react";

type Odds = {
  win: number;
  tie: number;
  loss: number;
};

export default function OddsDisplay({
  odds,
  isCalculating,
}: {
  odds: Odds | null;
  isCalculating: boolean;
}) {
  return (
    <div className="grid grid-cols-3 w-full gap-4 mt-4">
      <div className="flex flex-col gap-2 justify-center p-3 rounded-xl bg-green-700/60 shadow text-center">
        <p className="font-bold text-green-200">Win</p>
        <div className="text-2xl font-extrabold flex items-center justify-center h-8">
          {isCalculating ? (
            <Loader2 className="w-8 h-8 animate-spin" />
          ) : (
            <span>{odds ? (odds.win * 100).toFixed(2) : "0.00"}%</span>
          )}
        </div>
      </div>
      <div className="flex flex-col gap-2 justify-center p-3 rounded-xl bg-blue-700/60 shadow text-center">
        <p className="font-bold text-blue-200">Tie</p>
        <div className="text-2xl font-extrabold flex items-center justify-center h-8">
          {isCalculating ? (
            <Loader2 className="w-8 h-8 animate-spin" />
          ) : (
            <span>{odds ? (odds.tie * 100).toFixed(2) : "0.00"}%</span>
          )}
        </div>
      </div>
      <div className="flex flex-col gap-2 justify-center p-3 rounded-xl bg-red-700/60 shadow text-center">
        <p className="font-bold text-red-200">Loss</p>
        <div className="text-2xl font-extrabold flex items-center justify-center h-8">
          {isCalculating ? (
            <Loader2 className="w-8 h-8 animate-spin" />
          ) : (
            <span>{odds ? (odds.loss * 100).toFixed(2) : "0.00"}%</span>
          )}
        </div>
      </div>
    </div>
  );
}
