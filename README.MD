# Hex Game with AI Players

This project is a Python implementation of the [Hex board game](https://en.wikipedia.org/wiki/Hex_(board_game)), a strategy game where players aim to connect opposite sides of a hexagonal grid. The implementation includes human and AI players, multiple heuristic evaluation functions, and both text-based and graphical (Tkinter) interfaces. Key features include advanced AI algorithms like Minimax with alpha-beta pruning and Monte Carlo Tree Search (MCTS), customizable board sizes, and support for the swap rule.

## Demo Video

[Click Here](https://drive.google.com/drive/u/0/folders/1osukCqy0JtV_u8_tOhG3eJp8p_KE6TBI)

*Placeholder: []*

## Installation

### Prerequisites
- **Python**: Version 3.6 or higher.
- **Tkinter**: Usually included with Python; ensure it's installed (e.g., `sudo apt-get install python3-tk` on Ubuntu).
- **Image Assets**: The GUI requires three PNG files (`blank.png`, `red.png`, `blue.png`) for board visualization.

### Setup
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/rayyan-merchant/hex-game.git
   cd hex-game
   ```

2. **Install Dependencies**:
   No external libraries are required beyond Python’s standard library and Tkinter. If Tkinter is missing, install it:
   ```bash
   sudo apt-get install python3-tk  # Ubuntu/Debian
   brew install python-tk           # macOS
   ```

3. **Prepare Image Assets**:
   - The GUI expects `blank.png`, `red.png`, and `blue.png` in the project root directory.
   - If these are missing, create simple 35x35 pixel images:
     - `blank.png`: White background (empty cell).
     - `red.png`: Red hexagon (Player 2 piece).
     - `blue.png`: Blue hexagon (Player 1 piece).
   - Alternatively, contact the repository owner for the original assets.

## Usage

Run the game using:
```bash
python main.py
```

### Configuration
- **GUI or Text Mode**: At startup, choose whether to use the graphical interface (y/n).
- **Presets**: Select a preset (1–5) for pre-configured games or 0 for custom settings:
  - **Preset 1**: 11x11 board, two AlphaBetaPlayers with ShortestPathHeuristic and ChargeHeuristic sorting.
  - **Preset 2**: 11x11 board, two AlphaBetaPlayers with TwoDistanceHeuristic.
  - **Preset 3**: 11x11 board, AlphaBetaPlayer (ShortestPathHeuristic) vs. AlphaBetaPlayer (TwoDistanceHeuristic).
  - **Preset 4**: 7x7 board, GuiPlayer vs. AlphaBetaPlayer (TwoDistanceHeuristic).
  - **Preset 5**: 11x11 board, GuiPlayer vs. AlphaBetaPlayer (TwoDistanceHeuristic).
- **Custom Settings**: Specify board size, swap rule (y/n), and player types (Text, GUI, Random, AlphaBeta, MonteCarlo, or ChargeHeuristic).

### Playing the Game
- **Text Mode**: Input moves as `row,col` (e.g., `3,4`), `resign`, or `undo`. The board is displayed as ASCII art.
- **GUI Mode**: Click cells to place pieces, or use the Resign/Undo buttons. The current turn or winner is shown at the bottom.
- **AI Players**: Configure AlphaBetaPlayer with heuristics, search depth, and time limits. MonteCarloPlayer uses random rollouts (less effective).

## File Structure

- **`main.py`**: Entry point; handles game initialization, user input, and game loop (text or GUI).
- **`heuristic.py`**: Defines evaluation functions for AI:
  - `ShortestPathHeuristic`: Measures shortest path to connect sides.
  - `TwoDistanceHeuristic`: Considers second-best path options for robustness.
  - `ChargeHeuristic`: Experimental heuristic treating stones as charges to find contested moves.
- **`player.py`**: Implements player classes:
  - Human: `TextPlayer` (terminal input), `GuiPlayer` (GUI input).
  - AI: `RandomPlayer`, `AlphaBetaPlayer` (Minimax with alpha-beta), `MonteCarloPlayer` (MCTS), `ChargeHeuristicPlayer`.
- **`GUI.py`**: Provides a Tkinter-based graphical interface with clickable cells and resign/undo buttons.
- **`board.py`**: Defines `HexBoard`, managing game state, move validation, win detection, and ASCII board display.

## Features

- **Game Mechanics**:
  - Supports any board size (default 11x11).
  - Implements the swap rule, allowing Player 2 to mirror Player 1’s first move.
  - Efficient win detection via pathfinding.
- **AI Algorithms**:
  - **AlphaBetaPlayer**: Uses Minimax with alpha-beta pruning, transposition tables, killer moves, and heuristic-based move sorting.
  - **MonteCarloPlayer**: Pure MCTS with random rollouts (experimental, less effective).
  - **ChargeHeuristicPlayer**: Selects moves based on contested positions (experimental).
- **Heuristics**:
  - Path-based (`ShortestPathHeuristic`, `TwoDistanceHeuristic`) for evaluating connection strength.
  - Charge-based (`ChargeHeuristic`) for identifying strategic moves.
- **Interfaces**:
  - Text-based with ASCII board and debug output.
  - GUI with Tkinter, showing colored hexagons and turn/winner messages.

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature/your-feature`).
3. Commit changes (`git commit -m "Add your feature"`).
4. Push to the branch (`git push origin feature/your-feature`).
5. Open a pull request with a clear description of your changes.

Please ensure code follows PEP 8 style guidelines and includes comments for clarity. Focus areas for contributions:
- Improving `MonteCarloPlayer` with heuristic-guided rollouts.
- Optimizing `AlphaBetaPlayer` for larger boards.
- Enhancing the GUI (e.g., highlighting winning paths).
- Adding automated tests for AI performance.

## License

This project is licensed under the CC0 License. See the [LICENSE](LICENSE) file for details.
