import sys
import config
from typing import Any


def main() -> None:
    """Main function of the program."""

    if len(sys.argv) != 2:
        print("Error: arguments must be 'a_maze_ing.py config.txt' !")
        sys.exit(1)

    try:
        data: dict[str, Any] = config.get_valid_config(
            config.get_config(sys.argv[2]))
    except Exception as e:
        print(f"{e}")
        sys.exit(1)

    fake_maze = [
        [0xF, 0x9, 0x9, 0x9, 0xB],
        [0xD, 0x5, 0x3, 0xC, 0xA],
        [0xD, 0x6, 0xC, 0x9, 0xA],
        [0xD, 0x3, 0xE, 0x5, 0xA],
        [0x7, 0xC, 0x9, 0x6, 0xE]
    ]


if __name__ == "__main__":
    main()
