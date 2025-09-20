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
      className="flex flex-wrap gap-2 max-h-[200px] overflow-y-auto p-2 border rounded bg-gray-900"
    >
      {deck.map((c) => (
        <Card key={c} code={c} id={c} />
      ))}
    </div>
  );
}
