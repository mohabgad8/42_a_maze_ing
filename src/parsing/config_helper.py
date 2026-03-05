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

    min_width: int = 5
    min_height: int = 5

    return width >= min_width and height >= min_height
