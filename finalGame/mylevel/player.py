#!/usr/bin/python3

# Important Libraries
import pyglet, config
from graphics import *
from pygame import Rect
from pyglet.window import key
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
        # Movement items
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
        # Build the starting character sprite
        self.changeSprite()

# Build or change the player's Sprite
    def changeSprite(self, mode=None, facing=None, loop=None):


        # Dont bother changing the Sprite if nothing has changed
        if mode != self.mode or facing != self.facing or self.playerSprite is None:
            print(mode)
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
    def movement(self, config, t=0, keyTracking={},level=None):

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
        if key.SPACE in keyTracking.keys() or key.W in keyTracking.keys() or key.UP in keyTracking.keys():
            caught_input = True
            if not self.mode == 'Jump':
                mode = 'Jump'
                self.update = True
            if not self.airborne:
                self.jump_x = (1 / 2) * math.pi
                self.init_jump = True
                self.airborne = True

        if key.LALT in keyTracking.keys():
            if not self.attacking:
                self.attack_start = t
                self.attacking = True;
                self.changeSprite("Attack",self.facing,False)

        if key.LCTRL in keyTracking.keys():
            if not self.threw:
                self.threw = True
                if self.facing == 'Right':
                    weaponSpd = 3
                else:
                    weaponSpd = -3
                level.add_item(weaponSpd,0,"weapon",'Kunai',self.facing,self.playerSprite.x,self.playerSprite.y + self.playerSprite.height/2)
        # handle cases:
        #       attacking sequence
        if self.attacking:
            if t - self.attack_start > .41:
                self.attacking = False
                self.changeSprite("Idle",self.facing,True)
        #       vertical movement
        if self.airborne:
            # Already jumping: update normally
            self.update_position_airborne()
            self.playerSprite.y += self.dy
        else:
            # Check if theres ground below us:
            self.dy = -1
            vert_collision = self.will_collide_v(config)
            self.dy = 0
            # If nothing, then were falling
            if vert_collision == False:
                self.jump_x = ((3/2)*math.pi)-1.5
                self.airborne = True

        # Handle x movement
        hori_collision = self.will_collide_h(config)
        if hori_collision == False:
            self.playerSprite.x += self.dx

        # Handle sprite updates
        if update:
            self.changeSprite(mode,facing,loop)
        if not caught_input:
            self.changeSprite("Idle",self.facing,True)

        if self.debugging:
            print(['Px\t','Py\t','dx\t','dy\t'])
            print([self.playerSprite.x,self.playerSprite.y,self.dx,self.dy])
            print()

    # Draw our character
    def draw(self, t=0, keyTracking={}, config=None,enemies=None,level=None,*other):
        self.playerSprite.draw()
        self.check_dead(enemies,config)
        if self.dead:
            print('DEAD')
            if not self.remain_dead:
                self.changeSprite(mode= 'Dead',facing = self.facing,loop = False)

        else:
            self.movement(config, t=t, keyTracking=keyTracking,level=level)

    # A bunch of fun lil funtions that were
    # The death of me.... :)
    def update_position_airborne(self):
        #find the next x_coordinate for our jump
        if self.jump_x >= 3 * (math.pi/2.0):
            self.jump_x = 3 * (math.pi/2.0)
        else:
            self.jump_x += self.step

        # still tuning this parameter
        self.dy = 17*math.sin(self.jump_x)

        # Handle if the next update will be a collision
        if ((res := self.will_collide_v(config)) != False) and not self.init_jump:
            if res[0] == 'upper':
                self.dy = res[2]['ll']['y'] - res[1]['y'] - .01
                self.jump_x = math.pi + .5
            elif res[0] == 'lower':
                self.dy = -abs(res[2]['ul']['y'] - self.playerSprite.y) + .01
                self.jump_x = (3/2) * math.pi
                self.airborne = False

    def check_collision_vert(self,config):
        # Level-specific data
        level,width,height = (config.level,config.width,config.height)
        delta_x = 0
        delta_y = 0

        # Player collision hitbox
        x_pos = self.playerSprite.x + delta_x
        y_pos = self.playerSprite.y + delta_y
        player_line = {'bot' : {'x' : x_pos,'y' : y_pos},\
                       'top' : {'x' : x_pos,'y' : y_pos + ( self.playerSprite.height)}}

        # Check all terrain boxes
        for row in level.keys():
            for col in level[row]:

                # Terrain collision hitbox
                x,y = col*width + delta_x , row*height + delta_y
                ll = {'x' :     x           ,'y' :   y              }
                lr = {'x' :     x + width   ,'y' :   y              }
                ul = {'x' :     x           ,'y' :   y + height     }
                ur = {'x' :     x + width   ,'y' :   y + height     }
                hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

                # Check hit from above
                if self.within(player_line['top'],hitbox):
                    return ("upper", player_line['top'], hitbox)

                # Check hit from below
                if self.within(player_line['bot'], hitbox):
                    return ("lower", player_line['bot'], hitbox)

        return False

    def check_collision_hori(self,config):
        # Level-specific data
        level,width,height = (config.level,config.width,config.height)
        delta_x = 0
        delta_y = 0

        # Player collision hitbox
        x_pos = self.playerSprite.x + delta_x
        y_pos = self.playerSprite.y + delta_y
        player_box = {
                      'll' : {'x' : x_pos - self.playerSprite.width / 2 ,'y' : y_pos},                           \
                      'lr' : {'x' : x_pos + self.playerSprite.width / 2 ,'y' : y_pos},                           \
                      'ul' : {'x' : x_pos - self.playerSprite.width / 2 ,'y' : y_pos + self.playerSprite.height},\
                      'ur' : {'x' : x_pos + self.playerSprite.width / 2 ,'y' : y_pos + self.playerSprite.height} \
                     }

        # Terrain collision hitbox
        for row in level.keys():
            for col in level[row]:

                # Terrain collision hitbox
                x,y = col*width + delta_x , row*height + delta_y
                ll = {'x' : x,          'y' : y}
                lr = {'x' : x + width,  'y' : y}
                ul = {'x' : x,          'y' : y + height}
                ur = {'x' : x + width,  'y' : y + height}
                hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

                # Check collision with wall
                for point in player_box.keys():
                    if self.within(player_box[point],hitbox):
                        return (point,player_box[point],hitbox)
        return False

    def will_collide_v(self,config):
        self.playerSprite.y += self.dy

        collision = self.check_collision_vert(config)

        self.playerSprite.y -= self.dy

        return collision

    def will_collide_h(self,config):
        self.playerSprite.x += self.dx

        collision = self.check_collision_hori(config)

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
        if self.playerSprite.y < 0 or self.playerSprite.y > 600 : return True

        # Player collision parametrics
        x_pos = self.playerSprite.x + delta_x
        y_pos = self.playerSprite.y + delta_y

        player_box = {'ll' : {'x' : x_pos - self.playerSprite.width / 2 ,'y' : y_pos},\
                      'lr' : {'x' : x_pos + self.playerSprite.width / 2 ,'y' : y_pos},\
                      'ul' : {'x' : x_pos - self.playerSprite.width / 2 ,'y' : y_pos + self.playerSprite.height},\
                      'ur' : {'x' : x_pos + self.playerSprite.width / 2 ,'y' : y_pos + self.playerSprite.height}
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

            ll = {'x' : x - width/3,          'y' : y}
            lr = {'x' : x + width/3,          'y' : y}
            ul = {'x' : x - width/3,          'y' : y + height - 20}
            ur = {'x' : x + width/3,          'y' : y + height - 20}

            hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

            if self.debugging:
                for combo in hitbox.values():
                    pyglet.shapes.Circle(combo['x'],combo['y'], 2, color = (0,0,0)).draw()

            for point in player_box.keys():
                if self.within(player_box[point],hitbox):
                    self.dead = True
                    return True

        return False
