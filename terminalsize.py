#!/usr/bin/env python
"""
get terminal size, platform independent

originally retrieved from:
https://gist.github.com/jtriley/1108174
"""

import os
import shlex
import struct
import platform
import subprocess


def get_terminal_size():
    """
    getTerminalSize()

    - get width and height of console
    - works on linux,os x,windows,cygwin(windows)
    originally retrieved from:
    http://stackoverflow.com/questions/566746/how-to-get-console-window-width-in-python
    """
    current_os = platform.system()
    tuple_xy = None
    if current_os == 'Windows':
        tuple_xy = _get_terminal_size_windows()
        if tuple_xy is None:
            tuple_xy = _get_terminal_size_tput()
            # needed for window's python in cygwin's xterm!
    if current_os in ['Linux', 'Darwin'] or current_os.startswith('CYGWIN'):
        tuple_xy = _get_terminal_size_linux()
    if tuple_xy is None:
        print "default"
        tuple_xy = (80, 25)      # default value
    return tuple_xy


def _get_terminal_size_windows():
    try:
        from ctypes import windll, create_string_buffer
        # stdin handle is -10
        # stdout handle is -11
        # stderr handle is -12
        handle = windll.kernel32.GetStdHandle(-12)
        csbi = create_string_buffer(22)
        if windll.kernel32.GetConsoleScreenBufferInfo(handle, csbi):
            # (bufx, bufy, curx, cury, wattr, left, top, right, bottom, maxx, maxy)
            result = struct.unpack("hhhhHhhhhhh", csbi.raw)
            return result[7] - result[5] + 1, result[8] - result[6] + 1
    except BaseException:
        pass


def _get_terminal_size_tput():
    # get terminal width
    # src: http://stackoverflow.com/questions/263890/
    #    how-do-i-find-the-width-height-of-a-terminal-window
    try:
        cols = int(subprocess.check_call(shlex.split('tput cols')))
        rows = int(subprocess.check_call(shlex.split('tput lines')))
        return (cols, rows)
    except BaseException:
        pass


def _get_terminal_size_linux():
    """Unix version"""
    def ioctl_gwinsz(descriptor):
        """ioctl interaction"""
        try:
            import fcntl
            import termios
            result = struct.unpack('hh',
                                   fcntl.ioctl(descriptor,
                                               termios.TIOCGWINSZ,
                                               '1234'))
            return result
        except BaseException:
            pass

    result = ioctl_gwinsz(0) or ioctl_gwinsz(1) or ioctl_gwinsz(2)
    if not result:
        try:
            descriptor = os.open(os.ctermid(), os.O_RDONLY)
            result = ioctl_gwinsz(descriptor)
            os.close(descriptor)
        except BaseException:
            pass
    if not result:
        try:
            result = (os.environ['LINES'], os.environ['COLUMNS'])
        except BaseException:
            return None
    return int(result[1]), int(result[0])


def main():
    """main function"""
    sizex, sizey = get_terminal_size()
    print  'width =', sizex, 'height =', sizey


if __name__ == "__main__":
    main()