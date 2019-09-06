import random
import sys
WIDTH = 8
HEIGHT = 8


def draw_horizontal_border(top: bool):
    a, b = ' 1 2 3 4 5 6 7 8', ' ' + '+' + '-' * 8 + '+'
    c = (a, b) if top else (b, a)
    print(c[0], '\n', c[1])


def draw_board(board):
    # old
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
    other_tile = 'O' if tile == 'X' else 'X'

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
    return x in range(WIDTH) and y in range(HEIGHT)


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
    x_score = o_score = 0
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
    digits = '1 2 3 4 5 6 7 8'.split()
    while True:
        print('Enter your move, "quit" to end the game, or "hints" to toggle hints.')
        move = input().lower()
        if move == 'quit' or move == 'hints':
            return move
        if len(move) == 2 and move[0] in digits and move[1] in digits:
            x = int(move[0]) - 1
            y = int(move[1]) - 1
            if not is_valid_move(board, player_tile, x, y):
                continue
            else:
                break
        else:
            print('That is not a valid move. Enter the column (1-8) and then thr row (1-8).')
            print('For example, 81 will move on the top-right corner.')
    return [x, y]


def get_computer_move(board, computer_tile):
    possible_moves = get_valid_moves(board, computer_tile)
    random.shuffle(possible_moves)
    for x, y in possible_moves:
        if is_on_corner(x, y):
            return [x, y]
    best_score = -1
    best_move = []
    for x, y in possible_moves:
        board_copy = get_board_copy(board)
        make_move(board_copy, computer_tile, x, y)
        score = get_score_of_board(board_copy)[computer_tile]
        if score > best_score:
            best_move = [x, y]
            best_score = score
    return best_move


def print_score(board, player_tile, computer_tile):
    scores = get_score_of_board(board)
    print('You: %s points. Computer: %s points.' % (scores[player_tile], scores[computer_tile]))


def play_game(player_tile, computer_tile):
    show_hints = False
    turn = who_goes_first()
    print('The ' + turn + ' will go first.')

    board = get_new_board()
    board[3][3] = 'X'
    board[3][4] = 'O'
    board[4][3] = 'O'
    board[4][4] = 'X'

    while True:
        player_valid_moves = get_valid_moves(board, player_tile)
        computer_valid_moves = get_valid_moves(board, computer_tile)
        if player_valid_moves == [] and computer_valid_moves == []:
            return board
        elif turn == 'player':
            if not player_valid_moves:
                if show_hints:
                    valid_moves_board = get_board_with_valid_moves(board, player_tile)
                    draw_board(valid_moves_board)
                else:
                    draw_board(board)
                print_score(board, player_tile, computer_tile)

                move = get_player_move(board, player_tile)
                if move == 'quit':
                    print('Thanks for playing!')
                    sys.exit()
                elif move == 'hints':
                    show_hints = not show_hints
                    continue
                else:
                    make_move(board, player_tile, move[0], move[1])
            turn = 'computer'
        elif turn == 'computer':
            if not computer_valid_moves:
                draw_board(board)
                print_score(board, player_tile, computer_tile)
                input('Press Enter to see the computer\'s move')
                move = get_computer_move(board, computer_tile)
                make_move(board, computer_tile, move[0], move[1])
            turn = 'player'


def play():
    print('Welcome to Reversegam!')
    player_tile, computer_tile = enter_player_tile()
    while True:
        final_board = play_game(player_tile, computer_tile)
        draw_board(final_board)
        scores = get_score_of_board(final_board)
        print('X scored %s points. O scored %s points.' % (scores['X'], scores['O']))
        if scores[player_tile] > scores[computer_tile]:
            print('You beat the computer by %s points! Congratulations!'
                  % (scores[player_tile] - scores[computer_tile]))
        elif scores[player_tile] < scores[computer_tile]:
            print('You lost. The computer beat you by %s points.' % (scores[computer_tile] - scores[player_tile]))
        else:
            print('The game was a tie!')
        print('Do you want to play again? (yes or no)')
        if not input().lower().startswith('y'):
            break


play()
