def create_room(entry_door, exit_door,level, width=30, height=20):
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
    if level == 1:
        place_wall(board, (10,0), (10,10))
        place_wall(board, (5,15), (13,15))
        place_wall(board, (15,5), (19,5))
        place_wall(board, (15,15), (19,15))
        place_wall(board, (7,19), (7,25))
        place_wall(board, (8,19), (8,25))
        place_wall(board, (9,19), (9,25))
        place_wall(board, (10,19), (10,25))
        place_wall(board, (11,19), (11,25))
    if level == 2:
        place_wall(board, (0,8), (15,8))
        place_wall(board, (10,14), (19,14))
        place_wall(board, (10,15), (19,15))
        place_wall(board, (0,18), (15,18))
        place_wall(board, (7,21), (7,25))
        place_wall(board, (12,21), (12,29))
        place_wall(board, (0,25), (7,25))
    if level == 3:
        place_wall(board, (5, 10), (5, 10))
        place_wall(board, (15, 11), (15, 11))
        place_wall(board, (4, 20), (4, 20))
        place_wall(board, (10, 20), (10, 20))
        
    return board


    # create doors
def create_doors(board: list, entry_door: tuple, exit_door: tuple):
    if entry_door:
        board[entry_door[0]][entry_door[1]] = 2
    if exit_door:
        board[exit_door[0]][exit_door[1]] = 3

def place_wall(board, start_wall, end_wall):
    if start_wall[0] == end_wall[0]:
        for i in range(start_wall[1],end_wall[1]+1):
            board[start_wall[0]][i] = 1
    else:
        for i in range(start_wall[0],end_wall[0]+1):
            board[i][start_wall[1]] = 1
        
    




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
    room1 = create_room(None, (4, 29),1)
    for i in room1:
        print(" ".join(map(str, i)))
    room2 = create_room((5, 0),(19, 26),2)
    for i in room2:
        print(" ".join(map(str, i)))
    room3 = create_room((0,26),None,3)
    for i in room3:
        print(" ".join(map(str, i)))
    