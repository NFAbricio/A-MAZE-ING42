#para criar a estrutura geral do maze

#classe maze

#classe com os objetos (width, lenght, entry[tupla], exit[tupla])

class Maze:
    def __init__(self,
                 width:     int,
                 height:    int,
                 entry:     tuple[int, int],
                 exit_position:      tuple[int, int]) -> None:
        self.width = width
        self.height = height
        self.entry = entry
        self.exit_position = exit_position
        #criar o grid
        #calculo de 2 * variavel + 1(parede externa)
        #a ideia é deixar espaço para células paredes
        self.grade: list[list[int]] = []
        self.grade_width = 2 * width + 1
        self.grade_height = 2 * height + 1


        for _ in range(0, self.grade_height):
            row: list[int] = []
            for _ in range(self.grade_width):
                row.append(1)

            self.grade.append(row)