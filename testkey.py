#!/usr/bin/env python

# this solution will work only in Windows, as msvcrt is a Windows only package

import thread
import time


keybuffer= list()
lock= thread.allocate_lock()
running = True

try:
    from msvcrt import getch  # try to import Windows version

    def keypress():
        global keybuffer, running

        char = getch()

        lock.aquire()
        if ord(char)==0 or ord(char)==224: #Special keys
            keybuffer.push(getch())
        keybuffer.push(char)

        while len(keybuffer) > 100:
            keybuffer.pop(0)

        running=False
        lock.release()



except ImportError:

    def getch():   # define non-Windows version
        import sys, tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch


    def keypress():
        global keybuffer, running

        # get special char combinations on linux up to 5 byte
        a=[]
        a.push(getch())
        if ord(a[0])==27:
            a.push(getch())
            if ord(a[1])==91:
                a.push(getch())
                if (ord(a[2])>=49 and ord(a[2])<=54) or ord(a[2])==91:
                    a.push(getch())
                    if ord(a[3])>=48 and ord(a[3])<=57:
                        a.push(getch())

        lock.aquire()
        # add to keyboard buffer in reverse order to facilitate popping o stack
        while len(a) > 0:
            keybuffer.push(a.pop())

        # limit buffer size by discarting overflow
        while len(keybuffer) > 100:
            keybuffer.pop(0)

        running= False
        lock.release()



def scanForKeys():
    global running

    # wait for key in separate thread
    running= True
    thread.start_new_thread(keypress, ())

    # scan forever
    while True:
        # check if thread has run

        if not running:
            # restart thread
            thread.start_new_thread(keypress, ())

        # wait a short amount of time
        time.sleep(0.1)


def keyPressed():
    lock.aquire()
    value= len(keybuffer) > 0
    lock.release()
    return value


def readKey():
    try:
        lock.aquire()
        value= keybuffer.pop()
        lock.release()

        return value
    except IndexError:
        return None





