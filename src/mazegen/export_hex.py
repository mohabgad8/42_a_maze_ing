"""Export in hex."""

from .maze_utils import N, E, S, W


def path_to_letters(path: list[int]) -> str:
    """Convert the path to letters.

    Args:
        path (list[int]): the path (solution)

    Returns:
        str: str of directions
    """
    out: list[str] = []
    for d in path:
        if d == N:
            out.append("N")
        elif d == E:
            out.append("E")
        elif d == S:
            out.append("S")
        elif d == W:
            out.append("W")
    return ''.join(out)


def grid_as_hex_lines(grid: list[list[int]]) -> list[str]:
    """Convert the maze in hex.

    Args:
        grid (list[list[int]]): maze

    Returns:
        list[str]: str of hex
    """
    lines: list[str] = []
    for row in grid:
        parts: list[str] = []
        for cell in row:
            hex_value = f"{cell:X}"
            parts.append(hex_value)
        line = ''.join(parts)
        lines.append(line)
    return lines


def print_grid_hex(self) -> None:
    """Print the maze in hex."""
    for line in self.grid_as_hex_lines():
        print(line)


def write_output(filename: str, grid: list[list[int]],
                 entry: tuple[int, int], exit: tuple[int, int],
                 path_letters: str) -> None:
    """Write a file with the maze, coords of entry and exit, and the path.

    Args:
        filename (str): name of the file we will create
        grid (list[list[int]]): the maze
        entry (tuple[int, int]): coordinates of entry
        exit (tuple[int, int]): coordinates of exit
        path_letters (str): he path converts in str of letters
    """
    with open(filename, "w", encoding="utf-8") as file:
        for line in grid_as_hex_lines(grid):
            file.write(line + "\n")
        file.write("\n")
        ent_x, ent_y = entry
        exit_x, exit_y = exit
        file.write(f"{ent_x},{ent_y}\n")
        file.write(f"{exit_x},{exit_y}\n")
        file.write(path_letters + "\n")
