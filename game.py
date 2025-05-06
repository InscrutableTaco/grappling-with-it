import pygame
import sys
from utils import load_image

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.display = pygame.Surface((400, 300), pygame.SRCALPHA)
        pygame.display.set_caption("Grappling With It!")
        self.clock = pygame.time.Clock()

        self.assets = {
            'grapple-icon': load_image("grappling_hook.png")
        }

    def run(self):
        while True:
            self.screen.fill((0, 0, 0))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.display.blit(self.assets['grapple-icon'], (100, 100))
            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (100, 100))
            pygame.display.update()
            self.clock.tick(60)

game = Game()
game.run()