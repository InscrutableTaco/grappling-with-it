import pygame
from scripts.constants import GRAVITY, TERM_VEL, JUMP_VEL, WALK_SPEED, THROW_SPEED, GRAPPLE_LENGTH, GRAPPLE_SPEED, SWING_SPEED
from scripts.utils import to_grid
import math

class Entity:
    def __init__(self, game, kind, pos, size):
        self.game = game
        self.kind = kind
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.walk_speed = 0
        self.collisions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.action = ''
        #self.anim_offset = (-3, -3)
        self.flip = False
        
        if self.kind == 'player':
            self.set_action('idle')

    def set_action(self, action):
        if action != self.action:
            self.action = action
            self.animation = self.game.assets[self.kind + '/' + self.action].copy()

    def reset_collisions(self):
        for direction in self.collisions:
            self.collisions[direction] = False

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update_action(self, x_input):
        if abs(x_input) > 0 and self.collisions['down']:
            self.set_action('walk')
        elif self.collisions['down']:
            self.set_action('idle')
    
    def set_facing(self, x_input):
        if x_input < 0:
            self.flip = True
        if x_input > 0:
            self.flip = False

    def check_collisions(self, axis, movement, tilemap):
            if axis == 'x':
                hitbox = self.rect()
                for rect in tilemap.physics_rects_around(self.pos):
                    if hitbox.colliderect(rect):
                        if movement > 0:
                            self.collisions['right'] = True
                            hitbox.right = rect.left
                        if movement < 0:
                            self.collisions['left'] = True
                            hitbox.left = rect.right
                        self.pos[0] = hitbox.x

            elif axis == "y":
                hitbox = self.rect()
                for rect in tilemap.physics_rects_around(self.pos):
                    if hitbox.colliderect(rect):
                        if movement > 0:
                            self.collisions['down'] = True
                            hitbox.bottom = rect.top
                        if movement < 0:
                            self.collisions['up'] = True
                            hitbox.top = rect.bottom
                        self.pos[1] = hitbox.y
            else:
                raise Exception("Invalid axis")
                    
    def update(self, tilemap, movement=(0, 0)):
        self.reset_collisions()

        #save x and y movement
        move_x, move_y = self.velocity[0] + movement[0], self.velocity[1] + movement[1]
    
        #move horizontally, process collisions
        self.pos[0] += move_x
        self.check_collisions('x', move_x, tilemap)
        
        #move vertically, process collisions
        self.pos[1] += move_y
        self.check_collisions('y', move_y, tilemap)

        # set action, sprite direction per movement, collisions (unless throwing or swinging)
        if self.kind == 'player' and (self.action not in self.grapple_actions):
            self.update_action(move_x)
            self.set_facing(move_x)

        #print(f"end of update, y velocity is {self.velocity[1]} and y position is {self.pos[1]}")

    def render(self, surf, offset=(0, 0)):
        screen_pos = (self.pos[0] - offset[0], self.pos[1] - offset[1])
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), screen_pos)

class Player(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.walk_speed = WALK_SPEED
        self.jumps = 1
        self.max_jumps = 2
        self.grapple_actions = {'throwing', 'grappling', 'swinging'}

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        #update animation
        self.animation.update()

        #reset jumps
        if self.collisions['down'] == True:
            self.jumps = self.max_jumps
        #update velocity w/ gravity
        self.velocity[1] = min(TERM_VEL, self.velocity[1] + GRAVITY)

        #reset y velocity if colliding up or down. 
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 1 # this *should* be 0, but this currently causes the player to
                                # wiggle up and down, breaking collision on the ensuing frames :(

        if self.action in self.grapple_actions:
            if self.grapple.length >= self.grapple.max_length:
                del self.grapple
                self.action = 'idle'
            else:
                self.grapple.update(tilemap, movement=(0, 0))

    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)
        if self.action in self.grapple_actions:
            self.grapple.render(surf, offset=offset)
    
    def jump(self):
        if self.jumps >= 1 and self.collisions['down'] == True and self.action not in self.grapple_actions:
            self.game.sfx['jump'].play()
            self.velocity[1] = JUMP_VEL
            self.jumps -= 1
            self.set_action('jump')
            self.collisions['down'] = False

    def fire_grapple(self, game):
        sprite_offset = (-1, 12) if self.flip else (14, 12)
        pos = (self.pos[0] + sprite_offset[0], self.pos[1] + sprite_offset[1])
        
        self.grapple = Grapple(self.game, pos, self, (8, 8))
        self.set_action('throwing')

class Grapple(Entity):
    def __init__(self, game, pos, player, size=(8, 8)):
        super().__init__(game, 'grapple', pos, size)
        self.player = player
        self.origin = list(pos)
        self.flip = player.flip
        self.velocity = [-THROW_SPEED, -THROW_SPEED] if self.flip else [THROW_SPEED, -THROW_SPEED] 
        self.length = 0
        self.max_length = GRAPPLE_LENGTH
        self.anchored = False
        self.img = pygame.transform.scale2x(game.assets[self.kind].copy())
        self.handle_offset = (16, 16) if self.flip else (0, 16)

    def move_player(self):# move player to origin
                sprite_offset = (1, -12) if self.flip else (-14, -12)
                pos = [self.origin[0] + sprite_offset[0], self.origin[1] + sprite_offset[1]]
                self.player.pos = pos

    def update(self, tilemap, movement=(0, 0)):

        if not self.anchored:

            # ascend until out of rope or collision
            super().update(tilemap, movement)
            self.handle_pos = (self.pos[0] + self.handle_offset[0], self.pos[1] + self.handle_offset[1])
            self.length = math.dist(self.origin, self.handle_pos)
            if any(self.collisions.values()):
                self.anchored = True
                self.player.set_action('grappling')
                self.anchored_length = self.length

        else:

            if self.length > (.65 * self.anchored_length):
                
                # retract, moving the origin toward handle
                self.length = math.dist(self.origin, self.handle_pos)
                self.origin[0] = pygame.math.lerp(self.origin[0], self.handle_pos[0], GRAPPLE_SPEED)
                self.origin[1] = pygame.math.lerp(self.origin[1], self.handle_pos[1], GRAPPLE_SPEED)
                self.angle = math.atan2(abs(self.origin[0] - self.handle_pos[0]), self.origin[1] - self.handle_pos[1])
                self.move_player()

            else:

                if math.sin(self.angle) >= .3:
                    # swing, moving origin in an arc
                    self.player.set_action('swinging')
                    self.origin[0] = self.handle_pos[0] + self.length * math.cos(self.angle)
                    self.origin[1] = self.handle_pos[1] + self.length * math.sin(self.angle)
                    speed = SWING_SPEED if self.flip else -SWING_SPEED
                    self.angle += speed
                    self.move_player()
                else:
                    self.player.velocity = [0, JUMP_VEL] # this ia cheating but it works for now
                    
                    self.player.set_action('jump')
                    del self.player.grapple

    def render(self, surf, offset=(0, 0)):
        
        screen_pos = (self.pos[0] - offset[0], self.pos[1] - offset[1])
        surf.blit(pygame.transform.flip(self.img, self.flip, False), screen_pos)
        
        screen_orig = (self.origin[0] - offset[0], self.origin[1] - offset[1])
        screen_handle_pos = self.handle_pos[0] - offset[0], self.handle_pos[1] - offset[1]
        pygame.draw.line(surf, (94, 223, 177), screen_orig, screen_handle_pos, 3)









class Enemy(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

    def update(self, movement=(0, 0)):
        return super().update(movement)
    
    def render(self, surf, offset=(0, 0)):
        return super().render(surf, offset)