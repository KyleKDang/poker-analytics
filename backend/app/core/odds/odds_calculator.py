import concurrent.futures

from .simulation import simulate_chunk
from ..models.card import Card


def calculate_odds(
    hole_cards: list[Card],
    board_cards: list[Card],
    num_opponents: int,
    simulations: int = 10_000,
    workers: int = 4,
) -> dict[str, float]:
    """
    Calculate poker winning odds using Monte Carlo simulation with concurrency.

    Returns a dictionary with:
        - win (float): Probability of winning.
        - tie (float): Probability of tying.
        - loss (float): Probability of losing.
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