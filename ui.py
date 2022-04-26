color_scheme = {0: '  ', 1: '🌵', 2: '🚪', 3: '🚪', 4: '🤠', 5: '🌮', 6: '👾', 7: '💀'}



def display_board(board: list, player) -> None:
    print(f"HP: {player['HP']}   COINS: {player['COINS']}")
    for row in board:
        for cell in row:
            print(color_scheme[cell], end=' ')
        print()
    print()


