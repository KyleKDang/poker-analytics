"use client";

import { useState, useEffect } from "react";
import { Plus } from "lucide-react";
import api from "@/services/api";
import SessionItem from "@/components/SessionItem";

interface Session {
  id: number;
  user_id: number;
  start_time: string;
  end_time: string | null;
  notes: string | null;
  hand_count: number;
}

export default function SessionsPage() {
  const [sessions, setSessions] = useState<Session[]>([]);
  const [notes, setNotes] = useState("");
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSessions();
  }, []);

  const fetchSessions = async () => {
    try {
      const response = await api.get("/sessions");
      setSessions(response.data);
    } catch (err) {
      console.error("Error fetching sessions:", err);
    } finally {
      setLoading(false);
    }
  };

  const createSession = async () => {
    try {
      const response = await api.post("/sessions", {
        notes: notes.trim() || null,
      });
      setSessions([response.data, ...sessions]);
      setNotes("");
    } catch (err) {
      console.error("Error creating session:", err);
      alert("Failed to create session");
    }
  };

  const deleteSession = async (id: number) => {
    if (confirm("Delete this session? This will also delete all hands.")) {
      try {
        await api.delete(`/sessions/${id}`);
        setSessions(sessions.filter((s) => s.id !== id));
      } catch (err) {
        console.error("Error deleting session:", err);
        alert("Failed to delete session");
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen p-6 bg-green-900 flex items-center justify-center">
        <p className="text-white text-xl">Loading sessions...</p>
      </div>
    );
  }

  return (
    <div className="min-h-screen p-6 bg-green-900">
      <h1 className="mb-6 text-4xl font-extrabold text-yellow-400 text-center">
        Hand Sessions
      </h1>

      <div className="max-w-6xl mx-auto">
        <div className="mb-6 flex gap-3">
          <input
            type="text"
            placeholder="Session name..."
            value={notes}
            onChange={(e) => setNotes(e.target.value)}
            className="flex-1 p-3 rounded-lg bg-gray-700/80 text-white focus:ring-2 focus:ring-yellow-400"
          />
          <button
            onClick={createSession}
            className="px-6 py-3 bg-yellow-400 text-gray-900 font-bold rounded-lg hover:brightness-110 flex items-center gap-2"
          >
            <Plus className="w-5 h-5 cursor-pointer" />
            Create Session
          </button>
        </div>

        {sessions.length === 0 ? (
          <p className="text-gray-400 text-center py-8">
            No sessions yet. Create one to start logging hands!
          </p>
        ) : (
          <div className="space-y-4">
            {sessions.map((session) => (
              <SessionItem
                key={session.id}
                session={session}
                onDelete={deleteSession}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
