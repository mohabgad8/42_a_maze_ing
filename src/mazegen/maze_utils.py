"""Utils funtions."""

N, E, S, W = 0, 1, 2, 3
DIR_X = {N: 0, E: 1, S: 0, W: -1}
DIR_Y = {N: -1, E: 0, S: 1, W: 0}
OPP_WALL = {N: S, E: W, S: N, W: E}


def has_wall(cell: int, d: int) -> bool:
    """Check if cell has wall.

    Args:
        cell (int): coordonnees of the cell
        d (int): which wall of the cell we check

    Returns:
        bool: True or False
    """
    return ((cell >> d) & 1) == 1


def open_wall(cell: int, d: int) -> int:
    """Open a wall of a cell.

    Args:
        cell (int): coordonnees of the cell
        d (int): which wall of the cell we open

    Returns:
        int: return a cell without the wall that we removed
    """
    bitmask = 1 << d  # créer un bit à 1 à la position d
    inverted_mask = ~bitmask  # on invesve
    new_cell = cell & inverted_mask  # on enlève ce bit dans cell
    return new_cell


def get_direction_between(x: int, y: int, new_x: int, new_y: int) -> int:
    """Give the direction  between 2 cells.

    Args:
        x (int): x of the cell
        y (int): y of the cell
        new_x (int): x of the cell with wich we compare
        new_y (int):x of the cell with wich we compare

    Raises:
        ValueError: raise error if cells are not adjacent

    Returns:
        int: the direction
    """
    move_x = new_x - x
    move_y = new_y - y

    if move_x == 1 and move_y == 0:
        return E
    if move_x == -1 and move_y == 0:
        return W
    if move_x == 0 and move_y == 1:
        return S
    if move_x == 0 and move_y == -1:
        return N
    raise ValueError("Cells are not adjacent")
