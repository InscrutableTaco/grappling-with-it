import pygame
import sys
from scripts.utils import load_image
from scripts.entities import Enemy, Player
from bindings import Bindings

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1200, 900))
        self.display = pygame.Surface((1200, 900), pygame.SRCALPHA)
        pygame.display.set_caption("Grappling With It!")
        self.clock = pygame.time.Clock()
        self.player = Player(self, (50, 50), (16, 30))
        self.movement = [False, False] # left / right input
        self.bindings = Bindings(self)
        self.assets = {
            'grapple-icon': load_image("grappling_hook.png")
        }

    def run(self):
        while True:
            self.display.fill((6, 5, 4))
            self.player.update(((self.movement[1] - self.movement[0]) * 8, 0))
            self.player.render(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                self.bindings.read_input(self, event)
                            
            self.screen.blit(pygame.transform.scale(self.display, self.screen.get_size()), (0, 0))
            pygame.display.update()
            self.clock.tick(60)

Game().run()