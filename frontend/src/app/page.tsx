"use client";

import { useState } from "react";
import api from "@/services/api";

type Odds = {
    win: number;
    tie: number;
    loss: number;
};

export default function HomePage() {
    const [holeCards, setHoleCards] = useState<string[]>([]);
    const [boardCards, setBoardCards] = useState<string[]>([]);
    const [numOpponents, setNumOpponents] = useState<number>();
    const [hand, setHand] = useState<string>();
    const [odds, setOdds] = useState<Odds | null>(null);

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
        <div className="flex items-center justify-center min-h-screen bg-gradient-to-b from-gray-900 via-green-950 to-gray-900">
        </div>
    );
}