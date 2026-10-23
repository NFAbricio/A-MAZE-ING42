from mazegen.Maze import Maze

def maze_to_hex(maze: Maze) -> list[list[str]]:

    # sums the cells bit value and convert into hex

    hex_value = list[list[str]] = []

    grid = maze.grid
    height = maze.height
    width = maze.width

    for y in range(0, height):
        line: list[str] = [] #?
        for x in range(0, height):
            cur_y, cur_x = (y *2 + 1), (x * 2 + 1) #expand grid?
            value = 0
            if grid[cur_y - 1][cur_x] == 1:
                value += 1   # N
            if grid[cur_y][cur_x + 1] == 1:
                value += 2   # E
            if grid[cur_y + 1][cur_x] == 1:
                value += 4   # S
            if grid[cur_y][cur_x - 1] == 1:
                value += 8   # W
            line.append(hex(value)[2:].upper())
        hex_value.append(line)

    return hex_value