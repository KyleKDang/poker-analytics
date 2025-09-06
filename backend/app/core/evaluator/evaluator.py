from itertools import combinations
from collections import Counter

from ..models.card import Card, RANK_ORDER


HAND_RANKS = {
    "High Card": 1,
    "One Pair": 2,
    "Two Pair": 3,
    "Three of a Kind": 4,
    "Straight": 5,
    "Flush": 6,
    "Full House": 7,
    "Four of a Kind": 8,
    "Straight Flush": 9,
    "Royal Flush": 10,
}


def evaluate_five_card_hand(cards: list[Card]) -> dict[str, int | str | tuple[int]]:
    """
    Evaluate the best 5-card poker hand.

    Returns a dictionary with:
        - label (str): Hand name (e.g., "Flush", "Two Pair").
        - rank (int): Hand strength.
        - kickers (tuple[int]): Rank indices for tie-breaking.
    """
    sorted_cards = sorted(cards, key=lambda c: c.rank_value(), reverse=True)
    ranks = [c.rank for c in sorted_cards]
    suits = [c.suit for c in sorted_cards]

    rank_counts = Counter(ranks)
    counts_sorted = sorted(
        rank_counts.items(), key=lambda x: (-x[1], -RANK_ORDER.index(x[0]))
    )

    is_flush = len(set(suits)) == 1

    # Straight detection
    rank_indices = sorted({RANK_ORDER.index(r) for r in ranks}, reverse=True)
    is_straight = False
    straight_high = None

    for i in range(len(rank_indices) - 4):
        window = rank_indices[i : i + 5]
        if all(window[j] - 1 == window[j + 1] for j in range(4)):
            is_straight = True
            straight_high = window[0]
            break

    # Ace-low straight
    if set(ranks) >= {"A", "2", "3", "4", "5"}:
        is_straight = True
        straight_high = RANK_ORDER.index("5")

    # Straight flush / royal flush
    if is_straight and is_flush:
        if straight_high == RANK_ORDER.index("A"):
            return {
                "label": "Royal Flush",
                "rank": HAND_RANKS["Royal Flush"],
                "kickers": (),
            }
        return {
            "label": "Straight Flush",
            "rank": HAND_RANKS["Straight Flush"],
            "kickers": (straight_high,),
        }

    # Four of a Kind
    if counts_sorted[0][1] == 4:
        kickers = (
            RANK_ORDER.index(counts_sorted[0][0]),
            RANK_ORDER.index(counts_sorted[1][0]),
        )
        return {
            "label": "Four of a Kind",
            "rank": HAND_RANKS["Four of a Kind"],
            "kickers": kickers,
        }

    # Full House
    if counts_sorted[0][1] == 3 and counts_sorted[1][1] == 2:
        kickers = (
            RANK_ORDER.index(counts_sorted[0][0]),
            RANK_ORDER.index(counts_sorted[1][0]),
        )
        return {
            "label": "Full House",
            "rank": HAND_RANKS["Full House"],
            "kickers": kickers,
        }

    # Flush
    if is_flush:
        kickers = tuple(RANK_ORDER.index(r) for r in ranks)
        return {"label": "Flush", "rank": HAND_RANKS["Flush"], "kickers": kickers}

    if is_straight:
        return {
            "label": "Straight",
            "rank": HAND_RANKS["Straight"],
            "kickers": (straight_high,),
        }

    # Three of a Kind
    if counts_sorted[0][1] == 3:
        kickers = (RANK_ORDER.index(counts_sorted[0][0]),) + tuple(
            RANK_ORDER.index(r) for r, c in counts_sorted[1:]
        )
        return {
            "label": "Three of a Kind",
            "rank": HAND_RANKS["Three of a Kind"],
            "kickers": kickers,
        }

    # Two Pair
    if counts_sorted[0][1] == 2 and counts_sorted[1][1] == 2:
        kickers = (
            RANK_ORDER.index(counts_sorted[0][0]),
            RANK_ORDER.index(counts_sorted[1][0]),
            RANK_ORDER.index(counts_sorted[2][0]),
        )
        return {"label": "Two Pair", "rank": HAND_RANKS["Two Pair"], "kickers": kickers}

    # One Pair
    if counts_sorted[0][1] == 2:
        kickers = (RANK_ORDER.index(counts_sorted[0][0]),) + tuple(
            RANK_ORDER.index(r) for r, c in counts_sorted[1:]
        )
        return {"label": "One Pair", "rank": HAND_RANKS["One Pair"], "kickers": kickers}

    # High Card
    kickers = tuple(RANK_ORDER.index(r) for r in ranks)
    return {"label": "High Card", "rank": HAND_RANKS["High Card"], "kickers": kickers}


def evaluate_seven_card_hand(cards: list[Card]) -> dict[str, int | str | tuple[int]]:
    """
    Evaluate the best 5-card hand from 7 cards.

    Returns a dictionary with:
        - label (str): Hand name (e.g., "Flush", "Two Pair").
        - rank (int): Hand strength.
        - kickers (tuple[int]): Rank indices for tie-breaking.
    """
    if len(cards) != 7:
        raise ValueError(f"Expected 7 cards, got {len(cards)}")

    best_hand = None
    for combo in combinations(cards, 5):
        current = evaluate_five_card_hand(list(combo))

        if not best_hand or (current["rank"], tuple(current["kickers"])) > (
            best_hand["rank"],
            best_hand["kickers"],
        ):
            best_hand = current
            best_hand["kickers"] = tuple(current["kickers"])

    return best_hand
