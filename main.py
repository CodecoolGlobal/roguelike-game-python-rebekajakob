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
BOSS = 10
BASIC_WEAPON = 11
ADVANCED_WEAPON = 12
POTION = 13
STRONG_MONSTER = 14


def create_player() -> dict:
    """Sets the player's attributes
    'X'=starter position
    'Y'=starter position
    'HP'= hitpoint
    """
    player = {'X': PLAYER_START_X, 'Y': PLAYER_START_Y, 'HP': 100, 'COINS': 0, 'ATTACK': 5, 'INVENTORY': []}
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
        NPC: '🎅',
        BOSS: '👹',
        BASIC_WEAPON: '🏹',
        ADVANCED_WEAPON: '🔪',
        POTION: '💧',
        STRONG_MONSTER: '🦂'
        }
    player = create_player()
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    util.clear_screen()
    is_running = True
    current_room_index = 0
    while is_running:
        if 'BASIC WEAPON' in player['INVENTORY']:
            player['ATTACK'] = 10
        if 'ADVANCED WEAPON' in player['INVENTORY']:
            player['ATTACK'] = 20
        current_room = board[current_room_index]
        engine.put_player_on_board(current_room, player)
        ui.display_board(current_room, player, color_scheme)
        player_coordinates = player['X'], player['Y']

        for monster in engine.MONSTERS[current_room_index]:
            new_directions = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            if engine.check_target_cell(current_room, (monster['X'], monster['Y']), new_directions) == 0:
                current_room[monster['X']][monster['Y']] = EMPTY_CELL
                monster_coordinates = engine.new_creature_position((monster['X'], monster['Y']), new_directions)
                monster['X'], monster['Y'] = monster_coordinates[0], monster_coordinates[1]
                current_room[monster_coordinates[0]][monster_coordinates[1]] = MONSTER

        if current_room_index == 2:
            good_movements = 0
            new_directions = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            for boss in engine.BOSSES[0]:
                if engine.check_target_cell(current_room, (boss['X'], boss['Y']), new_directions) in [EMPTY_CELL, BOSS]:
                    good_movements += 1
            if good_movements == len(engine.BOSSES[0]):
                for boss in engine.BOSSES[0]:
                    current_room[boss['X']][boss['Y']] = EMPTY_CELL
                for boss in engine.BOSSES[0]:
                    boss_coordinates = engine.new_creature_position((boss['X'], boss['Y']), new_directions)
                    boss['X'], boss['Y'] = boss_coordinates[0], boss_coordinates[1]
                    current_room[boss_coordinates[0]][boss_coordinates[1]] = BOSS

        button = util.key_pressed()
        if button == 'q':
            print("Goodbye!")
            exit()
        elif button == 'c':
            player['COINS'] = 999
            player['HP'] = 999
        direction_vectors = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
        if button in direction_vectors:
            direction = direction_vectors[button]
            if engine.check_target_cell(current_room, player_coordinates, direction) == EMPTY_CELL:
                player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)

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
                player['COINS'] += random.randrange(5, 21)
                player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)

            elif engine.check_target_cell(current_room, player_coordinates, direction) == MONSTER:
                player['HP'] -= 10
                for monster in engine.MONSTERS[current_room_index]:
                    if monster['X'] == player_coordinates[0] + direction[0] and monster['Y'] == player_coordinates[1] + direction[1]:
                        monster['HP'] -= player['ATTACK']
                        if engine.check_creature_is_dead(monster):
                            engine.MONSTERS[current_room_index].remove(monster)
                            chance = [EMPTY_CELL, COIN]
                            current_room[monster['X']][monster['Y']] = random.choice(chance)

            elif engine.check_target_cell(current_room, player_coordinates, direction) == STRONG_MONSTER:
                player['HP'] -= 15
                for monster in engine.STRONG_MONSTERS[current_room_index]:
                    if monster['X'] == player_coordinates[0] + direction[0] and monster['Y'] == player_coordinates[1] + direction[1]:
                        monster['HP'] -= player['ATTACK']
                        if engine.check_creature_is_dead(monster):
                            engine.STRONG_MONSTERS[current_room_index].remove(monster)
                            chance = [COIN]
                            current_room[monster['X']][monster['Y']] = random.choice(chance)

            elif engine.check_target_cell(current_room, player_coordinates, direction) == BASIC_WEAPON:
                if 'BASIC WEAPON'not in player['INVENTORY']:
                    player['INVENTORY'].append('BASIC WEAPON')
                player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)

            elif engine.check_target_cell(current_room, player_coordinates, direction) == ADVANCED_WEAPON:
                if 'ADVANCED WEAPON'not in player['INVENTORY']:
                    player['INVENTORY'].append('ADVANCED WEAPON')
                player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)

            elif engine.check_target_cell(current_room, player_coordinates, direction) == BOSS:
                player['HP'] -= 15
                for boss_part in engine.BOSSES[0]:
                    if boss_part['X'] == player_coordinates[0] + direction[0] and boss_part['Y'] == player_coordinates[1] + direction[1]:
                        boss_part['HP'] -= player['ATTACK']
                        if engine.check_creature_is_dead(boss_part):
                            engine.BOSSES[0].remove(boss_part)
                            chance = [EMPTY_CELL]
                            current_room[boss_part['X']][boss_part['Y']] = random.choice(chance)
                        if len(engine.BOSSES[0]) == 0:
                            util.clear_screen()
                            ui.display_board(current_room, player, color_scheme)
                            print("YOU WON THE GAME!!")
                            exit()

            elif engine.check_target_cell(current_room, player_coordinates, direction) == NPC:
                print("What do you want?")
                answer = input("1. Potion (10 coin), 2. Weapon (50 coin), 3. Nevermind: ")
                if answer == '1':
                    if player['COINS'] >= 10:
                        print("Here is a potion.")
                        time.sleep(1.5)
                        while True:
                            new_directions = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                            if engine.check_target_cell(current_room, (16, 25), new_directions) == EMPTY_CELL:
                                potion_coordinates = engine.new_creature_position((16, 25), new_directions)
                                current_room[potion_coordinates[0]][potion_coordinates[1]] = POTION
                                player['COINS'] -= 10
                                break
                    else:
                        print("You don't have enough money!")
                        time.sleep(1)
                elif answer == '2':
                    if player['COINS'] >= 50:
                        print("Here is your weapon.")
                        time.sleep(1.5)
                        while True:
                            new_directions = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                            if engine.check_target_cell(current_room, (16, 25), new_directions) == EMPTY_CELL:
                                weapon_coordinates = engine.new_creature_position((16, 25), new_directions)
                                current_room[weapon_coordinates[0]][weapon_coordinates[1]] = ADVANCED_WEAPON
                                player['COINS'] -= 50
                                break
                    else:
                        print("You don't have enough money!")
                        time.sleep(1)
                elif answer == 3:
                    pass

            elif engine.check_target_cell(current_room, player_coordinates, direction) == TACO:
                if player['HP'] < 100:
                    player['HP'] += 15
                    player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)

            elif engine.check_target_cell(current_room, player_coordinates, direction) == POTION:
                if player['HP'] < 100:
                    player['HP'] = 100
                    player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)

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
