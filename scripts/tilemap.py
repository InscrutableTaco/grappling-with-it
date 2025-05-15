import pygame
from enum import Enum
from scripts.constants import TILE_SIZE
from scripts.utils import to_grid, to_pos

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
        self.str_type = str(self.type).lower().split('.')[1] # yuck!
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
            loc = (4 * self.tile_size + (i * self.tile_size), 17 * self.tile_size)
            tile = Tile(Tile_type.DIRT, loc)
            self.tilemap[str(tile.grid_pos)] = tile
        for i in range(15):
            loc = (4 * self.tile_size + (i * self.tile_size), 18 * self.tile_size)
            tile = Tile(Tile_type.DIRT, loc, 4)
            self.tilemap[str(tile.grid_pos)] = tile

        for i in range(45):
            loc = (4 * self.tile_size + (i * self.tile_size), 26 * self.tile_size)
            tile = Tile(Tile_type.DIRT, loc)
            self.tilemap[str(tile.grid_pos)] = tile
        for i in range(45):
            loc = (4 * self.tile_size + (i * self.tile_size), 27 * self.tile_size)
            tile = Tile(Tile_type.DIRT, loc, 4)
            self.tilemap[str(tile.grid_pos)] = tile

        self.add_tile((4, 26), 7)
        self.add_tile((4, 27), 5)
        self.add_tile((49, 26), 1)
        self.add_tile((49, 27), 3)

        for i in range(6):
            loc = (18 * self.tile_size + (i * self.tile_size), 12 * self.tile_size)
            tile = Tile(Tile_type.DIRT, loc)
            self.tilemap[str(tile.grid_pos)] = tile
        for i in range(6):
            loc = (18 * self.tile_size + (i * self.tile_size), 13 * self.tile_size)
            tile = Tile(Tile_type.DIRT, loc, 4)
            self.tilemap[str(tile.grid_pos)] = tile

        for i in range(6):
            loc = (5 * self.tile_size + (i * self.tile_size), 9 * self.tile_size)
            tile = Tile(Tile_type.DIRT, loc)
            self.tilemap[str(tile.grid_pos)] = tile
        for i in range(6):
            loc = (5 * self.tile_size + (i * self.tile_size), 10 * self.tile_size)
            tile = Tile(Tile_type.DIRT, loc, 4)
            self.tilemap[str(tile.grid_pos)] = tile

        self.add_tile((4, 9), 7)
        self.add_tile((4, 10), 5)
        self.add_tile((11, 9), 1)
        self.add_tile((11, 10), 3)

        self.add_tile((3, 17), 7)
        self.add_tile((3, 18), 5)
        self.add_tile((19, 17), 1)
        self.add_tile((19, 18), 3)

        self.add_tile((17, 12), 7)
        self.add_tile((17, 13), 5)
        self.add_tile((24, 12), 1)
        self.add_tile((24, 13), 3)

        self.add_tile((12, 3), 7)
        self.add_tile((12, 4), 5)
        self.add_tile((13, 3), 1)
        self.add_tile((13, 4), 3)

        self.add_tile((24, 3), 7)
        self.add_tile((24, 4), 5)
        self.add_tile((25, 3), 0)
        self.add_tile((25, 4), 4)
        self.add_tile((26, 3), 0)
        self.add_tile((26, 4), 4)
        self.add_tile((27, 3), 0)
        self.add_tile((27, 4), 4)
        self.add_tile((28, 3), 0)
        self.add_tile((28, 4), 4)
        self.add_tile((29, 3), 1)
        self.add_tile((29, 4), 3)

        self.add_tile((34, 3), 7)
        self.add_tile((34, 4), 5)
        self.add_tile((35, 3), 0)
        self.add_tile((35, 4), 4)
        self.add_tile((36, 3), 1)
        self.add_tile((36, 4), 3)

        self.add_tile((31, 12), 7)
        self.add_tile((31, 13), 5)
        self.add_tile((32, 12), 0)
        self.add_tile((32, 13), 4)
        self.add_tile((33, 12), 0)
        self.add_tile((33, 13), 4)
        self.add_tile((34, 12), 0)
        self.add_tile((34, 13), 4)
        self.add_tile((35, 12), 0)
        self.add_tile((35, 13), 4)
        self.add_tile((36, 12), 1)
        self.add_tile((36, 13), 3)
        
    def add_tile(self, grid_pos, variant):
        tile = Tile(Tile_type.DIRT, to_pos(grid_pos), variant)
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

    def render(self, surf, offset=(0, 0)):
        for tile in self.tilemap.values():
            real_pos = (tile.pos[0] - offset[0], tile.pos[1] - offset[1])
            surf.blit(self.game.assets[tile.str_type][tile.variant], real_pos)