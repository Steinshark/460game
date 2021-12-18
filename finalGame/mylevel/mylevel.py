#!/usr/bin/python3

# Important Libraries
import pyglet
from pprint import pp
import sys
# Our own Game Libraries
import sprites, config
from player import Player
from enemy import Enemy
from weapon import Object
from star import Star
from crate import Crate
from key import Key
import time
from pyglet.gl import glLoadIdentity, glTranslatef

# SI460 Level Definition
class Level:
    def __init__(self, sprites, hero, star, enemies=[]):

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

        #scrolling items
        self.delta_x = 0
        self.delta_y = 0
        self.scrollX = 0
        self.scrollY = 0

        #Dimensionality
        self.level_height = len(config.level.keys()) * config.height
        self.checkpoint = 0
        self.level_width = len(list(config.level.values())[0]) * config.width
        self.region_unlocks = {1 : [(22,1), (22,2)], 2: [(61,3), (61,4)]}
        self.region_objective = {0: "Objective: Kill 5 Zombies", 1: "Objective: Find the key", 2: "Objective: Finish Level"}
        self.level_won = False
        # items
        self.star = star
        self.key = key
        # Score handling
        self.score = 0
        height = 0
        self.score_label        = pyglet.text.Label('HELLO WORLD',font_name='Times New Roman',                          font_size = 20, x = 50 - self.scrollX, y = (height+self.scrollY)-40 , anchor_x = 'left',anchor_y = 'top')
        self.objective_label    = pyglet.text.Label(self.region_objective[self.checkpoint],font_name='Times New Roman', font_size = 20, x = 50 - self.scrollX, y = (height+self.scrollY)-70 , anchor_x = 'left',anchor_y = 'top')
        self.invulnerable_label = pyglet.text.Label('Invulnerable!',font_name='Times New Roman',                        font_size = 20, x = 50 - self.scrollX, y = (height+self.scrollY)-100, anchor_x = 'left',anchor_y = 'top')
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
        self.background.blit(self.background_x,self.background_y,height=max((config.rows+4)*config.height, height),width=max((config.cols+1)*config.width, width))
        self.score_label = pyglet.text.Label('Score: ' + str(self.score).zfill(5),      font_name='Times New Roman', font_size = 20, x = 50 - self.scrollX, y = (height+self.scrollY)-40, anchor_x = 'left',anchor_y = 'top')
        self.objective_label = pyglet.text.Label(self.region_objective[self.checkpoint],font_name='Times New Roman', font_size = 20, x = 50 - self.scrollX, y = (height+self.scrollY)-70, anchor_x = 'left',anchor_y = 'top')
        self.invulnerable_label = pyglet.text.Label('Invulnerable!',font_name='Times New Roman',                        font_size = 20, x = 50 - self.scrollX, y = (height+self.scrollY)-100, anchor_x = 'left',anchor_y = 'top')

        # Draw the gameboard
        self.drawBoard(config.level, self.background_x, self.background_y, config.height, config.width)
        self.drawBoard(config.goals, self.background_x, self.background_y, config.height, config.width)
        if self.star.spawned:
            self.star.draw(t,config=config,level=self)
        if self.key.spawned:
            self.key.draw(t,config=config,level=self)
        # Draw the enemies
        for enemy in self.enemies:
            enemy.draw(t,config=config,level=self)
            if enemy.remove:
                self.enemies.remove(enemy)

        for obj in self.objects:
            if not obj.draw(t,config=config,level=self,w=width,h=width):
                self.objects.remove(obj)

        # Draw the hero.
        self.hero.draw(t,keyTracking,self.enemies,config,level)

        # Calculate the scrolling
        dx = abs(self.hero.dx)
        dy = abs(self.hero.dy)
        relative_pos_x = self.hero.sprite.x + self.scrollX
        relative_pos_y = self.hero.sprite.y - self.scrollY
        if relative_pos_x >  .75 * width:
            self.scrollX -= dx
        if relative_pos_x < .25 * width:
            self.scrollX += dx
        if relative_pos_y > .75 * height:
            self.scrollY += dy
        if relative_pos_y < .15 * height:
            self.scrollY -= dy

        #self.background_x = -.9 * self.scrollX
        #self.background_y =   1 * self.scrollY

        # Shift the world
        if self.level_won:
            pyglet.text.Label('YOU WIN',font_name='Times New Roman',font_size = 50, x = 350 - self.scrollX, y = (height+self.scrollY)-300 , anchor_x = 'center',anchor_y = 'top').draw()

        self.score_label.draw()
        self.objective_label.draw()
        if self.hero.invincible:
            self.invulnerable_label.draw()

        glLoadIdentity()
        glTranslatef(self.scrollX, -self.scrollY, 0)
        self.check_checkpoint(config)

    def add_item(self,dx,dy,type,mode,facing,x,y):
        if type == 'block':
                self.objects.append(Crate(dx,dy,sprites=gameSprites,
                                        buildSprite = sprites.buildSprite,
                                        playerClass = type,
                                        mode = mode,
                                        facing = facing,
                                        speed = .05,
                                        scale = .15,
                                        loop = True,
                                        x=x,
                                        y=y))
        elif type == 'weapon':
            self.objects.append(Object(dx,dy,sprites=gameSprites,
                                        buildSprite = sprites.buildSprite,
                                        playerClass = type,
                                        mode = mode,
                                        facing = facing,
                                        speed = .05,
                                        scale = .15,
                                        loop = False,
                                        x=x,
                                        y=y))
    def play_sound(self,filename,loop):
        self.newSound = pyglet.media.load(filename)
        self.newSound.play()
        return

    def check_checkpoint(self,config):
        if self.checkpoint == 0:
            if self.hero.kills >= 5:
                self.checkpoint = 1
                self.unlock_region(1,config)
        elif self.checkpoint == 1:
            if not self.key.spawned:
                self. checkpoint = 2
                self.unlock_region(2,config)
    def unlock_region(self,region,config):
            for unlock_block in self.region_unlocks[region]:
                col,row = unlock_block
                del config.level[row][col]


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
star = Star(gameSprites,sprites.buildSprite,.01,.15,850,150)
key  = Key( gameSprites,sprites.buildSprite,.01,.15,50,1300)

# provide the level to the game engine
print('Starting level:', config.levelName)
level = Level(gameSprites, hero, star, enemies,)
