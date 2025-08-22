from app.core.models.card import Card
from app.core.odds.odds_calculator import calculate_odds


def test_deterministic_win():
    """
    Player has Four Aces already on the board.
    Should always win against 1 opponent.
    """
    hole = [Card("AS"), Card("AD")]
    board = [Card("AH"), Card("AC"), Card("2D"), Card("3D"), Card("4D")]
    
    odds = calculate_odds(hole, board, num_opponents=1, simulations=10)
    
    assert odds["win"] == 1.0
    assert odds["tie"] == 0.0
    assert odds["loss"] == 0.0

def test_sanity_random_hand():
    """
    Random realistic hand vs 2 opponents. Probabilities sum to ~1.
    """
    hole = [Card("KH"), Card("KC")]
    board = [Card("2H"), Card("7D"), Card("9S")]
    
    odds = calculate_odds(hole, board, num_opponents=2, simulations=1000, workers=2)
    
    total = odds["win"] + odds["tie"] + odds["loss"]
    assert 0.99 <= total <= 1.01  # allow minor floating-point rounding
    
    for key in ["win", "tie", "loss"]:
        assert 0.0 <= odds[key] <= 1.0

def test_full_board_tie():
    """
    Full board dealt, player has same hand as others → possible tie.
    """
    hole = [Card("2H"), Card("3H")]
    board = [Card("4H"), Card("5H"), Card("6H"), Card("7H"), Card("8H")]
    
    odds = calculate_odds(hole, board, num_opponents=1, simulations=10)
    
    # Sum should always be 1
    total = odds["win"] + odds["tie"] + odds["loss"]
    assert 0.99 <= total <= 1.01