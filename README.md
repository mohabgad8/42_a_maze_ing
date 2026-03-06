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

## Project Structure

```
.
├── a_maze_ing.py
├── config.txt
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
└── src
    ├── mazegen
    │   ├── __init__.py
    │   ├── ascii_display.py
    │   ├── export_hex.py
    │   ├── generator.py
    │   ├── maze_utils.py
    │   ├── solve.py
    │   ├── themes.py
    │   └── validate.py
    └── parsing
        ├── __init__.py
        ├── config_helper.py
        └── config.py
```

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

### Generation — Depth-First Search (DFS)

We chose DFS for maze generation because it naturally builds a fully connected structure by exploring one path deeply before backtracking. This produces a spanning-tree-like structure, ensuring all reachable cells are connected.

**Why DFS:**
- Guarantees full connectivity between all accessible cells
- Naturally produces long, winding corridors — characteristic of classic mazes
- Simple to implement and debug

**Implementation choice:** We used an iterative approach with an explicit stack rather than recursion, which avoids potential recursion depth limits and makes the backtracking process explicit and easier to control.

---

### Solving — Breadth-First Search (BFS)

We chose BFS to solve the maze because it guarantees finding the **shortest path** between entry and exit in an unweighted grid.

**Why BFS:**
- Unlike DFS, BFS explores level by level — the first time the exit is reached is always via the shortest path
- Well-suited for unweighted grid pathfinding
- Straightforward to implement iteratively using a queue

---

## Output File Format

The output file contains:

1. One line per row of the maze. Each cell is encoded as a single uppercase hexadecimal digit representing a 4-bit bitmask of its closed walls.
2. A blank line separator.
3. The entry coordinates (`x,y`).
4. The exit coordinates (`x,y`).
5. The shortest path from entry to exit as a string of direction letters (`N`, `E`, `S`, `W`).

### Wall bitmask encoding

| Bit | Value | Wall direction |
|-----|-------|---------------|
| 0 (LSB) | 1 | North |
| 1 | 2 | East |
| 2 | 4 | South |
| 3 | 8 | West |

A set bit (1) means the wall is **closed**. A clear bit (0) means the wall is **open**.

**Example:** `F` (binary `1111`) = all four walls closed. `6` (binary `0110`) = East and South walls closed, North and West open.

### Example output

```
9515...
EBAB...
...

0,0
19,14
SSEENNWWEE...
```

---

## Interactive Menu

Once the maze is generated and displayed, the following menu is available:

| Option | Action |
|--------|--------|
| `1` | Re-generate a new maze |
| `2` | Toggle the solution path display |
| `3` | Cycle through terminal colors |
| `4` | Quit |

---

## Reusable Module

The maze generation logic is packaged as a standalone, reusable Python module called `mazegen`. It can be installed via pip from the built package at the root of the repository.

### Installation

```bash
pip install mazegen-1.0.0-py3-none-any.whl
# or
pip install mazegen-1.0.0.tar.gz
```

### Building the package from source

```bash
python3 -m pip install --upgrade build
python3 -m build
# Output: dist/mazegen-1.0.0-py3-none-any.whl and dist/mazegen-1.0.0.tar.gz
```

### Usage example
```python
from mazegen.generator import MazeGenerator
from mazegen.solve import solve, path_to_cells

# Instantiate the generator
maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
    perfect=True,
    seed=42        # Optional: omit or set 0 for random
)

# Generate the maze
grid = maze.generate()

# Access the grid
grid = maze.grid        # list[list[int]], bitmask per cell
blocked = maze.blocked  # set of (x, y) forming the "42" pattern

# Solve the maze
path = solve(maze.grid, maze.blocked, maze.entry, maze.exit)

# Get path as set of coordinates
cells = path_to_cells(maze.entry, path)
```

### Custom parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `width` | `int` | Number of columns |
| `height` | `int` | Number of rows |
| `entry` | `tuple[int, int]` | Entry cell as (x, y) |
| `exit` | `tuple[int, int]` | Exit cell as (x, y) |
| `perfect` | `bool` | Perfect maze (one unique path). Default `False` |
| `seed` | `int` | Random seed. Default `0` |

### Accessing the maze structure

After calling `maze.generate()`:

- `maze.grid` — `list[list[int]]`: full grid, bitmask of walls per cell (0–15)
- `maze.blocked` — `set[tuple[int, int]]`: cells forming the "42" pattern
- `maze.entry` — `tuple[int, int]`: entry coordinates
- `maze.exit` — `tuple[int, int]`: exit coordinates
- `maze.width`, `maze.height` — dimensions

`solve()` returns a `list[int]` of directions, or `[]` if no path exists.

---

## Team & Project Management

### Team

| Login   |                      Role                             |
|---------|-------------------------------------------------------|
| `mgad`  |Documentation, parsing, validation, packaging, Makefile, README, merging and debugging
|`mghitta`| Research, DFS, BFS, constraints 3x3, adding pattern 42, output.txt, ascii display, toml

### Planning

**Anticipated planning:**
- Day 1: Documentation
- Day 2: MazeGenerator creation
- Day 3: Parsing, DFS and BFS implementation
- Day 4: constraints (no open 3x3, check perfect_maze, check opening wall, etc...)
- Day 5: Validation, output.txt, adding 42 pattern
- Day 6: Ascii display, Parsing and generator tests
- Day 7: Packaging, Makefile and README
- Day 8: Merging and solving conflicts
- Day 9: Final tests

**How it evolved:**
The implementation of the different algorithms was quite simple due to the various documentation consulted. What took more time than planned was the parsing and validation parts for both config.txt and the generator and the gestion of the contraints (open no 3x3, perfect/ not perfect, check opening wall).

### What worked well

- Implementing algorithms
- Planning and dividing the work

### Tools used

- **Python 3.10+** — main language
- **flake8** — style linting (PEP 8)
- **mypy** — static type checking
- **pdb** — debugging
- **build** — Python package builder
- **Claude (Anthropic)** — used as an AI assistant (see Resources section)

---

## Resources

### References

- [Maze generation algorithms — Wikipedia](https://en.wikipedia.org/wiki/Maze_generation_algorithm)
- [Recursive backtracker explanation — Jamis Buck's blog](https://weblog.jamisbuck.org/2010/12/27/maze-generation-recursive-backtracker)
- [BFS shortest path — Wikipedia](https://en.wikipedia.org/wiki/Breadth-first_search)
- [Python type hints — PEP 484](https://peps.python.org/pep-0484/)
- [PEP 257 — Docstring conventions](https://peps.python.org/pep-0257/)
- [flake8 documentation](https://flake8.pycqa.org/)
- [mypy documentation](https://mypy.readthedocs.io/)
- [Python packaging guide](https://packaging.python.org/en/latest/tutorials/packaging-projects/)
- [Randomized DFS for maze generation — Medium](https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742)
- [Breadth-first search in Python — DataCamp](https://www.datacamp.com/fr/tutorial/breadth-first-search-in-python)
- [ANSI escape codes reference — GitHub Gist](https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797)
- [Depth-first search algorithm — Codecademy](https://www.codecademy.com/article/depth-first-search-dfs-algorithm)
- [Maze generation visualizer](https://visualize-it.github.io/maze_generation/simulation.html)
- [Python maze solver — Real Python](https://realpython.com/python-maze-solver/)
- [Maze generation algorithm discussion — OpenClassrooms](https://openclassrooms.com/forum/sujet/algorithme-de-creation-et-resolution-de-labyrinth-44515)
- [ASCII maze generator](https://www.asciiart.eu/ascii-maze-generator)
- [Rendering an ASCII maze — Code Golf Stack Exchange](https://codegolf.stackexchange.com/questions/162403/render-an-ascii-maze)
- [Reading ASCII maze into 2D array — Stack Overflow](https://stackoverflow.com/questions/1541763/reading-in-an-ascii-maze-into-a-2d-array)
- [Converting characters to hexadecimal in Python — Python Discuss](https://discuss.python.org/t/how-to-convert-character-to-hexadecimal-and-back/25056/6)

### Sharing with students

We exchange a lot with jpik, because we were doing the same part of our project, even if we took different paths to realise it, and also with nmertens for design. Thanks to nthys, pfauveau and b who gives us a very good review (by testing) and advices.

### AI usage

**Claude (Anthropic)** was used during this project for the following tasks:

- **Debugging:** Identifying issues in the ANSI cursor positioning logic for the animation (the `\033[{n}A` escape sequence to move the cursor up by N lines).
- **Type annotations:** Reviewing function signatures to ensure mypy compliance, particularly around `Optional` types and generic containers.
- **README:** Assistance in structuring and writing this README to meet the subject's requirements.

**ChatGPT (OpenAI)**

- **Test** Provides tests for checking the constraints 3x3.

---