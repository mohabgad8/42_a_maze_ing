*This project has been created as part of the 42 curriculum by mgad, mghitta.*

# A-Maze-ing 🌀

## Description

A-Maze-ing is a procedural maze generator and solver built entirely in Python, with no external dependencies. The program reads a configuration file, generates a perfect maze using a depth-first search (recursive backtracker) algorithm, solves it with BFS to find the shortest path, and displays the result in the terminal with ANSI colors and a live generation animation.

The maze always embeds a hidden **"42"** pattern formed by fully closed cells, visible in the terminal rendering. The generated maze and its solution are saved to an output file in a hexadecimal bitmask format.

**Key features:**
- Procedural maze generation with DFS (perfect mazes — exactly one path between any two cells)
- BFS solver returning the optimal shortest path
- Live terminal animation during generation
- Interactive menu: regenerate, show/hide path, rotate colors, quit
- Saves maze and solution to a file
- Hidden "42" pattern embedded in every maze
- Reusable `mazegen` module installable via pip

---

## Instructions

### Requirements

- Python 3.10 or later

No external Python dependencies are required to run the program.

### Installation

```bash
# Clone the repository
git clone <repo_url> a_maze_ing
cd a_maze_ing

# (Optional) Create a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install linting tools
make install
```

### Run

```bash
make        # Run with default config.txt
# or
python3 a_maze_ing.py config.txt
```

### Other Makefile targets

```bash
make debug          # Run with pdb debugger
make lint           # Run flake8 + mypy (standard)
make lint-strict    # Run flake8 + mypy --strict
make clean          # Remove __pycache__, .mypy_cache, etc.
make build          # Build the pip-installable package
make install-pkg    # Build and install the package locally
```

---

## Configuration File

The configuration file must contain one `KEY=VALUE` pair per line. Lines starting with `#` are comments and are ignored.

### Mandatory keys

| Key | Description | Example |
|-----|-------------|---------|
| `WIDTH` | Number of columns in the maze | `WIDTH=20` |
| `HEIGHT` | Number of rows in the maze | `HEIGHT=15` |
| `ENTRY` | Entry cell coordinates (x,y) | `ENTRY=0,0` |
| `EXIT` | Exit cell coordinates (x,y) | `EXIT=19,14` |
| `OUTPUT_FILE` | Path to the output file | `OUTPUT_FILE=maze.txt` |
| `PERFECT` | Whether to generate a perfect maze | `PERFECT=True` |

### Optional keys

| Key | Description | Example |
|-----|-------------|---------|
| `SEED` | Random seed for reproducibility | `SEED=42` |

### Example `config.txt`

```
WIDTH=20
HEIGHT=15
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

---

## Algorithm

---

## Interactive Menu

Once the maze is generated and displayed, the following menu is available:

| Option | Action |
|--------|--------|
| `1` | Regenerate a new maze |
| `2` | Toggle the solution path display |
| `3` | Cycle through terminal colors |
| `4` | Quit |

---

## Reusable Module

---

## Team & Project Management

---

## Resources

---