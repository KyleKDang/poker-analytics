"use client";

import { useState } from "react";
import { DndContext, DragEndEvent } from "@dnd-kit/core";
import api from "@/services/api";

import Deck from "@/components/Deck";
import DroppableArea from "@/components/DroppableArea";

type Odds = {
  win: number;
  tie: number;
  loss: number;
};

export default function HomePage() {
  const suits = ["C", "D", "H", "S"];
  const ranks = [
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "T",
    "J",
    "Q",
    "K",
    "A",
  ];

  const [deck, setDeck] = useState<string[]>(
    suits.flatMap((s) => ranks.map((r) => r + s)),
  );
  const [holeCards, setHoleCards] = useState<string[]>([]);
  const [boardCards, setBoardCards] = useState<string[]>([]);
  const [numOpponents, setNumOpponents] = useState<number>(1);
  const [hand, setHand] = useState<string>();
  const [odds, setOdds] = useState<Odds | null>(null);

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over) return;

    const cardCode = active.id.toString().replace("deck-", "");
    if (!deck.includes(cardCode)) return;

    if (over.id === "hole" && holeCards.length < 2) {
      setHoleCards([...holeCards, cardCode]);
      setDeck(deck.filter((c) => c !== cardCode));
    } else if (over.id === "board" && boardCards.length < 5) {
      setBoardCards([...boardCards, cardCode]);
      setDeck(deck.filter((c) => c !== cardCode));
    }
  };

  const evaluateHand = async () => {
    try {
      const response = await api.post("/hands/evaluation", {
        hole_cards: holeCards,
        board_cards: boardCards,
      });
      setHand(response.data.hand);
    } catch (err) {
      console.log(err);
    }
  };

  const calculateOdds = async () => {
    try {
      const response = await api.post("/hands/odds", {
        hole_cards: holeCards,
        board_cards: boardCards,
        num_opponents: numOpponents,
      });
      setOdds(response.data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <DndContext onDragEnd={handleDragEnd}>
      <div className="min-h-screen p-6 bg-green-900">
        <h1 className="mb-6 text-4xl font-extrabold text-yellow-400 text-center">
          Hold'Em Analytics
        </h1>

        <div className="mb-4">
          <label>Opponents:</label>
          <input
            type="number"
            min={1}
            max={9}
            value={numOpponents}
            onChange={(e) => setNumOpponents(Number(e.target.value))}
            className="p-2 rounded text-black"
          />
        </div>

        <h2 className="mb-2 text-white font-semibold">Hole Cards</h2>
        <DroppableArea
          id="hole"
          cards={holeCards}
          onCardDrop={() => {}}
          maxCards={2}
        />

        <h2 className="mb-2 text-white font-semibold">Board Cards</h2>
        <DroppableArea
          id="board"
          cards={boardCards}
          onCardDrop={() => {}}
          maxCards={5}
        />

        <h2 className="mb-2 text-white font-semibold">Deck</h2>
        <Deck deck={deck} />
      </div>
    </DndContext>
  );
}
