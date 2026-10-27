from typing import List

def init_grid(grid: list[list[int]], height: int, width: int) -> list[list[int]]:
    # Criação da grid visual
    total_rows = 2 * height + 1
    total_columns = 2 * width + 1
    visual_grid = [[0 for _ in range(total_columns)] for _ in range(total_rows)]

    # Moldura externa
    for cell in range(total_columns):
        visual_grid[0][cell] = 1
        visual_grid[total_rows - 1][cell] = 1
    for cell in range(total_rows):
        visual_grid[cell][0] = 1
        visual_grid[cell][total_columns - 1] = 1

    # Células, pilares e estuturas internas
    for y in range(0, height):
        for x in range(0, width):
            visual_grid[2 * y + 1][2 * x + 1] = 0  # Centro Aberto
            visual_grid[2 * y][2 * x] = 1  # Pilar / Interseção

            """Position in cell_value ref:
            Center of grid: grid[2*y+1][2*x+1]
            North = grid    [2*y]   [2*x+1]  Bit (0)= 1 0b0001
            East = grid     [2*y+1] [2*x+2]    Bit (1)= 2 0b0010
            South = grid    [2*y+2] [2*x+1]  Bit (2)= 4 0b0100
            West = grid     [2*y+1] [2*x]  Bit (3)= 8 0b1000"""
            cell_value = grid[y][x]

            # Parede Leste
            if is_wall_closed(cell_value, 2) and x < width - 1:
                visual_grid[2 * y + 1][2 * x + 2] = 1

            # Parede Sul
            if is_wall_closed(cell_value, 4) and y < height - 1:
                visual_grid[2 * y + 2][2 * x + 1] = 1
    return visual_grid


def is_wall_closed(cell_value: int, direction_bit: int) -> bool:
    """Check if a specific directional wall is closed."""
    return (cell_value & direction_bit) > 0

def map_logical_path_to_visual(logical_path: list[tuple[int, int]]) -> set[tuple[int, int]]:
    visual_points = set()
    for i in range(len(logical_path)):
        y, x = logical_path[i]
        vr, vc = 2 * y + 1, 2 * x + 1
        visual_points.add((vr, vc))
        
        # Ponto médio com o próximo passo
        if i < len(logical_path) - 1:
            next_y, next_x = logical_path[i + 1]
            next_vr, next_vc = 2 * next_y + 1, 2 * next_x + 1
            mid_r = (vr + next_vr) // 2
            mid_c = (vc + next_vc) // 2
            visual_points.add((mid_r, mid_c))
            
    return visual_points
