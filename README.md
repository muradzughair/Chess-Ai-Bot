# ♟️ Python Chess AI – Human vs AI (Minimax + Alpha-Beta Pruning)

Welcome to a Python-powered Chess game built entirely from scratch using **Pygame** for rendering and a **custom AI engine** based on the **Minimax algorithm** with **Alpha-Beta pruning**.

This project enables a **human player (White)** to compete against a **smart AI opponent (Black)**. The chess logic, movement rules, check/checkmate detection, and AI evaluation are all implemented without any external chess libraries.

---

## 🎯 Project Objectives

- Build a **fully playable chess game** from scratch using Python.
- Create an **AI opponent** that can simulate future moves and make smart decisions.
- Implement and visualize the full chess rules including legal move validation, turn-taking.
- Provide clean visuals using **Pygame**, with interactive piece selection and move highlighting.
- Structure the code to be extendable for future features like castling, game-over detection.


---

## 🧠 AI Logic Explained

The AI uses the **Minimax algorithm** enhanced with **Alpha-Beta pruning** for efficiency.

### Key AI Features:
- **Search Depth**: Up to 3 levels deep (can be configured)
- **Move Simulation**: Considers thousands of legal move sequences per turn
- **Position Evaluation**:
  - Material count using custom weights (`pawn = 100`, `queen = 900`, etc.)
  - King safety awareness
  - No use of external engines like Stockfish or chess libraries
- **Alpha-Beta Pruning**: Speeds up decision-making by avoiding unnecessary branches

---

## 🛠️ Technologies Used

| Tech        | Purpose                                  |
|-------------|------------------------------------------|
| Python      | Core language                            |
| Pygame      | Game rendering and input handling        |
| Math, Copy  | Board simulation and evaluation          |
| OOP         | Clean AI player class and board logic    |



