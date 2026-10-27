from colors import ColorManager
from grid import init_grid
from renderer import print_visual_grid


def main() -> None:
    # 1. Dados lógicos do labirinto e do caminho 🧭
    grid_3x3 = [
        [9, 5, 3],
        [12, 5, 10],
        [10, 5, 6]
    ]
    caminho = [
        (0, 0), (0, 1), (0, 2),
        (1, 2), (1, 1), (1, 0),
        (2, 0), (2, 1), (2, 2)
    ]

    # 2. Inicialização dos componentes ⚙️
    color_mgr = ColorManager()
    v_grid = init_grid(grid_3x3, height=3, width=3)

    # 3. Execução da renderização 🖥️
    print(f"Paleta ativa: {color_mgr.current_palette.name}")
    print_visual_grid(
        v_grid,
        color_mgr,
        start=(1, 1),
        end=(5, 5),
        path=caminho
    )


if __name__ == "__main__":
    main()