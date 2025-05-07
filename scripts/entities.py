import pygame
from constants import GRAVITY, TERM_VEL

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

    def update(self, movement=(0, 0)):
        self.pos[0] += self.velocity[0] + movement[0]
        self.pos[1] += self.velocity[1] + movement[1]

        self.velocity[1] = min(TERM_VEL, self.velocity[1] + GRAVITY)

        if self.collisions['down'] or self.collisions['up']:
            self.velocity[1] = 0

    def render(self, surf):
        surf.blit(self.game.assets['grapple-icon'], self.pos)

class Player(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'player', pos, size)

    def update(self, movement=(0, 0)):
        return super().update(movement)
    
    def render(self, surf):
        return super().render(surf)

class Enemy(Entity):
    def __init__(self, game, pos, size):
        super().__init__(game, 'enemy', pos, size)

    def update(self, movement=(0, 0)):
        return super().update(movement)
    
    def render(self, surf):
        return super().render(surf)