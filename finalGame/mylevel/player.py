#!/usr/bin/python3

# Important Libraries
import pyglet, config, math
from pyglet.window import key
import sys
import time
# Our Hero ClassW
class Player:
    def __init__(self, sprites={},buildSprite=None,playerClass="hero",mode="Run",facing="Right",speed=0.05,scale=0.15,loop=True,x=380,y=250):

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
        self.Loop           = False


        # udpated items
        self.airborne = False
        self.dx = 0
        self.dy = 0
        self.jump_x = (3 / 2) * math.pi
        self.step = .1
        self.debugging = False
        self.attacking = False
        self.attack_start = 0
        self.dead = False
        self.remain_dead = False
        self.threw = False
        self.place_block = 0.0
        self.init_jump = False
        self.hitbox_size = .15*(self.sprites['hero']['Run']['Right'][0].get_image_data().width + self.sprites['hero']['Idle']['Right'][0].get_image_data().width) / 4

        # power ups
        self.set_invincible_time    = 0.0
        self.invincible             = False
        self.invincible_duration    = 17.0
        self.kills                  = 0
        self.changeSprite()

        self.hitbox = {'ll' : {'x' :x - self.hitbox_size ,'y' : y},\
                       'lr' : {'x' : x + self.hitbox_size ,'y' : y},\
                       'ul' : {'x' : x - self.hitbox_size ,'y' : y + self.sprite.height},\
                       'mr' : {'x' : x + self.hitbox_size ,'y' : y + self.sprite.height/2},\
                       'ml' : {'x' : x - self.hitbox_size ,'y' : y + self.sprite.height/2},\
                       'ur' : {'x' : x + self.hitbox_size ,'y' : y + self.sprite.height}
                     }
        # Build the starting character sprite

# Build or change the player's Sprite
    def changeSprite(self, mode=None, facing=None, loop=None):
        # Dont bother changing the Sprite if nothing has changed
        if mode != self.mode or facing != self.facing or self.sprite is None:

            # Should we change the default loop status (example death)
            if loop is not None:
                self.animationLoop = loop

            # Take in new Modes
            if mode is not None:
                self.mode = mode
            if facing is not None:
                self.facing = facing

            # If the sprite already exists take its x, y coordinates
            if self.sprite is not None:
                self.animationX = self.sprite.x
                self.animationY = self.sprite.y


            # Create a new sprite with the passed in buildSprite function
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
    def movement(self, config, t, keyTracking,level):
        # booleans set
        update, caught_input, self.dx,self.init_jump = (False, False, 0.0, False)
        mode,facing,loop = (self.mode,self.facing,True)

        # Check all key presses
        # RIGHT
        if key.D in keyTracking.keys() or key.RIGHT in keyTracking.keys():
            # Make sure velocity is set
            self.dx = 3.0
            caught_input = True

            # Ensure that player is doing the right action
            if not self.mode == 'Run' and not self.attacking:
                mode = 'Run'
                update = True
            if not self.facing == 'Right':
                facing = 'Right'
                update = True
        # LEFT
        if key.A in keyTracking.keys() or key.LEFT in keyTracking.keys():
            # Make sure velocity is set
            self.dx = -3.0
            caught_input = True

            # Ensure that player is doing the right action
            if not self.mode == 'Run' and not self.attacking:
                mode = 'Run'
                update = True
            if not self.facing == 'Left':
                facing = 'Left'
                update = True
        # RUN
        if key.LSHIFT in keyTracking.keys():
            self.dx *= 2
        # JUMP
        if key.W in keyTracking.keys() or key.SPACE in keyTracking.keys() or key.UP in keyTracking.keys():
            caught_input = True
            if not self.mode == 'Jump' and not self.attacking:
                mode = 'Jump'
                self.update = True
            if not self.airborne:
                level.play_sound('mylevel/music/jump.wav',False)
                self.jump_x = (1 / 2) * math.pi
                self.init_jump = True
                self.airborne = True

        if key.LCTRL in keyTracking.keys():
            if not self.threw:
                self.threw = True
                self.changeSprite(mode='Throw')
                update = False
                level.play_sound('mylevel/music/throw.wav',False)

                if self.facing == 'Right':
                    weaponSpd = 10
                else:
                    weaponSpd = -10
                level.add_item(weaponSpd,0,"weapon",'Kunai',self.facing,self.sprite.x,self.sprite.y + self.sprite.height/2)
        # handle cases:
        #       attacking sequence
        if key.LALT in keyTracking.keys():
            if not self.attacking:
                self.attacking = True
                update = False

                self.attack_start = t
                level.play_sound('mylevel/music/attack.wav',False)
                self.changeSprite(mode="Attack")

        # Place blocks
        if key.E in keyTracking.keys():
            if t - self.place_block > 2:
                self.place_block = t
                level.add_item(0,0,"block",'Block',self.facing,self.sprite.x,self.sprite.y + self.sprite.height/2)

        if self.attacking:
            for enemy in level.enemies:
                if enemy.dead:
                    continue
                distance_y = abs(self.sprite.y - enemy.sprite.y)
                if self.facing == 'Right':
                    distance_x = abs(self.hitbox['lr']['x'] - enemy.hitbox['ll']['x'])
                    if distance_x < 50 and distance_y < 100:
                        enemy.dead = True
                        enemy.died_at = time.time()
                        self.kills += 1
                        level.score += 200
                        self.attacking = False
                elif self.facing == 'Left':
                    distance_x = abs(self.hitbox['ll']['x'] - enemy.hitbox['lr']['x'])
                    if distance_x < 50 and distance_y < 100:
                        enemy.dead = True
                        enemy.died_at = time.time()
                        self.kills += 1
                        level.score += 200
                        self.attacking = False
            if t - self.attack_start > .41:
                self.attacking = False
                self.changeSprite("Idle",facing=facing,loop=False)
        #       vertical movement
        if self.airborne:
            # Already jumping: update normally
            self.update_position_airborne(level)
            self.sprite.y += self.dy
        else:
            # Check if theres ground below us:
            self.dy = -1
            vert_collision = self.will_collide_v(config,level)
            self.dy = 0
            # If nothing, then were falling
            if vert_collision == False:
                self.jump_x = ((3/2)*math.pi)-1.5
                self.airborne = True

        # Handle x movement
        if self.invincible:
            self.dx*= 1.3
        hori_collision = self.will_collide_h(config,level)
        if hori_collision == False:
            self.sprite.x += self.dx

        # Handle sprite updates
        if update:
            self.changeSprite(mode,facing,loop)

        # Set idle if no updates
        if not caught_input and not self.attacking and not self.attacking:
            self.changeSprite("Idle",self.facing,True)

    # Draw our character
    def draw(self, t, keyTracking, enemies,config,level,*other):
        self.update_hitbox()
        self.sprite.draw()
        self.check_dead(enemies,config)
        if self.dead:
            print('DEAD')
            self.update_position_airborne(level)
            self.sprite.y += self.dy
            if not self.remain_dead:
                self.changeSprite(mode= 'Dead',facing = self.facing,loop = False)
                level.play_sound('mylevel/music/hero_death.wav',False)
                self.remain_dead = True
        elif self.check_win(config,):
            level.level_won = True
            print("WON")

        else:
            self.movement(config, t, keyTracking,level)

    # A bunch of fun lil funtions that were
    # The death of me.... :)
    def update_position_airborne(self,level):
        #find the next x_coordinate for our jump
        if self.jump_x >= 3 * (math.pi/2.0):
            self.jump_x = 3 * (math.pi/2.0)
        else:
            self.jump_x += self.step

        # still tuning this parameter
        self.dy = 12*math.sin(self.jump_x)
        # Handle if the next update will be a collision
        if ((res := self.will_collide_v(config,level)) != False) and not self.init_jump:
            if res[0] == 'upper':
                #self.dy = res[2]['ll']['y'] - res[1]['y'] - .01
                #self.dy = (self.sprite.y + self.sprite.height - res[2]['ll']['y']) - .01
                self.dy = -5
                self.jump_x = math.pi + .5
            elif res[0] == 'lower':
                self.dy = -abs(res[2]['ul']['y'] - self.sprite.y) + .01
                self.jump_x = (3/2) * math.pi
                self.airborne = False

    def check_collision_vert(self,config,level):
        # Level-specific data
        configLevel,width,height = (config.level,config.width,config.height)

        # Check all terrain boxes
        for row in configLevel.keys():
            for col in configLevel[row]:

                # Terrain collision hitbox
                x,y = col*width , row*height
                ll = {'x' :     x           ,'y' :   y              }
                lr = {'x' :     x + width   ,'y' :   y              }
                ul = {'x' :     x           ,'y' :   y + height     }
                ur = {'x' :     x + width   ,'y' :   y + height     }
                hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

                # Check hit from above
                if self.within(self.hitbox['ul'],hitbox) or self.within(self.hitbox['ur'],hitbox) :
                    return ("upper", self.hitbox['ul'], hitbox)

                # Check hit from below
                if self.within(self.hitbox['ll'], hitbox) or self.within(self.hitbox['lr'],hitbox):
                    return ("lower", self.hitbox['ll'], hitbox)
        for crate in level.objects:
            if crate.playerClass == 'block':
                if self.within(self.hitbox['ll'], crate.hitbox) or self.within(self.hitbox['lr'],crate.hitbox):
                    return ("lower", self.hitbox['ll'], crate.hitbox)
                if self.within(self.hitbox['ul'],crate.hitbox) or self.within(self.hitbox['ur'],crate.hitbox) :
                    return ("upper", self.hitbox['ul'], crate.hitbox)

        return False

    def check_collision_hori(self,config,level):
        # Level-specific data
        configLevel,width,height = (config.level,config.width,config.height)


        if self.debugging:
            for point in self.hitbox.values():
                color = (255,0,0)
                pyglet.shapes.Circle(point['x'],point['y'], 2, color = color).draw()


        # Terrain collision hitbox
        for row in configLevel.keys():
            for col in configLevel[row]:

                # Terrain collision hitbox
                x,y = col*width  , row*height
                ll = {'x' : x,          'y' : y}
                lr = {'x' : x + width,  'y' : y}
                ul = {'x' : x,          'y' : y + height}
                ur = {'x' : x + width,  'y' : y + height}
                hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

                # Check collision with wall
                for point in self.hitbox.keys():
                    if self.within(self.hitbox[point],hitbox):
                        return (point,self.hitbox[point],hitbox)
        for crate in level.objects:
            if crate.playerClass == 'block':
                for point in self.hitbox:
                    if self.within(self.hitbox[point], crate.hitbox) or self.within(self.hitbox[point],crate.hitbox):
                        return (point, self.hitbox[point], crate.hitbox)
                    if self.within(self.hitbox[point],crate.hitbox) or self.within(self.hitbox[point],crate.hitbox) :
                        return (point, self.hitbox[point], crate.hitbox)

        return False

    def will_collide_v(self,config,level):
        self.sprite.y += self.dy
        self.update_hitbox()
        collision = self.check_collision_vert(config,level)
        self.sprite.y -= self.dy
        self.update_hitbox()

        return collision

    def will_collide_h(self,config,level):
        self.sprite.x += self.dx
        self.update_hitbox()
        collision = self.check_collision_hori(config,level)
        self.sprite.x -= self.dx
        self.update_hitbox()

        return collision

    def within(self,p1,hitbox):
        return \
        p1['x'] >= hitbox['ll']['x'] and \
        p1['x'] <= hitbox['lr']['x'] and \
        p1['y'] <= hitbox['ul']['y'] and \
        p1['y'] >= hitbox['ll']['y']

    def check_dead(self,enemies,config):
        if self.set_invincible:
            if time.time() - self.set_invincible_time > self.invincible_duration:
                self.invincible= False
            else:
                return False

        level,width,height = (config.level,config.width,config.height)
        if self.sprite.y < 0 :
            self.dead = True
            return True

        if self.debugging:
            for point in self.hitbox.values():
                color = (0,0,0)
                pyglet.shapes.Circle(point['x'],point['y'], 2, color = color).draw()

        # Terrain collision parametrics
        for enemy in enemies:
            if enemy.dead : continue
            x,y = enemy.sprite.x,enemy.sprite.y
            height = enemy.sprite.height
            width = enemy.sprite.width

            ll = {'x' : x - width/3 - 10,          'y' : y -5}
            lr = {'x' : x + width/3 + 10,          'y' : y -5}
            ul = {'x' : x - width/3 - 10,          'y' : y + height - 20}
            ur = {'x' : x + width/3 + 10,          'y' : y + height - 20}

            hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

            if self.debugging:
                for combo in hitbox.values():
                    pyglet.shapes.Circle(combo['x'],combo['y'], 2, color = (0,0,0)).draw()

            for point in self.hitbox.keys():
                if self.within(self.hitbox[point],hitbox):
                    self.dead = True
                    return True

        return False

    def update_hitbox(self):
        x = self.sprite.x
        y = self.sprite.y
        self.hitbox = {'ll' : {'x' :x - self.hitbox_size * 0.8 ,'y' : y},\
                       'lr' : {'x' : x + self.hitbox_size * 0.8 ,'y' : y},\
                       'ul' : {'x' : x - self.hitbox_size * 0.8 ,'y' : y + self.sprite.height},\
                       'mr' : {'x' : x + self.hitbox_size * 0.8 ,'y' : y + self.sprite.height/2},\
                       'ml' : {'x' : x - self.hitbox_size * 0.8 ,'y' : y + self.sprite.height/2},\
                       'ur' : {'x' : x + self.hitbox_size * 0.8 ,'y' : y + self.sprite.height}
                     }

    def set_invincible(self):
        self.set_invincible_time = time.time()
        self.invincible= True

    def check_win(self,config):
        for y in config.goals:
            for x in config.goals[y]:
                width = config.goals[y][x].width * self.animationScale
                height = config.goals[y][x].height * self.animationScale
                box = {
                             'll' : {'x' : x * config.width            ,'y' : y * config.height},                           \
                             'lr' : {'x' : x * config.width + width    ,'y' : y * config.height},                           \

                             'ul' : {'x' : x * config.width            ,'y' : y * config.height + height},\
                             'ur' : {'x' : x * config.width + width    ,'y' : y * config.height + height}
                            }
                for point in box.keys():
                    if self.within(self.hitbox[point],box):
                        return True

        return False
