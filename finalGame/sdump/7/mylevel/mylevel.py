#!/usr/bin/python3

# Important Libraries
import pyglet

# Our own Game Libraries
import sprites, config

# SI460 Level Definition
class Level:

    # Build our Level, passing in our sprites, the hero, and any initial
    # Enemies or Weapons fire existing in the world.
    def __init__(self, sprites, hero, enemies=[], weapons=[]):

        # Create the Background, this is one method of creating images,
        # we will work with multiple methods.
        # Take a look at how this is drawn in the on_draw function
        # and the self.background.blit method.
        self.background   = pyglet.resource.image(config.background)
        self.background_x = 0
        self.background_y = 0

        # Store the loaded sprites
        self.sprites = sprites

        # Store the Player, Enemy, and the Hero's Weapon Objects
        self.hero    = hero
        self.enemies = enemies
        self.weapons = weapons

        # Music in the Background
        self.sound = pyglet.media.Player()
        self.sound.queue(pyglet.media.load(config.background_music, streaming=True))
        self.sound.eos_action = 'loop'
        self.sound.loop = True
        self.sound.play()
        self.soundPlaying = True

    # Here is a complete drawBoard function which will draw the terrain.
    def drawBoard(self, level, delta_x=0, delta_y=0, height=50, width=50):
        for row in level.keys():
            for col in level[row].keys():
                level[row][col].anchor_x = 0
                level[row][col].anchor_y = 0
                level[row][col].blit(col*width+delta_x,row*height+delta_y, height=height, width=width)

    # Draw the terrain, enemies, weapon fire, and our fearless hero
    def draw(self, t=0, dt=0, width=800, height=600, keyTracking={}, mouseTracking={}, *other):

        # Create an easy array of what keys are pressed
        keyPressed = []
        if keyTracking != {}:
            for key in keyTracking:
                if key in config.keyMappings:
                    keyPressed.append(config.keyMappings[key])

        # Draw the game background
        if self.background.width < width:
            self.background.blit(self.background_x,self.background_y,height=height,width=width)
        else:
            self.background.blit(self.background_x,self.background_y,height=height)

        # Draw the gameboard
        self.drawBoard(config.level, self.background_x, self.background_y, config.height, config.width)

        # Draw any goals (level Enders)
        self.drawBoard(config.goals, self.background_x, self.background_y, config.height, config.width)

        # Draw the enemies
        for i in range(len(self.enemies)-1, -1, -1):
            enemyDeath, enemyWin, enemyWeaponsFire = self.enemies[i].draw(t, dt,            # Current Time
                                                                          {}, [],           # Keyboard and Mouse Input
                                                                          [], self.weapons, # incoming enemies and weapons fire
                                                                          {}, {},           # Goals (Level Finishers) and Objects (loot boxes)
                                                                          self)             # The level object
            if enemyDeath:
                del(self.enemies[i])

        # Draw the Hero!
        heroDeath, heroWin, heroWeaponsFire = self.hero.draw(t, dt,                         # Current Time
                                                             keyPressed, mouseTracking,     # Keyboard and Mouse Input
                                                             self.enemies, [],              # Incoming enemies and weapons fire
                                                             config.goals, {},              # Goals (Level Finishers) and Objects (loot boxes)
                                                             self)                          # The level object
        if heroWeaponsFire is not None:
            self.weapons.append(heroWeaponsFire)

        # Draw the weapon's fire (knifes, lasers, etc)
        for i in range(len(self.weapons)-1, -1, -1):
            weaponDeath, weaponWin, weaponCreatedWeapon = self.weapons[i].draw(t, dt,       # Current Time
                                                                               {}, [],      # Keyboard and Mouse Input
                                                                               [], [],      # incoming enemies and weapons fire
                                                                               {}, {},      # Goals (Level Finishers) and Objects (loot boxes)
                                                                               self)        # The level object
            if weaponDeath:
                del(self.weapons[i])

        # Return the status of the player
        return heroDeath

# Load all game sprites
print('Loading Sprites...')
gameSprites = sprites.loadAllImages(config.spritespath)

# Load in the hero
print('Loading the Hero...')
from player import Player
hero = Player(gameSprites,                  # Sprite Dictionary
              sprites.buildSprite,          # BuildSprite Function
              "hero", "Idle", "Right",      # Initial Sprite
              config.playerSpriteSpeed,     # Speed of Sprite Animation
              config.playerSpriteScale,     # Scale of Sprite
              True,                         # Sprite should loop continuously
              config.playerStartCol * config.width,   # Initial X Position
              config.playerStartRow * config.height)  # Initial Y Position

# Load in the Enemies
print('Loading the Enemies...')
from enemy import Enemy
enemies = []
for newEnemy in config.enemies:
    enemies.append(Enemy(gameSprites,                   # Sprite Dictionary
                         sprites.buildSprite,           # BuildSprite Function
                         config.enemyMap[newEnemy[2]],  # Initial Sprite
                         "Run", "Right",                # Initial Sprite Mode / Dir
                         config.playerSpriteSpeed,      # Speed of Sprite Animation
                         config.playerSpriteScale,      # Scale of Sprite
                         True,                          # Sprite should loop continuously
                         newEnemy[0] * config.width,    # Initial X Position
                         newEnemy[1] * config.height))  # Initial Y Position

# provide the level to the game engine
print('Starting level:', config.levelName)
level = Level(gameSprites, hero, enemies)
