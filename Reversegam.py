import random
import sys
WIDTH = 8
HEIGHT = 8


def draw_board(board):
    print('  12345678')
    print(' +--------+')
    for y in range(HEIGHT):
        print('%s|' % (y+1), end='')
        for x in range(WIDTH):
            print(board[x][y], end='')
        print('|%s' % (y+1))
    print(' +--------+')
    print('  12345678')


def get_new_board():
    board = []
    for i in range(WIDTH):
        board.append([' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '])
    return board


def is_valid_move(board, tile, x_start, y_start):
    if board[x_start][y_start] != ' ' or not is_on_board(x_start, y_start):
        return False

    if tile == 'X':
        other_tile = 'O'
    else:
        other_tile = 'X'

    tiles_to_flip = []

    for x_direction, y_direction in [[0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]:
        x, y = x_start, y_start
        x += x_direction
        y += y_direction
        while is_on_board(x, y) and board[x][y] == other_tile:
            # Keep moving in this direction
            x += x_direction
            y += y_direction
            if is_on_board(x, y) and board[x][y] == tile:
                # There are pieces to flip
                while True:
                    x -= x_direction
                    y -= y_direction
                    if x == x_start and y == y_start:
                        break
                    tiles_to_flip.append([x, y])

    if len(tiles_to_flip) == 0:
        return False
    return tiles_to_flip


def is_on_board(x, y):
    return 0 <= x <= (WIDTH - 1) and 0 <= y <= (HEIGHT - 1)


def get_board_with_valid_moves(board, tile):
    board_copy = get_board_copy(board)

    for x, y in get_valid_moves(board_copy, tile):
        board_copy[x][y] = '.'
    return board_copy


def get_valid_moves(board, tile):
    valid_moves = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if is_valid_move(board, tile, x, y):
                valid_moves.append([x, y])
    return valid_moves


def get_score_of_board(board):
    x_score = 0
    o_score = 0
    for x in range(WIDTH):
        for y in range(HEIGHT):
            if board[x][y] == 'X':
                x_score += 1
            if board[x][y] == 'Y':
                o_score += 1
    return {'X': x_score, 'O': o_score}


def enter_player_tile():
    tile = ''
    while not (tile == 'X' or tile == 'O'):
        print('Do you want to be X or O?')
        tile = input().upper()

        if tile == 'X':
            return ['X', 'O']
        else:
            return ['O', 'X']


def who_goes_first():
    if random.randint(0, 1) == 0:
        return 'computer'
    else:
        return 'player'


def make_move(board, tile, x_start, y_start):
    tiles_to_flip = is_valid_move(board, tile, x_start, y_start)
    if not tiles_to_flip:
        return False

    board[x_start][y_start] = tile

    for x, y in tiles_to_flip:
        board[x][y] = tile
    return True


def get_board_copy(board):
    board_copy = get_new_board()
    for x in range(WIDTH):
        for y in range(HEIGHT):
            board_copy[x][y] = board[x][y]
    return board_copy


def is_on_corner(x, y):
    return (x == 0 or x == WIDTH - 1) and (y == 0 or y == HEIGHT - 1)


def get_player_move(board, player_tile):

