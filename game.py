import pygame
import sys
from scripts.utils import load_image, load_images, load_sound, to_grid, to_pos
from scripts.constants import SCREEN_SIZE, DISPLAY_SIZE
from scripts.entities import Player
from scripts.bindings import Bindings
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        self.display = pygame.Surface(DISPLAY_SIZE, pygame.SRCALPHA)
        pygame.display.set_caption("Grappling With It!")

        self.clock = pygame.time.Clock()
        self.player = Player(self, to_pos((3, 15)), (32, 32))
        self.movement = [False, False]
        self.bindings = Bindings(self)
        self.assets = {
            'grapple-icon': load_image('grappling_hook.png'),
            'dirt': load_images('tiles/dirt'),
        }

        self.sfx = {
            'jump': load_sound('jump.wav')
        }

        self.sfx['jump'].set_volume(0.6)

        self.camera = [0, 0]

        self.tilemap = Tilemap(self)

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            self.camera[0] += (self.player.rect().centerx - self.display.get_width() / 2 - self.camera[0]) / 30
            self.camera[1] += (self.player.rect().centery - self.display.get_height() / 2 - self.camera[1]) / 30

            self.tilemap.render(self.display, offset=self.camera)
            print(f"walk speed is {self.player.walk_speed}, jumps is {self.player.jumps}")
            frame_movement = ((self.movement[1] - self.movement[0]) * self.player.walk_speed, 0)
            self.player.update(self.tilemap, frame_movement)
            self.player.render(self.display, offset=self.camera)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                self.bindings.read_input(self, event)
                            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)
            #print(to_grid(self.player.pos))

Game().run()