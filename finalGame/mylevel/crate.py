#!/usr/bin/python3

# Important Libraries
import pyglet, config, math
import time
# An Enemy Combatant
class Crate:
    def __init__(self,dx,dy, sprites={},buildSprite=None,playerClass="enemy-1",mode="Run",facing="Right",speed=0.05,scale=0.15,loop=True,x=380,y=250):

        # Store the sprites, and the sprite building function
        self.sprites        = sprites
        self.buildSprite    = buildSprite
        self.sprite         = None
        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = 1.3
        self.animationLoop  = loop

        self.offset         = 50 - ((facing=='Left') * 100)
        self.animationX     = x + self.offset
        self.animationY     = y + .5
        self.playerClass    = playerClass
        self.mode           = mode
        self.facing         = facing

        self.t_0   = time.time()




        # Build the starting character sprite
        self.changeSprite()
        self.hitbox = {'only':{'x' : self.sprite.x, 'y' : self.sprite.y}}


        x,y = self.sprite.x, self.sprite.y
        width,height = self.sprite.width, self.sprite.height
        self.hitbox = { 'll' : {'x' : x - width/2,            'y' : y} ,
                        'lr' : {'x' : x + width/2,            'y' : y} ,
                        'ul' : {'x' : x - width/2,            'y' : y + height},
                        'ur' : {'x' : x + width/2,            'y' : y + height}}

    # Build the initial character
    def changeSprite(self, mode=None, facing=None):
        if mode is not None:
            self.mode = mode
        if facing is not None:
            self.facing = facing
        if self.sprite is not None:
            self.animationX = self.sprite.x
            self.animationY = self.sprite.y
        self.sprite = self.buildSprite(self.sprites,
                                             self.playerClass,
                                             self.mode,
                                             self.facing,
                                             self.animationSpeed,
                                             self.animationScale,
                                             self.animationLoop,
                                             self.animationX,
                                             self.animationY)

    # Draw our character
    def draw(self, t=0, keyTracking={}, config=None,level=None,w=800,h=600,*other):
        self.sprite.draw()
        return self.check_remove(config,w,h,level)

    def check_remove(self,config,w,h,level):
        return      not (time.time() - self.t_0 > 3.2 or self.check_weapon_hit(level))

    def check_weapon_hit(self,level):
        for point in self.hitbox.values():
            color = (0,0,0)
            pyglet.shapes.Circle(point['x'],point['y'], 2, color = color).draw()

        for weapon in level.objects:
            if  weapon.mode in ['Block','star', 'key']:
                continue
            if self.within(weapon.hitbox['only'],self.hitbox):
                dead = True
                return True
        return False

    def check_terrain_hit(self,config):
        level,width,height = (config.level,config.width,config.height)

        # Terrain collision parametrics
        for row in level.keys():
            for col in level[row]:
                x,y = col*width + delta_x , row*height + delta_y
                ll = {'x' : x,          'y' : y}
                lr = {'x' : x + width,  'y' : y}
                ul = {'x' : x,          'y' : y + height}
                ur = {'x' : x + width,  'y' : y + height}
                hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

                for point in self.hitbox.keys():
                    if self.within(self.hitbox[point],hitbox):
                        return True

        return False


    def within(self,p1,hitbox):
        return \
        p1['x'] >= hitbox['ll']['x'] and \
        p1['x'] <= hitbox['lr']['x'] and \
        p1['y'] <= hitbox['ul']['y'] and \
        p1['y'] >= hitbox['ll']['y']
