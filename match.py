from board import Board
from player import Player


class Match:
    """
    Main Match class implementing SOLID principles:
    - SRP: Single responsibility for game flow management
    - OCP: Open for extension, closed for modification
    - LSP: Liskov substitution principle
    - ISP: Interface segregation principle
    - DIP: Dependency inversion principle
    """

    def __init__(self):
        self.board = Board()
        self.players = [Player("dark"), Player("light")]
        self.current_player_index = 0
        self.assign_pieces()

    def assign_pieces(self) -> None:
        """Assign pieces from board to players - follows SRP"""
        for row in range(8):
            for col in range(8):
                piece = self.board.get_piece_at((row, col))
                if piece:
                    for player in self.players:
                        if player.color == piece.color:
                            player.pieces.append(piece)

    def start_game(self) -> None:
        """Start the game loop - follows SRP"""
        print("Starting Checkers game!")
        self.display_with_highlights()

        while True:
            self.display_with_highlights()
            current_player = self.players[self.current_player_index]
            print(f"{current_player.color}'s turn")

            if not current_player.has_moves(self.board):
                print(f"{current_player.color} cannot move. Game over.")
                break

            move_result = self.make_move(current_player)
            if move_result is None:
                break
            elif move_result:
                self.switch_turn()

    def display_with_highlights(self) -> None:
        """Display board with highlighting for capturing pieces - follows SRP"""
        current_player = self.players[self.current_player_index]
        capturing_pieces = current_player.get_pieces_with_captures(self.board)
        self.board.highlight_positions = [p.position for p in capturing_pieces]
        self.board.display()

    def make_move(self, player) -> bool:
        """Handle a single move for a player - follows SRP"""
        capturing_pieces = player.get_pieces_with_captures(self.board)

        while True:
            try:
                # Get piece position
                raw_input = input(
                    "Enter piece position to move (row col or type 'GG' to quit): "
                )
                if raw_input.strip().lower() == "gg":
                    print("Game ended by user.")
                    return None

                parts = raw_input.split()
                if len(parts) != 2:
                    print("Invalid input. Please enter two numbers separated by space.")
                    continue

                from_pos = tuple(map(int, parts))
                piece = self.board.get_piece_at(from_pos)

                if not piece or piece.color != player.color:
                    print("Invalid piece selected.")
                    continue

                if capturing_pieces and piece not in capturing_pieces:
                    print("You must play a piece that can capture.")
                    continue

                # Handle captures
                captures = self.board.get_all_captures(piece)
                if captures:
                    return self.handle_captures(piece, captures)
                else:
                    return self.handle_simple_move(piece)

            except ValueError:
                print("Invalid input. Please enter two numbers separated by space.")
            except Exception as e:
                print(f"Error in input: {e}")

    def handle_captures(self, piece, captures: list) -> bool:
        """Handle capture moves - follows SRP"""
        print("Multiple captures available:")
        for i, path in enumerate(captures):
            print(f"{i + 1}: {path}")

        while True:
            try:
                choice = int(input("Select capture path number: ")) - 1
                if 0 <= choice < len(captures):
                    break
                else:
                    print(f"Please enter a number between 1 and {len(captures)}")
            except ValueError:
                print("Invalid input. Please enter a number.")

        full_path = captures[choice]

        # Execute the capture sequence
        for next_pos in full_path:
            mid_row = (piece.position[0] + next_pos[0]) // 2
            mid_col = (piece.position[1] + next_pos[1]) // 2
            self.board.grid[mid_row][mid_col] = None
            self.board.move_piece(piece, next_pos)

        # Continue capturing after king promotion
        while True:
            new_captures = self.board.get_all_captures(piece)
            if new_captures:
                print(f"Continuing captures as king... Options: {new_captures}")
                extra_path = new_captures[0]
                full_path.extend(extra_path)
                for next_pos in extra_path:
                    mid_row = (piece.position[0] + next_pos[0]) // 2
                    mid_col = (piece.position[1] + next_pos[1]) // 2
                    self.board.grid[mid_row][mid_col] = None
                    self.board.move_piece(piece, next_pos)
            else:
                break

        print(f"Full capture path executed: {full_path}")
        return True

    def handle_simple_move(self, piece) -> bool:
        """Handle simple (non-capture) moves - follows SRP"""
        while True:
            try:
                raw_dest = input(
                    "Enter destination position (row col or type 'GG' to quit): "
                )
                if raw_dest.strip().lower() == "gg":
                    print("Game ended by user.")
                    return None

                parts = raw_dest.split()
                if len(parts) != 2:
                    print("Invalid input. Please enter two numbers separated by space.")
                    continue

                to_pos = tuple(map(int, parts))

                if to_pos in self.board.get_simple_moves(piece):
                    self.board.move_piece(piece, to_pos)
                    return True
                else:
                    print("Invalid move. Try again.")
                    return False

            except ValueError:
                print("Invalid input. Please enter two numbers separated by space.")
            except Exception as e:
                print(f"Error in input: {e}")

    def switch_turn(self) -> None:
        """Switch to next player - follows SRP"""
        self.current_player_index = 1 - self.current_player_index
