from typing import Any

RANK_ORDER = "23456789TJQKA"
SUITS = "CDHS"

class Card:
    """Represents a standard playing card."""

    def __init__(self, code: str):
        if len(code) != 2 or code[0] not in RANK_ORDER or code[1] not in SUITS:
            raise ValueError(f"Invalid card code: {code}")
        self.rank: str = code[0]
        self.suit: str = code[1]
        self.code: str = code

    def rank_value(self) -> int:
        return RANK_ORDER.index(self.rank)
    
    def __repr__(self) -> str:
        return self.code
    
    def __hash__(self) -> int:
        return hash(self.code)
    
    def __eq__(self, other: Any) -> bool:
        if isinstance(other, Card):
            return self.code == other.code
        else:
            return False

    def __lt__(self, other: "Card") -> bool:
        return self.rank_value() < other.rank_value()