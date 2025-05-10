import pygame
import os

from scripts.constants import TILE_SIZE, ART_PATH, SFX_PATH, MUSIC_PATH

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

def load_sound(path):
    sound = pygame.mixer.Sound(SFX_PATH + path)
    return sound

def to_grid(pos):
    return [int(pos[0] // TILE_SIZE), int(pos[1] // TILE_SIZE)]

def to_pos(grid_pos):
    return [grid_pos[0] * TILE_SIZE, grid_pos[1] * TILE_SIZE]

class Animation:
    def __init__(self, images, img_dur=5, loop=True):
        self.images = images
        self.loop = loop
        self.img_duration = img_dur
        self.done = False
        self.frame = 0

    def copy(self):
        return Animation(self.images, self.img_duration, self.loop)
    
    def update(self):
        if self.loop:
            self.frame = (self.frame + 1) % (self.img_duration * len(self.images))
        else:
            self.frame = min(self.frame + 1, self.img_duration * len(self.images) - 1)
            if self.frame >= self.img_duration * len(self.images) - 1:
                self.done = True
    
    def img(self):
        return self.images[int(self.frame / self.img_duration)]

