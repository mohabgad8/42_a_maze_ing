import os
from src.mazegen import MazeGenerator
from src.mazegen.ascii_display import to_ascii
from src.mazegen.export_hex import write_output, path_to_letters
from src.mazegen.solve import solve
from src.mazegen.maze_utils import DIR_X, DIR_Y


def path_to_cells(entry, path):
    x, y = entry
    cells = {(x, y)}
    for d in path:
        x += DIR_X[d]
        y += DIR_Y[d]
        cells.add((x, y))
    return cells


def main():

    w, h = 20, 10
    seed = 42
    entry = (2, 2)
    exit = (9, 2)
    perfect = True

    show_path = False
    maze = MazeGenerator(w, h, seed, entry, exit, perfect)
    maze.generate()
    path = solve(maze.grid, maze.blocked, maze.entry, maze.exit)
    path_cells = path_to_cells(maze.entry, path) if show_path else None
    letters = path_to_letters(path)

    write_output("output.txt",
                 maze.grid,
                 maze.entry,
                 maze.exit,
                 letters)

    os.system("clear")
    while True:
        print("\n" * 2)
        print("Seed:", seed)
        print(to_ascii(
            grid=maze.grid,
            blocked=maze.blocked,
            entry=maze.entry,
            exit=maze.exit,
            show_path=show_path,
            path_cells=path_cells))

        print("\n[r] regenerate\n[p] toggle path \n[q] quit\n")
        choice = input("> ").strip().lower()

        if choice == "q":
            print("Bye 👋")
            break

        elif choice == "r":
            seed += 1
            maze = MazeGenerator(w, h, seed, entry, exit, perfect)
            maze.generate()

            path = solve(maze.grid, maze.blocked, maze.entry, maze.exit)
            path_cells = path_to_cells(maze.entry, path) if show_path else None

        elif choice == "p":
            show_path = not show_path

            path = solve(maze.grid, maze.blocked, maze.entry, maze.exit)
            path_cells = path_to_cells(maze.entry, path) if show_path else None
        else:
            print("Unknown command")


if __name__ == "__main__":
    main()
