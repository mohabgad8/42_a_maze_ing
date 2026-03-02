from .maze_utils import N, E, S, W


def path_to_letters(path: list[int]) -> str:
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
    for line in self.grid_as_hex_lines():
        print(line)


def write_output(filename: str, grid, entry, exit, path_letters: str) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        for line in grid_as_hex_lines(grid):
            file.write(line + "\n")
        file.write("\n")
        ent_x, ent_y = entry
        exit_x, exit_y = exit
        file.write(f"{ent_x},{ent_y}\n")
        file.write(f"{exit_x},{exit_y}\n")
        file.write(path_letters + "\n")