"""Validations of maze."""

from collections import deque
from typing import Deque
from .solve import init_visited

from .maze_utils import N, E, S, W, DIR_X, DIR_Y, has_wall


def reachable_count_from_entry(grid: list[list[int]],
                               blocked: set[tuple[int, int]],
                               entry: tuple[int, int]) -> int:
    """Count cells visited.

    Args:
        grid (list[list[int]]): the maze
        blocked (set[tuple[int, int]]): the pattern 42
        entry (tuple[int, int]): the coordinates of the entry

    Returns:
        int: _description_
    """
    width = len(grid[0])
    height = len(grid)
    start_x, start_y = entry
    count = 1
    queue: Deque[tuple[int, int]] = deque()
    queue.append((start_x, start_y))
    visited: list[list[bool]] = init_visited(width, height)
    visited[start_y][start_x] = True
    while queue:
        x, y = queue.popleft()
        for d in (N, E, S, W):
            if has_wall(grid[y][x], d):
                continue
            new_x = x + DIR_X[d]
            new_y = y + DIR_Y[d]
            if not (0 <= new_x < width and 0 <= new_y < height):
                continue
            if visited[new_y][new_x]:
                continue
            if (new_x, new_y) in blocked:
                continue
            visited[new_y][new_x] = True
            count += 1
            queue.append((new_x, new_y))
    return count


def _check_wall_consistency(
    grid: list[list[int]],
    blocked: set[tuple[int, int]],
) -> bool:
    """Check if directions are logical with adjacent cells.

    Args:
        grid (list[list[int]]): maze
        blocked (set[tuple[int, int]]): patterm 42

    Returns:
        bool: return True or False
    """
    width = len(grid[0])
    height = len(grid)

    for y in range(height):
        for x in range(width):

            if (x, y) in blocked:
                continue

            if x + 1 < width and (x + 1, y) not in blocked:
                if has_wall(grid[y][x], E) != has_wall(grid[y][x + 1], W):
                    return False

            if y + 1 < height and (x, y + 1) not in blocked:
                if has_wall(grid[y][x], S) != has_wall(grid[y + 1][x], N):
                    return False

    return True


def _validate_outer_borders(grid: list[list[int]]) -> list[str]:
    """Check that the maze is closed.

    Args:
        grid (list[list[int]]): maze

    Returns:
        list[str]: str of errors if a wall is missing
    """
    errors: list[str] = []
    width = len(grid[0])
    height = len(grid)

    for x in range(width):
        if not has_wall(grid[0][x], N):
            errors.append(f"Missing north outer wall at ({x}, 0)")
        if not has_wall(grid[height - 1][x], S):
            errors.append(f"Missing south outer wall at ({x}, {height - 1})")

    for y in range(height):
        if not has_wall(grid[y][0], W):
            errors.append(f"Missing west outer wall at (0, {y})")
        if not has_wall(grid[y][width - 1], E):
            errors.append(f"Missing east outer wall at ({width - 1}, {y})")

    return errors


def is_open_3x3(grid: list[list[int]], top_x: int, top_y: int) -> bool:
    """Check if all the interns wall are open (E and S).

    Args:
        grid (list[list[int]]):maze
        top_x (int): _description_
        top_y (int): _description_

    Returns:
        bool: True if 3x3 open
    """
    width = len(grid[0])
    height = len(grid)
    if top_x < 0 or top_y < 0:
        return False
    if top_x + 2 >= width or top_y + 2 >= height:
        return False

    for yy in range(top_y, top_y + 3):
        for xx in range(top_x, top_x + 2):
            if has_wall(grid[yy][xx], E):
                return False

    for yy in range(top_y, top_y + 2):
        for xx in range(top_x, top_x + 3):
            if has_wall(grid[yy][xx], S):
                return False

    return True


def _validate_no_open_3x3(grid: list[list[int]]) -> list[str]:
    """Check that is not 3x3 open.

    Args:
        grid (list[list[int]]): maze

    Returns:
        list[str]: errors if 3x3 detected
    """
    errors: list[str] = []
    width = len(grid[0])
    height = len(grid)

    for top_y in range(height - 2):
        for top_x in range(width - 2):
            if is_open_3x3(grid, top_x, top_y):
                errors.append("Open 3x3 area detected at top-left "
                              f"({top_x},{top_y})")
                return errors

    return errors


def count_open_edges(grid: list[list[int]], blocked: set[tuple[int, int]]
                     ) -> int:
    """Count number of edge open.

    Args:
        grid (list[list[int]]): maze
        blocked (set[tuple[int, int]]): pattern 42

    Returns:
        int: number od edge open
    """
    width = len(grid[0])
    height = len(grid)
    edges = 0

    for y in range(height):
        for x in range(width):
            if (x, y) in blocked:
                continue

            if x + 1 < width and (x + 1, y) not in blocked:
                if not has_wall(grid[y][x], E):
                    edges += 1

            if y + 1 < height and (x, y + 1) not in blocked:
                if not has_wall(grid[y][x], S):
                    edges += 1

    return edges


def is_perfect_maze(grid: list[list[int]], blocked: set[tuple[int, int]]
                    ) -> bool:
    """Check is maze is perfect.

    Args:
        grid (list[list[int]]): maze
        blocked (set[tuple[int, int]]): pattern 42

    Returns:
        bool: True if perfect
    """
    nodes = len(grid) * len(grid[0]) - len(blocked)
    return count_open_edges(grid, blocked) == nodes - 1


def validate_maze(
    grid: list[list[int]],
    blocked: set[tuple[int, int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> list[str]:
    """Check if errors appears.

    Args:
        grid (list[list[int]]): maze
        blocked (set[tuple[int, int]]): pattern 42
        entry (tuple[int, int]): coordinates of entry
        exit (tuple[int, int]): coordinates of exit

    Returns:
        list[str]: liste of errors (empty if no errors)
    """
    errors: list[str] = []
    width = len(grid[0])
    height = len(grid)

    for name, point in (("Entry", entry), ("Exit", exit)):
        x, y = point
        if not (0 <= x < width and 0 <= y < height):
            errors.append(f"{name} out of bounds: {point}")
    if entry in blocked:
        errors.append("Entry cannot be inside 42 motif")
    if exit in blocked:
        errors.append("Exit cannot be inside 42 motif")
    if entry == exit:
        errors.append("Entry and exit must be different cells")

    errors.extend(_validate_outer_borders(grid))
    if not _check_wall_consistency(grid, blocked):
        errors.append("Inconsistent walls between adjacent cells")
    errors.extend(_validate_no_open_3x3(grid))
    if not errors:
        reachable = reachable_count_from_entry(grid, blocked, entry)
        total = width * height - len(blocked)
        if reachable != total:
            errors.append(
                f"Connectivity error: reachable cells = {reachable} / {total}"
            )
    return errors
