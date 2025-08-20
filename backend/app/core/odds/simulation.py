import random
from typing import List, Tuple
from ..models.card import Card, RANK_ORDER, SUITS
from ..evaluator.hand import evaluate_seven_card_hand

def simulate_chunk(
        hole_cards: List[Card], 
        board_cards: List[Card], 
        num_opponents: int, 
        simulations: int
) -> Tuple[int, int]:
    """
    Run a Monte Carlo simulation chunk for poker odds.

    Args:
        hole_cards (List[Card]): Player's 2 hole cards.
        board_cards (List[Card]): Current community cards (0-5).
        num_opponents (int): Number of opponents in the hand.
        simulations (int): Number of simulations to run in this chunk.

    Returns:
        Tuple[int, int]: (wins, ties) for the player across all simulations.
    """
    # Build known and remaining deck
    known = set(hole_cards + board_cards)
    deck = [
        Card(rank + suit) 
        for rank in RANK_ORDER 
        for suit in SUITS 
        if Card(rank + suit) not in known
    ]

    wins, ties = 0, 0

    for _ in range(simulations):
        random.shuffle(deck)

        # Fill in missing community cards
        missing_board = 5 - len(board_cards)
        full_board = board_cards + deck[:missing_board]

        # Deal opponent hands
        idx = missing_board
        opponents_hands = [deck[idx + i*2: idx + i*2 + 2] for i in range(num_opponents)]

        # Evaluate hands
        player_score = evaluate_seven_card_hand(hole_cards + full_board)
        opponents_scores = [
            evaluate_seven_card_hand(opp + full_board) for opp in opponents_hands
        ]

        # Compare by rank then kickers
        max_opponent = max(
            opponents_scores,
            key=lambda s: (s["rank"], s["kickers"])
        )
        if (
            (player_score["rank"], player_score["kickers"]) > 
            (max_opponent["rank"], max_opponent["kickers"])
        ):
            wins += 1
        elif (
            (player_score["rank"], player_score["kickers"]) ==
            (max_opponent["rank"], max_opponent["kickers"])
        ):
            ties += 1

    return wins, ties