"use client";

type Odds = {
  win: number;
  tie: number;
  loss: number;
};

export default function OddsDisplay({ odds }: { odds: Odds | null }) {
  if (!odds) {
    return (
      <p className="mt-2 text-gray-400 text-center">
        Run a calculation to see odds
      </p>
    );
  }

  return (
    <div className="grid grid-cols-3 gap-4 mt-4">
      <div className="p-3 rounded-xl bg-green-700/60 shadow text-center">
        <p className="font-bold text-green-200">Win</p>
        <p className="text-2xl font-extrabold">{odds.win}%</p>
      </div>
      <div className="p-3 rounded-xl bg-blue-700/60 shadow text-center">
        <p className="font-bold text-blue-200">Tie</p>
        <p className="text-2xl font-extrabold">{odds.tie}%</p>
      </div>
      <div className="p-3 rounded-xl bg-red-700/60 shadow text-center">
        <p className="font-bold text-red-200">Loss</p>
        <p className="text-2xl font-extrabold">{odds.loss}%</p>
      </div>
    </div>
  );
}
