"use client";

import { useState, useEffect } from "react";
import {
  DndContext,
  DragEndEvent,
  DragOverlay,
  DragStartEvent,
} from "@dnd-kit/core";
import { createPortal } from "react-dom";

import api from "@/services/api";

import Card from "@/components/Card";
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

  const [activeCard, setActiveCard] = useState<string | null>(null);

  useEffect(() => {
    setDeck(suits.flatMap((s) => ranks.map((r) => r + s)));
  }, [suits, ranks]);

  const sortDeck = (deck: string[]) => {
    return deck.sort((a, b) => {
      const rankA = ranks.indexOf(a[0]);
      const rankB = ranks.indexOf(b[0]);
      const suitA = suits.indexOf(a[1]);
      const suitB = suits.indexOf(b[1]);
      return suitA - suitB || rankA - rankB;
    });
  };

  const handleDragStart = (event: DragStartEvent) => {
    setActiveCard(event.active.id.toString().replace("deck-", ""));
  };

  const handleDragEnd = (event: DragEndEvent) => {
    const { active, over } = event;
    setActiveCard(null);
    if (!over) return;

    const cardCode = active.id.toString().replace("deck-", "");

    const fromHole = holeCards.includes(cardCode);
    const fromBoard = boardCards.includes(cardCode);
    const fromDeck = deck.includes(cardCode);

    switch (over.id) {
      case "hole":
        if (holeCards.length < 2 && !fromHole) {
          setHoleCards((prev) => [...prev, cardCode]);
          if (fromBoard)
            setBoardCards((prev) => prev.filter((c) => c !== cardCode));
          if (fromDeck) setDeck((prev) => prev.filter((c) => c !== cardCode));
        }
        break;

      case "board":
        if (boardCards.length < 5 && !fromBoard) {
          setBoardCards((prev) => [...prev, cardCode]);
          if (fromHole)
            setHoleCards((prev) => prev.filter((c) => c !== cardCode));
          if (fromDeck) setDeck((prev) => prev.filter((c) => c !== cardCode));
        }
        break;

      case "deck":
        if (!fromDeck) {
          setDeck((prev) => sortDeck([...prev, cardCode]));
          if (fromHole)
            setHoleCards((prev) => prev.filter((c) => c !== cardCode));
          if (fromBoard)
            setBoardCards((prev) => prev.filter((c) => c !== cardCode));
        }
        break;

      default:
        break;
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
    <DndContext onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
      <div className="min-h-screen p-6 bg-green-900">
        <h1 className="mb-6 text-4xl font-extrabold text-yellow-400 text-center">
          Hold&apos;Em Analytics
        </h1>

        {/* Grid Layout */}
        <div className="grid grid-cols-2 grid-rows-[1fr_auto] gap-6 h-[80vh]">
          {/* Top Left: Droppable Areas */}
          <div className="p-4 rounded-lg bg-green-800/40">
            <div className="mb-4">
              <label htmlFor="num-opponents">Opponents:</label>
              <input
                id="num-opponents"
                type="number"
                min={1}
                max={9}
                value={numOpponents}
                onChange={(e) => setNumOpponents(Number(e.target.value))}
                className="p-2 rounded text-black"
              />
            </div>

            <h2 className="mb-2 text-white font-semibold">Hole Cards</h2>
            <DroppableArea id="hole" cards={holeCards} />

            <h2 className="mb-2 text-white font-semibold">Board Cards</h2>
            <DroppableArea id="board" cards={boardCards} />
          </div>

          {/* Top Right: Results Panel */}
          <div className="grid grid-rows-[1fr_auto] h-full p-4 rounded-lg bg-green-800/40">
            <ResultsPanel handRank={handRank} odds={odds} />

            <div className="flex gap-4 mt-6">
              <button
                onClick={evaluateHand}
                className="flex-1 px-4 py-2 bg-yellow-400 font-bold rounded hover:brightness-110"
              >
                Evaluate Hand
              </button>
              <button
                onClick={calculateOdds}
                className="flex-1 px-4 py-2 bg-yellow-400 font-bold rounded hover:brightness-110"
              >
                Calculate Odds
              </button>
            </div>
          </div>

          {/* Bottom: Deck */}
          <div className="col-span-2 p-4 rounded-lg bg-green-800/40">
            <h2 className="mb-2 text-white font-semibold">Deck</h2>
            <Deck deck={deck} />
          </div>
        </div>
      </div>

      {typeof window !== "undefined" &&
        createPortal(
          <DragOverlay>
            {activeCard ? (
              <Card code={activeCard} id={`overlay-${activeCard}`} size={80} />
            ) : null}
          </DragOverlay>,
          document.body,
        )}
    </DndContext>
  );
}
