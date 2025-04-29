import sys
import pygame

from constants import *
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot


def main():
    pygame.init()
    pygame.display.set_caption(WINDOW_TITLE)

    
    # Supposedly replaces the pygame window icon at the top left
    # Can't tell if this working (no icon showing before either)
    #   Filepath is correct. png seems like its allowed.
    #   Some other code (copied from asteroids clone) hiding the icon for some reason?
    win_icon = pygame.image.load('art/grappling_hook.png')
    pygame.display.set_icon(win_icon)

    # set up the screen, clock
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    # define groups of similar behavior, i.e. things we'll be iterating through
    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    # put things into groups
    # (things can be in multiple groups)
    #   .containers comes from pygame
    #   designed specifically for sprite grouping
    Asteroid.containers = (asteroids, updatable, drawable)
    Shot.containers = (shots, updatable, drawable)
    AsteroidField.containers = updatable
    Player.containers = (updatable, drawable)

    # create asteroid_field
    asteroid_field = AsteroidField()
    
    # position the player
    player = Player(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 )

    # initialize Δ time
    dt = 0

    # main loop
    while True:
    
        # stop game when it's time
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        # call the update function on every object in the updatable group - based on Δ time
        updatable.update(dt)

        # check for asteroid collisions
        for asteroid in asteroids:
            if asteroid.collides_with(player):
            
                # quits game immediately (change this)
                print("Game over!")
                sys.exit()

            # check for collisions between shots and asteroids
            #   remove collided shot / split the asteroid
            for shot in shots:
                if asteroid.collides_with(shot):
                    shot.kill()
                    asteroid.split()

        # resets the screen to black
        screen.fill("black")

        # draw objects to be drawn
        for obj in drawable:
            obj.draw(screen)

        # this actually updates the display; see also pygame.display.update()
        pygame.display.flip()

        # limit the framerate to 60 FPS
        dt = clock.tick(60) / 1000

# check if this file was the one that was run (i.e. don't run the main function if this is running imported somwhere)
# (a ubiquitous python check)
if __name__ == "__main__":
    main()
