import random

EMPTY_CELL = 0
WALL_CELL = 1
ENTRY_DOOR = 2
EXIT_DOOR = 3
PLAYER = 4
COIN = 5
MONSTER = 6
MONSTERS = []
TACO = 8
NPC = 9
BOSS = 10
BOSSES = []
BASIC_WEAPON = 11
ADVANCED_WEAPON = 12
POTION = 13

def create_room(entry_door: tuple, exit_door: tuple, level: int, width: int, height: int) -> list:
    """Generates the rooms for the game
    (hard coded rooms)
    """
    room = []
    for row in range(height):
        current_row = []
        for col in range(width):
            if row == 0 or row == height - 1:
                current_row.append(WALL_CELL)
            else:
                if col == 0 or col == width - 1:
                    current_row.append(WALL_CELL)
                else:
                    current_row.append(EMPTY_CELL)
        room.append(current_row)
    create_doors(room, entry_door, exit_door)
    if level == 0:
        place_inner_wall(room, (10, 0), (10, 10))
        place_inner_wall(room, (5, 15), (13, 15))
        place_inner_wall(room, (15, 5), (19, 5))
        place_inner_wall(room, (15, 15), (19, 15))
        place_inner_wall(room, (7, 19), (7, 25))
        place_inner_wall(room, (8, 19), (8, 25))
        place_inner_wall(room, (9, 19), (9, 25))
        place_inner_wall(room, (10, 19), (10, 25))
        place_inner_wall(room, (11, 19), (11, 25))
        place_object(room, (4, 3),TACO)
        place_object(room, (9, 22),TACO)
        place_object(room, (5, 5), BASIC_WEAPON)
        current_room_monsters = []
        monster0 = place_monster(room, (5, 7))
        current_room_monsters.append(monster0)
        monster1 = place_monster(room, (4, 27))
        current_room_monsters.append(monster1)
        monster2 = place_monster(room, (17, 25))
        current_room_monsters.append(monster2)
        MONSTERS.append(current_room_monsters)
    if level == 1:
        place_inner_wall(room, (0, 8), (15, 8))
        place_inner_wall(room, (10, 14), (19, 14))
        place_inner_wall(room, (10, 15), (19, 15))
        place_inner_wall(room, (0, 18), (15, 18))
        place_inner_wall(room, (7, 21), (7, 25))
        place_inner_wall(room, (12, 21), (12, 29))
        place_inner_wall(room, (0, 25), (7, 25))
        place_object(room, (2, 27),TACO)
        place_object(room, (3, 19),TACO)
        place_object(room, (1, 17),TACO)
        place_object(room, (16, 16),NPC)
        current_room_monsters = []
        monster0 = place_monster(room, (3, 8))
        current_room_monsters.append(monster0)
        monster1 = place_monster(room, (8, 5))
        current_room_monsters.append(monster1)
        monster2 = place_monster(room, (15, 13))
        current_room_monsters.append(monster2)
        monster3 = place_monster(room, (18, 9))
        current_room_monsters.append(monster3)
        monster4 = place_monster(room, (3, 27))
        current_room_monsters.append(monster4)
        MONSTERS.append(current_room_monsters)

    if level == 2:
        place_inner_wall(room, (5, 10), (5, 10))
        place_inner_wall(room, (15, 11), (15, 11))
        place_inner_wall(room, (4, 20), (4, 20))
        place_inner_wall(room, (10, 20), (10, 20))
        current_room_monsters = []
        MONSTERS.append(current_room_monsters)
        boss1 = place_boss(room, (10, 10))
        boss2 = place_boss(room, (11, 10))
        boss3 = place_boss(room, (12, 10))
        boss4 = place_boss(room, (10, 11))
        boss5 = place_boss(room, (10, 12))
        boss6 = place_boss(room, (12, 12))
        boss7 = place_boss(room, (12, 11))
        boss8 = place_boss(room, (11, 12))
        boss9 = place_boss(room, (11, 11))
        BOSSES.append([boss1, boss2, boss3, boss4, boss5, boss6, boss7, boss8, boss9])

    return room


def create_monster() -> dict:
    """Sets the monster's attributes
    'HP'= hitpoint
    """
    monster = {'X': 0, 'Y': 0, 'HP': 10}
    return monster


def place_monster(room: list, coordinate: tuple) -> None:
    monster = create_monster()
    room[coordinate[0]][coordinate[1]] = MONSTER
    monster['X'] = coordinate[0]
    monster['Y'] = coordinate[1]
    return monster


def create_boss() -> dict:
    """Sets the bosses attributes
    'HP'= hitpoint
    """
    boss = {'X': 0, 'Y': 0, 'HP': 20}
    return boss


def place_boss(room: list, coordinate: tuple) -> None:
    boss = create_boss()
    room[coordinate[0]][coordinate[1]] = BOSS
    boss['X'] = coordinate[0]
    boss['Y'] = coordinate[1]
    return boss


def monster_movement(monster, new_directions):
    new_position_monster = (monster[0] + new_directions[0], monster[1] + new_directions[1])
    return new_position_monster


def place_object(room: int, coordinate: tuple, item: int) -> None:
    room[coordinate[0]][coordinate[1]] = item


def create_board(width, heigth) -> list:
    """Puts the rooms together into one board list
    (rooms need to be added manually)
    """
    entry_exit_door_positions = [(None, (4, 29)), ((4, 0), (19, 26)), ((0, 26), None)]
    return [create_room(doors[0], doors[1], i, width, heigth) for i, doors in enumerate(entry_exit_door_positions)]

def boss_movement(boss, new_directions):
    new_position_boss = (boss[0] + new_directions[0], boss[1] + new_directions[1])
    return new_position_boss

def create_doors(room: list, entry_door: tuple, exit_door: tuple) -> None:
    """Adds doors to given room
    write None to not add the door
    """
    if entry_door:
        room[entry_door[0]][entry_door[1]] = ENTRY_DOOR
    if exit_door:
        room[exit_door[0]][exit_door[1]] = EXIT_DOOR


def place_inner_wall(board: list, start_wall: tuple, end_wall: tuple) -> None:
    """Helper function for the room creation
    """
    if start_wall[0] == end_wall[0]:
        for i in range(start_wall[1], end_wall[1]+1):
            board[start_wall[0]][i] = WALL_CELL
    else:
        for i in range(start_wall[0], end_wall[0]+1):
            board[i][start_wall[1]] = WALL_CELL


def put_player_on_board(room: list, player: dict) -> None:
    """puts player on given room,
    needs the player stats
    """
    room[player['X']][player['Y']] = PLAYER


def new_player_position(old_player_coordinates: tuple, direction: tuple) -> tuple:
    """puts player 1 block in the direction
    of the players current position"""
    new_player_coordinates = (old_player_coordinates[0] + direction[0], old_player_coordinates[1] + direction[1])
    return new_player_coordinates


def check_target_cell(room: list, player_coordinates: tuple, direction: tuple) -> int:
    """Returns what is in the the target cell
    """
    potential_cell = new_player_position(player_coordinates, direction)
    return room[potential_cell[0]][potential_cell[1]]


def check_creature_is_dead(player: dict) -> None:
    return player['HP'] <= 0



if __name__ == "__main__":
    pass
