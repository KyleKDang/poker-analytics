import concurrent.futures
from typing import List, Dict
from .simulation import simulate_chunk
from ..models.card import Card


def calculate_odds(
    hole_cards: List[Card],
    board_cards: List[Card],
    num_opponents: int,
    simulations: int = 10000,
    workers: int = 4,
) -> Dict[str, float]:
    """
    Orchestrate Monte Carlo poker odds calculation using concurrency.

    Args:
        hole_cards (List[Card]): Player's 2 hole cards.
        board_cards (List[Card]): Current community cards (0-5).
        num_opponents (int): Number of opponents.
        simulations (int): Total number of simulations.
        workers (int): Number of worker processes/threads.

    Returns:
        Dict[str, float]: {"win": float, "tie": float, "loss": float}
    """
    chunk_size = simulations // workers
    futures = []

    with concurrent.futures.ProcessPoolExecutor(max_workers=workers) as executor:
        for _ in range(workers):
            futures.append(
                executor.submit(
                    simulate_chunk,
                    hole_cards,
                    board_cards,
                    num_opponents,
                    chunk_size
                )
            )

    wins, ties = 0, 0
    for f in concurrent.futures.as_completed(futures):
        w, t = f.result()
        wins += w
        ties += t

    total = chunk_size * workers
    losses = total - wins - ties

    return {
        "win": wins / total,
        "tie": ties / total,
        "loss": losses / total
    }