import pygame
from scripts.constants import GRAVITY, TERM_VEL, JUMP_VEL

class Entity:
    def __init__(self, game, kind, pos, size):
        self.game = game
        self.kind = kind
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.collisions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }
        self.air_time = 0

    def rect(self):
        return pygame.Rect(self.pos[0], self.pos[1], self.size[0], self.size[1])

    def update(self, tilemap, movement=(0, 0)):

        self.collisions = {
            'up': False,
            'down': False,
            'left': False,
            'right': False
        }

        self.pos[0] += self.velocity[0] + movement[0]

        hitbox = self.rect()    
        for rect in tilemap.physics_rects_around(self.pos):
            if hitbox.colliderect(rect):
                if self.velocity[0] > 0:
                    self.collisions['right'] = True
                    hitbox.right = rect.left
                if self.velocity[0] < 0:
                    self.collisions['left'] = True
                    hitbox.left = rect.right
                self.pos[0] = hitbox.x

        self.pos[1] += self.velocity[1] + movement[1]

        hitbox = self.rect()
        for rect in tilemap.physics_rects_around(self.pos):
            if hitbox.colliderect(rect):
                if self.velocity[1] > 0:
                    self.collisions['down'] = True
                    hitbox.bottom = rect.top
                if self.velocity[1] < 0:
                    self.collisions['up'] = True
                    hitbox.top = rect.bottom
                self.pos[1] = hitbox.y

        # apply gravity
        self.velocity[1] = min(TERM_VEL, self.velocity[1] + GRAVITY)

        # reset fall speed when
        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0
            #self.air_time = max(0, self.air_time - 1)

    def render(self, surf):
        surf.blit(self.game.assets['grapple-icon'], self.pos)

class Player(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)
        self.jumps = 1
        self.max_jumps = 1
        print(self.jumps)

    def update(self, tilemap, movement=(0, 0)):
        super().update(tilemap, movement)
        if self.collisions['down'] == True:
            self.jumps = self.max_jumps
    
    def render(self, surf):
        super().render(surf)
    
    def jump(self):
        if self.jumps >= 1 and self.collisions['down'] == True:
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
    
    def render(self, surf):
        return super().render(surf)