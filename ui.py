import time
import util


def display_board(board: list, player: dict, color_scheme: dict) -> None:
    util.clear_screen()
    print(f"NAME: {player['NAME']}   HP: {player['HP']} %   COINS: {player['COINS']}   ATTACK: {player['ATTACK']}")
    for row in board:
        for cell in row:
            print(color_scheme[cell], end=' ')
        print()
    print()


def menu() -> int:
    print('''
    1. New Game
    2. Highscore
    3. Credits
    4. Quit
    ''')
    menu_option = None
    while menu_option not in ["1", "2", "3", "4"]:
        menu_option = input("Please choose a number from above: ")
    return int(menu_option)


def greet() -> None:
    print('''Hello adventurer''')
    answer = input('Are you ready for the game of your life? (y/n) ')
    if answer == "n":
        print("Bye")
        exit()


def credits() -> None:
    print('''Our lovely creators are:
    Balazs Mucsanyi
    Botond Bata
    Daniel Dudas
    Gabor Gabor
    Gabor Nagy
    Gergely Sarkadi
    Rebeka Jakob
    ''')


def newgame_settings() -> tuple:
    name = input("Please give me your name: ")
    valid_avatars = ["🤠", "👳", "👸", "🧝", "👮"]
    print('''Available avatars:
    1. 🤠
    2. 👳
    3. 👸
    4. 🧝
    5. 👮
    ''')
    avatar_number = None
    while avatar_number not in ["1", "2", "3", "4", "5"]:
        avatar_number = input("Please choose a number from above: ")
    return name, valid_avatars[int(avatar_number)-1]


def highscore() -> None:
    with open("log.txt", "r") as text:
        scores = text.read().splitlines()
        high_scores = []
        for item in scores:
            score = int(item.split()[1]) + int(item.split()[2])
            name = item.split()[0]
            high_scores.append((score, name))
        high_scores.sort(reverse=True)
        for item in high_scores[:5]:
            print(item[1] + "  " + str(item[0]))


def roll_the_credits(speed: float = 0.2) -> None:
    credits = '''Our lovely creators are:

    Balazs Mucsanyi
    Botond Bata
    Daniel Dudas
    Gabor Gabor
    Gabor Nagy
    Gergely Sarkadi
    Rebeka Jakob
    '''
    print('\n' * 3)
    time.sleep(speed)
    for name in credits.split('\n'):
        print(name)
        time.sleep(speed)
    for _ in range(30):
        print()
        time.sleep(speed)
