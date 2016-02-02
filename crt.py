"""
Emulate Pascal's Unit Crt as object

Lots of work yet to do
"""

import sys
import time
import thread
import lib.colorama
import lib.colorama.ansi

WINDOWS = None

try:
    from msvcrt import getch  # try to import Windows version
    WINDOWS = True

except ImportError:
    WINDOWS = False
    try:
        import tty
        import termios
    except ImportError:
        print "Import error"
        quit()


KEYBUFFER = None
LOCK = None
RUNNING = None


def __getch_unix():
    """
    getch linux

    define non-Windows version

    """
    old_settings = termios.tcgetattr(sys.stdin.fileno())
    try:
        tty.setraw(sys.stdin.fileno())
        character = sys.stdin.read(1)
    finally:
        termios.tcsetattr(
            sys.stdin.fileno(), termios.TCSADRAIN, old_settings
        )
    return character


def keypress_win():
    """keypress windows"""
    global KEYBUFFER, RUNNING, LOCK

    char = getch()

    LOCK.acquire()
    if ord(char) == 0 or ord(char) == 224: #Special keys
        KEYBUFFER.append(getch())
    KEYBUFFER.append(char)

    while len(KEYBUFFER) > 100:
        KEYBUFFER.pop(0)

    RUNNING = False
    LOCK.release()


def keypress_unix():
    """keypress linux"""
    global KEYBUFFER, RUNNING

    # get special char combinations on linux up to 5 byte
    character_array = []
    character_array.append(__getch_unix())
    if ord(character_array[0]) == 27:
        character_array.append(__getch_unix())
        if ord(character_array[1]) == 91:
            character_array.append(__getch_unix())
            if (
                    ord(character_array[2]) >= 49 and
                    ord(character_array[2]) <= 54
            ) or ord(character_array[2]) == 91:
                character_array.append(__getch_unix())
                if (
                        ord(character_array[3]) >= 48 and
                        ord(character_array[3]) <= 57
                    ):
                    character_array.append(__getch_unix())

    LOCK.acquire()
    # add to keyboard buffer in reverse order to facilitate popping o stack
    while len(character_array) > 0:
        KEYBUFFER.append(character_array.pop())

    # limit buffer size by discarting overflow
    while len(KEYBUFFER) > 100:
        KEYBUFFER.pop(0)

    RUNNING = False
    LOCK.release()


def key_pressed__():
    """has a key been pressed i.e. KEYBUFFER is not empty"""
    global LOCK, KEYBUFFER

    LOCK.acquire()
    value = len(KEYBUFFER) > 0
    LOCK.release()
    return value


def read_key__():
    """fetch a key from the keyboard buffer"""
    global LOCK, KEYBUFFER

    try:
        return KEYBUFFER.pop()
    except IndexError:
        return None



class Crt(object):
    """
    wrap all console interaction TurboPascal Style

    Constants:
        Black           Black color attribute
        Blink           Blink attribute
        Blue            Blue color attribute
        Brown           Brown color attribute
        BW40            40 columns black and white screen mode.
        BW80            80 columns black and white screen mode.
        C40             40 columns color screen mode.
        C80             80 columns color screen mode.
        CO40            40 columns color screen mode.
        CO80            80 columns color screen mode.
        Cyan            Cyan color attribute
        DarkGray        Dark gray color attribute
        Font8x8         Internal ROM font mode
        Green           Green color attribute
        LightBlue       Light Blue color attribute
        LightCyan       Light cyan color attribute
        LightGray       Light gray color attribute
        LightGreen      Light green color attribute
        LightMagenta    Light magenta color attribute
        LightRed        Light red color attribute
        Magenta         Magenta color attribute
        Mono            Monochrome screen mode (hercules screens)
        Red             Red color attribute
        ScreenHeight    Current screen height.
        ScreenWidth     Current screen width
        White           White color attribute
        Yellow          Yellow color attribute

    Types:
        tcrtcoord       Type to denote CRT coordinate

    Functions:
        AssignCrt       Assign file to CRT. (unsupported)
        ClrEol          Clear from cursor position till end of line.
        ClrScr          Clear current window.
        cursorbig       Show big cursor
        cursoroff       Hide cursor
        cursoron        Display cursor
        Delay           Delay program execution.
        DelLine         Delete line at cursor position.
        GotoXY          Set cursor position on screen.
        HighVideo       Switch to highlighted text mode
        InsLine         Insert an empty line at cursor position
        KeyPressed      Check if there is a keypress in the keybuffer
        LowVideo        Switch to low intensity colors.
        NormVideo       Return to normal (startup) modus
        NoSound         Stop system speaker
        ReadKey         Read key from keybuffer
        Sound           Sound system speaker
        TextBackground  Set text background
        TextColor       Set text color
        TextMode        Set screen mode.
        WhereX          Return X (horizontal) cursor position
        WhereY          Return Y (vertical) cursor position
        Window          Create new window on screen.

    Variables:
        CheckBreak      Check for CTRL-Break keystroke. Not used.
        CheckEOF        Check for EOF on standard input. Not used.
        CheckSnow       Check snow on CGA screens. Not used.
        DirectVideo     Use direct video access. DOS only
        LastMode        Last screen mode.
        TextAttr        Mask to filter text attribute
        WindMax         Lower right corner of currently defined window
        WindMaxX        X coordinate of lower right corner of the defined window
        WindMaxY        Y coordinate of lower right corner of the defined window
        WindMin         Upper left corner of currently defined window
        WindMinX        X coordinate of upper left corner of the defined window
        WindMinY        Y coordinate of upper left corner of the defined window
    """

    def __init__(self):
        """
        initialize class

        @todo has to many class attributes?
        """
        super(Crt, self).__init__()

        global KEYBUFFER, LOCK, RUNNING

        KEYBUFFER = list()
        LOCK = thread.allocate_lock()
        RUNNING = True

        # setup system appropriate functions
        if WINDOWS:
            self.keypress = keypress_win
        else:
            self.keypress = keypress_unix

        thread.start_new_thread(self.__scan_for_keys, ())

        self.write = sys.stdout.write
        """wrap stdout for writing"""

        self.delay = time.sleep
        """
        Delay execution for n seconds

        just wrap builtin method
        """

        self.key_pressed = key_pressed__
        self.read_key = read_key__

        # color constants
        self.black = 0
        self.red = 1
        self.green = 2
        self.yellow = 3
        self.blue = 4
        self.magenta = 5
        self.cyan = 6
        self.white = 7
        self.reset = 9

        # These are fairly well supported, but not part of the standard.
        self.lblack = 60
        self.lred = 61
        self.lgreen = 62
        self.lyellow = 63
        self.lblue = 64
        self.lmagenta = 65
        self.lcyan = 66
        self.lwhite = 67


    def __scan_for_keys(self):
        """repeatedly restart key scanning"""
        global RUNNING

        # wait for key in separate thread
        RUNNING = True
        thread.start_new_thread(self.keypress, ())

        # scan forever
        while True:
            # check if thread has run

            if not RUNNING:
                # restart thread
                RUNNING = True
                thread.start_new_thread(self.keypress, ())



    def write_ln(self, text):
        """write to stdout with newline"""
        self.write(str(text) + "\r\n")


    def clr_eol(self, mode=2):
        """Clear from cursor position till end of line."""
        self.write(lib.colorama.ansi.clear_line(mode))


    def clr_scr(self, mode=2):
        """Clear current window."""
        self.write(lib.colorama.ansi.clear_screen(mode))


    def cursor_big(self):
        """TBD"""
        pass


    def cursor_off(self):
        """TBD"""
        pass


    def cursor_on(self):
        """TBD"""
        pass


    def del_line(self):
        """
        DelLine removes the current line.

        Lines following the current line are scrolled 1 line up,
        and an empty line is inserted at the bottom of the current window.
        The cursor doesn't move.

        TBD
        """
        pass


    def ins_line(self):
        """
        InsLine inserts an empty line at the current cursor position.

        Lines following the current line are scrolled 1 line down,
        causing the last line to disappear from the window.
        The cursor doesn't move.

        TBD
        """
        pass


    def goto_xy(self, x_coordinate, y_coordinate):
        """
        GotoXY positions the cursor at (X,Y),

        X in horizontal, Y in vertical direction relative to the
        origin of the current window. The origin is located at (1,1),
        the upper-left corner of the window.

        TODO: Cache coordinates
        """
        self.write(lib.colorama.Cursor.POS(x_coordinate, y_coordinate))


    def high_video(self):
        """
        HighVideo switches the output to highlighted text.

        (It sets the high intensity bit of the video attribute)
        """
        self.write(lib.colorama.Style.BRIGHT)


    def norm_video(self):
        """
        NormVideo switches the output to the defaults, read at startup.

        (The defaults are read from the cursor position at startup)
        """
        self.write(lib.colorama.Style.NORMAL)


    def low_video(self):
        """
        LowVideo switches the output to non-highlighted text.

        (It clears the high intensity bit of the video attribute)
        """
        self.write(lib.colorama.Style.DIM)


    def sound(self):
        """
        Sound sounds the speaker at a frequency of hz. Under Windows,

        a system sound is played and the frequency parameter is ignored.
        On other operating systems, this routine may not be implemented.
        TBD
        """
        pass


    def no_sound(self):
        """
        NoSound stops the speaker sound.

        This call is not supported on all operating systems.
        TBD
        """
        pass

    def text_background(self, color):
        """
        TextBackground sets the background color to CL.

        CL can be one of the predefined color constants.
        """
        self.write(lib.colorama.ansi.code_to_chars(color + 40))


    def text_color(self, color):
        """
        TextColor sets the foreground color to CL.

        CL can be one of the predefined color constants.
        """
        self.write(lib.colorama.ansi.code_to_chars(color + 30))


    def text_mode(self, mode):
        """
        TextMode sets the textmode of the screen

        (i.e. the number of lines and columns of the screen).
        The lower byte is use to set the VGA text mode.
        TBD
        """
        pass


    def where_x(self):
        """
        WhereX returns the current X-coordinate of the cursor,

        relative to the current window. The origin is (1,1),
        in the upper-left corner of the window.
        TBD
        """
        pass


    def where_y(self):
        """
        WhereY returns the current X-coordinate of the cursor,

        relative to the current window. The origin is (1,1),
        in the upper-left corner of the window.
        TBD
        """
        pass


    def window(self):
        """
        Window creates a window on the screen, to which output will be sent.

        (X1,Y1) are the coordinates of the upper left corner of the window,
        (X2,Y2) are the coordinates of the bottom right corner of the
        window. These coordinates are relative to the entire screen, with
        the top left corner equal to (1,1). Further coordinate operations,
        except for the next Window call, are relative to the window's
        top left corner.
        """
        pass



# this should not be run from cli
if __name__ == "__main__":
    SCREEN = Crt()

    while True:
        print "\r" + str(KEYBUFFER)
        time.sleep(2)
        if SCREEN.read_key() == '#':
            break
