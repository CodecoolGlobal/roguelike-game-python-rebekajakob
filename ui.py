def display_board(board: list, player: dict, color_scheme: dict) -> None:
    print(f"HP: {player['HP']}   COINS: {player['COINS']}")
    for row in board:
        for cell in row:
            print(color_scheme[cell], end=' ')
        print()
    print()
