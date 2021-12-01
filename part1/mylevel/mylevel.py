#!/usr/bin/python3

# Important Libraries
import pyglet
from pprint import pp
# Our own Game Libraries
import sprites, config

# SI460 Level Definition
class Level:
    def __init__(self, sprites, hero, enemies=[]):

        # Create the Background, this is one method of creating images,
        # we will work with multiple methods.
        # Take a look at how this is drawn in the on_draw function
        # and the self.background.blit method.
        self.background   = pyglet.resource.image(config.background)
        self.background_x = 0
        self.background_y = 0

        # Store the loaded sprites and hero
        self.sprites = sprites
        self.hero    = hero
        self.enemies = enemies

    # Here is a complete drawBoard function which will draw the terrain.
    # Lab Part 1 - Draw the board here
    def drawBoard(self, level, delta_x=0, delta_y=0, height=50, width=50):
        # No reason other than im too stubborn to change this
        img = level

        # Just print the darn dictionary
        for row in img.keys():
            for col in img[row]:

                data = img[row][col]
                x,y = col*width + delta_x , row*height + delta_y

                img[row][col].blit(x,y,height=height,width=width)

    def draw(self, t=0, width=800, height=600, keyTracking={}, mouseTracking=[], *other):

        # Draw the game background
        if self.background.width < width:
            self.background.blit(self.background_x,self.background_y,height=height,width=width)
        else:
            self.background.blit(self.background_x,self.background_y,height=height)

        # Draw the gameboard
        self.drawBoard(config.level, 0, 0, config.height, config.width)

        # Draw the enemies
        for enemy in self.enemies:
            enemy.draw(t)

        # Draw the hero.
        self.hero.draw(t, keyTracking,config)

# Load all game sprites
print('Loading Sprites...')
gameSprites = sprites.loadAllImages(config.spritespath)

# Load in the hero
print('Loading the Hero...')
from player import Player
hero = Player(gameSprites,
              sprites.buildSprite,
              "hero", "Idle", "Right",
              config.playerSpriteSpeed,
              config.playerSpriteScale,
              True,
              config.playerStartCol * config.width,
              config.playerStartRow * config.height)

# Load in the Enemies
print('Loading the Enemies...')
enemies = []

# provide the level to the game engine
print('Starting level:', config.levelName)
level = Level(gameSprites, hero, enemies)
