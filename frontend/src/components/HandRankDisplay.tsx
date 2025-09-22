"use client";

export default function HandRankDisplay({ handRank }: { handRank?: string }) {
  return (
    <div className="mb-4 text-center">
      <p className="text-lg">
        <strong>Hand Rank:</strong>{" "}
        {handRank ? (
          <span className="font-semibold">{handRank}</span>
        ) : (
          <span className="text-gray-400">N/A</span>
        )}
      </p>
    </div>
  );
}
