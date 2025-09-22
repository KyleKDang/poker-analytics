"use client";

type Odds = {
  win: number;
  tie: number;
  loss: number;
};

export default function OddsDisplay({ odds }: { odds: Odds | null }) {
  return (
    <div className="grid grid-cols-3 w-full gap-4 mt-4">
      <div className="flex flex-col gap-2 justify-center p-3 rounded-xl bg-green-700/60 shadow text-center">
        <p className="font-bold text-green-200">Win</p>
        <p className="text-2xl font-extrabold">
          {odds ? (odds.win * 100).toFixed(2) : 0.0}%
        </p>
      </div>
      <div className="flex flex-col gap-2 justify-center p-3 rounded-xl bg-blue-700/60 shadow text-center">
        <p className="font-bold text-blue-200">Tie</p>
        <p className="text-2xl font-extrabold">
          {odds ? (odds.tie * 100).toFixed(2) : 0.0}%
        </p>
      </div>
      <div className="flex flex-col gap-2 justify-center p-3 rounded-xl bg-red-700/60 shadow text-center">
        <p className="font-bold text-red-200">Loss</p>
        <p className="text-2xl font-extrabold">
          {odds ? (odds.loss * 100).toFixed(2) : 0.0}%
        </p>
      </div>
    </div>
  );
}
