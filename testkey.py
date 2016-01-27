#!/usr/bin/env python
# this solution will work only in Windows, as msvcrt is a Windows only package

"""
Test script for keyboard capturing

Uses threads to scan for keypresses
"""

import thread
import time

keybuffer = list()
lock = thread.allocate_lock()
running = True


try:
    from msvcrt import getch  # try to import Windows version

    def keypress():
        """keypress windows"""
        global keybuffer, running

        char = getch()

        lock.aquire()
        if ord(char) == 0 or ord(char) == 224: #Special keys
            keybuffer.push(getch())
        keybuffer.push(char)

        while len(keybuffer) > 100:
            keybuffer.pop(0)

        running = False
        lock.release()

except ImportError:
    def getch():   # define non-Windows version
        """getch linux"""
        import sys
        import tty
        import termios
        file_descriptor = sys.stdin.fileno()
        old_settings = termios.tcgetattr(file_descriptor)
        try:
            tty.setraw(sys.stdin.fileno())
            character = sys.stdin.read(1)
        finally:
            termios.tcsetattr(file_descriptor, termios.TCSADRAIN, old_settings)
        return character


    def keypress():
        """keypress linux"""
        global keybuffer, running

        # get special char combinations on linux up to 5 byte
        character_array = []
        character_array.push(getch())
        if ord(character_array[0]) == 27:
            character_array.push(getch())
            if ord(character_array[1]) == 91:
                character_array.push(getch())
                if (
                    ord(character_array[2]) >= 49 and ord(character_array[2]) <= 54
                ) or ord(character_array[2]) == 91:
                    character_array.push(getch())
                    if ord(character_array[3]) >= 48 and ord(character_array[3]) <= 57:
                        character_array.push(getch())

        lock.aquire()
        # add to keyboard buffer in reverse order to facilitate popping o stack
        while len(character_array) > 0:
            keybuffer.push(character_array.pop())

        # limit buffer size by discarting overflow
        while len(keybuffer) > 100:
            keybuffer.pop(0)

        running = False
        lock.release()



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
            thread.start_new_thread(keypress, ())

        # wait a short amount of time
        time.sleep(0.1)


def key_pressed():
    """has a key been pressed i.e. keybuffer is not empty"""
    lock.aquire()
    value = len(keybuffer) > 0
    lock.release()
    return value


def read_key():
    """fetch a key from the keyboard buffer"""
    try:
        lock.aquire()
        value = keybuffer.pop()
        lock.release()

        return value
    except IndexError:
        return None





