import numpy as np
import pygame
import sys
import math

BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

ROW_COUNT = 6
COLUMN_COUNT = 7



def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board


def drop_circle(board, row, col, piece):   # this is to drop the piece in the matrix
    board[row][col] = piece


def is_valid_location(board, col):    # checking the valid locations
    return board[ROW_COUNT-1][col] == 0


def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))


def winning_move(board, piece):

    # checking the horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c+1] == piece and board[r][c+2] == piece and board[r][c+3] == piece:
                return True

    # checking the vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c] == piece and board[r+2][c] == piece and board[r+3][c] == piece:
                return True

    # checking for positive slopes
    for c in range(COLUMN_COUNT-3):
        for r in range(ROW_COUNT-3):
            if board[r][c] == piece and board[r+1][c+1] == piece and board[r+2][c+2] == piece and board[r+3][c+3] == piece:
                return True



    # checking for negative slopes
    for c in range(COLUMN_COUNT-3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r-1][c+1] == piece and board[r-2][c+2] == piece and board[r-3][c+3] == piece:
                return True

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            pygame.draw.rect(screen, BLUE, (c * SQUARE, r * SQUARE + SQUARE, SQUARE, SQUARE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARE + SQUARE / 2), int(r * SQUARE + SQUARE + SQUARE / 2)), radius)

    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARE + SQUARE / 2), height - int(r * SQUARE + SQUARE / 2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARE + SQUARE / 2), height - int(r * SQUARE + SQUARE / 2)), radius)
    pygame.display.update()



board = create_board()
print_board(board)
game_over = False
turn = 0

pygame.init()
SQUARE = 100

width = COLUMN_COUNT * SQUARE
height = (ROW_COUNT+1) * SQUARE

radius = int(SQUARE/2 - 5)
size = (width, height)

screen = pygame.display.set_mode(size)
draw_board(board)
pygame.display.update()
myfont = pygame.font.SysFont("monospace", 80)

while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()


        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, BLACK,(0,0,width,SQUARE))
            posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, RED, (posx, int(SQUARE/2)), radius)
            else:
                pygame.draw.circle(screen, YELLOW, (posx, int(SQUARE / 2)), radius)
        pygame.display.update()

        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.draw.rect(screen, BLACK, (0, 0, width, SQUARE))
            # print(event.pos)

            # Ask player 1 for input
            if turn == 0:
                posx = event.pos[0]
                col = int(math.floor(posx/SQUARE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_circle(board, row, col, 1)

                    if winning_move(board, 1):
                        label = myfont.render("Player 1 WINS !!", 1, RED)
                        screen.blit(label,(40, 10))
                        game_over = True



            # Ask player 2 for input
            else:
                posx = event.pos[0]
                col = int(math.floor(posx / SQUARE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_circle(board, row, col, 2)

                    if winning_move(board, 2):
                        label = myfont.render("Player 2 WINS !!", 1, YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

            print_board(board)
            draw_board(board)

            turn += 1
            turn = turn % 2  # Alternates between 0 and 1

            if game_over:
                pygame.time.wait(3000)
