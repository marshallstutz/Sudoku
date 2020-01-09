import pygame
import sys

class SudokuItem:
    def __init__(self, value, is_locked, min_value):
        self.value = value
        self.is_locked = is_locked
        self.min_value = min_value

board = []
row = 0
col = 0
max_value = 9
board_solved = 0
iterations = 0
BOXSIZE = 40
SMALLWIDTH = 2
LARGEWIDTH = 4

BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255, 0,0)
GREEN = (0,255,0)
GRAY = (128, 128, 128)

new_board = [[0,3,1,0,0,0,4,0,0],
            [0,4,0,0,0,0,0,5,2],
            [0,0,0,5,0,0,0,0,0],
            [0,0,6,1,0,0,2,0,0],
            [0,1,0,3,0,6,0,0,0],
            [7,0,0,2,0,0,0,9,1],
            [9,0,0,0,0,0,0,7,0],
            [0,0,0,0,6,0,0,0,0],
            [0,0,0,9,0,8,0,0,5]]

#new_board = [[0,0,0,0,0,0,0,0,0],
 #           [0,0,0,0,0,0,0,0,0],
  #          [0,0,0,0,0,0,0,0,0],
   #         [0,0,0,0,0,0,0,0,0],
    #        [0,0,0,0,0,0,0,0,0],
     #       [0,0,0,0,0,0,0,0,0],
      #      [0,0,0,0,0,0,0,0,0],
       #     [0,0,0,0,0,0,0,0,0],
        #    [0,0,0,0,0,0,0,0,0]]

def initialize_board(arr):
    global board
    for x in range(9):
        board.append(0)
        board[x] = []
        for y in range(9):
            board[x].append(0)
            if new_board[x][y] != 0:
                board[x][y] = SudokuItem(new_board[x][y], 1, 0) #Locked item
                fill_box(GRAY, x, y, board[x][y].value)
            else:
                board[x][y] = SudokuItem(new_board[x][y], 0, 1)
                fill_box(WHITE, x, y, '')
            pygame.display.update()

def get_next_val():
    global col
    global row
    global board_solved
    global board
    global iterations
    iterations += 1
    if board[row][col].min_value > max_value:
        board[row][col].min_value = 1
        return 0
    for i in range(board[row][col].min_value,10):
        if is_valid(i):
            board[row][col].min_value = i + 1
            fill_box(GREEN, row, col, i)
            pygame.display.update()
            return i
    board[row][col].min_value = 1
    return 0


def is_valid(val):
    global col
    global row
    global board
    global board_solved
    for i in range(9):
        if board[row][i].value == val:
            return 0
    for i in range(9):
        if board[i][col].value == val:
            return 0
    temp_row, temp_col = 0, 0
    if row % 3 == 0:
        temp_row = row
    elif row % 3 == 1:
        temp_row = row - 1
    else:
        temp_row = row - 2
    if col % 3 == 0:
        temp_col = col
    elif col % 3 == 1:
        temp_col = col - 1
    else:
        temp_col = col - 2
    if board[temp_row][temp_col].value == val or board[temp_row+1][temp_col].value == val or \
        board[temp_row+2][temp_col].value == val or board[temp_row][temp_col+1].value == val or \
        board[temp_row+1][temp_col+1].value == val or board[temp_row+2][temp_col+1].value == val or \
        board[temp_row][temp_col+2].value == val or board[temp_row+1][temp_col+2].value == val or \
        board[temp_row+2][temp_col+2].value == val:
        return 0
    return 1

def decrement():
    global col
    global row
    global board
    global board_solved
    if col > 0:
        col -= 1
    elif row > 0:
        row -= 1
        col = 8
    else:
        board_solved = -1
    if board[row][col].is_locked:
        decrement()

def increment():
    global col
    global row
    global board
    global board_solved
    if col < 8:
        col += 1
    elif row < 8:
        row += 1
        col = 0
    else:
        board_solved = 1
        return
    if board[row][col].is_locked:
        increment()

def solve_board(arr):
    global col
    global row
    global board_solved
    global board
    global max_value
    initialize_board(arr)
    board_solved = 0
    row = 0
    col = 0
    max_value = 9
    if board[0][0].value != 0:
        increment()
    while board_solved == 0:
        board[row][col].value = get_next_val()
        if board[row][col].value == 0:
            fill_box(RED, row, col, '')
            pygame.display.update()
            decrement()
        else:
            increment()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            pygame.display.update()
        #pygame.time.wait(10)
    print_board()
    return board_solved

def print_board():
    global board
    for i in range(9):
        for j in range(9):
            print(board[i][j].value, end = ' ')
        print()

def draw_outline():
    return

def fill_box(color, i, j, val):
    temp_rect = pygame.Rect(LARGEWIDTH + i * (BOXSIZE + SMALLWIDTH),LARGEWIDTH + j * (BOXSIZE + SMALLWIDTH), BOXSIZE, BOXSIZE)
    pygame.draw.rect(screen, color, temp_rect)
    pygame.draw.rect
    text_to_screen(screen, val, temp_rect.centerx - BOXSIZE/6, temp_rect.centery - BOXSIZE/2)

def text_to_screen(new_screen, text, x, y, size = 25,
            color = (0, 0, 0)):
    text = str(text)
    font = pygame.font.Font('C:\WINDOWS\Fonts\Comic.ttf', size)
    text = font.render(text, True, color)
    screen.blit(text, (x, y))

pygame.init()
screen = pygame.display.set_mode((500,400))
pygame.display.set_caption('Sudoku')
screen.fill(BLACK)
pygame.display.update()
board_solved = solve_board(new_board)
if board_solved == 1:
    print("completed successfully")
    print(iterations)
else:
    print("something went wrong")

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        pygame.display.update()