import ui  # TODO just for testing purposes, delete from final code
import util
import main


def create_room(entry_door, exit_door, level, width=30, height=20):
    board = []
    for row in range(height):
        current_row = []
        for col in range(width):
            if row == 0 or row == height - 1:
                current_row.append(1)
            else:
                if col == 0 or col == width - 1:
                    current_row.append(1)
                else:
                    current_row.append(0)
        board.append(current_row)
    create_doors(board, entry_door, exit_door)
    if level == 1:
        place_inner_wall(board, (10, 0), (10, 10))
        place_inner_wall(board, (5, 15), (13, 15))
        place_inner_wall(board, (15, 5), (19, 5))
        place_inner_wall(board, (15, 15), (19, 15))
        place_inner_wall(board, (7, 19), (7, 25))
        place_inner_wall(board, (8, 19), (8, 25))
        place_inner_wall(board, (9, 19), (9, 25))
        place_inner_wall(board, (10, 19), (10, 25))
        place_inner_wall(board, (11, 19), (11, 25))
    if level == 2:
        place_inner_wall(board, (0, 8), (15, 8))
        place_inner_wall(board, (10, 14), (19, 14))
        place_inner_wall(board, (10, 15), (19, 15))
        place_inner_wall(board, (0, 18), (15, 18))
        place_inner_wall(board, (7, 21), (7, 25))
        place_inner_wall(board, (12, 21), (12, 29))
        place_inner_wall(board, (0, 25), (7, 25))
    if level == 3:
        place_inner_wall(board, (5, 10), (5, 10))
        place_inner_wall(board, (15, 11), (15, 11))
        place_inner_wall(board, (4, 20), (4, 20))
        place_inner_wall(board, (10, 20), (10, 20))
    return board


def create_board():
    board = []
    board.append(create_room(None, (4, 29), 1))
    board.append(create_room((5, 0), (19, 26), 2))
    board.append(create_room((0, 26), None, 3))
    return board


def create_doors(board: list, entry_door: tuple, exit_door: tuple) -> None:
    if entry_door:
        board[entry_door[0]][entry_door[1]] = 2
    if exit_door:
        board[exit_door[0]][exit_door[1]] = 3


def place_inner_wall(board, start_wall, end_wall):
    if start_wall[0] == end_wall[0]:
        for i in range(start_wall[1], end_wall[1]+1):
            board[start_wall[0]][i] = 1
    else:
        for i in range(start_wall[0], end_wall[0]+1):
            board[i][start_wall[1]] = 1


def put_player_on_board(room, player):
    room[player['X']][player['Y']] = 4


def new_player_position(player_coordinates: tuple, direction: tuple) -> tuple:
    player_coordinates = (player_coordinates[0] + direction[0], player_coordinates[1] + direction[1])
    return player_coordinates


def check_target_cell(board, player_coordinates: tuple, direction: tuple) -> bool:
    potential_cell = new_player_position(player_coordinates, direction)
    return board[potential_cell[0]][potential_cell[1]] == ' '






if __name__ == "__main__":
    room1 = create_room(None, (4, 29), 1)
    room2 = create_room((5, 0), (19, 26), 2)
    room3 = create_room((0, 26), None, 3)

    color_scheme = {0: ' ', 1: '▅', 2: 'E', 3: 'X'}
    ui.display_board(room1, color_scheme)
    ui.display_board(room2, color_scheme)
    ui.display_board(room3, color_scheme)

    for i in room1:
        print(" ".join(map(str, i)))
    for i in room2:
        print(" ".join(map(str, i)))
    for i in room3:
        print(" ".join(map(str, i)))

