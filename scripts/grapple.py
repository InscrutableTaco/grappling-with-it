import pygame
import math

from scripts.tilemap import Tilemap

class Grapple():
    def __init__(self, game, pos, size):

        self.game = game
        self.pos = pos
        self.size = size

        origin = (self.pos[0] - game.camera[0], self.pos[1] - game.camera[1])
        terminus = (origin[0] + 100, origin[1] - 100)
        pygame.draw.line(game.display, (0, 0, 255), origin, terminus, 6)