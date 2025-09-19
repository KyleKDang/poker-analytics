"use client";

export default function HandRankDisplay({ handRank }: { handRank?: string }) {
  return (
    <div className="mb-4 text-center">
      <p>
        <strong>Hand Rank:</strong> {handRank ? <span>{handRank}</span> : "N/A"}
      </p>
    </div>
  );
}
