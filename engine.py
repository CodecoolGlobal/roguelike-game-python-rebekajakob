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
STRONG_MONSTER = 14
STRONG_MONSTERS = []


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
        place_object(room, (4, 3), TACO)
        place_object(room, (9, 22), TACO)
        place_object(room, (5, 5), BASIC_WEAPON)
        monster_positions = [(5, 7), (4, 27), (17, 25)]
        MONSTERS.append([place_monster(room, monster_position, MONSTER) for monster_position in monster_positions])
        strong_monster_positions = []
        STRONG_MONSTERS.append([place_monster(room, strong_monster_position, STRONG_MONSTER) for strong_monster_position in strong_monster_positions])

    if level == 1:
        place_inner_wall(room, (0, 8), (15, 8))
        place_inner_wall(room, (10, 14), (19, 14))
        place_inner_wall(room, (10, 15), (19, 15))
        place_inner_wall(room, (0, 18), (15, 18))
        place_inner_wall(room, (7, 21), (7, 25))
        place_inner_wall(room, (12, 21), (12, 29))
        place_inner_wall(room, (0, 25), (7, 25))
        place_object(room, (2, 27), TACO)
        place_object(room, (3, 19), TACO)
        place_object(room, (1, 17), TACO)
        place_object(room, (16, 25), NPC)
        monster_positions = [(3, 8), (8, 5), (15, 13), (18, 9), (3, 27)]
        MONSTERS.append([place_monster(room, monster_position, MONSTER) for monster_position in monster_positions])
        strong_monster_positions = [(3, 22), (10, 22)]
        STRONG_MONSTERS.append([place_monster(room, strong_monster_position, STRONG_MONSTER) for strong_monster_position in strong_monster_positions])

    if level == 2:
        place_inner_wall(room, (5, 10), (5, 10))
        place_inner_wall(room, (15, 11), (15, 11))
        place_inner_wall(room, (4, 20), (4, 20))
        place_inner_wall(room, (10, 20), (10, 20))
        place_object(room, (3, 20), TACO)
        place_object(room, (12, 28), TACO)
        place_object(room, (18, 3), TACO)
        place_object(room, (2, 2), TACO)
        monster_positions = []
        MONSTERS.append([place_monster(room, monster_position, MONSTER) for monster_position in monster_positions])
        strong_monster_positions = []
        STRONG_MONSTERS.append([place_monster(room, strong_monster_position, STRONG_MONSTER) for strong_monster_position in strong_monster_positions])
        boss_positions = []
        for x in range(10, 15):
            for y in range(10, 15):
                boss_positions.append((x, y))
        BOSSES.append([place_boss(room, boss_position) for boss_position in boss_positions])

    return room


def spawn_monsters(room: list) -> None:
    monster_positions = [(3, 8), (8, 5), (15, 13), (18, 9), (3, 27)]
    MONSTERS[1] = ([place_monster(room, monster_position, MONSTER) for monster_position in monster_positions])
    strong_monster_positions = [(3, 22), (10, 22)]
    STRONG_MONSTERS[1] = ([place_monster(room, strong_monster_position, STRONG_MONSTER) for strong_monster_position in strong_monster_positions])


def create_monster() -> dict:
    """Sets the monster's attributes
    'HP'= hitpoint
    """
    monster = {'X': 0, 'Y': 0, 'HP': 10}
    return monster


def create_strong_monster() -> dict:
    """Sets the monster's attributes
    'HP'= hitpoint
    """
    monster = {'X': 0, 'Y': 0, 'HP': 25}
    return monster


def place_monster(room: list, coordinate: tuple, monster_type) -> dict:
    if monster_type == MONSTER:
        monster = create_monster()
    elif monster_type == STRONG_MONSTER:
        monster = create_strong_monster()
    room[coordinate[0]][coordinate[1]] = monster_type
    monster['X'] = coordinate[0]
    monster['Y'] = coordinate[1]
    return monster


def create_boss() -> dict:
    """Sets the bosses attributes
    'HP'= hitpoint
    """
    boss = {'X': 0, 'Y': 0, 'HP': 20}
    return boss


def place_boss(room: list, coordinate: tuple) -> dict:
    boss = create_boss()
    room[coordinate[0]][coordinate[1]] = BOSS
    boss['X'] = coordinate[0]
    boss['Y'] = coordinate[1]
    return boss


def place_object(room: int, coordinate: tuple, item: int) -> None:
    room[coordinate[0]][coordinate[1]] = item


def create_board(width: int, heigth: int) -> list:
    """Puts the rooms together into one board list
    (rooms need to be added manually)
    """
    entry_exit_door_positions = [(None, (4, 29)), ((4, 0), (19, 26)), ((0, 26), None)]
    return [create_room(doors[0], doors[1], i, width, heigth) for i, doors in enumerate(entry_exit_door_positions)]


def new_creature_position(creature_coordinates: tuple, new_directions: tuple) -> tuple:
    new_position = creature_coordinates[0] + new_directions[0], creature_coordinates[1] + new_directions[1]
    return new_position


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


def move_player_there(player: dict, current_room: list, player_coordinates: tuple, direction: tuple) -> tuple:
    current_room[player_coordinates[0]][player_coordinates[1]] = EMPTY_CELL
    player_coordinates = new_creature_position(player_coordinates, direction)
    player['X'], player['Y'] = player_coordinates[0], player_coordinates[1]
    current_room[player_coordinates[0]][player_coordinates[1]] = PLAYER
    return player_coordinates


def check_target_cell(room: list, player_coordinates: tuple, direction: tuple) -> int:
    """Returns what is in the the target cell
    """
    potential_cell = new_creature_position(player_coordinates, direction)
    return room[potential_cell[0]][potential_cell[1]]


def check_creature_is_dead(player: dict) -> bool:
    return player['HP'] <= 0


def random_damage_multiplier(lower_bound: float = 0.7, upper_bound: float = 1.3) -> float:
    return random.uniform(lower_bound, upper_bound)


if __name__ == "__main__":
    pass
