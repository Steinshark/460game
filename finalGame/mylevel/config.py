#!/usr/bin/python3 -B

# SI460 - Game Level Configuration file - A default level configuration
#         file for the SI460 Graphics Course.  This file defines the layout
#         of the game, where the players and enemies exists and where the goal
#         is located.  Typically reaching the goal advances the user to
#         the next level.

# We are assuming a 800x600 world, which is allowed to go beyond that in
# both the x and y, and is divided up into 50x50 chunks in a grid-like
# fashion.

# Lets define the size of our grid in terms of width and height for
# EACH cell in the grid.
height = 50
width  = 50

# Define the board
levelDefinition = '''
36
35
34
33
32
31
30
29
28
27
26
25                                                                         hl hm hm hm hm um um um um um um um mm mr
24                                                                                        hl mm mm mm mm mm mm mr
23                                                                                        hl mm mm mm mr
22
21
20
19                                                                                                                   rl um um um um um ur
18                                                                                                                                                                         ul um um mm
17 um ur                                                                                                                                                                   ml mm mm mm
16 mm mr                               hl hr                                     um um um um um um um ur                                                                   ml mm mm mm
15 mm mr                                                             hl um um um mm mm mm mm mm mm mr                                                                      ml mm mm mm
14 mm mr                                                                ml mm mm mm mm mm mm mr                                                                   hl um um cl mm mm
13 mm mr                   hl hm hm hm hm hm hm hm hm um ur                ml mm mm mr
12 mm mr                                              ml mr
11 mm mr          hr                                  ml mr
10 mm mr                                              ml mr
09 mm cr wl ur                      bt                ml mr                                                 ul ur
08 mm mm mm mr                      bb                ml mr                                                 ml mr
07 mm mm mm cr wl um um um um um um um ur             ml mr                                     ul um um wr cl mr
06 mm mm mm mm mm mm mm mm mm mm mm mm cr wl um um wr cl cr wl um ur bu ul um          ul um um cl mm mm mm mm mr mm mm mm mm mm mm mm
05 mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm um       mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm
04 mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm          mm mm mm mm mm mm       mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm
03 mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm                               mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm
02 mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm                      mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm
01 mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm mm
00 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80
'''

# Define the objects
goalDefinition = '''
36
35
34
33
32
31
30
29
28
27
26                                                                                                  sm
25
24
23
22
21
20
19
18
17
16
15
14
13
12
11
10
09
08
07
06
05
04
03
02
01
00 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80
'''

# Define the enemies
enemyDefinition = '''
36
35
34
33
32
31
30
29
28
27
26                                                                                                  e1
25
24
23
22
21
20
19
18
17                                                                                  e1
16
15
14                                        e1
13
12
11
10
09
08                                        e1
07
06
05
04
03
02
01
00 00 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 76 77 78 79 80
'''


# Define where the player will start on the board
playerStartRow = 8
playerStartCol = 5


# Define the scaling for the player, and speed of the shifts between
# the various sprites that make up the players.
playerSpriteSpeed = 0.05
playerSpriteScale = 0.15
enemySpriteSpeed = 0.05
enemySpriteScale = 0.15

# Retrieve the level name from the directory name, don't change this...
import os
levelName = os.path.realpath(__file__).split('/')[-2]

# Define where the background image is
background = levelName + "/backgrounds/level1.png"

# Define what music to play
background_music = levelName + '/music/1.wav'

# Sound Effects, when a player changes it state to one of the
# following modes, play the following sounds.
sounds = {'hero':{'Jump':        levelName + '/music/jump.wav',
                  'Attack':      levelName + '/music/attack.wav',
                  'Jump-Attack': levelName + '/music/jump.wav',
                  'Jump-Throw':  levelName + '/music/throw.wav',
                  'Throw':       levelName + '/music/throw.wav',
                  'Dead':        levelName + '/music/hero_death.wav'  },
          'enemy-1': {'Dead':    levelName + '/music/enemy_death.wav' },
          'enemy-2': {'Dead':    levelName + '/music/enemy_death.wav' } }

# When our hero wins the game, play the following music
heroSoundWin = levelName + '/music/win.wav'

# Where are the sprites, tiles, and goals located?
tilepath     = levelName + '/tiles'
goalpath     = levelName + '/objects'
spritespath  = levelName + "/sprites"

# Define the Keyboard mappings
from pyglet.window import key
keyMappings = {key.LSHIFT: 'run',    key.RSHIFT: 'run',
               key.LALT:   'attack', key.RALT:   'attack',
               key.LCTRL:  'shoot',  key.RCTRL:  'shoot',
               key.SPACE:  'jump',
               key.RIGHT:  'right',
               key.LEFT:   'left',
               key.UP:     'up',
               key.DOWN:   'down'}

# Determine some very useful information needed in our game.
from layout import positionEnemies, board2grid
enemies = positionEnemies(enemyDefinition)

level, rows, cols = board2grid(levelDefinition, tilepath, returnSize=True)
goals = board2grid(goalDefinition, goalpath)
