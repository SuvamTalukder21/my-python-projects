# 🎮 Tic Tac Toe (Text-Based) in Python

## 📌 Overview

This is a **text-based Tic Tac Toe game** built in Python with support for:

* 👤 Human vs Human
* 🤖 Human vs AI
* 🤖 AI vs AI

The AI uses the **Minimax algorithm with Alpha-Beta pruning**, making it **unbeatable in hard mode**.

---

## 🚀 Features

* ✅ Interactive CLI-based gameplay
* ✅ Multiple player types (Human / CPU)
* ✅ Difficulty levels:

  * Easy → Random moves
  * Medium → Basic strategy
  * Hard → Minimax + Alpha-Beta (optimal play)
* ✅ Custom player names and symbols
* ✅ Score tracking
* ✅ Clean modular architecture
* ✅ Unit testing support (pytest)

---

## 🧠 AI Logic

The AI in **hard mode** uses:

* **Minimax Algorithm**

  * Simulates all possible future moves
  * Assumes opponent plays optimally

* **Alpha-Beta Pruning**

  * Skips unnecessary branches
  * Improves performance significantly

👉 Result: The AI will **never lose**

---

## 📁 Project Structure

```
tic_tac_toe/
│
├── src/
│   ├── game/
│   │   ├── board.py        # Board state, moves, display
│   │   ├── engine.py       # Game rules, win/draw logic
│   │   └── validator.py    # Move validation
│   │
│   ├── players/
│   │   ├── base.py         # Abstract player class
│   │   ├── human.py        # Human input handling
│   │   └── cpu.py          # AI logic (Minimax)
│   │
│   ├── ui/
│   │   ├── console.py      # Display output
│   │   └── input_handler.py # Input processing
│   │
│   └── utils/
│       ├── constants.py    # Symbols and game states
│       └── helpers.py      # Utility functions
│
├── tests/
│   ├── test_board.py
│   ├── test_engine.py
│   └── test_players.py
│
├── main.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1. Clone the repository

```
git clone <your-repo-url>
cd tic_tac_toe
```

### 2. Create virtual environment

```
python -m venv .venv
```

### 3. Activate environment

**Windows:**

```
.venv\Scripts\activate
```

**Mac/Linux:**

```
source .venv/bin/activate
```

### 4. Install dependencies

```
pip install -r requirements.txt
```

---

## ▶️ How to Run

```
python main.py
```

---

## 🎯 How to Play

1. Choose player types (human/cpu)
2. Select difficulty (if CPU)
3. Enter names and symbols
4. Make moves using:

   ```
   row column
   ```

   Example:

   ```
   1 2
   ```

---

## 🧪 Running Tests

```
pytest
```

---

## 🧩 Game Rules

* 3x3 grid
* Players take turns
* First to align 3 symbols wins:

  * Row
  * Column
  * Diagonal
* If grid is full → Draw

---

## 📊 Difficulty Levels

| Level  | Behavior             |
| ------ | -------------------- |
| Easy   | Random moves         |
| Medium | Basic logic          |
| Hard   | Minimax + Alpha-Beta |

---

## 🛠️ Technologies Used

* Python 3
* pytest (for testing)

---

## 🚧 Room for Improvement

Here are some ways this project can be enhanced:

### 🎮 Gameplay Enhancements

* Add **undo/redo moves**
* Add **game replay system**
* Add **move history display**

---

### 🤖 AI Improvements

* Add **difficulty tuning (depth-based AI)**
* Implement **memoization (transposition tables)**
* Add **heuristic evaluation for larger boards**

---

### 🖥️ UI Improvements

* Convert to **GUI (Tkinter / PyQt / Pygame)**
* Add **colored CLI output (rich library)**
* Add **animations**

---

### 🌐 Advanced Features

* Online multiplayer support
* REST API version of the game
* Web-based frontend (React + FastAPI)

---

### 🧪 Testing & Quality

* Increase unit test coverage
* Add integration tests
* Add CI/CD pipeline

---

## 🧠 What You Learned

This project demonstrates:

* Object-Oriented Design (OOP)
* Game loop architecture
* Input validation
* AI decision-making
* Minimax algorithm
* Alpha-Beta pruning
* Testing with pytest

---

## 📜 License

This project is open-source and free to use.

---

## 🙌 Acknowledgement

Built as part of learning **Python + Game AI fundamentals**.

---

## ⭐ Final Note

> This project is a strong foundation for building more advanced games and AI systems.

If you can build this, you’re already ahead of many beginners 🚀

---
