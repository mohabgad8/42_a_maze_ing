"""
    This file contains everything in relation with the config.txt file.
    Meaning:
    --------
        * Parsing the data received
        * Validation of the different data
"""


def parse_config(filename: str) -> dict[str, str]:
    """
        Parse config.txt and returns a dict containing different data.
    """

    config: dict[str, str] = {}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line: str = line.strip()
                if not line or line.startswith('#'):
                    continue
                if '=' not in line:
                    raise ValueError(
                        f"Error: '{line}' is invalid: doesn't contain '='")

                parts: list[str] = line.split('=', 1)
                key: str = parts[0].strip()
                value: str = parts[1].strip()

                if not key or not value:
                    raise ValueError(
                        f"Error: key or value missing for '{line}'")
                config[key] = value
        print(config)
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: file '{filename}' not found")
    except PermissionError:
        raise PermissionError(f"Error: don't have access to '{filename}'")
    except OSError:
        raise OSError(f"Error: something went wrong with '{filename}'")


def valid_config(
        parsed_config: dict[str, str]) -> dict[
            str, str | bool | int | tuple[int, int]]:
    """
        Returns a bool based on the validation of parsed config.

        Validation key points:
        ----------------------
        * Width and height aren't negatives. They are also within
            the limits of the maze. Which means: not too small to be able
            to contain the "42" logo.
    """

    MIN_WIDTH: int = 5
    MIN_HEIGHT: int = 5

    if not parsed_config:
        raise ValueError("Error: Something went wrong with parsed config.")

    validated_config: dict[
        str, str | bool | int | tuple[int, int]] = {}
    # Verify if width and height are correct
    try:
        width: int = int(parsed_config['WIDTH'])
        height: int = int(parsed_config['HEIGHT'])

        # In case 42 logo is 5x5
        if width < MIN_WIDTH or height < MIN_HEIGHT:
            raise ValueError("Error: Maze is too small fort the '42' logo.")

        validated_config['WIDTH'] = width
        validated_config['HEIGHT'] = height

        def parse_coords()
    except ValueError:
        raise ValueError("Error: Measurements are incorrect !")
    except KeyError:
        raise KeyError("Error: Key doesn't exist")

    # Get entry's coord.
    try:
        entry: str = parsed_config['ENTRY']
        entry_x: int = int((entry.split(',', 1)[0]))
        entry_y: int = int((entry.split(',', 1)[1]))
    except ValueError:
        raise ValueError("Error: entry's coordinates must be integers")

    # Check if entry's coord. are within limits
    if entry_x <= 0 or entry_y <= 0 or entry_x >= width or entry_y >= height:
        raise ValueError("Error: Coordinates are incorrect !")

    # Get exit's coord.
    try:
        end: str = parsed_config['EXIT']
        end_x: int = int((end.split(',', 1)[0]))
        end_y: int = int((end.split(',', 1)[1]))
    except ValueError:
        raise ValueError("Error: exit's coordinates must be integers")

    # Check if exit's coord. are within limits
    if end_x <= 0 or end_y <= 0 or end_x >= width or end_y >= height:
        raise ValueError("Error: Coordinates are incorrect !")

    # Check if entry and exit are similar
    if entry == end:
        raise ValueError("Error: Entry and Exit can't be identical !")

    return validated_config


if __name__ == "__main__":
    parse_config("config.txt")
