from colors import ColorManager
from grid import map_logical_path_to_visual

def print_visual_grid(
    v_grid: list[list[int]], 
    color_manager: ColorManager,
    start: tuple[int, int] | None = None,
    end: tuple[int, int] | None = None,
    path: list[tuple[int, int]] | None = None
) -> None:
    # 1. Obtém o conjunto de coordenadas visuais do caminho 🗺️
    path_points = map_logical_path_to_visual(path) if path else set()
    wall_color = color_manager.current_palette.wall_color
    
    # 2. Percorre a matriz e desenha cada caractere 🖨️
    for r, row in enumerate(v_grid):
        line_chars = []
        for c, cell in enumerate(row):
            if (r, c) == start:
                line_chars.append(color_manager.colorize("█", ColorManager.ENTRY_COLOR))
            elif (r, c) == end:
                line_chars.append(color_manager.colorize("█", ColorManager.EXIT_COLOR))
            elif (r,c) in path_points:
                line_chars.append(color_manager.colorize("█", ColorManager.PATH_COLOR))
            elif cell == 1:
                line_chars.append(color_manager.colorize("█", wall_color))
            else:
                line_chars.append(" ")
        print("".join(line_chars))