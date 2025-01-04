# Santorini
## CPSC 327 Pset6 - Santorini Board Game
### By Charles Sun and Peidong Chen

This project is a recreation of the **Santorini** board game, where you can play against human players, random opponents, or heuristic-based AI.

## How to Play
To start the game, run the following command in your terminal:

```bash
python3 main.py [player1] [player2] [enable_undo] [enable_score]
```
### Parameters:

- `player1`: The type of the first player. Choose from:
  - `human`: Human player
  - `heuristic`: AI with heuristic-based strategy
  - `random`: AI with random moves

- `player2`: The type of the second player. Same options as for `player1`.

- `enable_undo`: Enable or disable the undo feature. Set to:
  - `on`: Enables undo for the game.
  - `off`: Disables undo.

- `enable_score`: Enable or disable score tracking. Set to:
  - `on`: Enables score tracking.
  - `off`: Disables score tracking.

### Defaults:
If no command line arguments are provided, the game will default to:
```bash
python3 main.py human human off off
```
