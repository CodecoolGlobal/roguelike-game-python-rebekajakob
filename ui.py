def display_board(board: list, color_scheme: dict) -> None:
    for row in board:
        for cell in row:
            print(color_scheme[cell], end=' ')
        print()
    print()


