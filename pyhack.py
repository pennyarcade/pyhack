"""
Pyhack

Python roguelike game using (almost) only standard library calls
Console only for now
Attempts to be cross platform
"""

import os
import platform
from crt import Crt


def gamemap(room, screen):
    """draw game mask"""
    for i in range(1, len(room) + 1):
        screen.write_ln("".join(room[i]))


def player_pos(pos, room, stuff):
    """get player position"""
    for i in range(1, len(room) + 1):
        if stuff['player'] in room[i]:
            x_axis = i
            y_axis = room[i].index(stuff['player'])
            del pos[:]
            pos.append(x_axis)
            pos.append(y_axis)


def updater(pos, room, stuff, screen):
    """update game screen"""
    if platform.system() == 'Windows':
        os.system('cls')
    elif platform.system() == 'Linux':
        os.system('clear') #For linux.. I don't know what to do about mac :/
    gamemap(room, screen)
    player_pos(pos, room, stuff)


def move_up(ditcioary, inst_replace, inst_player, pos):
    """move player up"""
    (ditcioary[pos[0]]).pop(pos[1])
    (ditcioary[pos[0]]).insert(pos[1], inst_replace)
    (ditcioary[pos[0] - 1]).pop(pos[1])
    (ditcioary[pos[0] - 1]).insert(pos[1], inst_player)


def move_down(ditcioary, inst_replace, inst_player, pos):
    """move player down"""
    (ditcioary[pos[0]]).pop(pos[1])
    (ditcioary[pos[0]]).insert(pos[1], inst_replace)
    (ditcioary[pos[0] + 1]).pop(pos[1])
    (ditcioary[pos[0] + 1]).insert(pos[1], inst_player)


def move_left(ditcioary, inst_replace, inst_player, pos):
    """move player left"""
    (ditcioary[pos[0]]).pop(pos[1])
    (ditcioary[pos[0]]).insert(pos[1], inst_replace)
    (ditcioary[pos[0]]).pop(pos[1] - 1)
    (ditcioary[pos[0]]).insert(pos[1] - 1, inst_player)


def move_right(ditcioary, inst_replace, inst_player, pos):
    """move player right"""
    (ditcioary[pos[0]]).pop(pos[1])
    (ditcioary[pos[0]]).insert(pos[1], inst_replace)
    (ditcioary[pos[0]]).pop(pos[1] + 1)
    (ditcioary[pos[0]]).insert(pos[1] + 1, inst_player)


def do_up(pos, room, stuff, screen):
    """process up movement"""
    if room[pos[0]-1][pos[1]] != stuff['wall']:
        move_up(room, stuff['empty'], stuff['player'], pos)
        updater(pos, room, stuff, screen)
        screen.write_ln(pos)
    else:
        screen.write_ln("Bump! Wall : up")


def do_down(pos, room, stuff, screen):
    """process down movement"""
    if room[pos[0]+1][pos[1]] != stuff['wall']:
        move_down(room, stuff['empty'], stuff['player'], pos)
        updater(pos, room, stuff, screen)
        screen.write_ln(pos)
    else:
        screen.write_ln("Bump! wall : down")


def do_right(pos, room, stuff, screen):
    """process right movement"""
    if room[pos[0]][pos[1]+1] != stuff['wall']:
        move_right(room, stuff['empty'], stuff['player'], pos)
        updater(pos, room, stuff, screen)
        screen.write_ln(pos)
    else:
        screen.write_ln("Bump! wall : right")


def do_left(pos, room, stuff, screen):
    """process right movement"""
    if room[pos[0]][pos[1]-1] != stuff['wall']:
        move_left(room, stuff['empty'], stuff['player'], pos)
        updater(pos, room, stuff, screen)
        screen.write_ln(pos)
    else:
        screen.write_ln("Bump! wall : left")


def game_loop(pos, room, stuff, screen):
    """main game loop"""
    while True:
        pressedkey = screen.read_key()

        if pressedkey == 'w' or pressedkey == 'W':
            do_up(pos, room, stuff, screen)
        elif pressedkey == 's' or pressedkey == 'S':
            do_down(pos, room, stuff, screen)
        elif pressedkey == 'a' or pressedkey == 'A':
            do_left(pos, room, stuff, screen)
        elif pressedkey == 'd' or pressedkey == 'D':
            do_right(pos, room, stuff, screen)
        elif pressedkey == '#':
            quit()



def main():
    """
    main function

    @todo: does much to much right now
    """
    screen = Crt()
    screen.clr_scr()

            # 0   1    2    3    4    5    6    7
            # 8   9   10   11   12   13   14   15
    room = {
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

    stuff = {'wall' : "#",
             'player' : "@",
             'empty' : ".",
             'money' : "$",
             'chest' : "C"}
    # potion = ['hp','xp','dmg']
    # weapon = ['sword','nuclear bomb','TNT']


    pos = [] # 0 is X,1 is Y

    updater(pos, room, stuff, screen)

    game_loop(pos, room, stuff, screen)


# run main function
if __name__ == "__main__":
    main()
