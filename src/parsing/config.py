"""
    This file contains everything in relation with the config.txt file.
    Meaning:
    --------
        * Parsing the data received
        * Validation of the different data
"""
from . import config_helper as helper


def get_config(filename: str) -> dict[str, str]:
    """
        Parse config.txt and returns a dict containing different data.
    """

    config: dict[str, str] = {}
    required_keys: set[str] = {
        'width', 'height', 'entry', 'exit', 'output_file', 'perfect'}
    try:
        with open(filename, 'r') as file:
            for line in file:
                line = line.strip()

                if not line or line.startswith('#'):
                    continue

                if '=' not in line:
                    raise ValueError(
                        f"Error: '{line}' is invalid: doesn't contain '='")

                key, value = line.split('=', 1)
                if not key or not value:
                    raise ValueError(
                        f"Error: key or value missing for '{line}'")
                if key.strip().lower() not in config:
                    config[key.strip().lower()] = value.strip()
                else:
                    continue

        missing = required_keys - config.keys()
        if missing:
            raise ValueError(f"Error: missing parameter {missing}")
        return config
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: file '{filename}' not found")
    except PermissionError:
        raise PermissionError(f"Error: can't have access to '{filename}'")
    except OSError:
        raise OSError(f"Error: something went wrong with '{filename}'")


def get_valid_config(
        config: dict[str, str]) -> dict[
            str, str | bool | int | tuple[int, int]]:
    """
        Manipulates the parsed config dict and verifies if width/height/entry
        and exit are correctly formatted. Once the verifications are made,
        it will return a dict containing the different data.

        Validation key points:
        ----------------------
        * Width and height aren't negatives. They are also within
            the limits of the maze. Which means: not too small to be able
            to contain the "42" logo.
        * Entry and exit are within the actual maze and not beyond limits.
            They must be different.
    """

    if not config:
        raise ValueError("Error: Something went wrong with parsed config.")

    valid_config: dict[
        str, str | bool | int | tuple[int, int]] = {}
    # Verify if width and height are correct
    try:
        width: int = int(config['width'])
        height: int = int(config['height'])

    except ValueError:
        raise ValueError("Error: Measurements are incorrect !")
    except KeyError:
        raise KeyError("Error: Key doesn't exist")

    # In case 42 logo is 5x5
    if not helper.verify_size(width, height):
        raise ValueError("Error: width and height can't be negatives !")

    if helper.out_of_bound_size(width, height):
        raise ValueError("Error: width and height can't be bigger than 30 !")

    valid_config['width'] = width
    valid_config['height'] = height

    # Get entry's coord.
    try:
        entry_x, entry_y = helper.divide_coords(config['entry'])
    except ValueError as e:
        raise ValueError(f"{e}")

    if not helper.verify_coords(entry_x, entry_y, width, height):
        raise ValueError("Error: entry's coordinates are invalid !")
    valid_config['entry'] = (entry_x, entry_y)

    # Get exit's coord.
    try:
        exit_x, exit_y = helper.divide_coords(config['exit'])
    except ValueError as e:
        raise ValueError(f"{e}")

    if not helper.verify_coords(exit_x, exit_y, width, height):
        raise ValueError("Error: exit's coordinates are invalid !")
    valid_config['exit'] = (exit_x, exit_y)

    # Check if entry and exit are similar
    if entry_x == exit_x and entry_y == exit_y:
        raise ValueError("Error: Entry and Exit can't be identical !")

    # Output_file
    try:
        valid_config['output_file'] = config['output_file']
    except KeyError:
        raise KeyError("Error: output_file key is missing in config")

    # Perfect
    if config['perfect'].lower() == 'true':
        valid_config['perfect'] = True
    elif config['perfect'].lower() == 'false':
        valid_config['perfect'] = False
    else:
        raise ValueError("Error: perfect's parameter is invalid !")

    if config.get('seed'):
        try:
            valid_config['seed'] = int(config['seed'])
        except ValueError:
            raise ValueError("Error: seed must be an integer !")

    return valid_config
