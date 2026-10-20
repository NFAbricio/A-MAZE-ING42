import random
from mazegen.Maze import Maze
from mazegen.solver import bfs_solve_maze
from mazegen.generator import (dfs_generator, 
                               apply_entry_exit,
                               check_open_areas,
                               break_walls,
                               add_42_logo)

class MazeGenerator:
    def __init__(self,
                 width: int,
                 height: int,
                 entry: tuple[int, int],
                 exit: tuple[int, int],
                 perfect: bool,
                 seed: int| None) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit = exit
        self.perfect = perfect
        self.seed = seed

    def generate_maze(self) -> Maze:
        try:
            if self.seed is not None:
                random.seed(self.seed)

            max_attempts = 1000

            for _ in range(max_attempts):
                maze = Maze(
                    self.width,
                    self.height,
                    self.entry,
                    self.exit
                )

                dfs_generator(maze)
                apply_entry_exit(maze)

                if not check_open_areas(maze):
                    continue

                logo_pos = add_42_logo(maze)
                if not logo_pos:
                    print("The maze is not big enough do show the 42 logo")

                if not self.perfect:
                    break_walls(maze, logo_pos)

                path, _ = bfs_solve_maze(maze)
                if path:
                    self.logo_pos = logo_pos
                    self.maze = maze
                    return maze
            raise ValueError("Generate maze()> could not generate a maze")
        
        except (KeyError, Exception) as e:
            raise ValueError(f"generate_maze(): {e}")

    def solve(self, algotihm: str) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]: