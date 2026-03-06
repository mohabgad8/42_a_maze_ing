*This project has been created as part of the 42 curriculum by mgad, mghitta.*

# MazeGenerator

## Description

`MazeGenerator` is responsible for generating a maze represented as a
grid of cells. The generator builds the maze using an **iterative
Depth‑First Search (DFS)** algorithm.

The result is a connected maze where every reachable cell is carved from
an initially fully walled grid.

------------------------------------------------------------------------

### Maze Representation

The maze is stored as a **2D grid of integers**.

Each cell uses **bit flags** to represent the presence of walls.

  Direction   Bit position
  ----------- --------------
  North       0
  East        1
  South       2
  West        3

Example:

    15 (1111 in binary)

means that all four walls are present.

When a wall is removed, the corresponding bit is cleared.

Example:

    open_wall(cell, E)

removes the east wall of the cell.

------------------------------------------------------------------------

### Maze Generation Algorithm

The generator uses an **iterative Depth‑First Search (DFS)** algorithm
with a stack.

The algorithm works as follows:

1.  Start from the starting cell.
2.  Mark the cell as visited.
3.  Look for unvisited neighbouring cells.
4.  Randomly choose one neighbour.
5.  Remove the wall between the two cells.
6.  Push the neighbour onto the stack.
7.  Continue exploring from this new cell.
8.  If a cell has no unvisited neighbours, backtrack using the stack.

The algorithm stops when the stack becomes empty, meaning all reachable
cells have been explored.

------------------------------------------------------------------------

### Why DFS

DFS was chosen because it naturally produces maze structures with:

-   long corridors
-   few large open spaces
-   guaranteed connectivity

The algorithm is also efficient and simple to implement.

This implementation uses an **iterative approach with an explicit
stack** instead of recursion to avoid recursion depth limits and provide
clearer control over the backtracking process.

------------------------------------------------------------------------

### Imperfect Mazes

After generating a perfect maze (a spanning tree), additional
connections can optionally be added.

This creates **imperfect mazes** containing loops, making them more
complex to solve.

Extra connections are only added if they do not create forbidden
patterns such as open **3×3 areas**.

------------------------------------------------------------------------

### Special Pattern (42)

The generator supports embedding a blocked pattern representing **"42"**
in the center of the maze.

Cells belonging to this pattern are marked as **blocked** and are never
visited during generation.

------------------------------------------------------------------------

## Instruction

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

------------------------------

## Ressources

### Algorythms:

    https://medium.com/@nacerkroudir/randomized-depth-first-search-algorithm-for-maze-generation-fb2d83702742
    https://www.datacamp.com/fr/tutorial/breadth-first-search-in-python
    https://gist.github.com/fnky/458719343aabd01cfb17a3a4f7296797
    https://www.codecademy.com/article/depth-first-search-dfs-algorithm
    https://visualize-it.github.io/maze_generation/simulation.html
    https://realpython.com/python-maze-solver/

### No empty 3x3:
    https://openclassrooms.com/forum/sujet/algorithme-de-creation-et-resolution-de-labyrinth-44515

### Display Ascii:

    https://www.asciiart.eu/ascii-maze-generator
    https://codegolf.stackexchange.com/questions/162403/render-an-ascii-maze
    https://stackoverflow.com/questions/1541763/reading-in-an-ascii-maze-into-a-2d-array

### Convert in Hex:
    https://discuss.python.org/t/how-to-convert-character-to-hexadecimal-and-back/25056/6
