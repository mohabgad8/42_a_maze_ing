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
opposite_wall = {N: S, E: W, S: N, W: E}


class MazeGenerator:
    def __init__(self, width: int, height: int, seed: int = 0,
                 start_x: int = 0, start_y: int = 0):
        self.width = width
        self.height = height
        self.seed = seed
        self.start_x = start_x
        self.start_y = start_y

        self.rand_num_gen = random.Random(seed)
        self.grid: list[list[int]] = self.make_grid(width, height)
        self.entry: tuple[int, int, int] = (0, 0, N)
        self.exit: tuple[int, int, int] = (width - 1, height - 1, S)

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
                                                 opposite_wall[direction])

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
                                                 opposite_wall[direction])
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

    def generate_once(self) -> bool:
        visited = self.init_visited(self.width, self.height)
        if not self.in_bounds(self.start_x, self.start_y, self.width,
                              self.height):
            raise ValueError("Start position out of bounds")

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

    def generate(self, max_attempts=200) -> list[list[int]]:
        for attempt in range(max_attempts):
            self.reset(attempt)
            if self.generate_once():
                return self.grid
            raise RuntimeError("Generation failed after retries")

    def open_to_outside(self, x: int, y: int, d: int) -> None:
        if not self.in_bounds(x, y, self.width, self.height):
            raise ValueError("Cell out of bounds")
        self.grid[y][x] = self.open_wall(self.grid[y][x], d)

    def add_default_entrance_exit(self) -> None:
        ent_x, ent_y, ent_d = self.entry
        exit_x, exit_y, exit_d = self.exit
        self.open_to_outside(ent_x, ent_y, ent_d)
        self.open_to_outside(exit_x, exit_y, exit_d)

    def solve(self) -> list[int]:
        start_x, start_y, _ = self.entry
        end_x, end_y, _ = self.exit
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
        start_x, start_y, _ = self.entry
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
                visited[new_y][new_x] = True
                count += 1
                queue.append((new_x, new_y))
        return count

    def validate_connectivity(self, errors: list[str]) -> None:
        reachable = self.reachable_count_from_entry()
        total = self.height * self.width
        if reachable != total:
            errors.append("Connectivity error: reachable cells = "
                          f"{reachable} / {total}")

    def check_border_wall(self, x: int, y: int, direction: int) -> bool:
        ent_x, ent_y, ent_d = self.entry
        exit_x, exit_y, exit_d = self.exit
        if x == ent_x and y == ent_y and direction == ent_d:
            if not self.has_wall(self.grid[y][x], direction):
                return True
            return False
        elif x == exit_x and y == exit_y and direction == exit_d:
            if not self.has_wall(self.grid[y][x], direction):
                return True
            return False
        else:
            if self.has_wall(self.grid[y][x], direction):
                return True
            return False

    def validate_outer_borders(self, errors: list[str]) -> None:
        for y in range(self.height):
            for x in range(self.width):
                if x == 0:
                    if not self.check_border_wall(x, y, W):
                        errors.append(f"Invalid outer wall at ({x}, {y}) "
                                      "direction=W")
                if x == self.width - 1:
                    if not self.check_border_wall(x, y, E):
                        errors.append(f"Invalid outer wall at ({x}, {y}) "
                                      "direction=E")
                if y == 0:
                    if not self.check_border_wall(x, y, N):
                        errors.append(f"Invalid outer wall at ({x}, {y}) "
                                      "direction=N")
                if y == self.height - 1:
                    if not self.check_border_wall(x, y, S):
                        errors.append(f"Invalid outer wall at ({x}, {y}) "
                                      "direction=S")

    def validate_entry_exit(self, errors: list[str]) -> None:
        ent_x, ent_y, ent_d = self.entry
        exit_x, exit_y, exit_d = self.exit
        entry_ok = self.in_bounds(ent_x, ent_y, self.width, self.height)
        exit_ok = self.in_bounds(exit_x, exit_y, self.width, self.height)
        if not entry_ok:
            errors.append("Entry coordinates out of bounds")
        if not exit_ok:
            errors.append("Exit coordinates out of bounds")
        if entry_ok and exit_ok:
            if (ent_x, ent_y) == (exit_x, exit_y):
                errors.append("Entry and exit must be different cells")
            if ent_d not in (N, E, S, W):
                errors.append("Entry direction is invalid")
            if exit_d not in (N, E, S, W):
                errors.append("Exit direction is invalid")
            if ent_d in (N, E, S, W):
                if not ((ent_y == 0 and ent_d == N)
                        or (ent_y == self.height - 1 and ent_d == S)
                        or (ent_x == 0 and ent_d == W)
                        or (ent_x == self.width - 1 and ent_d == E)):
                    errors.append("Entry direction does not match "
                                  "its border position")
            if exit_d in (N, E, S, W):
                if not ((exit_y == 0 and exit_d == N)
                        or (exit_y == self.height - 1 and exit_d == S)
                        or (exit_x == 0 and exit_d == W)
                        or (exit_x == self.width - 1 and exit_d == E)):
                    errors.append("Exit direction does not match "
                                  "its border position")

    def validate(self) -> list[str]:
        errors: list[str] = []
        self.validate_entry_exit(errors)
        self.validate_outer_borders(errors)
        self.validate_wall_consistency(errors)
        # self.validate_no_open_3x3(errors)
        self.validate_connectivity(errors)
        return errors


if __name__ == "__main__":
    w, h = 20, 10
    seed = 42

    maze = MazeGenerator(w, h, seed=seed)

    maze.generate()
    maze.add_default_entrance_exit()

    errors = maze.validate()
    if errors:
        print("❌ Maze invalid:")
        for err in errors:
            print(f"- {err}")

    print(f"✅ Maze valid (w={w}, h={h}, seed={seed})\n")
    maze.print_grid_hex()

    path_dirs = maze.solve()
    print("\nPath:", maze.path_to_letters(path_dirs))
