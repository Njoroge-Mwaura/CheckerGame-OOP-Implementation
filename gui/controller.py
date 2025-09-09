import tkinter as tk
from typing import List, Tuple, Optional
from board import Board
from player import Player
from gui.renderer import BoardRenderer


class GameController:
    """
    SRP: Orchestrates GUI interactions: selection, moves, turn switching.
    OCP: Extend behaviors (e.g., hints, undo) without modifying Board/Player/Renderer.
    DIP: Depends on Board/Player abstractions via their public methods.
    """

    def __init__(self, root: tk.Tk):
        self.root = root
        self.board = Board()
        self.players = [Player("dark"), Player("light")]
        self.current_player_index = 0
        self._assign_pieces()

        self.renderer = BoardRenderer(root, board_size=8, square_px=80)
        self.selected_cell: Optional[Tuple[int, int]] = None
        self.current_move_targets: List[Tuple[int, int]] = []

        self.root.title("Checkers - SOLID GUI")
        self.renderer.canvas.bind("<Button-1>", self._on_click)
        self._redraw()

    def _assign_pieces(self) -> None:
        for r in range(8):
            for c in range(8):
                piece = self.board.get_piece_at((r, c))
                if piece:
                    for p in self.players:
                        if p.color == piece.color:
                            p.pieces.append(piece)

    def _current_player(self) -> Player:
        return self.players[self.current_player_index]

    def _other_player(self) -> Player:
        return self.players[1 - self.current_player_index]

    def _on_click(self, event) -> None:
        cell = self.renderer.pixel_to_cell(event.x, event.y)
        if cell is None:
            return

        r, c = cell
        piece = self.board.get_piece_at(cell)
        current_player = self._current_player()

        # If selecting own piece
        if piece and piece.color == current_player.color:
            self.selected_cell = cell
            self.current_move_targets = self.board.get_valid_moves(piece)
            self._redraw()
            return

        # If selecting a move target
        if self.selected_cell:
            selected_piece = self.board.get_piece_at(self.selected_cell)
            if selected_piece and cell in self.board.get_simple_moves(selected_piece):
                self.board.move_piece(selected_piece, cell)
                self._end_turn()
                return

            # Handle capture sequences
            captures = (
                self.board.get_all_captures(selected_piece) if selected_piece else []
            )
            if selected_piece and captures:
                flattened = set(pos for path in captures for pos in path)
                if cell in flattened:
                    # Execute the chosen capture step-by-step until reaching the clicked cell in the path
                    for path in captures:
                        if cell in path:
                            for step in path:
                                if selected_piece.position == step:
                                    continue
                                mid_row = (selected_piece.position[0] + step[0]) // 2
                                mid_col = (selected_piece.position[1] + step[1]) // 2
                                self.board.grid[mid_row][mid_col] = None
                                self.board.move_piece(selected_piece, step)
                                if step == cell:
                                    break
                            break
                    # After capture, check for additional forced captures
                    while True:
                        new_captures = self.board.get_all_captures(selected_piece)
                        if new_captures:
                            # Auto-continue first available capture path for simplicity
                            extra_path = new_captures[0]
                            for step in extra_path:
                                mid_row = (selected_piece.position[0] + step[0]) // 2
                                mid_col = (selected_piece.position[1] + step[1]) // 2
                                self.board.grid[mid_row][mid_col] = None
                                self.board.move_piece(selected_piece, step)
                        else:
                            break
                    self._end_turn()
                    return

        # Otherwise, ignore

    def _end_turn(self) -> None:
        self.selected_cell = None
        self.current_move_targets = []
        self.current_player_index = 1 - self.current_player_index
        self._redraw()
        self._check_game_over()

    def _check_game_over(self) -> None:
        current_player = self._current_player()
        if not current_player.has_moves(self.board):
            self._dialog(f"{current_player.color} cannot move. Game over.")

    def _capture_highlights(self) -> List[Tuple[int, int]]:
        current_player = self._current_player()
        return [p.position for p in current_player.get_pieces_with_captures(self.board)]

    def _redraw(self) -> None:
        self.renderer.draw(
            board=self.board,
            highlights=self._capture_highlights(),
            selected=self.selected_cell,
            move_targets=self.current_move_targets,
        )

    def _dialog(self, message: str) -> None:
        top = tk.Toplevel(self.root)
        top.title("Game Over")
        tk.Label(top, text=message, padx=20, pady=10).pack()
        tk.Button(top, text="OK", command=top.destroy).pack(pady=10)
