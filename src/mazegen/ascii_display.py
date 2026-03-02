from .maze_utils import N, E, S, W, has_wall
from typing import Optional


def to_ascii(grid: list[list[int]],
             blocked: set[tuple[int, int]],
             entry: tuple[int, int],
             exit: tuple[int, int],
             show_path: bool = False,
             path_cells: Optional[set[tuple[int, int]]] = None,) -> str:
    width = len(grid[0])
    height = len(grid)
    ent_x, ent_y = entry
    exit_x, exit_y = exit

    lines: list[str] = []
    top = "+"
    for x in range(width):
        if has_wall(grid[0][x], N):
            top += "---" + "+"
        else:
            top += "   " + "+"
    lines.append(top)

    for y in range(height):
        mid = ""
        for x in range(width):
            if has_wall(grid[y][x], W):
                mid += "|"
            else:
                mid += " "
            content = "   "
            if (x, y) in blocked:
                content = "###"
            elif (x, y) == (ent_x, ent_y):
                content = " S "
            elif (x, y) == (exit_x, exit_y):
                content = " E "
            elif show_path and (x, y) in path_cells:
                content = " . "
            mid += content
        if has_wall(grid[y][width - 1], E):
            mid += "|"
        else:
            mid += " "
        lines.append(mid)
        bot = "+"
        for x in range(width):
            if has_wall(grid[y][x], S):
                bot += "---" + "+"
            else:
                bot += "   " + "+"
        lines.append(bot)
    return "\n".join(lines)