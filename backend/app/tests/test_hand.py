import pytest
from app.core.evaluator.hand import evaluate_five_card_hand, HAND_RANKS
from app.core.evaluator.card import Card

def make_hand(codes):
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