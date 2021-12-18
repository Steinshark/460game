#!/usr/bin/python3

# Important Libraries
import pyglet, config, math
import time
# A key to continue to the end of the level
class Key:
    def __init__(self,sprites={},buildSprite=None,speed=0.05,scale=0.15,x=50,y=1300):

        # Store the sprites, and the sprite building function
        self.sprites        = sprites
        self.buildSprite    = buildSprite
        self.sprite         = buildSprite(sprites,'key','key','Right',.05,1,False,x,y)

        self.t_0            = time.time()
        self.spawned        = True
        self.mode           = 'key'

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
                level.score += 100
                self.spawned = False
                return True
        return False

    def within(self,p1,hitbox):
        return \
        p1['x'] >= hitbox['ll']['x'] and \
        p1['x'] <= hitbox['lr']['x'] and \
        p1['y'] <= hitbox['ul']['y'] and \
        p1['y'] >= hitbox['ll']['y']
