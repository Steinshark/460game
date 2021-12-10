#!/usr/bin/python3

# Important Libraries
import config, numpy

# Our Hero Class
class Player:

    # Build our Player, defaults as listed below:
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
        self.playerSprite   = None
        self.sprites        = sprites
        self.buildSprite    = buildSprite

        # Some basic settings (for the sprites) that are passed in with the class
        self.playerClass    = playerClass
        self.mode           = mode
        self.facing         = facing
        self.animationSpeed = speed
        self.animationScale = scale
        self.animationLoop  = loop
        self.animationX     = x
        self.animationY     = y

        # Additional Status Effects (death, HP, MP, etc...)
        self.death          = False

        # Jumping / Falling information (set later when the player actually jumps or falls)
        self.falling        = False       # Is our player falling at this point
        self.fallingTime    = 0.0         # time (worldTime) when we started to fall
        self.fallingPos     = 0.0         # Our Y position when we started to fall/jump
        self.fallingX       = 0.0         # Our X velcity when we started to fall/jump
        self.jumpVelocity   = 0.0         # Our initial velocity (v0) for our particle equation

        # Basic Game Physics Settings
        self.pixelsPerMeter      =  40.0  # How many pixels are in a meter        (based on your graphics design)
        self.walkMetersPerSecond =   2.5  # How fast do we walk in M/s            (avg is between 1.4 and 2.5)
        self.runMultiplier       =   3.0  # How much faster is a run over a walk  (avg is 5.0 m/s (so 2.0 * 2.5))
        self.jumpMetersPerSecond =   8.5  # How fast do we jump in the +Y         (avg is 4.2 m/s)
        self.gravity             = -11.5  # Acceration in Y due to gravity        (normal = -9.8)
        self.windResistance      =   0.01 # Allow for a slight reduction in x     (keep at 0.0 to have no effect)

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

    # Ensure that the position can't move greater than the space of a
    # single section of the terrain, lets not warp through walls
    def constrainMovement(self, delta_xy):
        if delta_xy[0]   >=  config.width:
            delta_xy[0]   =  config.width - 1
        elif delta_xy[0] <  -config.width:
            delta_xy[0]   = -config.width + 1
        if delta_xy[1]   >=  config.height:
            delta_xy[1]   =  config.height - 1
        elif delta_xy[1] <  -config.height:
            delta_xy[1]   = -config.height + 1
        return delta_xy

    # Move the character
    def movement(self, t=0, dt=0, keyPressed=[], mouseTracking={}, level=None):

        # Add the effect of wind resistance when jumping  or falling.
        self.fallingX = self.fallingX * (1.0 - self.windResistance)

        # Our initial proposed change in position
        delta_xy = numpy.array([self.fallingX*dt, -1.0, 0.0])

        # Lets handle jumping (when not already jumping / falling)
        if 'jump' in keyPressed and not self.falling and not self.death:
            if self.fallingTime == 0.0:
                self.fallingTime = t-dt
                self.fallingPos = self.playerSprite.y
                self.jumpVelocity = self.jumpMetersPerSecond
                self.changeSprite('Jump', self.facing, False)
            self.falling = True

        # If we are falling calculate our change in movement through y
        # This utilizes the Pt = P0 + V0t + 1/2 at^2 formula discussed in class
        if self.falling:
            dy = self.fallingPos + (self.jumpVelocity * self.pixelsPerMeter * (t-self.fallingTime)) + (0.5 * self.gravity * self.pixelsPerMeter * (t-self.fallingTime)**2)
            delta_xy[1] = dy - self.playerSprite.y

        # Handle Walking and Running inputs from the game player
        if 'right' in keyPressed and not self.falling and not self.death:
            self.changeSprite('Run', 'Right', True)
            self.fallingX = self.walkMetersPerSecond * self.pixelsPerMeter
            if 'run' in keyPressed:
                self.fallingX *= self.runMultiplier
            delta_xy[0] = self.fallingX * dt
        elif 'left' in keyPressed and not self.falling and not self.death:
            self.changeSprite('Run', 'Left', True)
            self.fallingX = -self.walkMetersPerSecond * self.pixelsPerMeter
            if 'run' in keyPressed:
                self.fallingX *= self.runMultiplier
            delta_xy[0] = self.fallingX * dt
        elif not self.falling:
            self.fallingX = 0.0
            if not self.death:
                self.changeSprite('Idle', self.facing, True)

        # Ensure that the max change in x or change in y is 1 less than
        # config.height and config.width, This prevents us from flying
        # through the terrain...
        delta_xy = self.constrainMovement(delta_xy)

        # Calculate the new position of the player based on adding
        # the delta to the old position
        proposed_xy = numpy.array([self.playerSprite.x, self.playerSprite.y, 0.0]) + delta_xy

        # Check for colisions with terrain
        if proposed_xy[0] != self.playerSprite.x or proposed_xy[1] != self.playerSprite.y:

            # Run the terrain collisions function against the new proposed x,y coordinates
            proposed_xy[0], proposed_xy[1], impact_x, impact_y = self.terrainCollisions(proposed_xy[0],
                                                                                        proposed_xy[1],
                                                                                        self.playerSprite.x,
                                                                                        self.playerSprite.y,
                                                                                        config.level)

            # If we successfully moved in the y, then we must be falling.
            if proposed_xy[1] != self.playerSprite.y:
                self.falling = True
                if self.fallingTime == 0.0:
                    self.fallingTime = t-dt
                    self.fallingPos = self.playerSprite.y

            # We impacted in the y, we should assume that we are stopped in the
            # y and let gravity take back over
            if impact_y:
                self.falling = False
                self.fallingTime = 0.0
                self.jumpVelocity = 0.0

            # We impacted in the X allow for attempts to move in a direction
            # in the future if the user requested to move right or left
            # this helps with jumping over terrain
            if impact_x:
                if 'right' in keyPressed and not self.death:
                    self.changeSprite(self.mode, 'Right', self.animationLoop)
                    self.fallingX = self.walkMetersPerSecond * self.pixelsPerMeter
                elif 'left' in keyPressed and not self.death:
                    self.changeSprite(self.mode, 'Left', self.animationLoop)
                    self.fallingX = -self.walkMetersPerSecond * self.pixelsPerMeter
                else:
                    self.fallingX = 0.0

        # Update the sprites position
        self.playerSprite.x = proposed_xy[0]
        self.playerSprite.y = proposed_xy[1]

    # Are we colliding with any terrain
    def terrainCollisions(self, x, y, ox, oy, level=None):

        # Store some impact information
        impact_x = False
        impact_y = False

        # Try to move in the y only, do we impact anything?
        col  = int(numpy.floor(ox / config.width))
        head = int(numpy.floor((y + (0.75 * self.playerSprite.height)) / config.height))
        feet = int(numpy.floor(y / config.height))
        if head in level and col in level[head]:
            y = min(oy, (head+1) * config.height)
            impact_y = True
        if feet in level and col in level[feet]:
            y = (feet + 1) * config.height
            impact_y = True

        # Try to move in the x now, any impacts?
        col  = int(numpy.floor(x / config.width))
        head = int(numpy.floor((y + (0.75 * self.playerSprite.height)) / config.height))
        feet = int(numpy.floor(y / config.height))
        if (head in level and col in level[head]) or (feet in level and col in level[feet]):
            min_x = (col+1) * config.width
            max_x = col * config.width
            if x < ox and x <= min_x:
                x = min_x
                impact_x = True
            elif x > ox and x >= max_x:
                x = max_x
                impact_x = True

        # Return the new and acceptable x and y position
        return x, y, impact_x, impact_y

    # Retrieve this player's bounding region for collision detection
    def bounds(self):
        return [ self.playerSprite.x - 0.25 * self.playerSprite.width,
                 self.playerSprite.y + 0.25 * self.playerSprite.height,
                 self.playerSprite.x + 0.25 * self.playerSprite.width,
                 self.playerSprite.y + 0.75 * self.playerSprite.height ]

    # Check for overlapping bounds (collision between moving objects)
    def overlappingBounds(self, other):
        R1 = self.bounds()
        R2 = other.bounds()
        if (R1[0]>=R2[2]) or (R1[2]<=R2[0]) or (R1[3]<=R2[1]) or (R1[1]>=R2[3]):
            return False
        return True

    # Are we colliding with any enemies
    def enemyCollisions(self, enemies):
        for enemy in enemies:
            if self.overlappingBounds(enemy):
                return True
        return False

    # Are we colliding with any weapons fire
    def weaponsCollisions(self, weapons):
        for weapon in weapons:
            if self.overlappingBounds(weapon):
                return True
        return False

    # Draw our character
    def draw(self, t=0, dt=0, keyTracking={}, mouseTracking=[], enemies=[], weapons=[], goals={}, objects={}, level=None, *other):

        # When we die our player shouldn't be able to control the character anymore...
        if self.death:
            self.movement(t, dt, {}, [], level)
        else:
            self.movement(t, dt, keyTracking, mouseTracking, level)

        # Have we been killed by collisions with enemies or enemy weapon fire?
        if self.enemyCollisions(enemies) or self.weaponsCollisions(weapons):
            self.death = True
            self.changeSprite('Dead', self.facing, False)

        # Time to draw the Player Sprite
        self.playerSprite.draw()

        # return if we died (boolean), did we reach the goal (boolean),
        # and a Created Weapon (Player Object) if one was launched
        return self.death, False, None
