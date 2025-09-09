# Checkers-OOP

A simple, Graphical User Interphase(GUI) Checkers game implemented in Python, structured to follow the SOLID principles. The project focuses on clarity, maintainability, and extensibility while keeping the core gameplay minimal and easy to run.

## Quick Start

```bash
python main.py
```

- During your turn, enter positions as two integers: `row col` (e.g., `2 5`).
- To quit at any input prompt, type `GG`.

## Project Structure (Core Files Only)

- `main.py`: Application entrypoint and minimal application orchestration
- `match.py`: Game flow (turn loop, input handling, switching turns)
- `board.py`: Board state, move rules, captures, display
- `pieces.py`: Piece abstractions (`Piece`, `Man`, `King`)
- `player.py`: Player state and queries (moves available, capture-capable pieces)

## SOLID Principles Applied

### main.py
- Single Responsibility (SRP): Runs the game by delegating to `Match`.
- Open/Closed (OCP): Easily extendable (e.g., swap `Match` with another orchestrator) without changing `main.py`.
- Liskov Substitution (LSP): Any object exposing `start_game()` could be injected in place of `Match`.
- Interface Segregation (ISP): Keeps responsibilities minimal; no mixed concerns.
- Dependency Inversion (DIP): Depends on an abstraction of a game orchestrator conceptually (constructed `Match`), not internal details.

### match.py
- SRP: Manages the game loop, player turns, move selection, and quitting logic.
- OCP: Input handling and flow can be extended (e.g., alternate input sources or extra rules) without altering board or piece logic.
- LSP: Works with any `Board` that provides the expected methods (`get_valid_moves`, `get_all_captures`, `move_piece`, etc.).
- ISP: Uses only what it needs from `Board` and `Player` (no broad interfaces).
- DIP: Orchestrates high-level flow; relies on `Board` and `Player` behaviors rather than their internal implementations.

### board.py
- SRP: Maintains board state and implements move/capture rules plus board rendering.
- OCP: Move rules can be extended by enhancing methods (e.g., promotion variants) without altering consumers.
- LSP: Any `Piece` respecting direction and color contracts works seamlessly (e.g., `Man`, `King`).
- ISP: Provides focused methods (`get_piece_at`, `get_valid_moves`, `get_all_captures`, `move_piece`, `display`).
- DIP: Collaborates with `Piece` via minimal expectations (`get_directions`, `color`, `position`).

### pieces.py
- SRP: Encapsulates piece-specific behavior (movement directions, promotion state) and exposes a minimal API to the board.
- OCP: New piece types can be introduced by subclassing `Piece` and respecting its contract.
- LSP: `Man` and `King` are substitutable wherever a `Piece` is expected.
- ISP: Keeps the piece API small (`get_valid_moves`, `get_directions`, `make_king`).
- DIP: Defers move validation to `Board` via `get_valid_moves(self, board)`.

### player.py
- SRP: Tracks player color and owned pieces; answers queries about possible moves.
- OCP: Additional player logic (e.g., AI strategies) can be layered without modifying this file.
- LSP: Any object with `pieces` and `color` that cooperates with `Board` methods can substitute.
- ISP: Provides only focused behavior (has moves, pieces that can capture).
- DIP: Depends only on `Board`’s public methods to compute availability of moves.

## Controls

- Select a piece: `row col` (e.g., `2 5`)
- Select destination: `row col` (e.g., `3 4`)
- Quit any time: `GG`

## Notes

- The code intentionally keeps a small, core surface area to highlight SOLID principles without excessive abstractions.
- All input validation is done in `match.py` with clear prompts and early returns on `GG`.
