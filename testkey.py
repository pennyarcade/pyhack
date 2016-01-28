#!/usr/bin/env python
# this solution will work only in Windows, as msvcrt is a Windows only package

"""
Test script for keyboard capturing

Uses threads to scan for keypresses
"""

import thread
import time

WINDOWS = None

try:
    from msvcrt import getch  # try to import Windows version
    WINDOWS = True

except ImportError:
    WINDOWS = False
    try:
        import sys
        import tty
        import termios
    except ImportError:
        print "Import error"
        quit()


def keypress_win():
    """keypress windows"""
    global keybuffer, running, lock

    char = getch()

    lock.acquire()
    if ord(char) == 0 or ord(char) == 224: #Special keys
        keybuffer.append(getch())
    keybuffer.append(char)

    while len(keybuffer) > 100:
        keybuffer.pop(0)

    running = False
    lock.release()


def keypress_unix():
    """keypress linux"""
    global keybuffer, running

    # get special char combinations on linux up to 5 byte
    character_array = []
    character_array.append(getch())
    if ord(character_array[0]) == 27:
        character_array.append(getch())
        if ord(character_array[1]) == 91:
            character_array.append(getch())
            if (
                ord(character_array[2]) >= 49 and ord(character_array[2]) <= 54
            ) or ord(character_array[2]) == 91:
                character_array.append(getch())
                if ord(character_array[3]) >= 48 and ord(character_array[3]) <= 57:
                    character_array.append(getch())

    lock.acquire()
    # add to keyboard buffer in reverse order to facilitate popping o stack
    while len(character_array) > 0:
        keybuffer.append(character_array.pop())

    # limit buffer size by discarting overflow
    while len(keybuffer) > 100:
        keybuffer.pop(0)

    running = False
    lock.release()


def getch_unix():   # define non-Windows version
    """getch linux"""
    file_descriptor = sys.stdin.fileno()
    old_settings = termios.tcgetattr(file_descriptor)
    try:
        tty.setraw(sys.stdin.fileno())
        character = sys.stdin.read(1)
    finally:
        termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
    return character


def scan_for_keys():
    """repeatedly restart key scanning"""
    global running

    # wait for key in separate thread
    running = True
    thread.start_new_thread(keypress, ())

    # scan forever
    while True:
        # check if thread has run

        if not running:
            # restart thread
            running = True
            thread.start_new_thread(keypress, ())


def key_pressed():
    """has a key been pressed i.e. keybuffer is not empty"""
    global lock, keybuffer

    lock.acquire()
    value = len(keybuffer) > 0
    lock.release()
    return value


def read_key():
    """fetch a key from the keyboard buffer"""
    global lock, keybuffer

    try:
        return = keybuffer.pop()
    except IndexError:
        return None


def main():
    """Main function"""
    global keybuffer, lock, running

    keybuffer = list()
    lock = thread.allocate_lock()
    running = True
    thread.start_new_thread(scan_for_keys, ())

    while True:
        print "\r" + str(keybuffer)
        time.sleep(2)
        if read_key() == '#':
            break


if __name__ == '__main__':
    # setup system appropriate functions
    if WINDOWS:
        keypress = keypress_win
    else:
        getch = getch_unix
        keypress = keypress_unix

    main()

