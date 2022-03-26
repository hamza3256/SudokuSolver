import pygame
import time
pygame.font.init()

LBLUE = (62, 115, 206)
DBLUE = (9, 49, 153)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)


class Grid:
    """
    # very easy; for test purposes
    board = [
        [4, 6, 7, 9, 2, 1, 3, 5, 8],
        [8, 9, 5, 4, 7, 3, 2, 6, 1],
        [2, 3, 1, 8, 6, 5, 7, 4, 9],
        [5, 1, 3, 6, 9, 8, 4, 2, 7],
        [9, 2, 8, 7, 0, 4, 6, 1, 3],
        [7, 4, 6, 1, 3, 2, 9, 8, 5],
        [3, 5, 4, 2, 8, 7, 1, 9, 6],
        [1, 8, 9, 3, 4, 6, 5, 7, 2],
        [6, 7, 2, 5, 1, 9, 8, 3, 4]
    ]


    """

    # # medium difficulty
    # board = [
    #     [0, 0, 3, 0, 0, 7, 1, 6, 0],
    #     [0, 0, 7, 0, 2, 0, 0, 0, 0],
    #     [0, 0, 2, 0, 0, 3, 0, 0, 8],
    #     [1, 7, 0, 4, 0, 0, 3, 9, 0],
    #     [9, 0, 4, 1, 6, 5, 2, 0, 7],
    #     [0, 5, 8, 0, 0, 9, 0, 1, 4],
    #     [4, 0, 0, 7, 0, 0, 8, 0, 0],
    #     [0, 0, 0, 0, 4, 0, 5, 0, 0],
    #     [0, 6, 9, 5, 0, 0, 4, 0, 0]
    # ]

    # board = [
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 2, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0],
    #     [0, 0, 0, 0, 0, 0, 0, 0, 0]
    # ]

    """
    # hard difficulty
    board = [
        [7, 0, 4, 0, 0, 0, 6, 0, 0],
        [0, 0, 0, 0, 3, 2, 7, 4, 0],
        [0, 0, 0, 0, 6, 0, 3, 5, 0],
        [0, 0, 6, 0, 7, 0, 4, 3, 0],
        [8, 0, 1, 3, 0, 0, 0, 7, 0],
        [0, 0, 0, 2, 5, 0, 0, 0, 1],
        [0, 6, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 2, 0, 0, 0, 0, 0, 0],
        [1, 0, 7, 0, 8, 3, 0, 0, 0]
    ]
    """

    board = [
        [8, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 3, 6, 0, 0, 0, 0, 0],
        [0, 7, 0, 0, 9, 0, 2, 0, 0],
        [0, 5, 0, 0, 0, 7, 0, 0, 0],
        [0, 0, 0, 0, 4, 5, 7, 0, 0],
        [0, 0, 0, 1, 0, 0, 0, 3, 0],
        [0, 0, 1, 0, 0, 0, 0, 6, 8],
        [0, 0, 8, 5, 0, 0, 0, 1, 0],
        [0, 9, 0, 0, 0, 0, 4, 0, 0]
    ]

    def __init__(self, rows, cols, width, height, solved):
        self.rows = rows
        self.cols = cols
        self.squares = [[Square(self.board[i][j], i, j, width, height)
                         for j in range(cols)] for i in range(rows)]
        self.width = width
        self.height = height
        self.model = None
        self.update_model()
        self.selected = None
        self.solved = solved

    def update_model(self):
        self.model = [[self.squares[i][j].value for j in range(
            self.cols)] for i in range(self.rows)]

    def place(self, val):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set(val)
            self.update_model()

            if valid(self.model, val, (row, col)) and self.solve():
                return True
            else:
                self.squares[row][col].set(0)
                self.squares[row][col].set_temp(0)
                self.update_model()
                return False

    def sketch(self, val):
        row, col = self.selected
        self.squares[row][col].set_temp(val)

    def draw(self):
        gap = self.width / 9
        for i in range(self.rows+1):
            if i % 3 == 0 and i != 0:
                thick = 4
            else:
                thick = 1
            pygame.draw.line(self.solved, BLACK, (0, i*gap),
                             (self.width, i*gap), thick)
            pygame.draw.line(self.solved, BLACK, (i * gap, 0),
                             (i * gap, self.height), thick)

        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].draw(self.solved)

    def select(self, row, col):
        for i in range(self.rows):
            for j in range(self.cols):
                self.squares[i][j].selected = False

        self.squares[row][col].selected = True
        self.selected = (row, col)

    def clear(self):
        row, col = self.selected
        if self.squares[row][col].value == 0:
            self.squares[row][col].set_temp(0)

    def click(self, pos):
        if pos[0] < self.width and pos[1] < self.height:
            gap = self.width / 9
            x = pos[0] // gap
            y = pos[1] // gap
            return (int(y), int(x))
        else:
            return None

    def is_finished(self):
        for i in range(self.rows):
            for j in range(self.cols):
                if self.squares[i][j].value == 0:
                    return False
        return True

    # solves sudoku board using backtracking algorithm
    def solve_visual(self):
        self.update_model()
        grid = find_empty(self.model)
        if not grid:
            return True
        else:
            row, col = grid
        pygame.event.pump()
        for i in range(1, 10):
            if valid(self.model, i, (row, col)) == True:
                self.model[row][col] = i
                self.squares[row][col].set(i)
                self.squares[row][col].draw_change(self.solved, True)
                self.update_model()
                pygame.display.update()
                pygame.time.delay(50)
                if self.solve_visual():
                    return True

                self.model[row][col] = 0
                self.squares[row][col].set(0)
                self.update_model()
                self.squares[row][col].draw_change(self.solved, False)
                pygame.display.update()
                pygame.time.delay(50)
        return False


class Square:
    rows = 9
    cols = 9

    def __init__(self, value, row, col, width, height):
        self.value = value
        self.temp = 0
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.selected = False

    def draw(self, solved):
        fnt = pygame.font.SysFont("sudoku", 40)

        gap = self.width / 9
        x = self.col * gap
        y = self.row * gap

        if self.temp != 0 and self.value == 0:
            text = fnt.render(str(self.temp), 1, LBLUE)
            solved.blit(text, (x+5, y+5))
        elif not(self.value == 0):
            text = fnt.render(str(self.value), 1, BLACK)
            solved.blit(text, (x + (gap/2 - text.get_width()/2),
                               y + (gap/2 - text.get_height()/2)))

        if self.selected:
            pygame.draw.rect(solved, DBLUE, (x, y, gap, gap), 3)

    def draw_change(self, solved, g=True):
        fnt = pygame.font.SysFont("sudoku", 40)

        gap = (self.width / 9)
        x = self.col * gap
        y = self.row * gap
        pygame.draw.rect(solved, BLACK, (x, y, gap, gap), 0)

        gap = gap - 1
        x = self.col * (gap + 1)
        y = self.row * (gap + 1)

        pygame.draw.rect(solved, BLACK, (x, y, gap+1, gap+1), 0)

        if g:
            pygame.draw.rect(solved, GREEN, (x, y, gap, gap), 0)
        else:
            pygame.draw.rect(solved, DBLUE, (x, y, gap, gap), 0)
        text = fnt.render(str(self.value), 1, BLACK)
        solved.blit(text, (x + (gap / 2 - text.get_width() / 2),
                           y + (gap / 2 - text.get_height() / 2)))

    def set(self, val):
        self.value = val

    def set_temp(self, val):
        self.temp = val


def find_empty(bo):
    for i in range(len(bo)):
        for j in range(len(bo[0])):
            if bo[i][j] == 0:
                return (i, j)  # row, col

    return None


def valid(bo, num, pos):
    for i in range(len(bo[0])):
        if bo[pos[0]][i] == num and pos[1] != i:
            return False

    for i in range(len(bo)):
        if bo[i][pos[1]] == num and pos[0] != i:
            return False

    box_x = pos[1] // 3
    box_y = pos[0] // 3

    for i in range(box_y*3, box_y*3 + 3):
        for j in range(box_x * 3, box_x*3 + 3):
            if bo[i][j] == num and (i, j) != pos:
                return False

    return True


def redraw_sudoku(solved, board, time, strikes, check):
    solved.fill(WHITE)

    fnt = pygame.font.SysFont("sudoku", 40)
    text = fnt.render("Time: " + format_time(time), 1, BLACK)
    solved.blit(text, (540 - 160, 560))

    text = fnt.render("X " * strikes, 1, DBLUE)
    solved.blit(text, (20, 560))
    if check == 1:
        text = fnt.render("Solved!", 1, DBLUE)
        solved.blit(text, (20, 560))
    elif check == 2:
        text = fnt.render("Failed", 1, DBLUE)
        solved.blit(text, (20, 560))

    board.draw()


def format_time(secs):
    sec = secs % 60
    minute = secs//60
    tm = " " + str(minute) + ":" + str(sec)
    return tm


def main():
    solved = pygame.display.set_mode((540, 600))
    pygame.display.set_caption(
        "Sudoku Solver — Solve it yourself or press SPACE to autosolve")
    board = Grid(9, 9, 540, 540, solved)
    key = None
    run = True
    start = time.time()
    strikes = 0
    result = 0
    while run:
        game_clock = round(time.time() - start)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1 or event.key == pygame.K_KP1:
                    key = 1
                if event.key == pygame.K_2 or event.key == pygame.K_KP2:
                    key = 2
                if event.key == pygame.K_3 or event.key == pygame.K_KP3:
                    key = 3
                if event.key == pygame.K_4 or event.key == pygame.K_KP4:
                    key = 4
                if event.key == pygame.K_5 or event.key == pygame.K_KP5:
                    key = 5
                if event.key == pygame.K_6 or event.key == pygame.K_KP6:
                    key = 6
                if event.key == pygame.K_7 or event.key == pygame.K_KP7:
                    key = 7
                if event.key == pygame.K_8 or event.key == pygame.K_KP8:
                    key = 8
                if event.key == pygame.K_9 or event.key == pygame.K_KP9:
                    key = 9
                if event.key == pygame.K_DELETE:
                    board.clear()
                    key = None

                if event.key == pygame.K_SPACE:
                    pygame.event.pump()
                    board.solve_visual()

                if event.key == pygame.K_RETURN:
                    i, j = board.selected
                    if board.squares[i][j].temp != 0:
                        if board.place(board.squares[i][j].temp):
                            print("Success")
                            result = 1
                        else:
                            print("Wrong")
                            result = 2
                            strikes += 1
                        key = None
                        if board.is_finished():
                            print("Game over")

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos)
                if clicked:
                    board.select(clicked[0], clicked[1])
                    key = None

        if board.selected and key != None:
            board.sketch(key)

        redraw_sudoku(solved, board, game_clock, strikes, result)
        pygame.display.update()


main()
pygame.quit()
