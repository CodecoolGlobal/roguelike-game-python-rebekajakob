# coloring
import colorama
import util

a = colorama.Fore.CYAN + "Q" + colorama.Style.RESET_ALL
print({a})


def get_keypress():
    key = ""
    while key != 'q':
        key = util.key_pressed()
        print(key)
        print({key})
# get_keypress()


# board size
def print_board(width=30, height=20):
    board = []
    for i in range(height):
        row = []
        for i in range(width):
            row.append("X")
        board.append(row)
    for row in board:
        print(' '.join(row))


print_board()

# teli karakter: █

"""board number legacy:
0 = space, where you walk
1 = border color
2 = entry door
3 = exit door
4 = player
5 = coin
"""



import time
import keyboard
def keypresses():
    while True:  # making a loop
        try:  # used try so that if user pressed other than the given key error will not be shown
            if keyboard.read_key() == "w":  # if key 'q' is pressed 
                keylog.append("w")
                return "w"
            if keyboard.is_pressed('a'):  # if key 'a' is pressed 
                return "a"
            if keyboard.is_pressed('s'):  # if key 's' is pressed 
                keylog.append("s")
                return "s"
            if keyboard.is_pressed('d'):  # if key 'd' is pressed 
                return "d"
        except:
            break  # if user pressed a key other than the given key the loop will break



import threading
def keylogger(keylog, time_counter):
    while True:
        key = None
        key = getch.getch()
        if key != None:
            keylog.append(key)
        time.sleep(0.05)
        time_counter += 0.05


def main_thread(keylog, time_counter):
    while True:
        if time_counter % 1 == 0:
            print("Move the enemies")
        

    
import getch
if __name__ == "__main__":
    keylog = []
    time_counter = 0
    t1 = threading.Thread(target=keylogger, args=(keylog, time_counter))
    t2 = threading.Thread(target=main_thread, args=(keylog,time_counter))

    t1.start()
    t2.start()





    