import random

from ..models.card import Card, RANK_ORDER, SUITS
from ..evaluator.evaluator import evaluate_hand


def simulate_chunk(
    hole_cards: list[Card],
    board_cards: list[Card],
    num_opponents: int,
    simulations: int,
) -> tuple[int, int]:
    """
    Run a Monte Carlo simulation chunk to estimate poker winning odds.

    Returns a tuple with:
        - wins (int): Number of simulations the player won.
        - ties (int): Number of simulations the player tied.
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
        opponents_hands = [
            deck[idx + i * 2 : idx + i * 2 + 2] for i in range(num_opponents)
        ]

        # Evaluate hands
        player_score = evaluate_hand(hole_cards + full_board)
        opponents_scores = [evaluate_hand(opp + full_board) for opp in opponents_hands]

        # Compare by rank then kickers
        max_opponent = max(opponents_scores, key=lambda s: (s["rank"], s["kickers"]))
        if (player_score["rank"], player_score["kickers"]) > (
            max_opponent["rank"],
            max_opponent["kickers"],
        ):
            wins += 1
        elif (player_score["rank"], player_score["kickers"]) == (
            max_opponent["rank"],
            max_opponent["kickers"],
        ):
            ties += 1

    return wins, ties
