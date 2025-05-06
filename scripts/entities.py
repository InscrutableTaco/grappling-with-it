from game import Game

class Entity:
    def __init__(self, game, pos, size):
        self.game = game
        self.pos = list(pos)
        self.size = size
        self.velocity = [0, 0]
        self.movement


    def update(self, movement=(0, 0)):
        self.pos[0] += self.velocity[0] + movement[0]
        self.pos[1] += self.velocity[1] + movement[1]

    def render(self, surf):
        surf.blit(self.game.assets['grapple-icon'], self.pos)

class Player(Entity):
    def __init__(self):
        super().__init__()

    def update(self, movement=(0, 0)):
        return super().update(movement)
    
    def render(self, surf):
        return super().render(surf)

class Enemy(Entity):
    def __init__(self):
        super().__init__()

    def update(self, movement=(0, 0)):
        return super().update(movement)
    
    def render(self, surf):
        return super().render(surf)