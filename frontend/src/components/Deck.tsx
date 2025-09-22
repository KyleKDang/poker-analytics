"use client";

import { useDroppable } from "@dnd-kit/core";
import Card from "./Card";

interface DeckProps {
  deck: string[];
}

export default function Deck({ deck }: DeckProps) {
  const { setNodeRef } = useDroppable({ id: "deck" });

  return (
    <div
      ref={setNodeRef}
      className="flex gap-2 max-h-[200px] overflow-x-auto p-4 border rounded bg-gray-900"
    >
      {deck.map((c) => (
        <div key={c} className="flex-shrink-0">
          <Card code={c} id={c} />
        </div>
      ))}
    </div>
  );
}
