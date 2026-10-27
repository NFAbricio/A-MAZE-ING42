"""Module responsible for terminal visualization and color styling"""

from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class ColorPalette:
    """Represents sets of ANSI escape codes for walls and accents"""

    name: str
    wall_color: str
    accent_color: str


class ColorManager:
    """Manages ANSI terminal color palettes and cycling states"""

    RESET: str = "\033[0m"
    BOLD: str = "\033[1m"

    # Static colors for funcional markers
    ENTRY_COLOR: str = "\033[92m"  # Bright Green
    EXIT_COLOR: str = "\033[91m"  # Bright Red
    PATH_COLOR: str = "\033[93m"  # Bright Yellow
    FORTY_TWO_COLOR: str = "\033[95m"  # Bright Magenta

    def __init__(self) -> None:
        """Initialize available palettes and the default active palette."""
        self._palettes: List[ColorPalette] = [
            ColorPalette(
                name="Cyber Blue", wall_color="\033[94m", accent_color="\033[34m"
            ),
            ColorPalette(
                name="Emerald", wall_color="\033[32m", accent_color="\033[92m"
            ),
            ColorPalette(
                name="Neon Purple", wall_color="\033[35m", accent_color="\033[95m"
            ),
            ColorPalette(name="Solar", wall_color="\033[33m", accent_color="\033[93m"),
            ColorPalette(
                name="Monochrome", wall_color="\033[97m", accent_color="\033[90m"
            ),
        ]
        self._current_index: int = 0

    @property
    def current_palette(self) -> ColorPalette:
        """Return the currently selected color palette."""
        return self._palettes[self._current_index]

    def cycle_palette(self) -> ColorPalette:
        """Cycle to the next wall color palette and return it."""
        self._current_index = (self._current_index + 1) % len(self._palettes)
        return self._current_index

    def colorize(self, text: str, color_code: str) -> str:
        """Wrap text with the given ANSI color and append the reset code."""
        return f"{color_code}{text}{self.RESET}"


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

# Debug Tests
# 1. Instanciamos o gerenciador de cores 🎨
color_mgr = ColorManager()

# 2. Definimos o labirinto lógico 2x2 em formato de "U" 🧭
grid_2x2 = [[13, 3], [13, 6]]
# 3. Geramos a matriz visual expandida (dimensões 5x5) 🧱
resultado_2x2 = init_grid(grid_2x2, height=2, width=2)
# Labirinto 3x3 com caminho completo em serpente:
# (0,0) -> (0,1) -> (0,2) -> (1,2) -> (1,1) -> (1,0) -> (2,0) -> (2,1) -> (2,2)
grid_3x3 = [
    [9, 5, 3],    # Linha 0: abre para a direita até (0,2), que desce
    [12, 5, 10],  # Linha 1: desce em (0,2)->(1,2), vai para a esquerda até (1,0)
    [10, 5, 6]    # Linha 2: desce em (1,0)->(2,0), vai para a direita até (2,2)
]

# Sequência completa de coordenadas lógicas (y, x):
caminho_longo = [
    (0, 0), (0, 1), (0, 2),
    (1, 2), (1, 1), (1, 0),
    (2, 0), (2, 1), (2, 2)
]

# 1. Geramos a grelha visual 7x7 a partir da lógica 3x3 🧱
resultado_3x3 = init_grid(grid_3x3, height=3, width=3)

# 2. Imprimimos com o traçado completo da solução 🟡
print(f"Paleta ativa: {color_mgr.current_palette.name}")
print_visual_grid(
    resultado_3x3,
    color_mgr,
    start=(1, 1),
    end=(5, 5),
    path=caminho_longo
)
# 4. Imprimimos com cores no terminal 💻
print(f"Paleta ativa: {color_mgr.current_palette.name}")


