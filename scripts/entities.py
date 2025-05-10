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
        self.air_time = 0

    def reset_collisions(self):
        for direction in self.collisions:
            self.collisions[direction] = False

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

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
        
        move_x = self.velocity[0] + movement[0]
        self.pos[0] += move_x
        self.check_collisions('x', move_x, tilemap)
        
        move_y = self.velocity[1] + movement[1]
        self.pos[1] += move_y
        self.check_collisions('y', move_y, tilemap)

        self.velocity[1] = min(TERM_VEL, self.velocity[1] + GRAVITY)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 1 # this should be zero

        #print(f"end of update, y velocity is {self.velocity[1]} and y position is {self.pos[1]}")

    def render(self, surf, offset=(0, 0)):
        real_pos = (self.pos[0] - offset[0], self.pos[1] - offset[1])
        surf.blit(self.game.assets['grapple-icon'], real_pos)

class Player(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.walk_speed = WALK_SPEED
        self.jumps = 1
        self.max_jumps = 2

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)
        if self.collisions['down'] == True:
            self.jumps = self.max_jumps
    
    def render(self, surf, offset=(0, 0)):
        super().render(surf, offset)
    
    def jump(self):
        if self.jumps >= 1 and self.collisions['down'] == True:
            self.game.sfx['jump'].play()
            self.velocity[1] = JUMP_VEL
            self.jumps -= 1
            #self.collisions['down'] = False
            #self.air_time = 40

    #def end_jump(self):
     #   pass

class Enemy(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

    def update(self, movement=(0, 0)):
        return super().update(movement)
    
    def render(self, surf, offset=(0, 0)):
        return super().render(surf, offset)