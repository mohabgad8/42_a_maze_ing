import os
import sys
import random
import time
from src.mazegen import MazeGenerator
from src.mazegen.ascii_display import to_ascii, animate_path
from src.mazegen.export_hex import write_output, path_to_letters
from src.mazegen.solve import solve, path_to_cells, path_to_ordered_cells
from src.mazegen.themes import designs
from src.parsing import get_config, get_valid_config


def main() -> None:
    design_index: int = 0
    try:
        if len(sys.argv) != 2:
            raise ValueError("Usage: python3 a_maze_ing.py <config_file>")

        parsed_config: dict = get_config(sys.argv[1])
        config: dict = get_valid_config(parsed_config)
        width: int = config['width']
        height: int = config['height']
        entry: tuple = config['entry']
        exit_pt: tuple = config['exit']
        perfect: bool = config['perfect']
        if config.get('seed'):
            seed: int = config['seed']
        else:
            seed: int = random.randint(0, 500)

        show_path: bool = False
        maze: MazeGenerator = MazeGenerator(
            width, height, entry, exit_pt, perfect, seed)
        maze.generate()
        path: list[int] = solve(maze.grid, maze.blocked, maze.entry, maze.exit)
        path_cells: set[tuple[int, int]] | None = path_to_cells(
            maze.entry, path) if show_path else None
        letters: str = path_to_letters(path)

        write_output(
            config['output_file'],
            maze.grid,
            maze.entry,
            maze.exit,
            letters)

        while True:
            os.system("clear")
            # print("Seed:", seed)
            print(to_ascii(
                grid=maze.grid,
                blocked=maze.blocked,
                entry=maze.entry,
                exit=maze.exit,
                show_path=show_path,
                path_cells=path_cells, design=designs[design_index]))

            print(
                "=== A-Maze-ing ===\n"
                "1. Re-generate a new maze\n"
                "2. Show/Hide path from entry to exit\n"
                "3. Rotate maze colors\n"
                "4. Quit\n"
            )
            choice = input("Choice ? (1-4)\n").strip().lower()

            if choice == "4":
                print("Bye 👋")
                break

            elif choice == "1":
                seed = random.randint(0, 500)
                maze: MazeGenerator = MazeGenerator(
                    width, height, entry, exit_pt, perfect, seed)
                maze.generate()

                path = solve(maze.grid, maze.blocked, maze.entry, maze.exit)
                path_cells = path_to_cells(
                    maze.entry, path) if show_path else None
                os.system("clear")
                continue
            elif choice == "2":
                os.system("clear")
                show_path = not show_path

                if show_path:
                    os.system("clear")
                    path = solve(
                        maze.grid, maze.blocked, maze.entry, maze.exit)
                    ordered = path_to_ordered_cells(maze.entry, path)

                    animate_path(
                        maze.grid,
                        maze.blocked,
                        maze.entry,
                        maze.exit,
                        ordered,
                        designs[design_index]
                    )
                    os.system("clear")
                    path_cells = path_to_cells(maze.entry, path)
                else:
                    path_cells = None
            elif choice == "3":
                design_index = (design_index + 1) % len(designs)
            else:
                print("Incorrect choice ! Try again...(1-4)")
                time.sleep(1)
    except Exception as e:
        print(e)
        sys.exit(1)


if __name__ == "__main__":
    main()
