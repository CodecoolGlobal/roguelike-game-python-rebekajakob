#coloring
import colorama

a = colorama.Fore.CYAN + "Q"
print({a})

#get keypress
import util
key = ""
while key != 'q':
    key = util.key_pressed()
    print({key})