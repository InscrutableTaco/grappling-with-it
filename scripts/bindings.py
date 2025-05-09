import pygame
class Bindings:
    def __init__(self, game):
        self.game = game 
        def press_left(self, game):
            game.movement[0] = True
        def press_right(self, game):
            game.movement[1] = True
        def depress_left(self, game):
            game.movement[0] = False
        def depress_right(self, game):
            game.movement[1] = False
        def press_jump(self, game):
            game.player.jump()
        def depress_jump(self, game):
            pass

        self.bindings_map = { # 'action':[(key set), press function, depress function]
            'left': [(pygame.K_LEFT, pygame.K_a), press_left, depress_left],
            'right': [(pygame.K_RIGHT, pygame.K_d), press_right, depress_right],
            'jump': [(pygame.K_SPACE, pygame.K_UP, pygame.K_w), press_jump, depress_jump],
        }   

    def read_input(self, game, event):
        if event.type == pygame.KEYDOWN:
            for action in self.bindings_map:
                if event.key in self.bindings_map[action][0]:
                    self.bindings_map[action][1](self, game)
        if event.type == pygame.KEYUP:
            for action in self.bindings_map:
                if event.key in self.bindings_map[action][0]:
                    self.bindings_map[action][2](self, game)
