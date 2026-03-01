#!/usr/bin/env python3

import random
from collections import deque
from typing import Deque


N, E, S, W = 0, 1, 2, 3
# comment on se déplace dans la grille
DIR_X = {N: 0, E: 1, S: 0, W: -1}
DIR_Y = {N: -1, E: 0, S: 1, W: 0}
# aller à l'est: (x + 1, y)
# aller au nord: (x, y - 1)
OPP_WALL = {N: S, E: W, S: N, W: E}


class MazeGenerator:
    PATTERN_42 = [
        [1, 0, 0, 0, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 0, 1, 1, 1],
        [0, 0, 1, 0, 1, 0, 0],
        [0, 0, 1, 0, 1, 1, 1]
    ]

    def __init__(self, width: int, height: int, seed: int = 0,
                 start_x: int = 0, start_y: int = 0):
        self.width = width
        self.height = height
        self.seed = seed
        self.start_x = start_x
        self.start_y = start_y

        self.rand_num_gen = random.Random(seed)
        self.grid: list[list[int]] = self.make_grid(width, height)
        self.entry: tuple[int, int] = (0, 0)
        self.exit: tuple[int, int] = (width - 1, height - 1)
        self.blocked: set[tuple[int, int]] = set()
        self.place_42()

    @staticmethod
    def has_wall(cell: int, d: int) -> bool:
        return ((cell >> d) & 1) == 1

    @staticmethod
    def open_wall(cell: int, d: int) -> int:
        bitmask = 1 << d  # créer un bit à 1 à la position d
        inverted_mask = ~bitmask  # on invesve
        new_cell = cell & inverted_mask  # on enlève ce bit dans cell
        return new_cell

    @staticmethod
    def make_grid(width: int, height: int) -> list[list[int]]:
        grid: list[list[int]] = []
        for y in range(height):
            row: list[int] = []
            for x in range(width):
                row.append(15)
            grid.append(row)
        return grid

    @staticmethod
    def init_visited(width: int, height: int) -> list[list[bool]]:
        visited: list[list[bool]] = []
        for y in range(height):
            row: list[bool] = []
            for x in range(width):
                row.append(False)
            visited.append(row)
        return visited

    @staticmethod
    def in_bounds(x: int, y: int, width: int, height: int) -> bool:
        if x < 0:
            return False
        if x >= width:
            return False
        if y < 0:
            return False
        if y >= height:
            return False
        return True

    def unvisited_neighbors(self, x: int, y: int,
                            visited: list[list[bool]]
                            ) -> list[tuple[int, int]]:
        neighbors: list[tuple[int, int]] = []
        for d in (N, E, S, W):
            new_x = x + DIR_X[d]
            new_y = y + DIR_Y[d]
            if not self.in_bounds(new_x, new_y, self.width, self.height):
                continue
            if visited[new_y][new_x]:
                continue
            if (new_x, new_y) in self.blocked:
                continue
            neighbors.append((new_x, new_y))
        return neighbors

    def get_direction_between(self, x: int, y: int, new_x: int, new_y: int
                              ) -> int:
        move_x = new_x - x
        move_y = new_y - y

        if move_x == 1 and move_y == 0:
            return E
        elif move_x == -1 and move_y == 0:
            return W
        elif move_x == 0 and move_y == 1:
            return S
        elif move_x == 0 and move_y == -1:
            return N
        else:
            raise ValueError("Cells are not adjacent")

    def open_between(self, x: int, y: int,
                     new_x: int, new_y: int) -> None:
        direction = self.get_direction_between(x, y, new_x, new_y)
        self.grid[y][x] = self.open_wall(self.grid[y][x], direction)
        self.grid[new_y][new_x] = self.open_wall(self.grid[new_y][new_x],
                                                 OPP_WALL[direction])

    def wall_open_hor(self, x: int, y: int) -> bool:
        return not self.has_wall(self.grid[y][x], E)

    def wall_open_ver(self, x: int, y: int) -> bool:
        return not self.has_wall(self.grid[y][x], S)

    def is_open_3x3(self, top_x: int, top_y: int) -> bool:
        if top_x < 0 or top_y < 0:
            return False
        if top_x + 2 >= self.width or top_y + 2 >= self.height:
            return False
        for yy in range(top_y, top_y + 3):
            for xx in range(top_x, top_x + 2):
                if not self.wall_open_hor(xx, yy):
                    return False
        for yy in range(top_y, top_y + 2):
            for xx in range(top_x, top_x + 3):
                if not self.wall_open_ver(xx, yy):
                    return False
        return True

    def would_create_open_3x3(self, x: int, y: int, new_x: int, new_y: int
                              ) -> bool:
        direction = self.get_direction_between(x, y, new_x, new_y)
        old_a = self.grid[y][x]
        old_b = self.grid[new_y][new_x]
        self.grid[y][x] = self.open_wall(self.grid[y][x], direction)
        self.grid[new_y][new_x] = self.open_wall(self.grid[new_y][new_x],
                                                 OPP_WALL[direction])
        min_x = min(x, new_x)
        min_y = min(y, new_y)

        created = False
        for top_y in range(min_y - 2, min_y + 1):
            for top_x in range(min_x - 2, min_x + 1):
                if self.is_open_3x3(top_x, top_y):
                    created = True
                    break
            if created:
                break
        self.grid[y][x] = old_a
        self.grid[new_y][new_x] = old_b
        return created

    # ========== 42 =========

    def place_42(self):
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

    # ========= 42 =========

    def generate_once(self) -> bool:
        visited = self.init_visited(self.width, self.height)
        for x, y in self.blocked:
            visited[y][x] = True
        if not self.in_bounds(self.start_x, self.start_y, self.width,
                              self.height):
            raise ValueError("Start position out of bounds")
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

    def reset(self, attempt):
        self.grid = self.make_grid(self.width, self.height)
        self.rand_num_gen = random.Random(self.seed + attempt * 7979)
        for (x, y) in self.blocked:
            self.grid[y][x] = 15

    def generate(self, max_attempts=200) -> list[list[int]]:
        for attempt in range(max_attempts):
            self.reset(attempt)
            if self.generate_once():
                errors = self.validate()
                if errors:
                    raise RuntimeError("Generated maze is invalid:\n"
                                       "\n".join(errors))
                if not self._is_perfect_maze():
                    raise RuntimeError("Generated maze is not perfect "
                                       "(should be a spanning tree).")
                return self.grid
        raise RuntimeError("Generation failed after retries")

    def solve(self) -> list[int]:
        start_x, start_y = self.entry
        end_x, end_y = self.exit
        queue: Deque[tuple[int, int]] = deque()
        queue.append((start_x, start_y))
        visited: list[list[bool]] = self.init_visited(self.width,
                                                      self.height)
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
                if self.has_wall(self.grid[y][x], d):
                    continue
                new_x = x + DIR_X[d]
                new_y = y + DIR_Y[d]
                if not (0 <= new_x < self.width and 0 <= new_y < self.height):
                    continue
                if visited[new_y][new_x]:
                    continue
                if (new_x, new_y) in self.blocked:
                    continue
                visited[new_y][new_x] = True
                parent[(new_x, new_y)] = (x, y, d)
                queue.append((new_x, new_y))
        return []

    def path_to_letters(self, path: list[int]) -> str:
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

    def grid_as_hex_lines(self) -> list[str]:
        lines: list[str] = []
        for row in self.grid:
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

    def check_consistency(self) -> bool:
        for y in range(self.height):
            for x in range(self.width):
                if self.in_bounds(x + 1, y,
                                  self.width, self.height):
                    if (self.has_wall(self.grid[y][x], E) !=
                            self.has_wall(self.grid[y][x + 1], W)):
                        return False
                if self.in_bounds(x, y + 1, self.width, self.height):
                    if (self.has_wall(self.grid[y][x], S) !=
                            self.has_wall(self.grid[y + 1][x], N)):
                        return False
        return True

    def validate_wall_consistency(self, errors: list[str]) -> None:
        if not self.check_consistency():
            errors.append("Inconsistent walls between adjacent cells")

    def reachable_count_from_entry(self) -> int:
        start_x, start_y = self.entry
        count = 1
        queue: Deque[tuple[int, int]] = deque()
        queue.append((start_x, start_y))
        visited: list[list[bool]] = self.init_visited(self.width,
                                                      self.height)
        visited[start_y][start_x] = True
        while queue:
            x, y = queue.popleft()
            for d in (N, E, S, W):
                if self.has_wall(self.grid[y][x], d):
                    continue
                new_x = x + DIR_X[d]
                new_y = y + DIR_Y[d]
                if not (0 <= new_x < self.width and 0 <= new_y < self.height):
                    continue
                if visited[new_y][new_x]:
                    continue
                if (new_x, new_y) in self.blocked:
                    continue
                visited[new_y][new_x] = True
                count += 1
                queue.append((new_x, new_y))
        return count

    def validate_connectivity(self, errors: list[str]) -> None:
        reachable = self.reachable_count_from_entry()
        total = self.height * self.width - len(self.blocked)
        if reachable != total:
            errors.append("Connectivity error: reachable cells = "
                          f"{reachable} / {total}")

    def validate_outer_borders(self, errors: list[str]) -> None:
        for x in range(self.width):
            if not self.has_wall(self.grid[0][x], N):
                errors.append(f"Missing north outer wall at ({x}, 0)")
            if not self.has_wall(self.grid[self.height - 1][x], S):
                errors.append("Missing south outer wall at "
                              f"({x}, {self.height - 1})")
        for y in range(self.height):
            if not self.has_wall(self.grid[y][0], W):
                errors.append(f"Missing west outer wall at (0, {y})")
            if not self.has_wall(self.grid[y][self.width - 1], E):
                errors.append(f"Missing east outer wall at ({self.width - 1}, "
                              f"{y})")

    def validate_entry_exit(self, errors: list[str]) -> None:
        ent_x, ent_y = self.entry
        exit_x, exit_y = self.exit
        entry_ok = self.in_bounds(ent_x, ent_y, self.width, self.height)
        exit_ok = self.in_bounds(exit_x, exit_y, self.width, self.height)
        if not entry_ok:
            errors.append("Entry coordinates out of bounds")
            return
        if not exit_ok:
            errors.append("Exit coordinates out of bounds")
            return
        if (ent_x, ent_y) in self.blocked:
            errors.append("Entry cannot be inside 42 motif")
        if (exit_x, exit_y) in self.blocked:
            errors.append("Exit cannot be inside 42 motif")
        if (ent_x, ent_y) == (exit_x, exit_y):
            errors.append("Entry and exit must be different cells")

    def validate_no_open_3x3(self, errors: list[str]) -> None:
        for top_y in range(self.height - 2):
            for top_x in range(self.width - 2):
                if self.is_open_3x3(top_x, top_y):
                    errors.append("Open 3x3 area detected at top-left "
                                  f"({top_x},{top_y})")
                    return

    def validate(self) -> list[str]:
        errors: list[str] = []
        self.validate_entry_exit(errors)
        self.validate_outer_borders(errors)
        self.validate_wall_consistency(errors)
        self.validate_no_open_3x3(errors)
        self.validate_connectivity(errors)
        return errors

    def write_output(self, filename: str) -> None:
        path = self.path_to_letters(self.solve())
        with open(filename, "w", encoding="utf-8") as file:
            for line in self.grid_as_hex_lines():
                file.write(line + "\n")
            file.write("\n")
            ent_x, ent_y = self.entry
            exit_x, exit_y = self.exit
            file.write(f"{ent_x},{ent_y}\n")
            file.write(f"{exit_x},{exit_y}\n")
            file.write(path + "\n")

    def _count_open_edges(self) -> int:
        edges = 0
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in self.blocked:
                    continue
                if x + 1 < self.width and (x + 1, y) not in self.blocked:
                    if not self.has_wall(self.grid[y][x], E):
                        edges += 1
                if y + 1 < self.height and (x, y + 1) not in self.blocked:
                    if not self.has_wall(self.grid[y][x], S):
                        edges += 1
        return edges

    def _is_perfect_maze(self) -> bool:
        nodes = self.width * self.height - len(self.blocked)
        edges = self._count_open_edges()
        return edges == nodes - 1

    def to_ascii(self, show_path: bool = False) -> str:
        ent_x, ent_y = self.entry
        exit_x, exit_y = self.exit

        path_cells: set[tuple[int, int]] = set()
        if show_path:
            path_cells = self.path_cells()
        lines: list[str] = []
        top = "+"
        for x in range(self.width):
            if self.has_wall(self.grid[0][x], N):
                top += "---" + "+"
            else:
                top += "   " + "+"
        lines.append(top)

        for y in range(self.height):
            mid = ""
            for x in range(self.width):
                if self.has_wall(self.grid[y][x], W):
                    mid += "|"
                else:
                    mid += " "
                content = "   "
                if (x, y) in self.blocked:
                    content = "###"
                elif (x, y) == (ent_x, ent_y):
                    content = " S "
                elif (x, y) == (exit_x, exit_y):
                    content = " E "
                elif show_path and (x, y) in path_cells:
                    content = " . "
                mid += content
            if self.has_wall(self.grid[y][self.width - 1], E):
                mid += "|"
            else:
                mid += " "
            lines.append(mid)
            bot = "+"
            for x in range(self.width):
                if self.has_wall(self.grid[y][x], S):
                    bot += "---" + "+"
                else:
                    bot += "   " + "+"
            lines.append(bot)
        return "\n".join(lines)

    def path_cells(self) -> set[tuple[int, int]]:
        cells: set[tuple[int, int]] = set()
        x, y = self.entry
        cells.add((x, y))
        for d in self.solve():
            x += DIR_X[d]
            y += DIR_Y[d]
            cells.add((x, y))
        return cells
