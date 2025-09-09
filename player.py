from typing import List, Any


class Player:
    """
    Player class implementing SOLID principles:
    - SRP: Single responsibility for player management
    - OCP: Open for extension, closed for modification
    - LSP: Liskov substitution principle
    - ISP: Interface segregation principle
    - DIP: Dependency inversion principle
    """

    def __init__(self, color: str):
        self.color = color
        self.pieces: List[Any] = []

    def has_moves(self, board) -> bool:
        """Check if player has any valid moves - follows SRP"""
        return any(board.get_valid_moves(piece) for piece in self.pieces)

    def get_pieces_with_captures(self, board) -> List[Any]:
        """Get pieces that can make captures - follows SRP"""
        return [p for p in self.pieces if board.get_all_captures(p)]
