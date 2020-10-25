from pynput import keyboard
from datetime import datetime
import os

START_TIME = datetime.now()

times = []

def press_callback(key):
    pass

def release_callback(key):
    if key == keyboard.Key.down:
        event()
    elif key == keyboard.Key.esc:
        on_exit()
        keyboard.Listener.stop(l)

def event():
    press = datetime.now()
    print("\nEnter annotation: ", end="")
    x = input()[3:]
    print("\nBookmarked! Your annotation:", x)
    print(press - START_TIME)
    times.append((press - START_TIME, x))

def on_exit():
    with open('bookmarks.txt', 'w') as f:
        f.write("Bookmarks given as time delta from: " + str(START_TIME)+ "\n\n")
        f.write("TIME_DELTA, ANNOTATION\n")
        for time in times:
            f.write(str(time[0]) + ", " + str(time[1])+"\n")
    f.close()

l = keyboard.Listener(on_press=press_callback, on_release=release_callback)
l.start()
l.join()
