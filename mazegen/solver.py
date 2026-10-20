from collections import deque
from mazegen.Maze import Maze

def bfs_solve_maze(maze: Maze) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:

    grid = maze.grade
    height = maze.grade_height
    width = maze.grade_width
    x1, y1 = maze.entry
    x2, y2 = maze.exit

    (entry_y, entry_x) = (x1 * 2 + 1), (y1 * 2 + 1)
    (exit_y, exit_x) = (x2 * 2 + 1), (y2 * 2 + 1)

    queue: deque[tuple[int, int]] = deque()
    visited: set[tuple[int, int]] = set()
    explored: list[tuple[int, int]] = [] # show pathfinder animation
    parent: dict[tuple[int, int], tuple[int, int]] = {} #prev and curr pos

    start = (entry_y, entry_x)
    end = (exit_y, exit_x)

    queue.append(start)
    visited.add(start)
    explored.append(start)

    directions = [
        (0, -1),
        (0, 1),
        (-1, 0),
        (1, 0)
    ]

    while queue:
        y, x = queue.popleft()

        if (y, x) == end:
            break

        for dy, dx in directions:
            new_y = y + dy
            new_x = x + dx

            #check if  new y and x are in maze bonds
            if not (0 <= new_y < height and 0 <= new_x < width):
                continue

            #check if its logo
            if grid[new_y][new_x] == 1 or grid[new_y][new_x] == 2:
                continue

            #chek if it is visited
            if (new_y, new_x) in visited:
                continue

            visited.add((new_y, new_x))
            explored.append((new_y, new_x))
            parent[(new_y, new_x)] = (y, x)
            queue.append((new_y, new_x))

    try:
        #reconstruct path
        path: list[tuple[int, int]] = []
        current = end

        while current != start:
            path.append(current)
            current = parent[current]

        path.append(start)
        #get the result from start
        path.reverse()

    except KeyError:
        return [], explored
    return path, explored