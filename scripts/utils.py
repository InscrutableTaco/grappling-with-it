import pygame
import os

from scripts.constants import TILE_SIZE

ART_PATH = "data/art/"
SFX_PATH = "data/sfx/"
MUSIC_PATH = "data/music/"

def load_image(path):
    img = pygame.image.load(ART_PATH + path).convert()
    img.set_colorkey((0, 0, 0))
    return img

def load_images(path):
    images = []
    for img_name in sorted(os.listdir(ART_PATH + path)):
        if img_name.lower().endswith(('.png', '.jpg', '.bmp', '.gif')):
            images.append(load_image(path + '/' + img_name))
    return images

def to_grid(pos):
    return [int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE)]

def to_pos(grid_pos):
    return [grid_pos[0] * TILE_SIZE, grid_pos[1] * TILE_SIZE]

