#!/usr/bin/python3

# Important Libraries
import config, numpy

# Import the Main Player Class
from player import Player

# The Enemy is a type of Player, use all of the Player's Defaults
class Enemy(Player):

    # Our Enemy's new movement function, lets just go back and forth
    def movement(self, t=0, dt=0, *other):

        # Our initial proposed change in position
        delta_xy = numpy.array([0.0, -1.0, 0.0])

        # Handle Walking and Running inputs from the game player
        # This is just a simplified version from the normal Player Class
        if 'Right' == self.facing and not self.death:
            delta_xy[0] = self.walkMetersPerSecond * self.pixelsPerMeter * dt
        elif 'Left' == self.facing and not self.death:
            delta_xy[0] = -self.walkMetersPerSecond * self.pixelsPerMeter * dt

        # Ensure that the max change in x or change in y is 1 less than
        # config.height and config.width, This prevents us from flying
        # through the terrain...
        delta_xy = self.constrainMovement(delta_xy)

        # Calculate the new position of the player based on adding
        # the delta to the old position
        proposed_xy = numpy.array([self.playerSprite.x, self.playerSprite.y, 0.0]) + delta_xy

        # Run the terrain collisions function against the new proposed x,y coordinates
        proposed_xy[0], proposed_xy[1], impact_x, impact_y = self.terrainCollisions(proposed_xy[0],
                                                                                    proposed_xy[1],
                                                                                    self.playerSprite.x,
                                                                                    self.playerSprite.y,
                                                                                    config.level)

        # If we successfully moved in the y, then we must be falling.
        # If we are falling or hit something in x, then turn around and move
        # a bit in the oposite direction.
        if proposed_xy[1] != self.playerSprite.y or impact_x:
            delta_xy = [-2.0 * delta_xy[0], 0.0, 0.0]
            proposed_xy = numpy.array([self.playerSprite.x, self.playerSprite.y, 0.0]) + delta_xy
            if self.facing == 'Left':
                self.changeSprite('Run', 'Right', True)
                self.facing = 'Right'
            else:
                self.changeSprite('Run', 'Left', True)
                self.facing = 'Left'

        # Update the sprites position
        self.playerSprite.x = proposed_xy[0]
        self.playerSprite.y = proposed_xy[1]
