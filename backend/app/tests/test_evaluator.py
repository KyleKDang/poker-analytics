from app.core.evaluator.evaluator import (
    evaluate_five_card_hand,
    evaluate_seven_card_hand,
    HAND_RANKS,
)
from app.core.models.card import Card


def make_hand(codes):
    """Helper to create Card objects from string codes."""
    return [Card(code) for code in codes]


def test_high_card():
    hand = make_hand(["2H", "5D", "9C", "JS", "KD"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "High Card"
    assert result["rank"] == HAND_RANKS["High Card"]


def test_one_pair():
    hand = make_hand(["AH", "AD", "5C", "7S", "9D"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "One Pair"
    assert result["rank"] == HAND_RANKS["One Pair"]


def test_two_pair():
    hand = make_hand(["KH", "KS", "5C", "5D", "9H"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "Two Pair"
    assert result["rank"] == HAND_RANKS["Two Pair"]


def test_three_of_a_kind():
    hand = make_hand(["8H", "8S", "8D", "2C", "KD"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "Three of a Kind"
    assert result["rank"] == HAND_RANKS["Three of a Kind"]


def test_straight():
    hand = make_hand(["4S", "5D", "6H", "7C", "8S"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "Straight"
    assert result["rank"] == HAND_RANKS["Straight"]


def test_wheel_straight():
    hand = make_hand(["AS", "2D", "3H", "4C", "5S"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "Straight"
    assert result["rank"] == HAND_RANKS["Straight"]


def test_flush():
    hand = make_hand(["2H", "5H", "9H", "KH", "7H"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "Flush"
    assert result["rank"] == HAND_RANKS["Flush"]


def test_full_house():
    hand = make_hand(["KH", "KS", "KC", "5D", "5C"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "Full House"
    assert result["rank"] == HAND_RANKS["Full House"]


def test_four_of_a_kind():
    hand = make_hand(["9H", "9S", "9D", "9C", "2H"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "Four of a Kind"
    assert result["rank"] == HAND_RANKS["Four of a Kind"]


def test_straight_flush():
    hand = make_hand(["4H", "5H", "6H", "7H", "8H"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "Straight Flush"
    assert result["rank"] == HAND_RANKS["Straight Flush"]


def test_royal_flush():
    hand = make_hand(["TH", "JH", "QH", "KH", "AH"])
    result = evaluate_five_card_hand(hand)
    assert result["label"] == "Royal Flush"
    assert result["rank"] == HAND_RANKS["Royal Flush"]


def test_high_card_seven():
    cards = make_hand(["AS", "KH", "7D", "6C", "3H", "2S", "9D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "High Card"
    assert result["rank"] == 1


def test_one_pair_seven():
    cards = make_hand(["AS", "AD", "7C", "6H", "3S", "9C", "2D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "One Pair"
    assert result["rank"] == 2


def test_two_pair_seven():
    cards = make_hand(["AS", "AD", "7C", "7H", "3S", "2C", "4D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "Two Pair"
    assert result["rank"] == 3


def test_three_of_a_kind_seven():
    cards = make_hand(["AS", "AD", "AC", "7H", "9S", "JC", "4D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "Three of a Kind"
    assert result["rank"] == 4


def test_straight_seven():
    cards = make_hand(["5S", "6H", "7C", "8D", "9S", "2C", "3D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "Straight"
    assert result["rank"] == 5


def test_flush_seven():
    cards = make_hand(["2H", "5H", "9H", "JH", "KH", "3C", "4D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "Flush"
    assert result["rank"] == 6


def test_full_house_seven():
    cards = make_hand(["AS", "AD", "AC", "7H", "7S", "2C", "4D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "Full House"
    assert result["rank"] == 7


def test_four_of_a_kind_seven():
    cards = make_hand(["AS", "AD", "AC", "AH", "7S", "2C", "4D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "Four of a Kind"
    assert result["rank"] == 8


def test_straight_flush_seven():
    cards = make_hand(["5H", "6H", "7H", "8H", "9H", "2C", "4D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "Straight Flush"
    assert result["rank"] == 9


def test_royal_flush_seven():
    cards = make_hand(["TH", "JH", "QH", "KH", "AH", "2C", "4D"])
    result = evaluate_seven_card_hand(cards)
    assert result["label"] == "Royal Flush"
    assert result["rank"] == 10
