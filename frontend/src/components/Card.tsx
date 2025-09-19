"use client";

import Image from "next/image";
import { useDraggable } from "@dnd-kit/core";

interface CardProps {
  code: string;
  size?: number;
  id: string;
}

export default function Card({ code, size = 80, id }: CardProps) {
  const { attributes, listeners, setNodeRef, transform, isDragging } =
    useDraggable({ id });

  const style = {
    transform: transform
      ? `translate3d(${transform.x}px, ${transform.y}px, 0)`
      : undefined,
    opacity: isDragging ? 0.5 : 1,
    zIndex: isDragging ? 999 : undefined,
  };
  return (
    <div ref={setNodeRef} style={style} {...listeners} {...attributes}>
      <Image
        src={`/cards/${code}.png`}
        alt={code}
        width={size}
        height={size * 1.4}
        className="rounded shadow cursor-grab"
      />
    </div>
  );
}
