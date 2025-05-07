import pygame
import os

ART_PATH = "data/art/"
SFX_PATH = "data/sound/sfx"
MUSIC_PATH = "data/sound/music"

def load_image(path):
    img = pygame.image.load(ART_PATH + path).convert()
    img.set_colorkey((134, 246, 216, 1))
    return img

def load_images(path):
    imgs = []
    for img in sorted(os.listdir(ART_PATH + path)):
        imgs.append(load_image(ART_PATH + '/' + img))
    return imgs     

