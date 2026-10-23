def path_to_directions(path: list[tuple[int,int]]) -> list[str]:

    path_str: list[str] = []

    for i in range(len(path) - 1):
        (y, x) = path[i]
        (dy, dx) = path[i + 1]

        if dy < y:
            path_str.append("N")
        elif dy > y:
            path_str.append("S")
        elif dx < x:
            path_str.append("W")
        elif dx > x:
            path_str.append("E")
    return path_str