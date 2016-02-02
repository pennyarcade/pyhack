"""
Pyhack

Python roguelike game using (almost) only standard library calls
Console only for now
Attempts to be cross platform
"""

import os
import platform
from crt import Crt


class PyHack(object):
    """main game class"""
    def __init__(self):
        super(PyHack, self).__init__()

        self.screen = Crt()
        self.screen.clr_scr()

                # 0   1    2    3    4    5    6    7
                # 8   9   10   11   12   13   14   15
        self.room = {
            1:[
                '#', '#', '#', '#', '#', '#', '#', '#',   # ^
                '#', '#', '#', '#', '#', '#', '#', '#'
            ],
            2:[
                '#', '.', '.', '.', '.', '.', '.', '.',   # |
                '.', '.', '.', '.', '.', '.', '.', '#'
            ],
            3:[
                '#', '.', '.', '.', '.', '.', '.', '.',   # |
                '.', '#', '#', '#', '#', '.', '.', '#'
            ],
            4:[
                '#', '.', '.', '.', '.', '.', '.', '#',   # |
                '.', '#', '.', '.', '.', '.', '.', '#'
            ],
            5:[
                '#', '.', '.', '.', '.', '.', '@', '#',   # |
                '.', '#', '.', '.', '#', '.', '.', '#'
            ],
            6:[
                '#', '.', '.', '.', '.', '.', '.', '#',   # x
                '.', '.', '.', '.', '#', '.', '.', '#'
            ],
            7:[
                '#', '.', '.', '.', '.', '#', '#', '#',   # |
                '.', '#', '#', '.', '#', '.', '.', '#'
            ],
            8:[
                '#', '.', '.', '.', '.', '.', '.', '.',   # |
                '.', '.', '#', '#', '#', '.', '.', '#'
            ],
            9:[
                '#', '.', '.', '.', '.', '.', '.', '.',   # |
                '.', '.', '.', '.', '.', '.', '.', '#'
            ],
            10:[
                '#', '#', '#', '#', '#', '#', '#', '#',   # |
                '#', '#', '#', '#', '#', '#', '#', '#'
            ]
        }
        # <---------------------y---------------------------->

        self.stuff = {
            'wall' : "#",
            'player' : "@",
            'empty' : ".",
            'money' : "$",
            'chest' : "C"
        }
        # self.potion = ['hp','xp','dmg']
        # self.weapon = ['sword','nuclear bomb','TNT']

        self.pos = [] # 0 is X,1 is Y

        self.updater()


    def updater(self):
        """update game screen"""
        # @todo: use Crt class to clear screen
        if platform.system() == 'Windows':
            os.system('cls')
        elif platform.system() == 'Linux':
            os.system('clear') #For linux.. I don't know what to do about mac :/
        self.gamemap()
        self.player_pos()


    def gamemap(self):
        """draw game mask"""
        for i in range(1, len(self.room) + 1):
            self.screen.write_ln("".join(self.room[i]))


    def player_pos(self):
        """get player position"""
        for i in range(1, len(self.room) + 1):
            if self.stuff['player'] in self.room[i]:
                x_axis = i
                y_axis = self.room[i].index(self.stuff['player'])
                del self.pos[:]
                self.pos.append(x_axis)
                self.pos.append(y_axis)


    def game_loop(self):
        """main game loop"""
        while True:
            pressedkey = self.screen.read_key()

            if pressedkey == 'w' or pressedkey == 'W':
                self.do_up()
            elif pressedkey == 's' or pressedkey == 'S':
                self.do_down()
            elif pressedkey == 'a' or pressedkey == 'A':
                self.do_left()
            elif pressedkey == 'd' or pressedkey == 'D':
                self.do_right()
            elif pressedkey == '#':
                quit()


    def do_up(self):
        """process up movement"""
        if self.room[self.pos[0]-1][self.pos[1]] != self.stuff['wall']:
            self.move_up(self.stuff['empty'], self.stuff['player'])
            self.updater()
            self.screen.write_ln(self.pos)
        else:
            self.screen.write_ln("Bump! Wall : up")


    def do_down(self):
        """process down movement"""
        if self.room[self.pos[0]+1][self.pos[1]] != self.stuff['wall']:
            self.move_down(self.stuff['empty'], self.stuff['player'])
            self.updater()
            self.screen.write_ln(self.pos)
        else:
            self.screen.write_ln("Bump! wall : down")


    def do_right(self):
        """process right movement"""
        if self.room[self.pos[0]][self.pos[1]+1] != self.stuff['wall']:
            self.move_right(self.stuff['empty'], self.stuff['player'])
            self.updater()
            self.screen.write_ln(self.pos)
        else:
            self.screen.write_ln("Bump! wall : right")


    def do_left(self):
        """process right movement"""
        if self.room[self.pos[0]][self.pos[1]-1] != self.stuff['wall']:
            self.move_left(self.stuff['empty'], self.stuff['player'])
            self.updater()
            self.screen.write_ln(self.pos)
        else:
            self.screen.write_ln("Bump! wall : left")


    def move_up(self, inst_replace, inst_player):
        """move player up"""
        (self.room[self.pos[0]]).pop(self.pos[1])
        (self.room[self.pos[0]]).insert(self.pos[1], inst_replace)
        (self.room[self.pos[0] - 1]).pop(self.pos[1])
        (self.room[self.pos[0] - 1]).insert(self.pos[1], inst_player)


    def move_down(self, inst_replace, inst_player):
        """move player down"""
        (self.room[self.pos[0]]).pop(self.pos[1])
        (self.room[self.pos[0]]).insert(self.pos[1], inst_replace)
        (self.room[self.pos[0] + 1]).pop(self.pos[1])
        (self.room[self.pos[0] + 1]).insert(self.pos[1], inst_player)


    def move_left(self, inst_replace, inst_player):
        """move player left"""
        (self.room[self.pos[0]]).pop(self.pos[1])
        (self.room[self.pos[0]]).insert(self.pos[1], inst_replace)
        (self.room[self.pos[0]]).pop(self.pos[1] - 1)
        (self.room[self.pos[0]]).insert(self.pos[1] - 1, inst_player)


    def move_right(self, inst_replace, inst_player):
        """move player right"""
        (self.room[self.pos[0]]).pop(self.pos[1])
        (self.room[self.pos[0]]).insert(self.pos[1], inst_replace)
        (self.room[self.pos[0]]).pop(self.pos[1] + 1)
        (self.room[self.pos[0]]).insert(self.pos[1] + 1, inst_player)


def main():
    """
    main function

    kick off the game
    """

    game = PyHack()
    game.game_loop()


# run main function
if __name__ == "__main__":
    main()
