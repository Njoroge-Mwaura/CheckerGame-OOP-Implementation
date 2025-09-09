# Checkers-OOP

A Checkers game implemented in Python with both console and graphical interfaces, structured to follow the SOLID principles. The project focuses on clarity, maintainability, and extensibility while keeping the core gameplay minimal and easy to run.

## Quick Start

### Console Version
```bash
python main.py
```

- During your turn, enter positions as two integers: `row col` (e.g., `2 5`).
- To quit at any input prompt, type `GG`.

### Graphical User Interface (GUI)
```bash
python gui/main.py
```

- Click on a piece to select it (highlighted in blue)
- Click on a valid destination to move the piece
- Pieces that can capture are highlighted in red
- The game automatically switches turns and checks for game over
- Close the window to quit

## Project Structure

### Core Files
- `main.py`: Console application entrypoint and minimal application orchestration
- `match.py`: Game flow (turn loop, input handling, switching turns)
- `board.py`: Board state, move rules, captures, display
- `pieces.py`: Piece abstractions (`Piece`, `Man`, `King`)
- `player.py`: Player state and queries (moves available, capture-capable pieces)

### GUI Files
- `gui/main.py`: GUI application entrypoint
- `gui/controller.py`: Game controller managing user interactions and game flow
- `gui/renderer.py`: Board rendering and visual display using Tkinter
- `gui/__init__.py`: Package initialization

### Legacy Files
- `legacy/v2checkers.py`: Original implementation (for reference)

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
- DIP: Depends only on `Board`'s public methods to compute availability of moves.

## GUI Implementation

The graphical interface is built using Tkinter and follows SOLID principles:

### gui/controller.py
- SRP: Manages user interactions, piece selection, move execution, and game flow.
- OCP: Can be extended with new interaction patterns without modifying existing code.
- LSP: Works with any board and player objects that implement the expected interface.
- ISP: Uses only the methods it needs from Board and Player classes.
- DIP: Depends on abstractions (Board, Player) rather than concrete implementations.

### gui/renderer.py
- SRP: Handles all visual rendering and coordinate transformations.
- OCP: Can be extended with new visual styles or rendering methods.
- LSP: Works with any board object that provides the expected data structure.
- ISP: Provides focused rendering methods without mixing concerns.
- DIP: Depends on board data structure rather than specific board implementation.

### gui/main.py
- SRP: Simple entry point that initializes the GUI application.
- OCP: Can be extended to support different window configurations or themes.
- LSP: Works with any controller that implements the expected interface.
- ISP: Minimal interface - just initializes and runs the application.
- DIP: Depends on controller abstraction rather than concrete implementation.

## Controls

### Console Version
- Select a piece: `row col` (e.g., `2 5`)
- Select destination: `row col` (e.g., `3 4`)
- Quit any time: `GG`

### GUI Version
- Select a piece: Click on the piece
- Move piece: Click on destination square
- Quit: Close the window or use window controls

## Notes

- The code intentionally keeps a small, core surface area to highlight SOLID principles without excessive abstractions.
- All input validation is done in `match.py` with clear prompts and early returns on `GG`.