import tkinter as tk
from typing import List, Tuple, Optional


class BoardRenderer:
    """
    SRP: Responsible only for rendering the board and pieces and coordinate transforms.
    OCP: Configurable colors and sizes without changing code consumers.
    DIP: Depends on the abstract surface (tk.Canvas) and board public API (size, grid/piece fields).
    """

    def __init__(self, root: tk.Tk, board_size: int = 8, square_px: int = 80):
        self.root = root
        self.board_size = board_size
        self.square_px = square_px
        self.canvas = tk.Canvas(
            root,
            width=self.board_size * self.square_px,
            height=self.board_size * self.square_px,
            bg="#f0f0f0",
            highlightthickness=0,
        )
        self.canvas.pack()

        # Configurable palette
        self.light_color = "#EEEED2"
        self.dark_color = "#769656"
        self.highlight_color = "#F6F669"
        self.move_color = "#FFCC00"
        self.dark_piece_color = "#2C2C2C"
        self.light_piece_color = "#FFFFFF"
        self.king_ring_color = "#D4AF37"

    def draw(
        self,
        board,
        highlights: List[Tuple[int, int]] = None,
        selected: Optional[Tuple[int, int]] = None,
        move_targets: List[Tuple[int, int]] = None,
    ) -> None:
        self.canvas.delete("all")
        if highlights is None:
            highlights = []
        if move_targets is None:
            move_targets = []

        # Draw squares
        for r in range(self.board_size):
            for c in range(self.board_size):
                x0 = c * self.square_px
                y0 = r * self.square_px
                x1 = x0 + self.square_px
                y1 = y0 + self.square_px
                is_dark = (r + c) % 2 == 1
                color = self.dark_color if is_dark else self.light_color
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline=color)

        # Highlight capture-capable pieces
        for hr, hc in highlights:
            x0, y0, x1, y1 = self._cell_bbox(hr, hc)
            self.canvas.create_rectangle(
                x0, y0, x1, y1, outline=self.highlight_color, width=4
            )

        # Highlight selected and its move targets
        if selected is not None:
            sr, sc = selected
            x0, y0, x1, y1 = self._cell_bbox(sr, sc)
            self.canvas.create_rectangle(x0, y0, x1, y1, outline="#FFA500", width=4)
            for tr, tc in move_targets:
                cx, cy = self._cell_center(tr, tc)
                radius = self.square_px * 0.12
                self.canvas.create_oval(
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                    fill=self.move_color,
                    outline="",
                )

        # Draw pieces
        for r in range(self.board_size):
            for c in range(self.board_size):
                piece = board.get_piece_at((r, c))
                if piece is None:
                    continue
                cx, cy = self._cell_center(r, c)
                radius = self.square_px * 0.38
                color = (
                    self.dark_piece_color
                    if piece.color == "dark"
                    else self.light_piece_color
                )
                outline = "#000000" if piece.color == "light" else "#444444"
                self.canvas.create_oval(
                    cx - radius,
                    cy - radius,
                    cx + radius,
                    cy + radius,
                    fill=color,
                    outline=outline,
                    width=2,
                )
                if piece.is_king:
                    ring_r = radius * 0.65
                    self.canvas.create_oval(
                        cx - ring_r,
                        cy - ring_r,
                        cx + ring_r,
                        cy + ring_r,
                        outline=self.king_ring_color,
                        width=4,
                    )

        self.canvas.update_idletasks()

    def pixel_to_cell(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        r = y // self.square_px
        c = x // self.square_px
        if 0 <= r < self.board_size and 0 <= c < self.board_size:
            return (r, c)
        return None

    def _cell_bbox(self, r: int, c: int) -> Tuple[int, int, int, int]:
        x0 = c * self.square_px
        y0 = r * self.square_px
        x1 = x0 + self.square_px
        y1 = y0 + self.square_px
        return x0, y0, x1, y1

    def _cell_center(self, r: int, c: int) -> Tuple[int, int]:
        x0, y0, x1, y1 = self._cell_bbox(r, c)
        return (x0 + x1) // 2, (y0 + y1) // 2
