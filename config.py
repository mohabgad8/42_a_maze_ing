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


def validate_config(parsed_config: dict[str, str]) -> bool:
    """
        Returns a bool based on the validation of parsed config.
    """

    if not parse_config:
        return False
    try:
        for key, value in parsed_config.items():

    except ValueError as e:
        print(f"{e}")
        return False




if __name__ == "__main__":
    parse_config("config.txt")
