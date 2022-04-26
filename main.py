import util
import engine
import ui

PLAYER_ICON = '@'
PLAYER_START_X = 17
PLAYER_START_Y = 2

BOARD_WIDTH = 30
BOARD_HEIGHT = 20


def create_player():
    player = {'X': PLAYER_START_X, 'Y': PLAYER_START_Y, 'HP': 100}
    return player


def main():
    player = create_player()
    board = engine.create_board()
    util.clear_screen()
    is_running = True
    while is_running:
    #     engine.put_player_on_board(board, player)
    #     ui.display_board(board)

    #     key = util.key_pressed()
    #     if key == 'q':
    #         is_running = False
    #     else:
    #         pass
    #     util.clear_screen()

    # while True:
    # button = util.key_pressed()
    # direction_vectors = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
    # if button in direction_vectors:
    #     direction = direction_vectors[button]
    #     if check_target_cell(player_coordinates, direction):
    #         board[player_coordinates[0]][player_coordinates[1]] = ' '
    #         player_coordinates = new_player_position(player_coordinates, direction)
    #         board[player_coordinates[0]][player_coordinates[1]] = '@'
    # util.clear_screen()
    # print_board(board)



if __name__ == '__main__':
    main()
