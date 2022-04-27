import util
import engine
import ui
import time
import random

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
DEAD_PLAYER = 7
TACO = 8
NPC = 9


def create_player() -> dict:
    """Sets the player's attributes
    'X'=starter position
    'Y'=starter position
    'HP'= hitpoint
    """
    player = {'X': PLAYER_START_X, 'Y': PLAYER_START_Y, 'HP': 100, 'COINS': 0}
    return player



def main() -> None:
    color_scheme = {
        EMPTY_CELL: '  ',
        WALL_CELL: '🌵',
        ENTRY_DOOR: '🚪',
        EXIT_DOOR: '🚪',
        PLAYER: '🤠',
        TACO: '🌮',
        COIN: '💰',
        MONSTER: '👾',
        DEAD_PLAYER: '💀',
        NPC: '🎅'
        }
    player = create_player()
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    util.clear_screen()
    is_running = True
    current_room_index = 0
    while is_running:
        current_room = board[current_room_index]
        engine.put_player_on_board(current_room, player)
        ui.display_board(current_room, player, color_scheme)
        player_coordinates = player['X'], player['Y']

        for monster in engine.MONSTERS[current_room_index]:
            new_directions = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            if engine.check_target_cell(current_room, (monster['X'], monster['Y']), new_directions) == 0:
                current_room[monster['X']][monster['Y']] = EMPTY_CELL
                monster_coordinates = engine.monster_movement((monster['X'], monster['Y']), new_directions)
                monster['X'], monster['Y'] = monster_coordinates[0], monster_coordinates[1]
                current_room[monster_coordinates[0]][monster_coordinates[1]] = MONSTER

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
                current_room[player_coordinates[0]][player_coordinates[1]] = PLAYER

            elif engine.check_target_cell(current_room, player_coordinates, direction) == ENTRY_DOOR:
                current_room[player_coordinates[0]][player_coordinates[1]] = EMPTY_CELL
                current_room_index -= 1
                current_room = board[current_room_index]
                if current_room_index == 0:
                    player['X'], player['Y'] = 4, 28
                elif current_room_index == 1:
                    player['X'], player['Y'] = 18, 26

            elif engine.check_target_cell(current_room, player_coordinates, direction) == EXIT_DOOR:
                current_room[player_coordinates[0]][player_coordinates[1]] = EMPTY_CELL
                current_room_index += 1
                current_room = board[current_room_index]
                if current_room_index == 1:
                    player['X'], player['Y'] = 4, 1
                elif current_room_index == 2:
                    player['X'], player['Y'] = 1, 26

            elif engine.check_target_cell(current_room, player_coordinates, direction) == COIN:
                player['COINS'] += 1
                current_room[player_coordinates[0]][player_coordinates[1]] = EMPTY_CELL
                player_coordinates = engine.new_player_position(player_coordinates, direction)
                player['X'], player['Y'] = player_coordinates[0], player_coordinates[1]
                current_room[player_coordinates[0]][player_coordinates[1]] = PLAYER

            elif engine.check_target_cell(current_room, player_coordinates, direction) == MONSTER:
                player['HP'] -= 10
                for monster in engine.MONSTERS[current_room_index]:
                    if monster['X'] == player_coordinates[0] + direction[0] and monster['Y'] == player_coordinates[1] + direction[1]:
                        monster['HP'] -= 10
                        engine.MONSTERS[current_room_index].remove(monster)
                        if engine.check_creature_is_dead(monster):
                            chance = [EMPTY_CELL, EMPTY_CELL, COIN]
                            current_room[monster['X']][monster['Y']] = random.choice(chance)
            
            elif engine.check_target_cell(current_room, player_coordinates, direction) == NPC:
                print("Hello, player!")
                time.sleep(2)
            
            elif engine.check_target_cell(current_room, player_coordinates, direction) == TACO:
                if player['HP'] < 100:
                    player['HP'] += 10
                    current_room[player_coordinates[0]][player_coordinates[1]] = EMPTY_CELL
                    player_coordinates = engine.new_player_position(player_coordinates, direction)
                    player['X'], player['Y'] = player_coordinates[0], player_coordinates[1]
                    current_room[player_coordinates[0]][player_coordinates[1]] = PLAYER


            if engine.check_creature_is_dead(player):
                current_room[player_coordinates[0]][player_coordinates[1]] = DEAD_PLAYER
                is_running = False
                util.clear_screen()
                ui.display_board(current_room, player, color_scheme)
                print("GAME OVER! You are dead!")
                print()
                break

        util.clear_screen()


if __name__ == '__main__':
    main()
