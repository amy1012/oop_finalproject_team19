# OOP Programming Group Project

## Part 3

This project is a **Python-based Tic-Tac-Toe game** implemented with a clear modular design. The system separates **game logic**, **environment state**, **player strategies (human / AI)**, and **GUI interaction**, making it easy to understand, extend, and maintain.

Key features include:

* A clean **environment abstraction** that manages the board state, turn-taking, legality checks, and win/draw conditions.
* Multiple **player types**, including human players and AI players.
* An AI opponent implemented using the **Minimax algorithm**, allowing the computer to play optimally.
* A simple **GUI interface** for interactive play.

This project is suitable for learning:

* Object-Oriented Programming (OOP)
* Game state modeling
* Basic AI decision-making (Minimax)
* Separation of concerns in software design

---

## Project Structure

```text
.
├── environment.py     # Game environment: board state, rules, win/draw logic
├── players.py         # Player definitions (Human, AI / Minimax player)
├── game_manager.py    # Game flow control and coordination
├── gui_main.py        # GUI entry point
└── README.md          # Project documentation
```

### File Responsibilities

* **environment.py**
  Defines the `TicTacToeEnvironment` class, which is responsible for:

  * Storing and resetting the board state
  * Tracking the current player
  * Validating actions
  * Determining win, loss, or draw conditions

* **players.py**
  Implements different player behaviors, including:

  * Human player input handling
  * AI player logic based on the Minimax algorithm

* **game_manager.py**
  Acts as the controller of the game, coordinating:

  * Turns between players
  * Interaction between players and the environment
  * Game termination conditions

* **gui_main.py**
  Provides the graphical user interface and serves as the main entry point for running the game.

---

## How to Run

### 1. Environment Requirements

* Python **3.8 or above**

### 2. Install Dependencies

This project only relies on **standard Python libraries**. No additional third-party packages are required.

If you want to be safe, you can still create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # macOS / Linux
# venv\\Scripts\\activate  # Windows
```

### 3. Run the Game

Execute the GUI entry file:

```bash
python gui_main.py
```

After running the command, the game window will open and you can start playing Tic-Tac-Toe against another player or the AI.

---

## Dependencies

This project uses only **Python built-in libraries**, including:

* `typing` – for type hints and improved code readability
* Standard GUI libraries used in `gui_main.py` (depending on implementation)

No external packages are required.

---

## Notes

* The AI player uses the **Minimax algorithm**, ensuring optimal play.
* The modular structure makes it easy to:

  * Add new AI strategies
  * Replace the GUI with a CLI version
  * Extend the game to larger board sizes

This project is designed for educational purposes and OOP practice.
