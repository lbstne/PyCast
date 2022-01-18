# Example Scene to show case the capacities of the raytracing engine
# Two metallic spheres on a rough surface enclosed by two parallel mirrors

import pygame
from constants import *
from render import *
from raycast import *

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))

#cube = RectangularPrism(2, 1, 5, Vector(0,0.5,0), Material(1,0,1, (1,1,1)))

gold = Material(1,0.9,1,0, (1,0.75,0.4))
silver = Material(1,0.8,1,0, (0.9,1,0.9))
stone = Material(1,0.1,1,0.9, (0.95,1,0.95))
copper = Material(1,0.8,1,0, (1, 0.5, 0.28))

left = Plane(Vector(0,0,-1), Vector(0,1,0), Vector(2,0.5,0), 5, 5, silver)
right = Plane(Vector(0,0,-1), Vector(0,1,0), Vector(-2,0.5,0), 5, 5, silver)
ground = Plane(Vector(0,0,1), Vector(1,0,0), Vector(0,0,0),100, 100, stone)
copper_sphere = Sphere(1, Vector(0,1,0), copper)
gold_sphere = Sphere(0.5, Vector(-1.5,0.5,0), gold)

objects = [ground, gold_sphere, copper_sphere, left, right]

camera_pos = Vector(0,0.5,-2)
camera_angle =[0,0]

window.fill(BKGD_COLOR)
cast_rays(camera_pos, camera_angle, objects, WIDTH // PIXELS_PER_RAY, HEIGHT // PIXELS_PER_RAY, PIXELS_PER_RAY, window)


while True:
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    has_moved = False

    keys = pygame.key.get_pressed()
        
    if keys[pygame.K_SPACE]:
        camera_pos = camera_pos + Vector(0,1,0)
        has_moved = True
    elif keys[pygame.K_LSHIFT]:
        camera_pos = camera_pos + Vector(0,-1,0)
        has_moved = True

    if keys[pygame.K_d]:
        camera_pos = camera_pos + get_dir_vect(camera_angle[0], camera_angle[1]).cross(Vector(0,1,0))
        has_moved = True
    elif keys[pygame.K_a]:
        camera_pos = camera_pos - get_dir_vect(camera_angle[0], camera_angle[1]).cross(Vector(0,1,0))
        has_moved = True

    if keys[pygame.K_w]:
        camera_pos = camera_pos + get_dir_vect(camera_angle[0], camera_angle[1])
        has_moved = True
    elif keys[pygame.K_s]:
        camera_pos = camera_pos - get_dir_vect(camera_angle[0], camera_angle[1])
        has_moved = True

    if keys[pygame.K_RIGHTBRACKET]:
        Y_FOV += pi/8
        has_moved = True
    elif keys[pygame.K_LEFTBRACKET]:
        Y_FOV -= pi/8
        has_moved = True

    if keys[pygame.K_RIGHT]:
        camera_angle[0] -= pi/8
        has_moved = True
    if keys[pygame.K_LEFT]:
        camera_angle[0] += pi/8
        has_moved = True

    if keys[pygame.K_UP]:
        camera_angle[1] += pi/8
        has_moved = True
    if keys[pygame.K_DOWN]:
        camera_angle[1] -= pi/8
        has_moved = True

    if keys[pygame.K_EQUALS]:
        X_FOV += pi/8
        has_moved = True
    elif keys[pygame.K_MINUS]:
        X_FOV -= pi/8
        has_moved = True

    if has_moved:
        window.fill(BKGD_COLOR)
        cast_rays(camera_pos, camera_angle, objects, WIDTH // PIXELS_PER_RAY, HEIGHT // PIXELS_PER_RAY, PIXELS_PER_RAY, window)

    if keys[pygame.K_c]:
        PIXELS_PER_RAY //= 5
        cast_rays(camera_pos, camera_angle, objects, WIDTH // PIXELS_PER_RAY, HEIGHT // PIXELS_PER_RAY, PIXELS_PER_RAY, window)
        PIXELS_PER_RAY *= 5