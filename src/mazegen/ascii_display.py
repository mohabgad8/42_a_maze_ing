"""Diplay in ascii."""

from .maze_utils import N, E, S, W, has_wall
from typing import Optional


def to_ascii(grid: list[list[int]],
             blocked: set[tuple[int, int]],
             entry: tuple[int, int],
             exit: tuple[int, int],
             show_path: bool = False,
             path_cells: Optional[set[tuple[int, int]]] = None,
             design: dict[str, str] = None) -> str:
    """Write the maze and path en ascii.

    Args:
        grid (list[list[int]]): maze
        blocked (set[tuple[int, int]]): the pattern 42
        entry (tuple[int, int]): entry of the maze
        exit (tuple[int, int]): exit of the maze
        show_path (bool, optional): if we show the path. Defaults to False.
        path_cells (Optional[set[tuple[int, int]]], optional):
            the coordinates of the path. Defaults to None.

    Returns:
        str: maze convert in str
    """
    width = len(grid[0])
    height = len(grid)
    ent_x, ent_y = entry
    exit_x, exit_y = exit

    lines: list[str] = []
    top = design["corner"]
    for x in range(width):
        if has_wall(grid[0][x], N):
            top += design["ver_wall"] + design["corner"]
        else:
            top += "   " + design["corner"]
    lines.append(top)

    for y in range(height):
        mid = ""
        for x in range(width):
            if has_wall(grid[y][x], W):
                mid += design["hor_wall"]
            else:
                mid += " "
            content = "   "
            if (x, y) in blocked:
                content = design["pattern"]
            elif (x, y) == (ent_x, ent_y):
                content = design["Start"]
            elif (x, y) == (exit_x, exit_y):
                content = design["Exit"]
            elif show_path and (x, y) in path_cells:
                content = design["path"]
            mid += content
        if has_wall(grid[y][width - 1], E):
            mid += design["hor_wall"]
        else:
            mid += " "
        lines.append(mid)
        bot = design["corner"]
        for x in range(width):
            if has_wall(grid[y][x], S):
                bot += design["ver_wall"] + design["corner"]
            else:
                bot += "   " + design["corner"]
        lines.append(bot)
    return "\n".join(lines)
