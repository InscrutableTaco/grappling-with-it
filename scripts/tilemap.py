import pygame
from enum import Enum
from scripts.constants import TILE_SIZE
from scripts.utils import to_grid

NEIGHBOR_OFFSETS = [(-1, 0), (-1, -1), (0, -1), (1, -1), (1, 0), (0, 0), (-1, 1), (0, 1), (1, 1)]

class Tile_type(Enum):
    GRASS = 1
    STONE = 2
    METAL = 3
    BACKGROUND = 4
    DIRT = 5

class Tile:
    def __init__(self, tile_type, pos=(0, 0), variant=0, tile_size=TILE_SIZE):
        self.type = tile_type
        self.str_type = str(self.type).lower().split('.')[1]
        self.pos = pos
        self.grid_pos = to_grid(pos)
        self.variant = variant
        self.tile_size=tile_size
        self.solid = False

        match self.type:
            case self.type.BACKGROUND:
                self.solid = False
            case _:
                self.solid = True

class Tilemap:
    def __init__(self, game, tile_size=TILE_SIZE):
        self.game = game
        self.tile_size = tile_size
        self.tilemap = {}

        # test tiles
        for i in range(15):
            loc = (100 + (i * self.tile_size), 600)
            tile = Tile(Tile_type.DIRT, loc)
            self.tilemap[str(tile.grid_pos)] = tile

    def tiles_around(self, pos): #return list of tiles around a position
        tiles = []
        grid_pos = to_grid(pos)
        for offset in NEIGHBOR_OFFSETS:
            neighbor = str([grid_pos[0] + offset[0], grid_pos[1] + offset[1]])
            if neighbor in self.tilemap:
                tile = self.tilemap[neighbor]
                tiles.append(tile)
        return tiles
    
    def physics_rects_around(self, pos):
        rects = []
        for tile in self.tiles_around(pos):
            if tile.solid:
                rects.append(pygame.Rect(tile.pos[0], tile.pos[1], self.tile_size, self.tile_size))
        return rects

    def render(self, surf):
        for tile in self.tilemap.values():
            surf.blit(self.game.assets[tile.str_type][tile.variant], tile.pos)