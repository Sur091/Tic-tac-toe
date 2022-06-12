import pygame as py


def check_winner(lst):
    for a in range(3):
        if lst[a][0] and lst[a][0] == lst[a][1] == lst[a][2]:
            return lst[a][0]
    for b in range(3):
        if lst[0][b] and lst[0][b] == lst[1][b] == lst[2][b]:
            return lst[0][b]
    if lst[0][0] and lst[0][0] == lst[1][1] == lst[2][2]:
        return lst[0][0]
    if lst[0][2] and lst[0][2] == lst[1][1] == lst[2][0]:
        return lst[0][2]
    for a in range(3):
        for b in range(3):
            if not lst[a][b]:
                return ''
    return "tie"


def show_text(string):
    text = font.render(string, True, (0, 128, 0))
    window.blit(text, (width // 2 - 8 * len(string), height // 2 - 16))


scores = {"human": -1, "ai": 1, "tie": 0}


def minimax(lst, depth):
    result = check_winner(lst)
    if result:
        return scores[result]
    best_score = None
    if depth % 2 == 1:
        for a in range(3):
            for b in range(3):
                if lst[a][b] == '':
                    lst[a][b] = "human"
                    score = minimax(lst, depth + 1)
                    lst[a][b] = ''
                    if best_score is None or score < best_score:
                        best_score = score
        return best_score

    if depth % 2 == 0:
        for a in range(3):
            for b in range(3):
                if lst[a][b] == '':
                    lst[a][b] = "ai"
                    score = minimax(lst, depth + 1)
                    lst[a][b] = ''
                    if best_score is None or score > best_score:
                        best_score = score
        return best_score


def ai(lst):
    best_score = None
    best_move = None
    for a in range(3):
        for b in range(3):
            if lst[a][b] == '':
                lst[a][b] = "ai"
                score = minimax(lst, 1)
                lst[a][b] = ''
                if best_score is None or score > best_score:
                    best_score = score
                    best_move = a, b
    return best_move


class Board:
    def __init__(self, turn="human"):
        self.board = list(['', '', ''] for a in range(3))
        self.turn = turn
        self.winner = ''

    def update(self):
        self.winner = check_winner(self.board)
        if self.winner == "human":
            show_text("Human won")
            return
        if self.winner == "ai":
            show_text("A.I. won")
            return
        if self.winner == "tie":
            show_text("It's a tie")
            return

    def play(self, pos):
        if self.turn == "human":
            x, y = int(pos[1] / height * 3), int(pos[0] / width * 3)
            self.board[x][y] = "human"
            self.turn = "ai"
            if check_winner(self.board): return
            x, y = ai(self.board)
            self.board[x][y] = "ai"
            self.turn = "human"

    def draw_board(self, surface):
        x_, y_ = width // 3, height // 3
        for a in range(x_, width, x_):
            py.draw.line(surface, (0, 0, 0), (a, 0), (a, height))

        for a in range(y_, height, y_):
            py.draw.line(surface, (0, 0, 0), (0, a), (width, a))

        for a in range(3):
            for b in range(3):
                if self.board[b][a] == "human":
                    # draw X
                    py.draw.line(surface, (0, 0, 0), (a * x_ + offset, b * y_ + offset),
                                 ((a + 1) * x_ - offset, (b + 1) * y_ - offset), edge_thickness)
                    py.draw.line(surface, (0, 0, 0), ((a + 1) * x_ - offset, b * y_ + offset),
                                 (a * x_ + offset, (b + 1) * y_ - offset), edge_thickness)

                elif self.board[b][a] == "ai":
                    # draw O
                    py.draw.circle(surface, (0, 0, 0), (a * x_ + x_ // 2, b * y_ + x_ // 2), x_ // 2 - offset,
                                   edge_thickness)


py.init()

width, height = 300, 300

window = py.display.set_mode((width, height))

running = True

offset = 15

clock = py.time.Clock()
frame_rate = 60

edge_thickness = 2

board = Board()

font = py.font.Font("freesansbold.ttf", 32)

while running:
    clock.tick(frame_rate)

    window.fill((255, 255, 255))
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        if event.type == py.MOUSEBUTTONDOWN:
            board.play(py.mouse.get_pos())

    board.draw_board(window)
    board.update()
    if board.turn == "ai" and board.winner != "tie":
        i, j = ai(board.board)
        board.board[i][j] = "ai"
        board.turn = "human"
    py.display.update()
