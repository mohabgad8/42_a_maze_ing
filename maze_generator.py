import random


N, E, S, W = 0, 1, 2, 3
# comment on se déplace dans la grille
DIR_X = {N: 0, E: 1, S: 0, W: -1}
DIR_Y = {N: -1, E: 0, S: 1, W: 0}
# aller à l'est: (x + 1, y)
# aller au nord: (x, y - 1)
opposite_walls = {N: S, E: W, S: N, W: E}


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
        # on crée les lignes
        for y in range(height):
            row: list[int] = []
            # on cré les colonnes pour chaque ligne
            for x in range(width):
                row.append(15)
            grid.append(row)
        return grid

    @staticmethod
    def make_visited(width: int, height: int) -> list[list[bool]]:
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
        # on teste les 4 directions
        for d in (N, E, S, W):
            new_x = x + DIR_X[d]
            new_y = y + DIR_Y[d]
            # dans la grille ?
            if not self.in_bounds(new_x, new_y, self.width, self.height):
                continue
            if visited[new_y][new_x]:
                continue
            neighbors.append((new_x, new_y))
        return neighbors

    def open_between(self, x: int, y: int,
                     new_x: int, new_y: int) -> None:
        move_x = new_x - x
        move_y = new_y - y

        if move_x == 1 and move_y == 0:
            direction = E
        elif move_x == -1 and move_y == 0:
            direction = W
        elif move_x == 0 and move_y == 1:
            direction = S
        elif move_x == 0 and move_y == -1:
            direction = N
        else:
            raise ValueError("Cells are not adjacent")
        self.grid[y][x] = self.open_wall(self.grid[y][x], direction)
        self.grid[new_y][new_x] = self.open_wall(self.grid[new_y][new_x],
                                                 opposite_walls[direction])

    def generate(self) -> list[list[list]]:
        rand_num_gen = random.Random(seed)

        self.grid = self.make_grid(self.width, self.height)
        visited = self.make_visited(self.width, self.height)

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
            # choisi au hasard la case non visitée à visiter
            new_x, new_y = rand_num_gen.choice(neighbors)
            self.open_between(x, y, new_x, new_y)

            visited[new_y][new_x] = True
            stack.append((new_x, new_y))
        return self.grid

    def open_to_outside(self, x: int, y: int, d: int) -> None:
        if not self.in_bounds(x, y, self.width, self.height):
            raise ValueError("Cell out of bounds")
        self.grid[y][x] = self.open_wall(self.grid[y][x], d)

    def add_default_entrance_exit(self) -> None:
        ent_x, ent_y, ent_d = self.entry
        exit_x, exit_y, exit_d = self.exit
        self.open_to_outside(ent_x, ent_y, ent_d)
        self.open_to_outside(exit_x, exit_y, exit_d)

    def solve(self) -> None:
        from collections import deque

        start_x, start_y, _ = self.entry
        end_x, end_y, _ = self.exit

        queue = deque()
        queue.append((start_x, start_y))

        visited: list[list[bool]] = []
        for y in range(self.height):
            row: list[bool] = []
            for x in range(self.width):
                row.append(False)
            visited.append(row)
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
        return " ".join(out)

    def grid_as_hex_lines(self) -> list[str]:
        lines: list[str] = []
        for row in self.grid:
            parts: list[str] = []
            for cell in row:
                hex_value = f"{cell:X}"
                parts.append(hex_value)
            line = " ".join(parts)
            lines.append(line)
        return lines

    def print_grid_hex(self) -> None:
        for line in self.grid_as_hex_lines():
            print(line)


if __name__ == "__main__":
    w, h = 7, 7
    seed = 42

    maze = MazeGenerator(w, h, seed=seed)
    maze.generate()
    maze.add_default_entrance_exit()
    print("\n")
    maze.print_grid_hex()
    print("\n")
    path = maze.solve()
    print(maze.path_to_letters(path))
