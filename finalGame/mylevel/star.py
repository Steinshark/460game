#!/usr/bin/python3

# Important Libraries
import pyglet, config, math
import time
# An Enemy Combatant
class Star:
    def __init__(self,sprites={},buildSprite=None,speed=0.05,scale=0.15,x=850,y=150):

        # Store the sprites, and the sprite building function
        self.sprites        = sprites
        self.buildSprite    = buildSprite
        self.sprite         = buildSprite(sprites,'star','star','Right',.05,1,False,x,y)

        self.t_0            = time.time()
        self.spawned        = True
        self.mode           = 'star'
        self.time_to_live   = 45
        x,y = self.sprite.x, self.sprite.y
        width,height = self.sprite.width, self.sprite.height
        self.hitbox = { 'll' : {'x' : x - width/2,            'y' : y} ,
                        'lr' : {'x' : x + width/2,            'y' : y} ,
                        'ul' : {'x' : x - width/2,            'y' : y + height},
                        'ur' : {'x' : x + width/2,            'y' : y + height}}

    # Draw our character
    def draw(self, t=0, keyTracking={}, config=None,level=None,w=800,h=600,*other):

        self.sprite.draw()
        return  not self.check_remove(config,w,h,level)

    def check_remove(self,config,w,h,level):
        for point in self.hitbox:
            if self.within(self.hitbox[point],level.hero.hitbox):
                level.hero.set_invincible()
                level.score += 300
                self.spawned = False
                return True
        if time.time() - self.t_0 > self.time_to_live:
            self.spawned = False
            return True
        for weapon in level.objects:
            if  weapon.mode == 'Block':
                continue
            if self.within({'x' : weapon.sprite.x+weapon.sprite.width/2, 'y': weapon.sprite.y+weapon.sprite.height/2},self.hitbox):
                dead = True
                return True
        return False

    def within(self,p1,hitbox):
        return \
        p1['x'] >= hitbox['ll']['x'] and \
        p1['x'] <= hitbox['lr']['x'] and \
        p1['y'] <= hitbox['ul']['y'] and \
        p1['y'] >= hitbox['ll']['y']
