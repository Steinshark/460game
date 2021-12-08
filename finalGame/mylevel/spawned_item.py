#!/usr/bin/python3

# Important Libraries
import pyglet, config
from graphics import *
from pygame import Rect
import time
# An Enemy Combatant
class Object:
    def __init__(self,dx,dy, sprites={},buildSprite=None,playerClass="enemy-1",mode="Run",facing="Right",speed=0.05,scale=0.15,loop=True,x=380,y=250):

        # Store the sprites, and the sprite building function
        self.objSprites      = sprites
        self.buildSprite  = buildSprite
        self.objSprite = None


        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop  = loop
        self.animationX     = x
        self.animationY     = y + .5
        self.playerClass    = playerClass
        self.mode           = mode
        self.facing         = facing

        self.t_0   = time.time()
        self.dx = dx
        self.dy = dy


        # Build the starting character sprite
        self.changeSprite()



    # Build the initial character
    def changeSprite(self, mode=None, facing=None):
        if mode is not None:
            self.mode = mode
        if facing is not None:
            self.facing = facing
        if self.objSprite is not None:
            self.animationX = self.objSprite.x
            self.animationY = self.objSprite.y
        self.objSprite = self.buildSprite(self.objSprites,
                                             self.playerClass,
                                             self.mode,
                                             self.facing,
                                             self.animationSpeed,
                                             self.animationScale,
                                             self.animationLoop,
                                             self.animationX,
                                             self.animationY)
    # Move the character
    def movement(self, config, t=0, keyTracking={}):
        self.objSprite.x += self.dx
        self.objSprite.y += self.dy
        pass



    # Draw our character
    def draw(self, t=0, keyTracking={}, config=None,level=None,w=800,h=600,*other):
        self.movement(config, t, keyTracking)
        self.objSprite.draw()

        if self.check_remove(config,w,h,level):
            level.hero.threw = False
            return False
        return True

    def check_remove(self,config,w,h,level):
        return      self.objSprite.x > w or self.objSprite.x < 0 or\
                    self.objSprite.y > h or self.objSprite.y < 0 or\
                    time.time() - self.t_0 > 10 or\
                    self.check_terrain_hit(config) or\
                    self.check_enemy_hit(level)





    def check_enemy_hit(self,level):
        item_hitbox = {'point':{'x' : self.objSprite.x, 'y' : self.objSprite.y}}

        for enemy in level.enemies:
            if enemy.will_this_kill_me(item_hitbox) and not enemy.dead:
                enemy.dead = True
                return True
        return False

    def check_terrain_hit(self,config):

        level,width,height = (config.level,config.width,config.height)

        player_box = {'only':{'x' : self.objSprite.x, 'y' : self.objSprite.y}}
        delta_x = 0
        delta_y = 0
        # Terrain collision parametrics
        for row in level.keys():
            for col in level[row]:
                x,y = col*width + delta_x , row*height + delta_y
                ll = {'x' : x,          'y' : y}
                lr = {'x' : x + width,  'y' : y}
                ul = {'x' : x,          'y' : y + height}
                ur = {'x' : x + width,  'y' : y + height}
                hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

                for point in player_box.keys():
                    if self.within(player_box[point],hitbox):
                        return True

        return False

    def will_collide_v(self,config):
        self.objSprite.x += self.dx
        self.objSprite.y += self.dy

        collision = self.check_collision_vert(config)

        self.objSprite.x -= self.dx
        self.objSprite.y -= self.dy

        return collision

    def will_collide_h(self,config):
        self.objSprite.x += self.dx

        collision = self.check_collision_hori(config)

        self.objSprite.x -= self.dx

        return collision

    def within(self,p1,hitbox):
        return \
        p1['x'] >= hitbox['ll']['x'] and \
        p1['x'] <= hitbox['lr']['x'] and \
        p1['y'] <= hitbox['ul']['y'] and \
        p1['y'] >= hitbox['ll']['y']
