"use client";

import { useState, useEffect } from "react";
import { Trash2, ChevronDown, ChevronRight } from "lucide-react";
import api from "@/services/api";
import HandRow from "./HandRow";

interface Session {
  id: number;
  user_id: number;
  start_time: string;
  end_time: string | null;
  notes: string | null;
}

interface Hand {
  id: number;
  session_id: number;
  hole_cards: string[];
  board_cards: string[];
  player_position: string;
  action_taken: string | null;
  result: string | null;
  created_at: string;
}

interface SessionItemProps {
  session: Session;
  onDelete: (id: number) => void;
}

export default function SessionItem({ session, onDelete }: SessionItemProps) {
  const [isOpen, setIsOpen] = useState(false);
  const [hands, setHands] = useState<Hand[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (isOpen && hands.length === 0) {
      fetchHands();
    }
  }, [isOpen]);

  const fetchHands = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/sessions/${session.id}/hands`);
      setHands(response.data);
    } catch (err) {
      console.error("Error fetching hands:", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="border-2 border-green-700 rounded-lg overflow-hidden bg-green-800/40">
      <div
        className="flex items-center justify-between p-4 cursor-pointer hover:bg-green-800/60 transition-colors"
        onClick={() => setIsOpen(!isOpen)}
      >
        <div className="flex items-center gap-3">
          {isOpen ? (
            <ChevronDown className="w-5 h-5 text-yellow-400" />
          ) : (
            <ChevronRight className="w-5 h-5 text-yellow-400" />
          )}
          <div>
            <h3 className="text-xl font-bold text-white">
              {session.notes || "Unnamed Session"}
            </h3>
            <p className="text-sm text-gray-400">
              {new Date(session.start_time).toLocaleString()} • {hands.length}{" "}
              hands
            </p>
          </div>
        </div>
        <button
          onClick={(e) => {
            e.stopPropagation();
            onDelete(session.id);
          }}
          className="p-2 hover:bg-red-600 rounded transition-colors"
        >
          <Trash2 className="w-5 h-5 text-white" />
        </button>
      </div>

      {isOpen && (
        <div className="p-4 bg-gray-800/50">
          {loading ? (
            <p className="text-gray-400 text-center py-4">Loading hands...</p>
          ) : hands.length === 0 ? (
            <p className="text-gray-400 text-center py-4">
              No hands logged yet
            </p>
          ) : (
            <div className="space-y-2">
              {hands.map((hand, index) => (
                <HandRow key={hand.id} hand={hand} handNumber={index + 1} />
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
