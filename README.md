# Woven Monopoly
A Python command-line application to play the game of Woven Monopoly.

## Prerequisites
This application was written and tested using **Python 3.11.8**. It only uses Python standard libraries.

## Installation
To clone the repository:
```bash
git clone https://github.com/claire-ef/woven-monopoly.git
cd woven-monopoly
```
## Code Execution
To simulate the game with rolls_1.json:
```bash
python main.py data/board.json -p data/rolls_1.json
```

To simulate the game with rolls_2.json:
```bash
python main.py data/board.json -p data/rolls_2.json
```

### Viewing Game Progress
By default, the game runs quietly and outputs only the final required results. To the game progress each turn, the `-v` (verbosity) flag can be used:
* `python main.py data/board.json -p data/rolls_1.json -v`: shows the initial and ending game state
* `python main.py data/board.json -p data/rolls_1.json -v 2`: shows all player actions
* `python main.py data/board.json -p data/rolls_1.json -v 3`: shows board state at every turn

### Command-Line Options
While the game adheres to the requested rules by default, different gameplay options are
available using command-line arguments.

| Argument | Description | Example |
| :--- | :--- | :--- |
| `-r` / `--random` |Use random dice rolls instead of preset rolls. | `python main.py data/board.json -r` |
| `--initial_balance` |Change the amount of money each player starts with. | `--initial_balance 25` |
| `--rent_multiplier` | Adjust the global proportion of rent to property price. | `--rent_multiplier 0.5` |
| `--players` | Change the number of players and their names (minimal 2). | `--players Alice Bob Charlie` |

See all options with `python main.py --help`.
