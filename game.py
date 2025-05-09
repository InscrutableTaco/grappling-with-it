import pygame
import sys
from scripts.utils import load_image, load_images, to_grid
from scripts.entities import Enemy, Player
from scripts.bindings import Bindings
from scripts.tilemap import Tilemap

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        self.display = pygame.Surface((1200, 900), pygame.SRCALPHA)
        pygame.display.set_caption("Grappling With It!")
        self.clock = pygame.time.Clock()
        self.player = Player(self, (150, 150), (16, 30))
        self.movement = [False, False]
        self.bindings = Bindings(self)
        self.assets = {
            'grapple-icon': load_image('grappling_hook.png'),
            'dirt': load_images('tiles/dirt'),
        }
        self.tilemap = Tilemap(self)

    def run(self):
        while True:
            self.display.fill((0, 0, 0))

            self.tilemap.render(self.display)
            frame_movement = ((self.movement[1] - self.movement[0]) * 8, 0)
            self.player.update(self.tilemap, frame_movement)

            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                self.bindings.read_input(self, event)

            print (self.player.collisions['down'])
                            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()