def display_board(board: list, player: dict, color_scheme: dict) -> None:
    print(f"NAME: {player['NAME']}   HP: {player['HP']}   COINS: {player['COINS']}   INVENTORY: {', '.join(player['INVENTORY'])}  ATTACK: {player['ATTACK']}")
    for row in board:
        for cell in row:
            print(color_scheme[cell], end=' ')
        print()
    print()

def menu():
    print('''Hello adventurer''')
    answer = input('Are you ready for the game of your life? (y/n) ')
    if answer == "n":
        print("Bye")
        exit()
    print('''
    1. New Game
    2. Highscore
    3. Credits
    4. Quit
    ''')
    menu_option = None
    while menu_option not in ["1","2","3","4"]:
        menu_option = input("Please choose a number from above: ")
    return int(menu_option)

def credits():
    print('''Our lovely creators are:
    Balazs Mucsanyi
    Botond Bata
    Daniel Dudas
    Gabor Gabor
    Gabor Nagy
    Gergely Sarkadi
    Rebeka Jakob
    ''')

def newgame_settings():
    name = input("Please give me your name: ")
    valid_avatars = ["🤠","👳","👸","🧝","👮"]
    print('''Available avatars:
    1. 🤠
    2. 👳
    3. 👸
    4. 🧝
    5. 👮
    ''')
    avatar_number = None
    while avatar_number not in ["1","2","3","4","5"]:
        avatar_number = input("Please choose a number from above: ")
    return name, valid_avatars[int(avatar_number)-1]
