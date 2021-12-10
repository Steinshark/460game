#!/usr/bin/python3

# Important Libraries
import pyglet
from pprint import pp
# Our own Game Libraries
import sprites, config
from player import Player
from enemy import Enemy
from spawned_item import Object
from pyglet.gl import glLoadIdentity, glTranslatef

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
        self.objects = []

        # Sound things
        self.player = pyglet.media.Player()
        self.background_music = pyglet.media.load('mylevel/music/1.wav')
        self.player.queue(self.background_music)
        # start playing the music
        self.player.loop = True
        self.player.play()
        self.delta_x = 0
        self.delta_y = 0
        self.scrollX = 0
        self.scrollY = 0

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
            enemy.draw(t,config=config,level=self)

        for obj in self.objects:
            if not obj.draw(t,config=config,level=self,w=800,h=600):
                print("REMOVED")
                self.objects.remove(obj)

        # Draw the hero.
        self.hero.draw(t,keyTracking,self.enemies,config,level)
        dx = abs(self.hero.dx)
        dy = abs(self.hero.dy)
        print(self.hero.playerSprite.y-self.scrollY)
        if self.hero.facing == 'Right' and self.hero.playerSprite.x-self.scrollX >  .75 * width:
            self.scrollX -= dx
        if self.hero.facing == 'Left' and self.hero.playerSprite.x-self.scrollX < .25 * width:
            self.scrollX += dx
        if self.hero.playerSprite.y - self.scrollY > .75 * height:
            self.scrollY += dy
        if self.hero.playerSprite.y - self.scrollY < .25 * height:
            self.scrollY -= dy
        # Shift the world
        glLoadIdentity()
        glTranslatef(self.scrollX, -self.scrollY, 0)

    def add_item(self,dx,dy,type,mode,facing,x,y):
        self.objects.append(Object(dx,dy,sprites=gameSprites,
                                    buildSprite = sprites.buildSprite,
                                    playerClass = type,
                                    mode = mode,
                                    facing = facing,
                                    speed = .05,
                                    scale = .15,
                                    loop = True,
                                    x=x,
                                    y=y))
    def play_sound(self,filename,loop):
        self.newSound = pyglet.media.load(filename)
        self.newSound.play()
        return

# Load all game sprites
print('Loading Sprites...')
gameSprites = sprites.loadAllImages(config.spritespath)

# Load in the hero
print('Loading the Hero...')
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

enemies = [Enemy(   gameSprites,\
                    sprites.buildSprite,"enemy-1", "Run","Right",\
                    config.playerSpriteSpeed,
                    config.playerSpriteScale,
                    True,
                    enemy[0] * config.width ,\
                    enemy[1] * config.height+ 1) for enemy in config.enemies]



# provide the level to the game engine
print('Starting level:', config.levelName)
level = Level(gameSprites, hero, enemies)
