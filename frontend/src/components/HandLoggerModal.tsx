"use client";

import { useState, useEffect, useCallback } from "react";
import { Save, X } from "lucide-react";
import api from "@/services/api";

interface HandLoggerModalProps {
  isOpen: boolean;
  onClose: () => void;
  holeCards: string[];
  boardCards: string[];
}

interface Session {
  id: number;
  notes: string | null;
  start_time: string;
  hand_count: number;
}

const POSITIONS = ["early", "middle", "late"];
const ACTIONS = ["fold", "call", "raise", "check"];
const RESULTS = ["win", "loss", "tie"];

export default function HandLoggerModal({
  isOpen,
  onClose,
  holeCards,
  boardCards,
}: HandLoggerModalProps) {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [selectedSession, setSelectedSession] = useState("");
  const [position, setPosition] = useState("middle");
  const [action, setAction] = useState("call");
  const [result, setResult] = useState("win");
  const [isLoading, setIsLoading] = useState(false);

  useEffect(() => {
    if (!isOpen) return;

    const fetchSessions = async () => {
      try {
        const response = await api.get("/sessions");
        setSessions(response.data);
        if (response.data.length > 0 && !selectedSession) {
          setSelectedSession(response.data[0].id.toString());
        }
      } catch (err) {
        console.error("Error fetching sessions:", err);
      }
    };

    fetchSessions();
  }, [isOpen, selectedSession]);

  const handleSave = async () => {
    if (!selectedSession) {
      alert("Please select a session");
      return;
    }

    if (holeCards.length !== 2) {
      alert("Please select exactly 2 hole cards");
      return;
    }

    if (boardCards.length < 3 || boardCards.length > 5) {
      alert("Board must have 3-5 cards");
      return;
    }

    setIsLoading(true);

    try {
      await api.post("/hands", {
        session_id: parseInt(selectedSession),
        hole_cards: holeCards,
        board_cards: boardCards,
        player_position: position,
        action_taken: action,
        result: result,
      });
      onClose();
    } catch (error) {
      console.error("Error saving hand:", error);
      let errorMessage = "Unknown error";
      if (error instanceof Error) {
        errorMessage = error.message;
      }
      if (typeof error === "object" && error !== null && "response" in error) {
        const axiosError = error as {
          response?: { data?: { detail?: string } };
        };
        const apiError = axiosError.response?.data?.detail;
        if (apiError) {
          errorMessage = apiError;
        }
      }
      alert("Error saving hand: " + errorMessage);
    } finally {
      setIsLoading(false);
    }
  };

  if (!isOpen) return null;

  return (
    <div
      className="fixed inset-0 bg-black/70 flex items-center justify-center z-50"
      onClick={onClose}
    >
      <div
        className="bg-gray-800/95 backdrop-blur-lg border-2 border-yellow-400 p-6 rounded-2xl max-w-md w-full max-h-[90vh] overflow-y-auto shadow-2xl"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-bold text-yellow-400">Log Hand</h2>
          <button
            onClick={onClose}
            className="p-2 hover:bg-gray-700 rounded transition-colors"
          >
            <X className="w-6 h-6 text-white" />
          </button>
        </div>

        <div className="space-y-4">
          {/* Session Selection */}
          <div>
            <label className="block text-white font-semibold mb-2">
              Session
            </label>
            {sessions.length === 0 ? (
              <p className="text-gray-400 text-sm">
                No sessions found. Create one in the Sessions page first.
              </p>
            ) : (
              <select
                value={selectedSession}
                onChange={(e) => setSelectedSession(e.target.value)}
                className="w-full p-3 rounded-lg bg-gray-700/80 text-white focus:ring-2 focus:ring-yellow-400"
              >
                {sessions.map((session) => (
                  <option key={session.id} value={session.id}>
                    {session.notes || "Unnamed Session"} -{" "}
                    {new Date(session.start_time).toLocaleDateString()}
                  </option>
                ))}
              </select>
            )}
          </div>

          {/* Position Selection */}
          <div>
            <label className="block text-white font-semibold mb-2">
              Position
            </label>
            <div className="grid grid-cols-3 gap-2">
              {POSITIONS.map((pos) => (
                <button
                  key={pos}
                  onClick={() => setPosition(pos)}
                  className={`py-2 rounded-lg font-semibold transition-colors ${
                    position === pos
                      ? "bg-yellow-400 text-gray-900"
                      : "bg-gray-700 text-white hover:bg-gray-600"
                  }`}
                >
                  {pos.charAt(0).toUpperCase() + pos.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Action Selection */}
          <div>
            <label className="block text-white font-semibold mb-2">
              Your Action
            </label>
            <div className="grid grid-cols-4 gap-2">
              {ACTIONS.map((a) => (
                <button
                  key={a}
                  onClick={() => setAction(a)}
                  className={`py-2 rounded-lg font-semibold transition-colors ${
                    action === a
                      ? "bg-yellow-400 text-gray-900"
                      : "bg-gray-700 text-white hover:bg-gray-600"
                  }`}
                >
                  {a.charAt(0).toUpperCase() + a.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Result Selection */}
          <div>
            <label className="block text-white font-semibold mb-2">
              Result
            </label>
            <div className="flex gap-2">
              {RESULTS.map((r) => (
                <button
                  key={r}
                  onClick={() => setResult(r)}
                  className={`flex-1 py-2 rounded-lg font-semibold transition-colors ${
                    result === r
                      ? r === "win"
                        ? "bg-green-600 text-white ring-2 ring-yellow-400"
                        : r === "loss"
                          ? "bg-red-600 text-white ring-2 ring-yellow-400"
                          : "bg-gray-600 text-white ring-2 ring-yellow-400"
                      : r === "win"
                        ? "bg-green-600/50 text-white hover:bg-green-600/70"
                        : r === "loss"
                          ? "bg-red-600/50 text-white hover:bg-red-600/70"
                          : "bg-gray-600/50 text-white hover:bg-gray-600/70"
                  }`}
                >
                  {r.charAt(0).toUpperCase() + r.slice(1)}
                </button>
              ))}
            </div>
          </div>

          {/* Hand Summary */}
          <div className="bg-green-900/50 p-3 rounded-lg border border-green-700">
            <p className="text-white text-sm">
              <span className="font-semibold">Hole:</span>{" "}
              {holeCards.join(", ") || "None"}
            </p>
            <p className="text-white text-sm">
              <span className="font-semibold">Board:</span>{" "}
              {boardCards.join(", ") || "None"}
            </p>
            <p className="text-white text-sm">
              <span className="font-semibold">Position:</span>{" "}
              {position.charAt(0).toUpperCase() + position.slice(1)}
            </p>
          </div>

          {/* Save Button */}
          <button
            onClick={handleSave}
            disabled={isLoading || sessions.length === 0}
            className="w-full py-3 bg-yellow-400 text-gray-900 font-bold rounded-lg hover:brightness-110 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2 transition-all"
          >
            <Save className="w-5 h-5" />
            {isLoading ? "Saving..." : "Save Hand"}
          </button>
        </div>
      </div>
    </div>
  );
}
