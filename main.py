import util
import engine
import ui

PLAYER_START_X = 17
PLAYER_START_Y = 2

BOARD_WIDTH = 30
BOARD_HEIGHT = 20

EMPTY_CELL = 0
WALL_CELL = 1
ENTRY_DOOR = 2
EXIT_DOOR = 3
PLAYER = 4
COIN = 5
MONSTER = 6


def create_player():
    """Sets the player's attributes
    'X'=starter position
    'Y'=starter position
    'HP'= hitpoint
    """
    player = {'X': PLAYER_START_X, 'Y': PLAYER_START_Y, 'HP': 100, 'COINS': 0}
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
        ui.display_board(current_room, player)
        player_coordinates = player['X'], player['Y']

        button = util.key_pressed()
        if button == 'q':
            print("Goodbye!")
            exit()
        direction_vectors = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if button in direction_vectors:
            direction = direction_vectors[button]
            if engine.check_target_cell(current_room, player_coordinates, direction) == EMPTY_CELL:
                current_room[player_coordinates[0]][player_coordinates[1]] = EMPTY_CELL
                player_coordinates = engine.new_player_position(player_coordinates, direction)
                player['X'], player['Y'] = player_coordinates[0], player_coordinates[1]
                current_room[player_coordinates[0]][player_coordinates[1]] = 4
  
            elif engine.check_target_cell(current_room, player_coordinates, direction) == ENTRY_DOOR:
                current_room[player_coordinates[0]][player_coordinates[1]] = 0
                current_room_index -= 1
                current_room = board[current_room_index]
                if current_room_index == 0:
                    player['X'], player['Y'] = 4, 28
                elif current_room_index == 1:
                    player['X'], player['Y'] = 18, 26

            elif engine.check_target_cell(current_room, player_coordinates, direction) == EXIT_DOOR:
                current_room[player_coordinates[0]][player_coordinates[1]] = 0
                current_room_index += 1    
                current_room = board[current_room_index]
                if current_room_index == 1:
                    player['X'], player['Y'] = 4, 1
                elif current_room_index == 2:
                    player['X'], player['Y'] = 1, 26

            elif engine.check_target_cell(current_room, player_coordinates, direction) == COIN:
                player['COINS'] += 1
                current_room[player_coordinates[0]][player_coordinates[1]] = 0
                player_coordinates = engine.new_player_position(player_coordinates, direction)
                player['X'], player['Y'] = player_coordinates[0], player_coordinates[1]
                current_room[player_coordinates[0]][player_coordinates[1]] = 4

            elif engine.check_target_cell(current_room, player_coordinates, direction) == MONSTER:
                player['HP'] -= 10
                # monster['HP'] -= 10

            if engine.check_hp(player):
                current_room[player_coordinates[0]][player_coordinates[1]] = 7
                is_running = False
                util.clear_screen()
                ui.display_board(current_room, player)
                print("GAME OVER! You are dead!")
                print()
                break
        util.clear_screen()


if __name__ == '__main__':
    main()
