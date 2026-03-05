#!/usr/bin/env python3
"""Generate the maze."""


import random
from typing import Optional
from .validate import validate_maze, is_perfect_maze, is_open_3x3
from .maze_utils import (
    N, E, S, W, DIR_X, DIR_Y, OPP_WALL,
    has_wall, open_wall, get_direction_between,
)


class MazeGenerator:
    """Generate a maze.

    Raises:
        if start not in maze:
        if start in block:
        raise ValueError("incorrect value to generate maze")
        raise ValueError("Start point cannot be in 42 motif")
        RuntimeError: Generated maze is invalid
        RuntimeError: Generated maze is not perfect
        RuntimeError: Generation failed after retries
    """

    PATTERN_42 = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]
    ]

    def __init__(self, width: int, height: int,
                 entry: Optional[tuple[int, int]] = None,
                 exit: Optional[tuple[int, int]] = None,
                 perfect: bool = False,
                 seed: int = 0,
                 start_x: int = 0,
                 start_y: int = 0) -> None:
        """Initialize class.

        Args:
            width (int): width of the maze
            height (int): height of the maze
            seed (int, optional): seed for random generation. Defaults to 0.
            entry (Optional[tuple[int, int]], optional): entry of the maze.
                                                         Defaults to None.
            exit (Optional[tuple[int, int]], optional): exit of the maze.
                                                        Defaults to None.
            perfect (bool, optional): choose if maze will be perfect or not.
                                                        Defaults to False.
            start_x (int, optional): x for first case. Defaults to 0.
            start_y (int, optional): y for first case. Defaults to 0.
        """
        self.width = width
        self.height = height
        self.seed = seed
        self.perfect = perfect
        self.entry = entry if entry is not None else (0, 0)
        self.exit = exit if exit is not None else (self.width - 1,
                                                   self.height - 1)
        self.start_x = start_x
        self.start_y = start_y

        self.validate_params()

        self.rand_num_gen = random.Random(seed)
        self.grid: list[list[int]] = self.make_grid()
        self.blocked: set[tuple[int, int]] = set()
        self.place_42()

    def validate_params(self) -> None:
        """Validate constructor parameters."""

        if not isinstance(self.width, int) or not isinstance(self.height, int):
            raise TypeError("WIDTH and HEIGHT must be integers")

        if self.width <= 0 or self.height <= 0:
            raise ValueError(
                f"WIDTH and HEIGHT must be > 0 "
                f"(got width={self.width}, height={self.height})"
            )

        for name, point in (
            ("ENTRY", self.entry),
            ("EXIT", self.exit),
            ("START", (self.start_x, self.start_y)),
        ):
            x, y = point
            if not (0 <= x < self.width and 0 <= y < self.height):
                raise ValueError(f"{name} out of bounds: {point}")

        if self.entry == self.exit:
            raise ValueError("ENTRY and EXIT must be different")

    def make_grid(self) -> list[list[int]]:
        """Make the grid.

        Args:
            width (int): width of the grid
            height (int): height of the gride

        Returns:
            list[list[int]]: grid in 2D
        """
        grid: list[list[int]] = []
        for y in range(self.height):
            row: list[int] = []
            for x in range(self.width):
                row.append(15)
            grid.append(row)
        return grid

    def in_bounds(self, x: int, y: int) -> bool:
        """Check in the cell is in the maze.

        Args:
            x (int): x of the cell
            y (int): y of the cell
            width (int): width of the maze
            height (int): height of the maze

        Returns:
            bool: true ou false
        """
        if x < 0:
            return False
        if x >= self.width:
            return False
        if y < 0:
            return False
        if y >= self.height:
            return False
        return True

    def unvisited_neighbors(self, x: int, y: int,
                            visited: list[list[bool]]
                            ) -> list[tuple[int, int]]:
        """Create list of unvisited neighbors.

        Args:
            x (int): x of the cell
            y (int): y of the cell
            visited (list[list[bool]]):list of visited cells

        Returns:
            list[tuple[int, int]]: list in 2 Dof unvisited neighbors
        """
        neighbors: list[tuple[int, int]] = []
        for d in (N, E, S, W):
            new_x = x + DIR_X[d]
            new_y = y + DIR_Y[d]
            if not self.in_bounds(new_x, new_y):
                continue
            if visited[new_y][new_x]:
                continue
            if (new_x, new_y) in self.blocked:
                continue
            neighbors.append((new_x, new_y))
        return neighbors

    def open_between(self, x: int, y: int,
                     new_x: int, new_y: int) -> None:
        """Open the walls between 2 cells.

        Args:
            x (int): x of the cell
            y (int): y of the cell
            new_x (int): x of the cell with wich we compare
            new_y (int):x of the cell with wich we compare
        """
        direction = get_direction_between(x, y, new_x, new_y)
        self.grid[y][x] = open_wall(self.grid[y][x], direction)
        self.grid[new_y][new_x] = open_wall(self.grid[new_y][new_x],
                                            OPP_WALL[direction])

    def init_visited(self, width: int, height: int) -> list[list[bool]]:
        """Initialize cell not visited.

        Args:
            width (int): width of the grid
            height (int): height of the grid

        Returns:
            list[list[bool]]: list in 2D of false (cells non visited)
        """
        visited: list[list[bool]] = []
        for y in range(height):
            row: list[bool] = []
            for x in range(width):
                row.append(False)
            visited.append(row)
        return visited

    def wall_open_hor(self, x: int, y: int) -> bool:
        """Check if a cell is open as it East side.

        Args:
            x (int): x of the cell
            y (int): y of the cell

        Returns:
            bool: True or False
        """
        return not has_wall(self.grid[y][x], E)

    def wall_open_ver(self, x: int, y: int) -> bool:
        """Check if a cell is open as it South side.

        Args:
            x (int): x of the cell
            y (int): y of the cell

        Returns:
            bool: True or False
        """
        return not has_wall(self.grid[y][x], S)

    def would_create_open_3x3(self, x: int, y: int, new_x: int, new_y: int
                              ) -> bool:
        """Check if action would create 3x3.

        Args:
            x (int): x of the cell
            y (int): y of the cell
            new_x (int): x of the cell with wich we compare
            new_y (int):x of the cell with wich we compare

        Returns:
            bool: True or False
        """
        direction = get_direction_between(x, y, new_x, new_y)
        old_a = self.grid[y][x]
        old_b = self.grid[new_y][new_x]
        self.grid[y][x] = open_wall(self.grid[y][x], direction)
        self.grid[new_y][new_x] = open_wall(self.grid[new_y][new_x],
                                            OPP_WALL[direction])
        min_x = min(x, new_x)
        min_y = min(y, new_y)

        created = False
        for top_y in range(min_y - 2, min_y + 1):
            for top_x in range(min_x - 2, min_x + 1):
                if is_open_3x3(self.grid, top_x, top_y):
                    created = True
                    break
            if created:
                break
        self.grid[y][x] = old_a
        self.grid[new_y][new_x] = old_b
        return created

    def place_42(self) -> int:
        """Place the 42 at center and add it to blocked set.

        Returns:
            int: number af case of the pattern
        """
        self.blocked.clear()
        pattern_width = len(self.PATTERN_42[0])
        pattern_height = len(self.PATTERN_42)
        if self.width < pattern_width + 2 or self.height < pattern_height + 2:
            print("Warning: maze too small to place 42 pattern, skipping.")
            return 0
        top_x = (self.width - pattern_width) // 2
        top_y = (self.height - pattern_height) // 2
        for dy in range(pattern_height):
            for dx in range(pattern_width):
                if self.PATTERN_42[dy][dx] == 1:
                    x = top_x + dx
                    y = top_y + dy
                    self.blocked.add((x, y))
                    self.grid[y][x] = 15
        return len(self.blocked)

    def generate_once(self) -> bool:
        """Try generate maze.

        Raises:
            ValueError: raise if start cell not in maze
            ValueError: raise if start cell not in pattern

        Returns:
            bool: True or False
        """
        visited = self.init_visited(self.width, self.height)
        for x, y in self.blocked:
            visited[y][x] = True
            if not self.in_bounds(self.start_x, self.start_y):
                raise ValueError("incorrect value to generate maze")
            if (self.start_x, self.start_y) in self.blocked:
                raise ValueError("Start point cannot be in 42 motif")
        stack: list[tuple[int, int]] = [(self.start_x, self.start_y)]
        visited[self.start_y][self.start_x] = True

        while stack:
            x, y = stack[-1]
            neighbors = self.unvisited_neighbors(x, y, visited)
            if not neighbors:
                stack.pop()
                continue
            candidates = []
            for new_x, new_y in neighbors:
                if not self.would_create_open_3x3(x, y, new_x, new_y):
                    candidates.append((new_x, new_y))
            if not candidates:
                stack.pop()
                continue
            new_x, new_y = self.rand_num_gen.choice(candidates)
            self.open_between(x, y, new_x, new_y)
            visited[new_y][new_x] = True
            stack.append((new_x, new_y))

        for row in visited:
            if not all(row):
                return False
        return True

    def reset(self, attempt: int) -> None:
        """Reset the grid after trying to create maze.

        Args:
            attempt (int): the number of the try
        """
        self.grid = self.make_grid()
        self.rand_num_gen = random.Random(self.seed + attempt * 7979)
        for (x, y) in self.blocked:
            self.grid[y][x] = 15

    def _add_extra_connections(self) -> None:
        """Add connections to create imperfect maze."""
        opened = 0
        cells_to_open = self.width * self.height // 10
        cells = [
            (x, y)
            for y in range(self.height)
            for x in range(self.width)
            if (x, y) not in self.blocked
        ]
        tries = 0
        max_tries = cells_to_open * 50
        while opened < cells_to_open and tries < max_tries:
            tries += 1
            x, y = self.rand_num_gen.choice(cells)
            d = self.rand_num_gen.choice((N, E, S, W))

            new_x = x + DIR_X[d]
            new_y = y + DIR_Y[d]
            if not self.in_bounds(new_x, new_y):
                continue
            if has_wall(self.grid[y][x], d):
                if not self.would_create_open_3x3(x, y, new_x, new_y):
                    self.open_between(x, y, new_x, new_y)
                    opened += 1

    def generate(self, max_attempts=200) -> list[list[int]]:
        """Generate maze.

        Args:
            (max_attempts (int, optional): max tries to build maze.
            Defaults to 200.)

        Raises:
            RuntimeError: generate maze failed
            RuntimeError: generate maze failed
            RuntimeError: generate maze failed after retries

        Returns:
            list[list[int]]: maze
        """
        for attempt in range(max_attempts):
            self.reset(attempt)
            if self.generate_once():
                if not self.perfect:
                    self._add_extra_connections()
                errors = validate_maze(self.grid, self.blocked, self.entry,
                                       self.exit)
                if errors:
                    raise RuntimeError("Generated maze is invalid:\n"
                                       "\n".join(errors))
                if self.perfect and not is_perfect_maze(self.grid,
                                                        self.blocked):
                    raise RuntimeError("Generated maze is not perfect.")
                return self.grid
        raise RuntimeError("Generation failed after retries")
