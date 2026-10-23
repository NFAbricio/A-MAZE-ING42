from mazegen.Maze import Maze
from utils.hex_utils import maze_to_hex
from utils.path_utils import path_to_directions

def export_maze(maze: Maze,
                path: list[tuple[int, int]],
                output_files: str) -> None:
    """
    Create file.txt with:
    Directions
    Hex values
    Entry and exit poins

    the file needs be regenareted every time
    """

    hex_values = maze_to_hex(maze)

    entry_y, entry_x = maze.entry
    exit_y, exit_x = maze.exit_position

    direction_path = path_to_directions(path)

    with open(output_files, "w") as file:
        for line in hex_values:
            file.write("".join(line) + "\n")
        file.write(f"\n{entry_y}{entry_x}\n")
        file.write(f"\n{exit_y}{exit_x}\n")
        file.write("".join(direction_path) + "\n")

def print_maze_file(output_file: str) -> None:
    try:
        with open(output_file, "r") as file:
            for line in file:
                print(line, end="")
    except (FileNotFoundError, PermissionError, Exception) as e:
        print(f"print_maze_file() failed -> {e}")
