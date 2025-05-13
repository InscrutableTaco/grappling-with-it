import pygame
from scripts.constants import GRAVITY, TERM_VEL, JUMP_VEL, WALK_SPEED

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

        #update action and direction based on movement / collisions
        if self.kind == 'player':
            self.update_action(move_x)
            self.set_facing(move_x)

        #update animation
        self.animation.update()

        #print(f"end of update, y velocity is {self.velocity[1]} and y position is {self.pos[1]}")

    def render(self, surf, offset=(0, 0)):
        real_pos = (self.pos[0] - offset[0], self.pos[1] - offset[1])
        surf.blit(pygame.transform.flip(self.animation.img(), self.flip, False), real_pos)

class Player(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.walk_speed = WALK_SPEED
        self.jumps = 1
        self.max_jumps = 2

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)

        #reset jumps
        if self.collisions['down'] == True:
            self.jumps = self.max_jumps
        #update velocity w/ gravity
        self.velocity[1] = min(TERM_VEL, self.velocity[1] + GRAVITY)

        #reset y velocity if colliding up or down. 
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 1 # this *should* be 0, but this currently causes the player to
                                # wiggle up and down, breaking collision on the ensuing frames :(
    
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)
    
    def jump(self):
        if self.jumps >= 1 and self.collisions['down'] == True:
            self.game.sfx['jump'].play()
            self.velocity[1] = JUMP_VEL
            self.jumps -= 1
            self.set_action('jump')
            self.collisions['down'] = False

    def fire_grapple(self, game):
        offset = (-14, 12) if self.flip else (14, 12)
        direction = ('left' if self.flip else 'right')
        pos = (self.pos[0] + offset[0], self.pos[1] + offset[1])
        
        self.rope = Rope(self.game, pos, direction, (32, 32))

class Rope(Entity):
    def __init__(self, game, pos, direction, size=(32, 32)):
        kind = 'rope'
        super().__init__(game, kind, pos, size)
        self.direction = direction
        self.velocity = [-50, -50] if self.direction == 'left' else [50, -50] 
        print(self.direction)









class Enemy(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

    def update(self, movement=(0, 0)):
        return super().update(movement)
    
    def render(self, surf, offset=(0, 0)):
        return super().render(surf, offset)