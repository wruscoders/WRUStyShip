import os
import random
from collections import namedtuple
import pygame

Point = namedtuple('Point', 'x y')
Size = namedtuple('Size', 'w h')

pygame.init()

# Define constants for the screen width and height
SCREEN = Size(800, 600)
FPS = 60


# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode(SCREEN)
BACKGROUND = pygame.Color('black')

# Load some assets
ASSETS = 'assets'

# Ship
SHIP_SIZE = Size(80, 80)
SHIP_POS = Point(SCREEN.w//2-SHIP_SIZE.w//2, SCREEN.h-SHIP_SIZE.h)
SHIP_PNG = pygame.image.load(os.path.join(
    ASSETS, 'fighter.png'))
SHIP = pygame.transform.scale(SHIP_PNG, SHIP_SIZE)

# Laser
LASER_SIZE = Size(20, 20)
LASER_PNG = pygame.image.load(os.path.join(
    ASSETS, 'laser.png'))
LASER = pygame.transform.rotate(
    pygame.transform.scale(LASER_PNG, LASER_SIZE), 90)

# Asteroid
ASTEROID_SIZE = Size(100, 100)
ASTEROID_PNG = pygame.image.load(os.path.join(
    ASSETS, 'asteroid.png'))
ASTEROID = pygame.transform.scale(ASTEROID_PNG, ASTEROID_SIZE)

# Place ship in it's initial position
ship_rect = pygame.Rect(SHIP_POS, SHIP_SIZE)
ship_vel = 5


def draw_ship():
    screen.blit(SHIP, ship_rect)


# Create list of active lasers
lasers = []
laser_vel = (0, -7)


def create_laser():
    global lasers
    location = Point(ship_rect.centerx-LASER_SIZE.w //
                     2, ship_rect.top-LASER_SIZE.h)
    lasers.append(pygame.Rect(location, LASER_SIZE))


def draw_lasers():
    global lasers

    for laser in lasers:
        screen.blit(LASER, laser)
        laser.move_ip(laser_vel)

    lasers = [laser for laser in lasers if laser.bottom > 0]


# Create list of active asteroids
asteroids = []
asteroid_vel = (0, 3)
asteroid_probability = .01


def create_asteroid():
    global asteroids

    if random.uniform(0, 1) < asteroid_probability:
        location = Point(random.randint(0, SCREEN.w), 0)
        asteroids.append(pygame.Rect(location, ASTEROID_SIZE))


def draw_asteroids():
    global asteroids
    global lasers

    for asteroid in asteroids:
        screen.blit(ASTEROID, asteroid)
        asteroid.move_ip(asteroid_vel)

    for asteroid in list(asteroids):
        if asteroid.top > SCREEN.h:
            asteroids.remove(asteroid)
        hit_by = asteroid.collidelist(lasers)
        if hit_by >= 0:
            asteroids.remove(asteroid)
            lasers.remove(lasers[hit_by])

def main():
    # Start up a game clock. Used to control frame rate.
    clock = pygame.time.Clock()

    draws = [draw_ship, draw_lasers, draw_asteroids]

    # Run until the user asks to quit
    running = True
    while running:
        # Wait for the next clock tick
        clock.tick(FPS)

        # Look at every event in the queue
        for event in pygame.event.get():
            # Did the user hit a key?
            if event.type == pygame.KEYDOWN:
                # Was it the Escape key? If so, stop the loop.
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    create_laser()

            # Did the user click the window close button? If so, stop the loop.
            elif event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            ship_rect.move_ip(-ship_vel, 0)
        if keys[pygame.K_s]:
            ship_rect.move_ip(0, ship_vel)
        if keys[pygame.K_d]:
            ship_rect.move_ip(ship_vel, 0)
        if keys[pygame.K_w]:
            ship_rect.move_ip(0, -ship_vel)

        # Fill the background with black
        screen.fill(pygame.Color('black'))

        create_asteroid()

        # Draw things that are on the draw list
        for draw in draws:
            draw()

        # Flip the display
        pygame.display.flip()

    # Done! Time to quit.
    pygame.quit()


if __name__ == "__main__":
    main()
