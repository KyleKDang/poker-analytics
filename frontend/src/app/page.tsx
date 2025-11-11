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
import HandLoggerModal from "@/components/HandLoggerModal";

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
  const [showLogger, setShowLogger] = useState(false);
  const [showAuthMessage, setShowAuthMessage] = useState(false);
  const [isCalculating, setIsCalculating] = useState(false);

  useEffect(() => {
    setDeck(suits.flatMap((s) => ranks.map((r) => r + s)));
  }, []);

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
      const response = await api.post("/analytics/evaluate", {
        hole_cards: holeCards,
        board_cards: boardCards,
      });
      setHandRank(response.data.hand);
    } catch (err) {
      console.log(err);
    }
  };

  const calculateOdds = async () => {
    setIsCalculating(true);
    try {
      const response = await api.post("/analytics/odds", {
        hole_cards: holeCards,
        board_cards: boardCards,
        num_opponents: numOpponents,
      });
      setOdds(response.data);
    } catch (err) {
      console.log(err);
    } finally {
      setIsCalculating(false);
    }
  };

  const handleLogHand = () => {
    const token = localStorage.getItem("token");
    if (!token) {
      if (!showAuthMessage) {
        setShowAuthMessage(true);
        setTimeout(() => setShowAuthMessage(false), 3000);
      }
      return;
    }
    setShowLogger(true);
  };

  return (
    <DndContext onDragStart={handleDragStart} onDragEnd={handleDragEnd}>
      <div className="flex items-center h-[calc(100vh-73px)] p-6 bg-green-900">
        {/* Grid Layout */}
        <div className="grid grid-cols-2 grid-rows-[1fr_auto] gap-6 h-[80vh]">
          {/* Top Left: Droppable Areas */}
          <div className="p-4 rounded-lg bg-green-800/40">
            <div className="mb-4">
              <label
                htmlFor="num-opponents"
                className="block text-white font-semibold mb-2"
              >
                Number of Opponents:{" "}
                <span className="text-yellow-400 text-xl">{numOpponents}</span>
              </label>
              <input
                id="num-opponents"
                type="range"
                min={1}
                max={9}
                value={numOpponents}
                onChange={(e) => setNumOpponents(Number(e.target.value))}
                className="w-full h-2 bg-gray-700 rounded-lg appearance-none cursor-pointer accent-yellow-400"
              />
            </div>

            <h2 className="mb-2 text-white font-semibold">Hole Cards</h2>
            <DroppableArea id="hole" cards={holeCards} />

            <h2 className="mb-2 text-white font-semibold">Board Cards</h2>
            <DroppableArea id="board" cards={boardCards} />
          </div>

          {/* Top Right: Results Panel */}
          <div className="grid grid-rows-[1fr_auto] h-full p-4 rounded-lg bg-green-800/40">
            <ResultsPanel
              handRank={handRank}
              odds={odds}
              isCalculating={isCalculating}
            />

            <div className="flex gap-4 mt-6">
              <button
                onClick={evaluateHand}
                className="flex-1 px-4 py-2 bg-gradient-to-br from-yellow-300 to-yellow-400 text-gray-900 font-bold rounded-lg hover:from-yellow-200 hover:to-yellow-300 transition-all shadow-lg hover:shadow-yellow-400/50 hover:scale-[1.02]"
              >
                Evaluate Hand
              </button>
              <button
                onClick={calculateOdds}
                disabled={isCalculating}
                className="flex-1 px-4 py-2 bg-gradient-to-br from-yellow-300 to-yellow-400 text-gray-900 font-bold rounded-lg hover:from-yellow-200 hover:to-yellow-300 transition-all shadow-lg hover:shadow-yellow-400/50 hover:scale-[1.02]"
              >
                {isCalculating ? "Calculating..." : "Calculate Odds"}
              </button>
              <button
                onClick={handleLogHand}
                disabled={holeCards.length !== 2 || boardCards.length < 3}
                className="flex-1 px-4 py-2 bg-gradient-to-br from-yellow-300 to-yellow-400 text-gray-900 font-bold rounded-lg hover:from-yellow-200 hover:to-yellow-300 disabled:opacity-50 disabled:cursor-not-allowed transition-all shadow-lg hover:shadow-yellow-400/50 hover:scale-[1.02]"
              >
                Log Hand
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

      {showAuthMessage && (
        <div className="fixed bottom-4 right-4 bg-red-600 text-white px-6 py-3 rounded-lg shadow-lg z-50">
          Please log in to save hands
        </div>
      )}

      <HandLoggerModal
        isOpen={showLogger}
        onClose={() => setShowLogger(false)}
        holeCards={holeCards}
        boardCards={boardCards}
      />

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
