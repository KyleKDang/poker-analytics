"use client";

import { useState, useEffect } from "react";
import { DndContext, DragEndEvent } from "@dnd-kit/core";
import api from "@/services/api";

import Deck from "@/components/Deck";
import DroppableArea from "@/components/DroppableArea";
import ResultsPanel from "@/components/ResultsPanel";

type Odds = {
  win: number;
  tie: number;
  loss: number;
};

const suits = ["S", "H", "D", "C"];
const ranks = ["2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K", "A"];

export default function HomePage() {
  const [deck, setDeck] = useState<string[]>([]);
  const [holeCards, setHoleCards] = useState<string[]>([]);
  const [boardCards, setBoardCards] = useState<string[]>([]);
  const [numOpponents, setNumOpponents] = useState<number>(1);
  const [handRank, setHandRank] = useState<string>();
  const [odds, setOdds] = useState<Odds | null>(null);

  useEffect(() => {
    setDeck(suits.flatMap((s) => ranks.map((r) => r + s)));
  }, [suits, ranks]);

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    if (!over) return;

    const cardCode = active.id.toString().replace("deck-", "");
    if (over.id === "hole" && holeCards.length < 2) {
      setHoleCards([...holeCards, cardCode]);
      setBoardCards(boardCards.filter((c) => c !== cardCode));
      setDeck(deck.filter((c) => c !== cardCode));
    } else if (over.id === "board" && boardCards.length < 5) {
      setBoardCards([...boardCards, cardCode]);
      setHoleCards(holeCards.filter((c) => c !== cardCode));
      setDeck(deck.filter((c) => c !== cardCode));
    }
  };

  const evaluateHand = async () => {
    try {
      const response = await api.post("/hands/evaluation", {
        hole_cards: holeCards,
        board_cards: boardCards,
      });
      setHandRank(response.data.hand);
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
          Hold&apos;Em Analytics
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

        <div className="flex gap-4 mt-6">
            <button
            onClick={evaluateHand}
            className="px-4 py-2 bg-yellow-400 font-bold hover:brightness-110"
            >
            Evaluate Hand
            </button>
            <button
            onClick={calculateOdds}
            className="px-4 py-2 bg-yellow-400 font-bold hover:brightness-110"
            >
            Calculate Odds
            </button>
        </div>

        <ResultsPanel handRank={handRank} odds={odds} />
      </div>
    </DndContext>
  );
}
