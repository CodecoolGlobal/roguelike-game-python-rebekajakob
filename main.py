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
    """Sets the player's attributes
    'X'=starter position
    'Y'=starter position
    'HP'= hitpoint
    """
    player = {'X': PLAYER_START_X, 'Y': PLAYER_START_Y, 'HP': 100}
    return player


def main():
    player = create_player()
    board = engine.create_board()
    util.clear_screen()
    is_running = True
    current_room_index = 0
    while is_running:
        current_room = board[current_room_index]
        engine.put_player_on_board(current_room, player)
        ui.display_board(current_room, color_scheme)
        player_coordinates = player['X'], player['Y']

        button = util.key_pressed()
        direction_vectors = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if button in direction_vectors:
            direction = direction_vectors[button]
            if engine.check_target_cell(current_room, player_coordinates, direction) == 1: # player made a move to en empty cell
                current_room[player_coordinates[0]][player_coordinates[1]] = 0
                player_coordinates = engine.new_player_position(player_coordinates, direction)
                player['X'], player['Y'] = player_coordinates[0], player_coordinates[1]
                current_room[player_coordinates[0]][player_coordinates[1]] = 4
                
            elif engine.check_target_cell(current_room, player_coordinates, direction) == 2: # player went to the entry door of the room
                current_room[player_coordinates[0]][player_coordinates[1]] = 0
                current_room_index -= 1
                current_room = board[current_room_index]
                if current_room_index == 0:
                    player['X'], player['Y'] = 4 , 28
                elif current_room_index == 1:
                    player['X'], player['Y'] = 18, 26
                   
            elif engine.check_target_cell(current_room, player_coordinates, direction) == 3: # player went to the exit door of the room
                current_room[player_coordinates[0]][player_coordinates[1]] = 0
                current_room_index += 1    
                current_room = board[current_room_index]
                if current_room_index == 1:
                    player['X'], player['Y'] = 4 , 1
                elif current_room_index == 2:
                    player['X'], player['Y'] = 1, 26
        util.clear_screen()





if __name__ == '__main__':
    main()
