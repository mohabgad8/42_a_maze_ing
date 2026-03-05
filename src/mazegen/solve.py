"""solve the maze."""

from collections import deque
from typing import Deque

from .maze_utils import N, E, S, W, DIR_X, DIR_Y, has_wall


def init_visited(width: int, height: int) -> list[list[bool]]:
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


def solve(grid: list[list[int]],
          blocked: set[tuple[int, int]],
          entry: tuple[int, int],
          exit: tuple[int, int],) -> list[int]:
    """Solve the maze with bfs.

    Args:
        grid (list[list[int]]): maze
        blocked (set[tuple[int, int]]): pattern 42
        entry (tuple[int, int]): entry of maze
        exit (tuple[int, int]): exit of maze

    Returns:
        list[int]: the path from entry to exit
    """
    width = len(grid[0])
    height = len(grid)
    start_x, start_y = entry
    end_x, end_y = exit
    queue: Deque[tuple[int, int]] = deque()
    queue.append((start_x, start_y))
    visited: list[list[bool]] = init_visited(width, height)
    visited[start_y][start_x] = True
    parent: dict[tuple[int, int], tuple[int, int, int]] = {}
    while queue:
        x, y = queue.popleft()
        if (x, y) == (end_x, end_y):
            path: list[int] = []
            current = (end_x, end_y)
            start = (start_x, start_y)
            while current != start:
                par_x, par_y, d_from_parent = parent[current]
                path.append(d_from_parent)
                current = (par_x, par_y)
            path.reverse()
            return path
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
            parent[(new_x, new_y)] = (x, y, d)
            queue.append((new_x, new_y))
    return []


def path_to_cells(entry: tuple[int, int], path: list[int]) -> set[tuple[int]]:
    """Convert the path in coordinates.

    Args:
        entry (_type_): _description_
        path (_type_): _description_

    Returns:
        _type_: _description_
    """
    x, y = entry
    cells = {(x, y)}
    for d in path:
        x += DIR_X[d]
        y += DIR_Y[d]
        cells.add((x, y))
    return cells


def path_to_ordered_cells(
    entry: tuple[int, int],
    path: list[int]
) -> list[tuple[int, int]]:
    """
    Convert the path in coordinates.
    Returns a list instead of a set to be able to stop at each case.
    """

    x, y = entry
    cells = [(x, y)]
    for d in path:
        x += DIR_X[d]
        y += DIR_Y[d]
        cells.append((x, y))
    return cells
