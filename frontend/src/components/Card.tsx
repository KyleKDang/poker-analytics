"use client";

import Image from "next/image";
import { useDraggable } from "@dnd-kit/core";

interface CardProps {
  code: string;
  size?: number;
  id: string;
}

export default function Card({ code, size = 60, id }: CardProps) {
  const { attributes, listeners, setNodeRef, transform, isDragging } =
    useDraggable({ id });

  const style = {
    transform: transform
      ? `translate3d(${transform.x}px, ${transform.y}px, 0)`
      : "translate3d(0,0,0)",
    opacity: isDragging ? 0.5 : 1,
  };
  return (
    <div
      ref={setNodeRef}
      style={style}
      {...listeners}
      {...attributes}
      className="inline-flex items-center justify-center p-1 bg-white rounded shadow cursor-grab"
    >
      <Image
        src={`/cards/${code}.png`}
        alt={code}
        width={200}
        height={300}
        style={{ width: `${size}px`, height: "auto" }}
      />
    </div>
  );
}
