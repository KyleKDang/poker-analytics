import random
from typing import List, Tuple
from ..evaluator.card import Card, RANK_ORDER, SUITS
from ..evaluator.hand import evaluate_seven_card_hand



def simulate_chunk(
        hole_cards: List[str], 
        board_cards: List[str], 
        num_opponents: int, 
        simulations: int
) -> Tuple[int, int]:
    """
    Run a chunk of Monte Carlo poker simulations and return win/tie counts.

    Args:
        hole_cards (List[str]): Player's 2 hole cards (e.g., ["AS", "KH"]).
        board_cards (List[str]): Current community cards (0-5 cards).
        num_opponents (int): Number of opponents to simulate against.
        simulations (int): Number of random simulations to run.

    Returns:
        Tuple[int, int]: A tuple (wins, ties) across all simulations.
    """
    # Build known and remaining deck
    known = set(hole_cards + board_cards)
    deck = [
        Card(rank + suit) 
        for rank in RANK_ORDER 
        for suit in SUITS 
        if rank + suit not in known
    ]

    wins, ties = 0, 0

    for _ in range(simulations):
        random.shuffle(deck)

        # Fill in missing community cards
        missing_board = 5 - len(board_cards)
        current_board = [Card(c) for c in board_cards] + deck[:missing_board]

        # Deal opponent hands
        opponents_hands = []
        idx = missing_board
        for _ in range(num_opponents):
            opponents_hands.append(deck[idx:idx+2])
            idx += 2

        # Evaluate hands
        player_cards = [Card(c) for c in hole_cards] + current_board
        player_score = evaluate_seven_card_hand(player_cards)
        opponents_scores = [
            evaluate_seven_card_hand(opp + current_board) for opp in opponents_hands
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