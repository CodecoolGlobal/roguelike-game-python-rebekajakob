def create_room(entry_door, exit_door, width=30, height=20):
    board = []
    for i in range(height):
        row = []
        for col in range(width):
            if i == 0 or i == height - 1:
                row.append(1)
            else:
                if col == 0 or col == width - 1:
                    row.append(1)
                else:
                    row.append(0)
        board.append(row)
    create_doors(board, entry_door, exit_door)
    return board


    # create doors
def create_doors(board: list, entry_door: tuple, exit_door: tuple):
    if entry_door:
        board[entry_door[0]][entry_door[1]] = 2
    if exit_door:
        board[exit_door[0]][exit_door[1]] = 3
    




def put_player_on_board(board, player):
    '''
    Modifies the game board by placing the player icon at its coordinates.

    Args:
    list: The game board
    dictionary: The player information containing the icon and coordinates

    Returns:
    Nothing
    '''
    pass


if __name__ == "__main__":
    level_1_board = create_room(None, (0, 10))
    for i in level_1_board:
        print(" ".join(map(str, i)))
    level_2_board = create_room((19, 10), None)
    for i in level_2_board:
        print(" ".join(map(str, i)))
    