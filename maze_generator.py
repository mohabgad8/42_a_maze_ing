import random


N, E, S, W = 0, 1, 2, 3
# comment on se déplace dans la grille
Dir_x = {N: 0, E: 1, S: 0, W: -1}
Dir_y = {N: -1, E: 0, S: 1, W: 0}
# aller à l'est: (x + 1, y)
# aller au nord: (x, y - 1)
opposite_walls = {N: S, E: W, S: N, W: E}


def has_wall(cell: int, d: int) -> bool:
    return ((cell >> d) & 1) == 1


def open_wall(cell: int, d: int) -> int:
    bitmask = 1 << d  # créer un bit à 1 à la position d
    inverted_mask = ~bitmask  # on invesve
    new_cell = cell & inverted_mask  # on enlève ce bit dans cell
    return new_cell


def open_between(grid: list[list[int]], x: int, y: int,
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
    grid[y][x] = open_wall(grid[y][x], direction)
    grid[new_y][new_x] = open_wall(grid[new_y][new_x],
                                   opposite_walls[direction])


def make_grid(width: int, heigth: int) -> list[list[int]]:
    grid: list[list[int]] = []
    # on crée les lignes
    for y in range(heigth):
        row: list[int] = []
        # on cré les colonnes pour chaque ligne
        for x in range(width):
            row.append(15)
        grid.append(row)
    return grid


def make_visited(width: int, heigth: int) -> list[list[bool]]:
    visited: list[list[bool]] = []
    for y in range(heigth):
        row: list[bool] = []
        for x in range(width):
            row.append(False)
        visited.append(row)
    return visited


def in_bounds(x: int, y: int, width: int, heigth: int) -> bool:
    if x < 0:
        return False
    if x >= width:
        return False
    if y < 0:
        return False
    if y >= heigth:
        return False
    return True


def unvisited_neighbors(x: int, y: int, 
                        width: int, heigth: int, 
                        visited: list[list[bool]]) -> list[tuple[int, int]]:
    neighbors: list[tuple[int, int]] = []
    # on teste les 4 directions
    for d in (N, E, S, W):
        new_x = x + Dir_x[d]
        new_y = y + Dir_y[d]
        # dans la grille ?
        if not in_bounds(new_x, new_y, width, heigth):
            continue
        if visited[new_y][new_x]:
            continue
        neighbors.append((new_x, new_y))
    return neighbors


def generate_dfs(width: int, heigth: int, seed: int = 0, start_x: int = 0,
                 start_y: int = 0) -> list[list[list]]:
    rand_num_gen = random.Random(seed)

    grid = make_grid(width, heigth)
    visited = make_visited(width, heigth)

    if not in_bounds(start_x, start_y, width, heigth):
        raise ValueError("Start position out of bounds")

    stack: list[tuple[int, int]] = [(start_x, start_y)]
    visited[start_y][start_x] = True

    while stack:
        x, y = stack[-1]

        neighbors = unvisited_neighbors(x, y, width, heigth, visited)

        if not neighbors:
            stack.pop()
            continue
        # choisi au hasard la case non visitée à visiter
        new_x, new_y = rand_num_gen.choice(neighbors)
        open_between(grid, x, y, new_x, new_y)

        visited[new_y][new_x] = True
        stack.append((new_x, new_y))
    return grid


def open_to_outside(grid: list[list[int]], x: int, y: int, d: int) -> None:
    grid[y][x] = open_wall(grid[y][x], d)


def add_default_entrance_exit(grid: list[list[int]]) -> None:
    heigth = len(grid)
    width = len(grid[0])
    open_to_outside(grid, 0, 0, N)
    open_to_outside(grid, width - 1, heigth - 1, S)


def print_grid_hex(grid: list[list[int]]) -> None:
    for row in grid:
        print(" ".join(f"{cell:X}" for cell in row))


if __name__ == "__main__":
    w, h = 80, 5
    seed = 4

    grid = generate_dfs(w, h, seed=seed)

    # optionnel : si tu as ces fonctions
    add_default_entrance_exit(grid)

    print(f"Grille générée (w={w}, h={h}, seed={seed}) :")
    print_grid_hex(grid)
