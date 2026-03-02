from collections import deque
from typing import Deque

from .maze_utils import N, E, S, W, DIR_X, DIR_Y, has_wall


def _reachable_count(
    grid: list[list[int]],
    blocked: set[tuple[int, int]],
    entry: tuple[int, int],
) -> int:
    """BFS: nombre de cellules atteignables depuis
    entry (en excluant blocked)."""
    width = len(grid[0])
    height = len(grid)
    sx, sy = entry

    visited = [[False] * width for _ in range(height)]
    visited[sy][sx] = True

    queue: Deque[tuple[int, int]] = deque([(sx, sy)])
    count = 1

    while queue:
        x, y = queue.popleft()
        for d in (N, E, S, W):
            if has_wall(grid[y][x], d):
                continue
            nx = x + DIR_X[d]
            ny = y + DIR_Y[d]
            if not (0 <= nx < width and 0 <= ny < height):
                continue
            if visited[ny][nx]:
                continue
            if (nx, ny) in blocked:
                continue
            visited[ny][nx] = True
            count += 1
            queue.append((nx, ny))

    return count


def _check_wall_consistency(
    grid: list[list[int]],
    blocked: set[tuple[int, int]],
) -> bool:
    """Vérifie que E/W et N/S sont cohérents entre cellules adjacentes."""
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


def _is_open_3x3(grid: list[list[int]], top_x: int, top_y: int) -> bool:
    """
    Même définition que ton code:
    un bloc 3x3 est 'ouvert' si toutes les cloisons internes
    E et S sont ouvertes.
    """
    width = len(grid[0])
    height = len(grid)
    if top_x < 0 or top_y < 0:
        return False
    if top_x + 2 >= width or top_y + 2 >= height:
        return False

    # ouvertures horizontales internes (E) sur 3 # lignes,
    # 2 colonnes de cloisons
    for yy in range(top_y, top_y + 3):
        for xx in range(top_x, top_x + 2):
            if has_wall(grid[yy][xx], E):
                return False

    # ouvertures verticales internes (S) sur 2 lignes de cloisons, 3 colonnes
    for yy in range(top_y, top_y + 2):
        for xx in range(top_x, top_x + 3):
            if has_wall(grid[yy][xx], S):
                return False

    return True


def _validate_no_open_3x3(grid: list[list[int]]) -> list[str]:
    errors: list[str] = []
    width = len(grid[0])
    height = len(grid)

    for top_y in range(height - 2):
        for top_x in range(width - 2):
            if _is_open_3x3(grid, top_x, top_y):
                errors.append("Open 3x3 area detected at top-left "
                              f"({top_x},{top_y})")
                return errors

    return errors


def count_open_edges(grid: list[list[int]], blocked: set[tuple[int, int]]
                     ) -> int:
    """Compte les arêtes ouvertes (E et S uniquement, pas de double-compte)."""
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
    nodes = len(grid) * len(grid[0]) - len(blocked)
    return count_open_edges(grid, blocked) == nodes - 1


def validate_maze(
    grid: list[list[int]],
    blocked: set[tuple[int, int]],
    entry: tuple[int, int],
    exit: tuple[int, int],
) -> list[str]:
    """Renvoie une liste d'erreurs (vide si tout est OK)."""
    errors: list[str] = []

    # entry/exit
    if entry in blocked:
        errors.append("Entry cannot be inside 42 motif")
    if exit in blocked:
        errors.append("Exit cannot be inside 42 motif")
    if entry == exit:
        errors.append("Entry and exit must be different cells")

    # bords
    errors.extend(_validate_outer_borders(grid))

    # cohérence murs
    if not _check_wall_consistency(grid, blocked):
        errors.append("Inconsistent walls between adjacent cells")

    # pas de 3x3
    errors.extend(_validate_no_open_3x3(grid))

    # connectivité
    reachable = _reachable_count(grid, blocked, entry)
    total = len(grid) * len(grid[0]) - len(blocked)
    if reachable != total:
        errors.append("Connectivity error: reachable cells = "
                      f"{reachable} / {total}")

    return errors
