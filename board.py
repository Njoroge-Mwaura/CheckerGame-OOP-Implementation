from typing import List, Tuple, Optional
from pieces import Man


class Board:
    """
    Main Board class implementing SOLID principles:
    - SRP: Single responsibility for board management
    - OCP: Open for extension, closed for modification
    - LSP: Liskov substitution principle
    - ISP: Interface segregation principle
    - DIP: Dependency inversion principle
    """

    def __init__(self):
        self.grid = [[None for _ in range(8)] for _ in range(8)]
        self.highlight_positions: List[Tuple[int, int]] = []
        self.setup_board()

    def setup_board(self) -> None:
        """Setup initial board state - follows SRP"""
        # Setup dark pieces (top 3 rows)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    piece = Man("dark", (row, col))
                    self.grid[row][col] = piece

        # Setup light pieces (bottom 3 rows)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    piece = Man("light", (row, col))
                    self.grid[row][col] = piece

    def get_piece_at(self, position: Tuple[int, int]) -> Optional[object]:
        """Get piece at specific position"""
        row, col = position
        if not self.in_bounds(position):
            return None
        return self.grid[row][col]

    def move_piece(self, piece, destination: Tuple[int, int]) -> bool:
        """
        Move a piece to destination and handle captures/promotions
        Returns True if a capture occurred
        """
        start_position = piece.position
        end_position = destination

        # Move the piece
        self.grid[start_position[0]][start_position[1]] = None
        piece.position = end_position
        self.grid[end_position[0]][end_position[1]] = piece

        # Check for promotion
        if (piece.color == "light" and end_position[0] == 0) or (
            piece.color == "dark" and end_position[0] == 7
        ):
            piece.make_king()

        # Check if this was a capture move
        if abs(end_position[0] - start_position[0]) == 2:
            mid_row = (start_position[0] + end_position[0]) // 2
            mid_col = (start_position[1] + end_position[1]) // 2
            self.grid[mid_row][mid_col] = None
            return True

        return False

    def get_valid_moves(self, piece) -> List[Tuple[int, int]]:
        """Get valid moves for a piece - follows SRP"""
        captures = self.get_all_captures(piece)
        if captures:
            return [path[-1] for path in captures]
        else:
            return self.get_simple_moves(piece)

    def get_simple_moves(self, piece) -> List[Tuple[int, int]]:
        """Get simple (non-capture) moves for a piece - follows SRP"""
        moves = []
        directions = piece.get_directions()
        row, col = piece.position

        for dr, dc in directions:
            new_pos = (row + dr, col + dc)
            if self.in_bounds(new_pos) and self.grid[new_pos[0]][new_pos[1]] is None:
                moves.append(new_pos)

        return moves

    def get_all_captures(
        self, piece, position=None, visited=None
    ) -> List[List[Tuple[int, int]]]:
        """Get all possible capture sequences for a piece - follows SRP"""
        if visited is None:
            visited = set()
        if position is None:
            position = piece.position

        captures = []
        row, col = position
        directions = piece.get_directions()

        for dr, dc in directions:
            mid_pos = (row + dr, col + dc)
            end_pos = (row + 2 * dr, col + 2 * dc)

            if (
                not self.in_bounds(end_pos)
                or not self.in_bounds(mid_pos)
                or mid_pos in visited
            ):
                continue

            enemy = self.grid[mid_pos[0]][mid_pos[1]]
            if (
                enemy
                and enemy.color != piece.color
                and self.grid[end_pos[0]][end_pos[1]] is None
            ):
                next_visited = visited.copy()
                next_visited.add(mid_pos)
                next_captures = self.get_all_captures(piece, end_pos, next_visited)

                if next_captures:
                    for path in next_captures:
                        captures.append([end_pos] + path)
                else:
                    captures.append([end_pos])

        return captures

    def in_bounds(self, position: Tuple[int, int]) -> bool:
        """Check if position is within board bounds"""
        row, col = position
        return 0 <= row < 8 and 0 <= col < 8

    def display(self) -> None:
        """Display the board with current highlights - follows SRP"""
        print("   " + " ".join(str(i) for i in range(8)))

        for row in range(8):
            row_str = str(row) + "  "
            for col in range(8):
                piece = self.grid[row][col]

                if (row, col) in self.highlight_positions:
                    row_str += "* "
                elif piece is None:
                    row_str += ". "
                elif piece.color == "dark":
                    row_str += "Dk " if piece.is_king else "D "
                else:
                    row_str += "Lk " if piece.is_king else "L "

            print(row_str)
        self.highlight_positions = []

    @property
    def size(self) -> int:
        """Get board size"""
        return 8
