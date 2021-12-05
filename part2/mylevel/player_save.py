#!/usr/bin/python3

# Important Libraries
import pyglet, config
from graphics import *
from pygame import Rect
# Our Hero ClassW
class Player:
    def __init__(self, sprites={},
                       buildSprite=None,
                       playerClass="hero",
                       mode="Run",
                       facing="Right",
                       speed=0.05,
                       scale=0.15,
                       loop=True,
                       x=380,
                       y=250):

        # Store the sprites, and the sprite building function
        self.sprites      = sprites
        self.buildSprite  = buildSprite
        self.playerSprite = None


        # Some basic settings
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop  = loop
        self.animationX     = x
        self.animationY     = y
        self.playerClass    = playerClass
        self.mode           = mode
        self.facing         = facing

        # Movement items
        self.airborne = False

        self.P_0 = Point3D(float(x),float(y)+20,0.0)
        self.position = self.P_0
        self.V_0 = Vector3D(0.0,0.0,0.0)

        self.t_0   = 0.0
        self.a = Vector3D(0.0,0.0,0.0)
        self.dx = 0
        self.dy = 0
        self.jump_x = math.pi / 2
        self.step = .1
        self.jumping_x = 0.0
        self.grounded = True
        # Build the starting character sprite
        self.changeSprite()

        self.hitbox_terrain = [[self.playerSprite.x + .5*self.playerSprite.width,  self.playerSprite.y],\
                                [self.playerSprite.x + .5*self.playerSprite.width,  self.playerSprite.y + .75*self.playerSprite.height]]



    # Build the initial character
    def changeSprite(self, mode=None, facing=None):
        if mode is not None:
            self.mode = mode
        if facing is not None:
            self.facing = facing
        if self.playerSprite is not None:
            self.animationX = self.playerSprite.x
            self.animationY = self.playerSprite.y
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
    def movement(self, config, t=0, keyTracking={}):
        # booleans set

        update = False
        update_movement = False
        self.dx = 0.0
        # Debug
        print(['x','y'])
        print(["%.3f" % self.playerSprite.x,"%.3f" % self.playerSprite.y])

        # Check all key presses
        # D
        if 100 in keyTracking.keys():
            # Make sure velocity is set
            self.dx = 3.0
            if not self.airborne:
                update_movement = True

            # Ensure that player is doing the right action
            if not self.mode == 'Run':
                self.mode = 'Run'
                update = True
            if not self.facing == 'Right':
                self.facing = 'Right'
                update = True
        # A
        if 97 in keyTracking.keys():
            # Make sure velocity is set
            self.dx = -3.0
            if not self.airborne:
                update_movement = True

            # Ensure that player is doing the right action
            if not self.mode == 'Run':
                self. mode = 'Run'
                update = True
            if not self.facing == 'Left':
                self.facing = 'Left'
                update = True
        # SHIFT
        if 65505 in keyTracking.keys():
            if not self.airborne:
                self.dx *= 3
        # W
        if 119 in keyTracking.keys():
            self.t_0 = t
            self.P_0 = self.position
            self.airborne = True


        self.collision = self.check_collision_vert(config)
        self.hori_collision = self.check_collision_hori(config)

        if not self.hori_collision == False:
            pass
        # if jumping
        if self.airborne:

            # if not colliding with anything, update jump as normal
            if self.collision == False:
                self.update_position_airborne(t=t)
                pass

            # else, get information on collision
            else:
                direction, player_hitpoint, hitbox = self.collision

                # if collision from top, then set the player to falling
                if direction == 'upper':
                    self.playerSprite.y = hitbox['ll']['y']-0.001 - self.playerSprite.height
                    self.jump_x = math.pi + .5

                # else if collision from bottom, determine if this is
                # landing or launching
                elif direction == 'lower':

                    # if we are launching, then update the position
                    # and set ground to False
                    if self.grounded:
                        self.update_position_airborne(t=t)
                        self.grounded = False

                    # if not grounded, then we are landing
                    # so reset all jumping parametrics
                    else:
                        self.playerSprite.y = hitbox['ur']['y']
                        self.airborne = False
                        self.grounded = True
                        self.dy = 0
                        self.jump_x = math.pi/2

        # check for collision with wall
        else:
            if self.collision == False:
                self.airborne = True
                self.grounded = False
                self.jump_x = (3*math.pi/2)



        if update:
            self.changeSprite()

        if update_movement or self.airborne:
            self.playerSprite.x += self.dx
            self.playerSprite.y += self.dy

        else:
            self.mode = 'Idle'
            self.P_0 = self.position
            self.changeSprite()


        #self.update_position(t - self.t_0)

    # Draw our character
    def draw(self, t=0, keyTracking={}, config=None,*other):
        self.movement(config, t, keyTracking)
        self.playerSprite.draw()

    def update_position_airborne(self,t=0):
        if self.jump_x >= 3 * (math.pi/2.0):
            self.jump_x = 3 * (math.pi/2.0)
        else:
            self.jump_x += self.step

        y = math.sin(self.jump_x)
        #y_1 = math.sin((self.jump_x-self.step))

        self.dy = 17*y
        print(['X', 'DY'])
        print([self.jump_x,self.dy])

    def check_collision_vert(self,config):
        level,width,height = (config.level,config.width,config.height)
        delta_x = 0
        delta_y = 0

        # Player collision parametrics
        x_pos = (self.playerSprite.x + 0*self.playerSprite.width/2) + delta_x
        y_pos = self.playerSprite.y + delta_y
        player_line = {'bot' : {'x' : x_pos,'y' : y_pos},\
                       'top' : {'x' : x_pos,'y' : y_pos + 0.75 * self.playerSprite.height}}

        for point in player_line.values():
            color = (0,0,0)
            if point == player_line['top']:
                color = (250,50,50)
            pyglet.shapes.Circle(point['x'],point['y'], 2, color = color).draw()

        # Terrain collision parametrics
        for row in level.keys():
            for col in level[row]:
                img = level[row][col]
                x,y = col*width + delta_x , row*height + delta_y
                ll = {'x' : x,          'y' : y}
                lr = {'x' : x + width,  'y' : y}
                ul = {'x' : x,          'y' : y + height}
                ur = {'x' : x + width,  'y' : y + height}
                hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

                color = [(255,0,0),(0,255,0),(0,0,255),(0,0,0)]
                i = 0
                for combo in hitbox.values():
                    colors = color[i]
                    pyglet.shapes.Circle(combo['x'],combo['y'], 2, color = colors).draw()
                    i += 1
                # Check hit from above
                if self.within(player_line['top'],hitbox):

                #if  player_line['top']['x'] >= hitbox['ll']['x'] and \
                #    player_line['top']['x'] <= hitbox['lr']['x'] and \
                #    player_line['top']['y'] <= hitbox['ul']['y'] and \
                #    player_line['top']['y'] >= hitbox['ll']['y']:

                    return ("upper", player_line['top'], hitbox)

                if self.within(player_line['bot'], hitbox):
                    for combo in hitbox.values():
                        pyglet.shapes.Circle(combo['x'],combo['y'], 2, color = (0,0,0)).draw()
                    return ("lower", player_line['bot'], hitbox)

        return False

    def check_collision_hori(self,config):
        level,width,height = (config.level,config.width,config.height)
        delta_x = 0
        delta_y = 0

        # Player collision parametrics
        x_pos = self.playerSprite.x + delta_x
        y_pos = self.playerSprite.y + delta_y

        player_box = {'ll' : {'x' : x_pos - self.playerSprite.width / 2 ,'y' : y_pos},\
                      'lr' : {'x' : x_pos + self.playerSprite.width / 2 ,'y' : y_pos},\
                      'ul' : {'x' : x_pos - self.playerSprite.width / 2 ,'y' : y_pos + self.playerSprite.height},\
                      'ur' : {'x' : x_pos + self.playerSprite.width / 2 ,'y' : y_pos + self.playerSprite.height}
                     }

        for point in player_box.values():
            color = (0,0,0)
            pyglet.shapes.Circle(point['x'],point['y'], 2, color = color).draw()

        # Terrain collision parametrics
        for row in level.keys():
            for col in level[row]:
                img = level[row][col]
                x,y = col*width + delta_x , row*height + delta_y
                ll = {'x' : x,          'y' : y}
                lr = {'x' : x + width,  'y' : y}
                ul = {'x' : x,          'y' : y + height}
                ur = {'x' : x + width,  'y' : y + height}
                hitbox = {'ll' : ll ,'lr' : lr ,'ul' : ul ,'ur' : ur}

                color = [(255,0,0),(0,255,0),(0,0,255),(0,0,0)]
                i = 0
                for combo in hitbox.values():
                    colors = color[i]
                    pyglet.shapes.Circle(combo['x'],combo['y'], 2, color = colors).draw()
                    i += 1

                for point in player_box.keys():
                    if self.within(player_box[point],hitbox):
                        return (point,player_box[point],hitbox)

        return False


    def within(self,p1,hitbox):
        return \
        p1['x'] >= hitbox['ll']['x'] and \
        p1['x'] <= hitbox['lr']['x'] and \
        p1['y'] <= hitbox['ul']['y'] and \
        p1['y'] >= hitbox['ll']['y']
