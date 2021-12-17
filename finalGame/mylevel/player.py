#!/usr/bin/python3

# Important Libraries
import pyglet, config
from graphics import *
from pygame import Rect
from pyglet.window import key
import sys
# Our Hero ClassW
class Player:
    def __init__(self, sprites={},buildSprite=None,playerClass="hero",mode="Run",facing="Right",speed=0.05,scale=0.15,loop=True,x=380,y=250):

        # Store the sprites, and the sprite building function
        self.sprites      = sprites
        self.buildSprite  = buildSprite
        self.playerSprite = None

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
        self.debugging = True
        self.attacking = False
        self.attack_start = 0
        self.dead = False
        self.remain_dead = False
        self.threw = False
        self.place_block = 0.0
        self.init_jump = False
        self.hitbox_size = .15*(self.sprites['hero']['Run']['Right'][0].get_image_data().width + self.sprites['hero']['Idle']['Right'][0].get_image_data().width) / 4
        # Build the starting character sprite
        self.changeSprite()

# Build or change the player's Sprite
    def changeSprite(self, mode=None, facing=None, loop=None):
        # Dont bother changing the Sprite if nothing has changed
        if mode != self.mode or facing != self.facing or self.playerSprite is None:

            # Should we change the default loop status (example death)
            if loop is not None:
                self.animationLoop = loop

            # Take in new Modes
            if mode is not None:
                self.mode = mode
            if facing is not None:
                self.facing = facing

            # If the sprite already exists take its x, y coordinates
            if self.playerSprite is not None:
                self.animationX = self.playerSprite.x
                self.animationY = self.playerSprite.y


            # Create a new sprite with the passed in buildSprite function
            self.playerSprite = self.buildSprite(self.sprites,
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
        if key.D in keyTracking.keys() or key   .RIGHT in keyTracking.keys():
            # Make sure velocity is set
            self.dx = 3.0
            caught_input = True

            # Ensure that player is doing the right action
            if not self.mode == 'Run':
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
            if not self.mode == 'Run':
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
            if not self.mode == 'Jump':
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
                level.play_sound('mylevel/music/throw.wav',False)

                if self.facing == 'Right':
                    weaponSpd = 10
                else:
                    weaponSpd = -10
                level.add_item(weaponSpd,0,"weapon",'Kunai',self.facing,self.playerSprite.x,self.playerSprite.y + self.playerSprite.height/2)
        # handle cases:
        #       attacking sequence
        if key.LALT in keyTracking.keys():
            if not self.attacking:
                self.attacking = True
                self.attack_start = t
                level.play_sound('mylevel/music/attack.wav',False)
                self.changeSprite(mode="Attack")

        # Place blocks
        if key.E in keyTracking.keys():
            if t - self.place_block > 2:
                self.place_block = t
                level.add_item(0,0,"block",'Block',self.facing,self.playerSprite.x,self.playerSprite.y + self.playerSprite.height/2)

        if self.attacking:
            for enemy in level.enemies:
                distance_y = abs(self.playerSprite.y - enemy.sprite.y)
                distance_x = self.playerSprite.x - enemy.sprite.x + self.playerSprite.width
                print(f'dx: {distance_x} dy: {distance_y} ')

                if self.facing == 'Right':
                    if distance_x > 0 and distance_x < 30 and distance_y < 50:
                        enemy.dead = True
                elif self.facing == 'Left':
                    if distance_x < 0 and distance_x > -30 and distance_y < 50:
                        enemy.dead = True
            if t - self.attack_start > .41:
                self.attacking = False
                self.changeSprite("Idle",facing=facing,loop=False)
        #       vertical movement
        if self.airborne:
            # Already jumping: update normally
            self.update_position_airborne(level)
            self.playerSprite.y += self.dy
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
        hori_collision = self.will_collide_h(config,level)
        if hori_collision == False:
            self.playerSprite.x += self.dx

        # Handle sprite updates
        if update:
            self.changeSprite(mode,facing,loop)

        # Set idle if no updates
        if not caught_input and not self.attacking and not self.attacking:
            self.changeSprite("Idle",self.facing,True)

    # Draw our character
    def draw(self, t, keyTracking, enemies,config,level,*other):

        self.playerSprite.draw()
        self.check_dead(enemies,config)
        if self.dead:
            print('DEAD')
            self.update_position_airborne(level)
            self.playerSprite.y += self.dy
            if not self.remain_dead:
                self.changeSprite(mode= 'Dead',facing = self.facing,loop = False)
                level.play_sound('mylevel/music/hero_death.wav',False)
                self.remain_dead = True
        elif self.check_win(config):
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
                #self.dy = (self.playerSprite.y + self.playerSprite.height - res[2]['ll']['y']) - .01
                self.dy = -5
                self.jump_x = math.pi + .5
            elif res[0] == 'lower':
                self.dy = -abs(res[2]['ul']['y'] - self.playerSprite.y) + .01
                self.jump_x = (3/2) * math.pi
                self.airborne = False

    def check_collision_vert(self,config,level):
        # Level-specific data
        configLevel,width,height = (config.level,config.width,config.height)


        # Player collision hitbox
        x_pos = self.playerSprite.x
        y_pos = self.playerSprite.y
        player_box = {'ll' : {'x' : x_pos - self.hitbox_size*.8 ,'y' : y_pos},\
                      'lr' : {'x' : x_pos + self.hitbox_size*.8 ,'y' : y_pos},\
                      'ul' : {'x' : x_pos - self.hitbox_size*.8 ,'y' : y_pos + self.playerSprite.height*.85},\
                      'ur' : {'x' : x_pos + self.hitbox_size*.8 ,'y' : y_pos + self.playerSprite.height*.85}
                     }

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
                if self.within(player_box['ul'],hitbox) or self.within(player_box['ur'],hitbox) :
                    return ("upper", player_box['ul'], hitbox)

                # Check hit from below
                if self.within(player_box['ll'], hitbox) or self.within(player_box['lr'],hitbox):
                    return ("lower", player_box['ll'], hitbox)
        for crate in level.objects:
            if crate.playerClass == 'block':
                if self.within(player_box['ll'], crate.hitbox) or self.within(player_box['lr'],crate.hitbox):
                    return ("lower", player_box['ll'], crate.hitbox)
                if self.within(player_box['ul'],crate.hitbox) or self.within(player_box['ur'],crate.hitbox) :
                    return ("upper", player_box['ul'], crate.hitbox)

        return False

    def check_collision_hori(self,config,level):
        # Level-specific data
        configLevel,width,height = (config.level,config.width,config.height)

        # Player collision hitbox
        x_pos = self.playerSprite.x
        y_pos = self.playerSprite.y
        player_box = {
                      'll' : {'x' : x_pos - self.hitbox_size ,'y' : y_pos},                           \
                      'lr' : {'x' : x_pos + self.hitbox_size ,'y' : y_pos},                           \
                      'ml' : {'x' : x_pos - self.hitbox_size ,'y' : y_pos + self.playerSprite.height*.5},\

                      'mr' : {'x' : x_pos + self.hitbox_size ,'y' : y_pos + self.playerSprite.height*.5},\

                      'ul' : {'x' : x_pos - self.hitbox_size ,'y' : y_pos + self.playerSprite.height},\
                      'ur' : {'x' : x_pos + self.hitbox_size ,'y' : y_pos + self.playerSprite.height} \
                     }

        if self.debugging:
            for point in player_box.values():
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
                for point in player_box.keys():
                    if self.within(player_box[point],hitbox):
                        return (point,player_box[point],hitbox)
        for crate in level.objects:
            if crate.playerClass == 'block':
                for point in player_box:
                    if self.within(player_box[point], crate.hitbox) or self.within(player_box[point],crate.hitbox):
                        return (point, player_box[point], crate.hitbox)
                    if self.within(player_box[point],crate.hitbox) or self.within(player_box[point],crate.hitbox) :
                        return (point, player_box[point], crate.hitbox)

        return False

    def will_collide_v(self,config,level):
        self.playerSprite.y += self.dy
        collision = self.check_collision_vert(config,level)
        self.playerSprite.y -= self.dy

        return collision

    def will_collide_h(self,config,level):
        self.playerSprite.x += self.dx
        collision = self.check_collision_hori(config,level)
        self.playerSprite.x -= self.dx

        return collision

    def within(self,p1,hitbox):
        return \
        p1['x'] >= hitbox['ll']['x'] and \
        p1['x'] <= hitbox['lr']['x'] and \
        p1['y'] <= hitbox['ul']['y'] and \
        p1['y'] >= hitbox['ll']['y']

    def check_dead(self,enemies,config):
        level,width,height = (config.level,config.width,config.height)
        delta_x = 0
        delta_y = 0
        if self.playerSprite.y < 0 :
            self.dead = True
            return True

        # Player collision parametrics
        x_pos = self.playerSprite.x + delta_x
        y_pos = self.playerSprite.y + delta_y

        player_box = {'ll' : {'x' : x_pos - self.hitbox_size ,'y' : y_pos},\
                      'lr' : {'x' : x_pos + self.hitbox_size ,'y' : y_pos},\
                      'ul' : {'x' : x_pos - self.hitbox_size ,'y' : y_pos + self.playerSprite.height},\
                      'ur' : {'x' : x_pos + self.hitbox_size ,'y' : y_pos + self.playerSprite.height}
                     }

        if self.debugging:
            for point in player_box.values():
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

            for point in player_box.keys():
                if self.within(player_box[point],hitbox):
                    self.dead = True
                    return True

        return False

    def check_win(self,config):
        x_pos = self.playerSprite.x
        y_pos = self.playerSprite.y
        player_box = {'ll' : {'x' : x_pos - self.hitbox_size*.8 ,'y' : y_pos},\
                      'lr' : {'x' : x_pos + self.hitbox_size*.8 ,'y' : y_pos},\
                      'ul' : {'x' : x_pos - self.hitbox_size*.8 ,'y' : y_pos + self.playerSprite.height*.85},\
                      'ur' : {'x' : x_pos + self.hitbox_size*.8 ,'y' : y_pos + self.playerSprite.height*.85}
                     }
        for y in config.goals:
            for x in config.goals[y]:
                width = config.goals[y][x].width * self.animationScale
                height = config.goals[y][x].height * self.animationScale
                print(width)
                box = {
                             'll' : {'x' : x * config.width            ,'y' : y * config.height},                           \
                             'lr' : {'x' : x * config.width + width    ,'y' : y * config.height},                           \

                             'ul' : {'x' : x * config.width            ,'y' : y * config.height + height},\
                             'ur' : {'x' : x * config.width + width    ,'y' : y * config.height + height}
                            }
                print(f'{box["ll"]} : {box["lr"]} : {box["ul"]} : {box["ur"]}')
                for point in box.keys():
                    if self.within(player_box[point],box):
                        return True

        return False
