import pygame

from scripts.constants import SPAWN_POS
from scripts.utils import to_pos

class Bindings:
    def __init__(self, game):
        self.game = game

        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(x) for x in range(pygame.joystick.get_count())]
        for joystick in self.joysticks:
            print("Initializing joystick")
            joystick.init()

        # Ignore small movements
        self.joystick_deadzone = 0.2  

        def press_left(self, game):
            game.movement[0] = True
        def depress_left(self, game):
            game.movement[0] = False

        def press_right(self, game):
            game.movement[1] = True
        def depress_right(self, game):
            game.movement[1] = False

        def press_jump(self, game):
            game.player.jump()
        def depress_jump(self, game):
            pass

        def press_grapple(self, game):
            game.player.fire_grapple(game)
        def depress_grapple(Self,game):
            pass

        def press_reset(self, game):
            game.player.pos = list(to_pos(SPAWN_POS))
        def depress_reset(self, game):
            pass

        self.bindings_map = { # 'action':[(key set), press function, depress function]
            'left': [{pygame.K_LEFT, pygame.K_a}, press_left, depress_left],
            'right': [{pygame.K_RIGHT, pygame.K_d}, press_right, depress_right],
            'jump': [{pygame.K_SPACE, pygame.K_UP, pygame.K_w}, press_jump, depress_jump],
            'grapple': [{pygame.K_x, pygame.K_g}, press_grapple, depress_grapple],
            'reset': [{pygame.K_r}, press_reset, depress_reset],
        }

        self.controller_bindings = {
            'left': [('axis', 0, -1)],  # Left on left analog stick
            'right': [('axis', 0, 1)],  # Right on left analog stick
            'jump': [('button', 0)],    # A button (Switch Pro) / A button (Xbox) / X button (PlayStation)
            'grapple': [('button', 1)], # B button (Switch Pro) / B button (Xbox) / Circle button (PlayStation)
            'reset': [('button', 6)],   # Plus/Back/Select button
        }
        
        # For tracking axis movements
        self.axis_states = {}

    def read_input(self, game, event):
        # Keyboard events
        if event.type == pygame.KEYDOWN:
            for action in self.bindings_map:
                if event.key in self.bindings_map[action][0]:
                    self.bindings_map[action][1](self, game)

        if event.type == pygame.KEYUP:
            for action in self.bindings_map:
                if event.key in self.bindings_map[action][0]:
                    self.bindings_map[action][2](self, game)

        # Controller events
        if event.type == pygame.JOYBUTTONDOWN:
            for action, bindings in self.controller_bindings.items():
                for binding in bindings:
                    if binding[0] == 'button' and binding[1] == event.button:
                        self.bindings_map[action][1](self, game)

        if event.type == pygame.JOYBUTTONUP:
            for action, bindings in self.controller_bindings.items():
                for binding in bindings:
                    if binding[0] == 'button' and binding[1] == event.button:
                        self.bindings_map[action][2](self, game)

        if event.type == pygame.JOYAXISMOTION:
            axis = event.axis
            value = event.value

            if axis in [0, 1]:  # Left stick X and Y
                prev_value = self.axis_states.get((event.joy, axis), 0)
                self.axis_states[(event.joy, axis)] = value

                if axis == 0:
                    # Left direction
                    if prev_value > -self.joystick_deadzone and value <= -self.joystick_deadzone:
                        self.bindings_map['left'][1](self, game)
                    elif prev_value <= -self.joystick_deadzone and value > -self.joystick_deadzone:
                        self.bindings_map['left'][2](self, game)

                    # Right direction
                    if prev_value < self.joystick_deadzone and value >= self.joystick_deadzone:
                        self.bindings_map['right'][1](self, game)
                    elif prev_value >= self.joystick_deadzone and value < self.joystick_deadzone:
                        self.bindings_map['right'][2](self, game)
