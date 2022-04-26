# coloring
import colorama

a = colorama.Fore.CYAN + "Q" + colorama.Style.RESET_ALL
print({a})

import util
def get_keypress():
    key = ""
    while key != 'q':
        key = util.key_pressed()
        print(key)
        print({key})
# get_keypress()

# board size
def print_board(width=30, height=20):
    board = []
    for i in range(height):
        row = []
        for i in range(width):
            row.append("X")
        board.append(row)
    for row in board:
        print(' '.join(row))
print_board()


# teli karakter: █

"""board number legacy:
0 = space, where you walk
1 = border color
2 = entry door
3 = exit door
4 = player
"""