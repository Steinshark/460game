#!/usr/bin/python3

# Important Libraries
import pyglet, config
import time
from graphics import *
# Our Hero Class
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
        self.grounded = True

        self.P_0 = Point3D(float(x),float(y),0.0)
        self.V_0 = Vector3D(0.0,0.0,0.0)

        self.t_0   = 0.0
        self.a = Vector3D(0.0,0.0,0.0)
        # Build the starting character sprite
        self.changeSprite()

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
    def movement(self, t=0, keyTracking={}):
        update = False
        update_movement = False
        if 119 in keyTracking.keys():
            self.t_0 = t
            self.P_0 = self.position

        if 100 in keyTracking.keys():
            if not self.airborne:
                self.V_0 = Vector3D(3.0,0.0,0.0)
                update_movement = True
            if not self.mode == 'Run':
                self. mode = 'Run'
                update = True
            if not self.facing == 'Right':
                self.facing = 'Right'
                update = True

        elif 97 in keyTracking.keys():
            if not self.airborne:
                self.V_0 = Vector3D(3.0,0.0,0.0)
                update_movement = True
            if not self.mode == 'Run':
                self. mode = 'Run'
                update = True
            if not self.facing == 'Left':
                self.facing = 'Left'
                update = True

        elif not 100 in keyTracking.keys() and not 97 in keyTracking.keys():
            self.mode = 'Idle'
        self.update_position(t - self.t_0)

        if update:
            self.changeSprite()
        if not update_movement:
            self.V_0 = Vector3D(0.0,0.0,0.0)
        print(t - self.t_0)

    # Draw our character
    def draw(self, t=0, keyTracking={}, *other):
        self.movement(t, keyTracking)
        self.playerSprite.draw()
    # Update the character parametrically
    def update_position(self,t=0):
        vect1 = self.P_0 + (self.V_0 * t)
        vect_a = self.a * 0.5 * (t ** 2)
        vect2 = vect1 + vect_a
        self.position = vect2
        print(self.position)
