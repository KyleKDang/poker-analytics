"use client";

import Card from "./Card";

interface DeckProps {
  deck: string[];
}

export default function Deck({ deck }: DeckProps) {
  return (
    <div className="flex flex-wrap gap-2 max-h-[200px] overflow-y-auto p-2 border rounded bg-gray-900">
      {deck.map((c) => (
        <Card key={c} code={c} id={`deck-${c}`} />
      ))}
    </div>
  );
}
