import util
def display_board(board: list, player: dict, color_scheme: dict, current_room_index) -> None:
    util.clear_screen()
    print(current_room_index)
    print(f"HP: {player['HP']}   COINS: {player['COINS']}   INVENTORY: {', '.join(player['INVENTORY'])}  ATTACK: {player['ATTACK']}")
    for row in board:
        for cell in row:
            print(color_scheme[cell], end=' ')
        print()
    print()
