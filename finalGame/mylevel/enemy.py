#!/usr/bin/python3

# Important Libraries
import pyglet, config, math, time
# An Enemy Combatant
class Enemy:
    def __init__(self, sprites={},buildSprite=None,playerClass="enemy-1",mode="Run",facing="Right",speed=0.05,scale=0.15,loop=True,x=380,y=250):

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

        # Movement items
        self.airborne = False
        self.debugging = False
        self.jump_x = math.pi + .5
        self.step = .1
        self.dead = False
        self.remain_dead = False
        import random
        self.dx = random.uniform(.5,1) * 2.5
        self.dy = 0
        # Build the starting character sprite
        self.hitbox_size = .15*(self.sprites['hero']['Run']['Right'][0].get_image_data().width + self.sprites['hero']['Idle']['Right'][0].get_image_data().width) / 4
        self.died_at = 0.0
        self.remove = False
        self.changeSprite()

        self.hitbox = {'ll' : {'x' :x - self.hitbox_size ,'y' : y},\
                       'lr' : {'x' : x + self.hitbox_size ,'y' : y},\
                       'ul' : {'x' : x - self.hitbox_size ,'y' : y + self.sprite.height},\
                       'ur' : {'x' : x + self.hitbox_size ,'y' : y + self.sprite.height}
                     }



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
    def movement(self, config, t=0, keyTracking={}):
        mode,facing,loop = ('Run',self.facing,True)

        if self.will_collide_h(config) or not self.will_collide_v(config):
            self.dx = -1 * self.dx
            if self.facing == 'Right':
                facing = 'Left'
            else:
                facing = 'Right'
            self.changeSprite(mode=mode,facing=facing,loop=loop)

        self.sprite.x += self.dx
        self.sprite.y += self.dy
        pass


    # Draw our character
    def draw(self, t=0, keyTracking={}, config=None,level=None,*other):
        self.update_hitbox()
        if not self.dead:
            self.movement(config, t, keyTracking)
        else:
            if not self.remain_dead:
                level.play_sound('mylevel/music/enemy_death.wav',False)
                self.changeSprite(mode='Dead',facing = self.facing,loop=False)
                self.remain_dead = True
            else:
                if time.time() - self.died_at > 3:
                    self.remove = True
        self.sprite.draw()

    def update_position_airborne(self):
        if self.jump_x >= 3 * (math.pi/2.0):
            self.jump_x = 3 * (math.pi/2.0)
        else:
            self.jump_x += self.step


        self.dy = 17*math.sin(self.jump_x)

        if ((res := self.will_collide_v(config)) != False) and not self.init_jump:
            if res[0] == 'upper':
                self.dy = res[2]['ll']['y'] - res[1]['y'] - .01
                self.jump_x = math.pi + .5
            else:
                self.dy = res[2]['ul']['y'] - res[1]['y'] - .01
                self.jump_x = (3/2) * math.pi
                self.airborne = False
        self.update_hitbox()

    def check_collision_vert(self,config):
        level,width,height = (config.level,config.width,config.height)
        delta_x = 0
        delta_y = 0

        # Player collision parametrics
        x_pos = self.sprite.x + delta_x
        y_pos = self.sprite.y + delta_y

        player_line = {'bot' : {'x' : x_pos,'y' : y_pos},\
                       'top' : {'x' : x_pos,'y' : y_pos + ( self.sprite.height)}}
                       #+ 0.75 * self.sprite.height

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

                # Check hit from above
                if self.within(player_line['top'],hitbox):
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
        x_pos = self.sprite.x + delta_x
        y_pos = self.sprite.y + delta_y

        player_box = {'ll' : {'x' : x_pos - self.sprite.width / 2 ,'y' : y_pos},\
                      'lr' : {'x' : x_pos + self.sprite.width / 2 ,'y' : y_pos},\
                      'ul' : {'x' : x_pos - self.sprite.width / 2 ,'y' : y_pos + self.sprite.height},\
                      'ur' : {'x' : x_pos + self.sprite.width / 2 ,'y' : y_pos + self.sprite.height}
                     }

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



                for point in player_box.keys():
                    if self.within(player_box[point],hitbox):
                        return (point,player_box[point],hitbox)

        return False

    def will_collide_v(self,config):
        self.sprite.x += self.dx
        self.sprite.y -= 50

        collision = self.check_collision_vert(config)

        self.sprite.x -= self.dx
        self.sprite.y += 50

        return collision

    def will_collide_h(self,config):
        self.sprite.x += self.dx

        collision = self.check_collision_hori(config)

        self.sprite.x -= self.dx

        return collision

    def will_this_kill_me(self,hitbox):
        for point in hitbox:
            if self.within(hitbox[point],self.hitbox):
                self.died_at = time.time()
                return True

    def update_hitbox(self):
        x = self.sprite.x
        y = self.sprite.y
        self.hitbox = {'ll' : {'x' : x - self.hitbox_size ,'y' : y},\
                       'lr' : {'x' : x + self.hitbox_size ,'y' : y},\
                       'ul' : {'x' : x - self.hitbox_size ,'y' : y + self.sprite.height},\
                       'ur' : {'x' : x + self.hitbox_size ,'y' : y + self.sprite.height}
                     }

    def within(self,p1,hitbox):
        return \
        p1['x'] >= hitbox['ll']['x'] and \
        p1['x'] <= hitbox['lr']['x'] and \
        p1['y'] <= hitbox['ul']['y'] and \
        p1['y'] >= hitbox['ll']['y']
