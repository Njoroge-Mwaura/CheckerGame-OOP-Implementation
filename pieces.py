from abc import ABC, abstractmethod
from typing import List, Tuple


class Piece(ABC):
    """
    Abstract base class for pieces implementing SOLID principles:
    - SRP: Single responsibility for piece behavior
    - OCP: Open for extension, closed for modification
    - LSP: Liskov substitution principle
    - ISP: Interface segregation principle
    - DIP: Dependency inversion principle
    """

    def __init__(self, color: str, position: Tuple[int, int]):
        self.color = color
        self.position = position
        self.is_king = False

    @abstractmethod
    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        """Get valid moves for this piece - follows ISP"""
        pass

    def make_king(self) -> None:
        """Promote piece to king - follows SRP"""
        self.is_king = True

    def get_directions(self) -> List[Tuple[int, int]]:
        """Get movement directions - follows SRP"""
        if self.is_king:
            return [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        return [(-1, -1), (-1, 1)] if self.color == "light" else [(1, -1), (1, 1)]

    def can_be_promoted(self, position: Tuple[int, int]) -> bool:
        """Check if piece can be promoted at given position - follows SRP"""
        row = position[0]
        return (self.color == "light" and row == 0) or (
            self.color == "dark" and row == 7
        )


class Man(Piece):
    """Man piece implementation - follows LSP"""

    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        """Get valid moves using board's validation - follows DIP"""
        return board.get_valid_moves(self)


class King(Piece):
    """King piece implementation - follows LSP"""

    def __init__(self, color: str, position: Tuple[int, int]):
        super().__init__(color, position)
        self.is_king = True  # Kings start as kings

    def get_valid_moves(self, board) -> List[Tuple[int, int]]:
        """Get valid moves using board's validation - follows DIP"""
        return board.get_valid_moves(self)
