import util
import engine
import ui

PLAYER_ICON = '@'
PLAYER_START_X = 17
PLAYER_START_Y = 2

BOARD_WIDTH = 30
BOARD_HEIGHT = 20

color_scheme = {0: ' ', 1: '▅', 2: 'E', 3: 'X', 4: 'O'}


def create_player():
    player = {'X': PLAYER_START_X, 'Y': PLAYER_START_Y, 'HP': 100}
    return player


def main():
    player = create_player()
    board = engine.create_board()
    util.clear_screen()
    is_running = True
    current_room = board[0]
    while is_running:
        engine.put_player_on_board(current_room, player)
        ui.display_board(current_room, color_scheme)
        player_coordinates = player['X'], player['Y']

        button = util.key_pressed()
        direction_vectors = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if button in direction_vectors:
            direction = direction_vectors[button]
            if engine.check_target_cell(current_room, player_coordinates, direction):
                current_room[player_coordinates[0]][player_coordinates[1]] = ' '
                player_coordinates = engine.new_player_position(current_room, player_coordinates, direction)
                current_room[player_coordinates[0]][player_coordinates[1]] = '@'
        util.clear_screen()
        ui.display_board(current_room, color_scheme)



if __name__ == '__main__':
    main()
