"use client";

import { useDroppable } from "@dnd-kit/core";
import Card from "./Card";

interface DroppableAreaProps {
  id: string;
  cards: string[];
  onCardDrop: (cardCode: string) => void;
  maxCards: number;
}

export default function DroppableArea({
  id,
  cards,
  onCardDrop,
  maxCards,
}: DroppableAreaProps) {
  const { setNodeRef } = useDroppable({ id });

  return (
    <div
      ref={setNodeRef}
      className="flex min-h-[100px] space-x-2 p-2 border-2 border-dashed rounded bg-gray-800"
    >
      {cards.map((c, i) => (
        <Card key={i} code={c} id={`${id}-${c}`} />
      ))}
      {cards.length === 0 && (
        <span className="text-gray-400">Drop cards here</span>
      )}
    </div>
  );
}
