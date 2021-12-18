#!/usr/bin/python3

# Important Libraries
import pyglet, config, math
import time
# An Enemy Combatant
class Object:
    def __init__(self,dx,dy, sprites={},buildSprite=None,playerClass="enemy-1",mode="Run",facing="Right",speed=0.05,scale=0.15,loop=True,x=380,y=250):

        # Store the sprites, and the sprite building function
        self.sprites      = sprites
        self.buildSprite  = buildSprite
        self.sprite = None


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
        self.hitbox = {'only' : {'x' : x + self.sprite.width/2, 'y' : y + self.sprite.height/2}}


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
    # Move the character
    def movement(self, config, t=0, keyTracking={}):
        self.sprite.x += self.dx
        self.sprite.y += self.dy
        pass


    # Draw our character
    def draw(self, t=0, keyTracking={}, config=None,level=None,w=800,h=600,*other):
        self.movement(config, t, keyTracking)
        self.update_hitbox()
        self.sprite.draw()
        if self.check_remove(config,w,h,level):
            level.hero.threw = False
            return False
        return True

    def check_remove(self,config,w,h,level):
        return      self.sprite.x+level.scrollX > w or self.sprite.x < 0 or\
                    self.sprite.y-level.scrollY > w or self.sprite.y < 0 or\
                    time.time() - self.t_0 > 10 or\
                    self.check_terrain_hit(config) or\
                    self.check_enemy_hit(level)

    def check_enemy_hit(self,level):
        item_hitbox = {'point':{'x' : self.sprite.x, 'y' : self.sprite.y}}
        for enemy in level.enemies:
            if enemy.will_this_kill_me(item_hitbox) and not enemy.dead:
                level.score += 100
                level.hero.kills += 1
                enemy.dead = True
                return True
        return False

    def check_terrain_hit(self,config):
        level,width,height = (config.level,config.width,config.height)
        # Terrain collision parametrics
        for row in level.keys():
            for col in level[row]:
                x,y = col*width , row*height
                ll = {'x' : x,          'y' : y}
                lr = {'x' : x + width,  'y' : y}
                ul = {'x' : x,          'y' : y + height}
                ur = {'x' : x + width,  'y' : y + height}
                hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

                for point in self.hitbox.keys():
                    if self.within(self.hitbox[point],hitbox):
                        return True

        return False

    def will_collide_v(self,config):
        self.sprite.x += self.dx
        self.sprite.y += self.dy
        self.update_hitbox()
        collision = self.check_collision_vert(config)

        self.sprite.x -= self.dx
        self.sprite.y -= self.dy

        return collision

    def will_collide_h(self,config):
        self.sprite.x += self.dx
        self.update_hitbox()
        collision = self.check_collision_hori(config)

        self.sprite.x -= self.dx

        return collision

    def update_hitbox(self):
        x = self.sprite.x
        y = self.sprite.y
        self.hitbox = {'only' : {'x' : x + self.sprite.width/2, 'y' : y + self.sprite.height/2}}

    def within(self,p1,hitbox):
        return \
        p1['x'] >= hitbox['ll']['x'] and \
        p1['x'] <= hitbox['lr']['x'] and \
        p1['y'] <= hitbox['ul']['y'] and \
        p1['y'] >= hitbox['ll']['y']
