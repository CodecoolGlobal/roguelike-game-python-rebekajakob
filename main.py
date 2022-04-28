from defer import return_value
import util
import engine
import ui
import time
import random
import sys
import select
import tty
import termios



PLAYER_START_X = 17
PLAYER_START_Y = 2
# PLAYER_START_X = 4
# PLAYER_START_Y = 28

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
CURRENTROOMINDEX = 0



def create_player() -> dict:
    """Sets the player's attributes
    'X'=starter position
    'Y'=starter position
    'HP'= hitpoint
    """
    player = {'X': PLAYER_START_X, 'Y': PLAYER_START_Y, 'HP': 100, 'COINS': 0, 'ATTACK': 5, 'INVENTORY': [], 'NAME' : None}
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
        NPC: '🧙',
        BOSS: '👹',
        BASIC_WEAPON: '🏹',
        ADVANCED_WEAPON: '🔪',
        POTION: '💧',
        STRONG_MONSTER: '🦂'
        }
    ui.greet()
    menu_option = None
    while menu_option != 1:
        menu_option = ui.menu()
        if menu_option == 4:
            exit()
        elif menu_option == 3:
            ui.credits()
        elif menu_option == 2:
            print()
            ui.highscore()
    character_name, avatar  = ui.newgame_settings()
    color_scheme[4] = avatar
    player = create_player()
    player['NAME'] = character_name.upper()
    board = engine.create_board(BOARD_WIDTH, BOARD_HEIGHT)
    util.clear_screen()

    def isData():
        return select.select([sys.stdin], [], [], 0) == ([sys.stdin], [], [])

    old_settings = termios.tcgetattr(sys.stdin)
    try:
        tty.setcbreak(sys.stdin.fileno())
        timer = 0
        game_state = {"current_room_index": 0, "current_room":board[0], 'cheater': False}
        while True:
            if 'BASIC WEAPON' in player['INVENTORY']:
                player['ATTACK'] = 10
            if 'ADVANCED WEAPON' in player['INVENTORY']:
                player['ATTACK'] = 20
            current_room = board[game_state["current_room_index"]]
            engine.put_player_on_board(current_room, player)
            ui.display_board(current_room, player, color_scheme)
            player_coordinates = player['X'], player['Y']
            do_monster_movement(game_state, current_room, timer, player, color_scheme)
            timer += 1
            time.sleep(0.02)
            if isData():
                button = sys.stdin.read(1)
                if button == '\x1b':         # x1b is ESC
                    break
                if not handle_keypress(button, player, current_room, game_state, board, color_scheme, player_coordinates): 
                    break
    finally:
        exit()
        termios.tcsetattr(sys.stdin, termios.TCSADRAIN, old_settings)


def handle_keypress(button, player, current_room, game_state, board, color_scheme, player_coordinates):
    if button == 'q':
        print("Goodbye!")
        exit()
    elif button == 'c':
        player['COINS'] = 999
        player['HP'] = 999
        player['ATTACK'] = 999
        game_state['cheater'] = True
    elif button == 'i':
            print(f"INVENTORY: {', '.join(player['INVENTORY'])}")
            time.sleep(2)
    elif button == "p":
        print(f"STATISTICS: DEAD MONSTERS: {dead_monsters}")
        time.sleep(2)
    direction_vectors = {'w': (-1, 0), 's': (1, 0), 'a': (0, -1), 'd': (0, 1)}
    if button in direction_vectors:
        direction = direction_vectors[button]
        if engine.check_target_cell(current_room, player_coordinates, direction) == EMPTY_CELL:
            player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)

        elif engine.check_target_cell(current_room, player_coordinates, direction) == ENTRY_DOOR:
            current_room[player_coordinates[0]][player_coordinates[1]] = EMPTY_CELL
            game_state["current_room_index"] -= 1
            current_room = board[game_state["current_room_index"]]
            if game_state["current_room_index"] == 0:
                player['X'], player['Y'] = 4, 28
            elif game_state["current_room_index"] == 1:
                player['X'], player['Y'] = 18, 26
            


        elif engine.check_target_cell(current_room, player_coordinates, direction) == EXIT_DOOR:
            current_room[player_coordinates[0]][player_coordinates[1]] = EMPTY_CELL
            game_state["current_room_index"] += 1
            current_room = board[game_state["current_room_index"]]
            if game_state["current_room_index"] == 1:
                player['X'], player['Y'] = 4, 1
            elif game_state["current_room_index"] == 2:
                player['X'], player['Y'] = 1, 26

        elif engine.check_target_cell(current_room, player_coordinates, direction) == COIN:
            player['COINS'] += random.randrange(5, 21)
            player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)

        elif engine.check_target_cell(current_room, player_coordinates, direction) == MONSTER:
            player['HP'] -= 10
            for monster in engine.MONSTERS[game_state["current_room_index"]]:
                if monster['X'] == player_coordinates[0] + direction[0] and monster['Y'] == player_coordinates[1] + direction[1]:
                    monster['HP'] -= player['ATTACK']
                    if engine.check_creature_is_dead(monster):
                        engine.MONSTERS[game_state["current_room_index"]].remove(monster)
                        chance = [EMPTY_CELL, COIN]
                        current_room[monster['X']][monster['Y']] = random.choice(chance)

        elif engine.check_target_cell(current_room, player_coordinates, direction) == STRONG_MONSTER:
            player['HP'] -= int(15 * random.uniform(0.7, 1.3))
            for monster in engine.STRONG_MONSTERS[current_room_index]:
                if monster['X'] == player_coordinates[0] + direction[0] and monster['Y'] == player_coordinates[1] + direction[1]:
                    monster['HP'] -= player['ATTACK'] * random.uniform(0.7, 1.3)
                    if engine.check_creature_is_dead(monster):
                        engine.STRONG_MONSTERS[game_state["current_room_index"]].remove(monster)
                        dead_monsters += 1
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
            player['HP'] -= int(15 * random.uniform(0.7, 1.3))
            for boss_part in engine.BOSSES[0]:
                if boss_part['X'] == player_coordinates[0] + direction[0] and boss_part['Y'] == player_coordinates[1] + direction[1]:
                    boss_part['HP'] -= player['ATTACK'] * random.uniform(0.7, 1.3)
                    if engine.check_creature_is_dead(boss_part):
                        engine.BOSSES[0].remove(boss_part)
                        chance = [EMPTY_CELL]
                        current_room[boss_part['X']][boss_part['Y']] = random.choice(chance)
                    if len(engine.BOSSES[0]) == 0:
                        dead_monsters += 1
                        util.clear_screen()
                        ui.display_board(current_room, player, color_scheme)
                        if not cheater:
                            highscore = player['NAME'], str(player['COINS']), str(dead_monsters)
                            with open("log.txt", "a") as log:
                                log.write((' '.join(highscore) + '\n'))
                        print("YOU WON THE GAME!!")
                        exit()

        elif engine.check_target_cell(current_room, player_coordinates, direction) == NPC:
            if len(engine.MONSTERS[1]) == 0 and len(engine.STRONG_MONSTERS[1]) == 0:
                answer = input('Do you want to hunt more? (Y,N): ')
                if answer == 'y':
                    engine.spawn_monsters(current_room)
                    util.clear_screen()
                    ui.display_board(current_room, player, color_scheme)
                     
            
            print("What do you want?")
            answer = input("1. Potion (15 coin), 2. Weapon (75 coin), 3. Nevermind: ")
            if answer == '1':
                if player['COINS'] >= 15:
                    print("Here is a potion.")
                    time.sleep(1.5)
                    while True:
                        new_directions = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                        if engine.check_target_cell(current_room, (16, 25), new_directions) == EMPTY_CELL:
                            potion_coordinates = engine.new_creature_position((16, 25), new_directions)
                            current_room[potion_coordinates[0]][potion_coordinates[1]] = POTION
                            player['COINS'] -= 15
                            break
                else:
                    print("You don't have enough money!")
                    time.sleep(1)
            elif answer == '2':
                if player['COINS'] >= 75:
                    print("Here is your weapon.")
                    time.sleep(1.5)
                    while True:
                        new_directions = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
                        if engine.check_target_cell(current_room, (16, 25), new_directions) == EMPTY_CELL:
                            weapon_coordinates = engine.new_creature_position((16, 25), new_directions)
                            current_room[weapon_coordinates[0]][weapon_coordinates[1]] = ADVANCED_WEAPON
                            player['COINS'] -= 75
                            break
                else:
                    print("You don't have enough money!")
                    time.sleep(1)
            elif answer == 3:
                pass

        elif engine.check_target_cell(current_room, player_coordinates, direction) == TACO:
            if player['HP'] < 85:
                player['HP'] += 15
                player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)
       
        elif engine.check_target_cell(current_room, player_coordinates, direction) == POTION:
            if player['HP'] < 100:
                player['HP'] = 100
                player_coordinates = engine.player_step_there(player, current_room, player_coordinates, direction)

        if engine.check_creature_is_dead(player):
            player['HP'] = 0
            current_room[player_coordinates[0]][player_coordinates[1]] = DEAD_PLAYER
            is_running = False
            util.clear_screen()
            ui.display_board(current_room, player, color_scheme)
            print("GAME OVER! You are dead!")
            print()
            return False
        
        ui.display_board(current_room, player, color_scheme, game_state["current_room_index"])
    return True


def do_monster_movement(game_state, current_room, timer, player, color_scheme):
    if timer % 50 == 0:
        for monster in engine.MONSTERS[game_state["current_room_index"]]:
            new_directions = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            if engine.check_target_cell(current_room, (monster['X'], monster['Y']), new_directions) == 0:
                current_room[monster['X']][monster['Y']] = EMPTY_CELL
                monster_coordinates = engine.new_creature_position((monster['X'], monster['Y']), new_directions)
                monster['X'], monster['Y'] = monster_coordinates[0], monster_coordinates[1]
                current_room[monster_coordinates[0]][monster_coordinates[1]] = MONSTER

        for monster in engine.STRONG_MONSTERS[game_state["current_room_index"]]:
            new_directions = random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])
            if engine.check_target_cell(current_room, (monster['X'], monster['Y']), new_directions) == 0:
                current_room[monster['X']][monster['Y']] = EMPTY_CELL
                monster_coordinates = engine.new_creature_position((monster['X'], monster['Y']), new_directions)
                monster['X'], monster['Y'] = monster_coordinates[0], monster_coordinates[1]
                current_room[monster_coordinates[0]][monster_coordinates[1]] = STRONG_MONSTER

        if game_state["current_room_index"] == 2:
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
        ui.display_board(current_room, player, color_scheme, game_state["current_room_index"])
        


if __name__ == '__main__':
    main()
