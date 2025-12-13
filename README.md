# OOP Programming Group Project 

## Project Overview

### Part 3: Tic-Tac-Toe (GUI and AI)

This project implements a fully modular **Tic-Tac-Toe (井字棋)** game using object-oriented design principles.

The system is carefully structured to separate responsibilities, including:

* Game environment and rules
* Player strategies (Human and AI)
* Game flow control
* Graphical user interface (GUI)

This design improves code readability, maintainability, and extensibility, and demonstrates proper use of OOP concepts.

### Supported Game Modes

* Human vs Human
* Human vs AI
* AI vs AI

### AI Difficulty Levels

* **Easy**: Random move selection
* **Medium**: Rule-based strategy
* **Hard**: Minimax algorithm for optimal decision-making

The graphical user interface is implemented using **tkinter**, allowing users to interactively select game modes and difficulty levels.

---

## Project Structure

```text
.
├── environment.py      # Tic-Tac-Toe environment (board state, rules, win/draw checking)
├── players.py          # Player implementations (Human and AI players)
├── game_manager.py     # Game flow control and mode/difficulty management
├── gui_main.py         # Graphical user interface entry point
└── README.md
```

---

## How to Run

1. Make sure **Python 3** is installed on your system.
2. Open a terminal in the project directory.
3. Run the following command:

```bash
python gui_main.py
```

After execution, a GUI window will open, allowing the user to select the game mode and AI difficulty, and then play the game interactively.

---

## Dependencies

This project uses **only Python standard libraries**:

* `tkinter`
* `random`
* `typing`
* `abc`

No additional package installation is required.

---

## Contribution List

* **Part 1 & Part 2 :**
  陳冠穎

* **Part 3 :**
  莊尹安、王芊婷
