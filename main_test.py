import os
from src.mazegen import MazeGenerator
from src.mazegen.ascii_display import to_ascii
from src.mazegen.export_hex import write_output, path_to_letters
from src.mazegen.solve import solve, path_to_cells
from src.mazegen.themes import designs


def main():
    design_index = 0
    try:
        w, h = 20, 15
        seed = 42
        # entry = (1, 1)
        # exit = (1, 1)
        perfect = False

        show_path = False
        maze = MazeGenerator(w, h, seed)
        maze.generate()
        path = solve(maze.grid, maze.blocked, maze.entry, maze.exit)
        path_cells = path_to_cells(maze.entry, path) if show_path else None
        letters = path_to_letters(path)

        write_output("output.txt",
                    maze.grid,
                    maze.entry,
                    maze.exit,
                    letters)

        while True:
            os.system("clear")
            print("\n" * 2)
            print("Seed:", seed)
            print(to_ascii(
                grid=maze.grid,
                blocked=maze.blocked,
                entry=maze.entry,
                exit=maze.exit,
                show_path=show_path,
                path_cells=path_cells, design=designs[design_index]))

            print("\n[r] regenerate\n[p] toggle path\n[c] change color\n[q] quit\n")
            choice = input("> ").strip().lower()

            if choice == "q":
                print("Bye 👋")
                break

            elif choice == "r":
                seed += 1
                maze = MazeGenerator(w, h, seed)
                maze.generate()

                path = solve(maze.grid, maze.blocked, maze.entry, maze.exit)
                path_cells = path_to_cells(maze.entry, path) if show_path else None

            elif choice == "p":
                show_path = not show_path

                path = solve(maze.grid, maze.blocked, maze.entry, maze.exit)
                path_cells = path_to_cells(maze.entry, path) if show_path else None
            elif choice == "c":
                design_index = (design_index + 1) % len(designs)
            else:
                print("Unknown command")
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()
