def divide_coords(coords: str) -> tuple[int, int]:
    """
    Verifies the coordinates of entry and exit.
    Makes sure they are in the correct format.
    Args:
        - coords: str
    Return:
        - parsed_coords: tuple[int]
    """

    try:
        x, y = (
            int(coords.split(',', 1)[0]),
            int(coords.split(',', 1)[1]))
    except ValueError:
        raise ValueError("Error: coordinates are invalid !")

    return x, y


def verify_coords(x: int, y: int, width: int, height: int) -> bool:
    """
    This function concerns entry and exit.
    Verifies that coordinates are within limits.
    Args:
        - x: int
        - y: int
        - width: int
        - height: int
    Return:
        - True or False based on the verification of coordinates.
    """

    return x >= 0 and y >= 0 and x < width and y < height


def verify_size(width: int, height: int) -> bool:
    """
    This function concerns the size of the maze.
    Verifies if the maze's size is actually possible.
    Args:
        - width: int
        - height: int
    Return:
        - True or False based on the verification of size.
    """

    return width > 0 and height > 0 and width * height >= 2


def out_of_bound_size(width: int, height: int) -> bool:
    """
    Verify if width and height are correct and maze is doable.
    Doable means maze can actually be created in terminal
    without a visual discomfort.
    """

    return width > 30 or height > 30
