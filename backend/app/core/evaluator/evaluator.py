from itertools import combinations
from .card import Card

def evaluate_hand(cards: list[str]) -> dict:
    """
    Takes 7 card strings like ["AS", "KH", "QH", "JD", "TC", "9H", "8D"]
    Returns best hand info: rank, label, best 5-card hand
    """
    all_cards = [Card(code) for code in cards]
    best = None

    # TODO: Implement evluate_five_card_hand and uncomment the code below
    # for combo in combinations(all_cards, 5):
    #     result = evaluate_five_card_hand(list(combo))
    #     if not best or result['rank'] > best['rank'] or (
    #         result['rank'] == best['rank'] and result['kickers'] > best['kickers']
    #     ):
    #         best = result
    #         best['hand'] = [card.code for code in combo]

    # return {
    #     "rank": best['rank'],
    #     "label": best['label'],
    #     "best_hand": best['hand']
    # }
    pass