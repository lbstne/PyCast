import pygame
from constants import *
from objects import Line, Material, Plane, RectangularPrism, Sphere
from vectors import Vector
from math import pi, sin, cos

pygame.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))


'''floor = Plane(Vector(1,0,0), Vector(0,0,1), Vector(0,0,0), 1, 1, Material(1,0.5,1, (0.9,0.9,0.9)))
roof = Plane(Vector(0,0,1), Vector(1,0,0), Vector(0,1,0), 1, 1, Material(1,0.5,1, (0.9,0.9,0.9)))
back = Plane(Vector(1,0,0), Vector(0,1,0), Vector(0,0.5,-0.5), 1, 1, Material(1,0.5,1, (0.9,0.9,0.9)))
front = Plane(Vector(0,1,0), Vector(1,0,0), Vector(0,0.5,0.5), 1, 1, Material(1,1,1, (0.9,0.9,0.9)))
left = Plane(Vector(0,0,-1), Vector(0,1,0), Vector(0.5,0.5,0), 1, 1, Material(1,0.5,1, (0.9,0.9,0.9)))
right = Plane(Vector(0,0,1), Vector(0,1,0), Vector(-0.5,0.5,0), 1, 1, Material(1,0.5,1, (0.9,0.9,0.9)))'''

#cube = RectangularPrism(2, 1, 5, Vector(0,0.5,0), Material(1,0,1, (1,1,1)))

ground = Plane(Vector(0,0,1), Vector(1,0,0), Vector(0,0,0),100, 100, Material(1,0,1, (0,1,0)))
sphere = Sphere(1, Vector(3,1,0), Material(1,0,1, (1,1,1)))

objects = [ground, sphere]

def get_dir_vect(yaw, pitch): #yaw is left-right angle, pitch is angle from horizontal
    x = sin(yaw) * cos(pitch)
    y = sin(pitch)
    z = cos(yaw) * cos(pitch)

    return Vector(x, y, z).normalize()

def cast_ray(direction, pos, objects, caster, depth):
    ray = Line(direction, pos)
    intersections = []

    for object in objects:
        intersection = object.get_intersection(ray)

        if intersection is not None and object is not caster:
            intersections.append((intersection, object))

    #Find the closest intersection
    if not len(intersections) == 0:
        collision = intersections[0][0]
        object = intersections[0][1]

        for intersection in intersections:
            if (Vector(*intersection[0]) - pos).get_mag() < (Vector(*collision) - pos).get_mag():
                collision = intersection[0]
                object = intersection[1]

        material = object.get_material()
        material_color = material.get_color()

        diffuse_brightness = object.get_normal(collision).normalize().dot(LIGHT) * 255

        shadow_ray = Line(LIGHT, Vector(*collision))

        if depth >= MAX_RECURSION_DEPTH:
            return (max(min(diffuse_brightness * LIGHT_TEMP[0] * material_color[0], 255), 0), max(min(diffuse_brightness * LIGHT_TEMP[1] * material_color[1], 255), 0), max(min(diffuse_brightness * LIGHT_TEMP[2] * material_color[2], 255), 0))

        for obstruction in objects:
            if obstruction.get_intersection(shadow_ray) is not None and obstruction is not object:
                diffuse_brightness = 0
                break

        diffuse_color = (diffuse_brightness * LIGHT_TEMP[0] * material_color[0], diffuse_brightness * LIGHT_TEMP[1] * material_color[1], diffuse_brightness * LIGHT_TEMP[2] * material_color[2])

        reflect_dir = direction - 2*(object.get_normal(collision).normalize().dot(direction))*object.get_normal(collision).normalize()

        if not material.get_reflectivity() == 0:
            reflect_color = cast_ray(reflect_dir, Vector(*collision), objects, object, depth + 1) 
        else:
            reflect_color = (0,0,0)

        red = max(min(reflect_color[0]*material.get_reflectivity()*material_color[0] + diffuse_color[0]*(1 - material.get_reflectivity()), 255), 0)
        green = max(min(reflect_color[1]*material.get_reflectivity()*material_color[1] + diffuse_color[1]*(1 - material.get_reflectivity()), 255), 0)
        blue = max(min(reflect_color[2]*material.get_reflectivity()*material_color[2] + diffuse_color[2]*(1 - material.get_reflectivity()), 255), 0)

        return (red, green, blue)

    return BKGD_COLOR

def cast_rays(start_pos, start_angle):
    start_yaw = start_angle[0]
    start_pitch = start_angle[1]

    for y in range(HEIGHT // PIXELS_PER_RAY):
        pitch = Y_FOV/2 - y * (Y_FOV / (HEIGHT / PIXELS_PER_RAY - 1)) + start_pitch

        for x in range(WIDTH // PIXELS_PER_RAY):
            yaw = X_FOV/2 - x * (X_FOV / (HEIGHT / PIXELS_PER_RAY - 1)) + start_yaw

            pos = start_pos

            direction = get_dir_vect(yaw, pitch)

            color = cast_ray(direction, pos, objects, None, 1)

            x_pos = x*PIXELS_PER_RAY
            y_pos = y*PIXELS_PER_RAY

            pygame.draw.rect(window, color, ((x_pos, y_pos), (PIXELS_PER_RAY, PIXELS_PER_RAY)))

camera_pos = Vector(0,0.5,-2)
camera_angle =[0,0]

window.fill(BKGD_COLOR)
cast_rays(camera_pos, camera_angle)

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
        cast_rays(camera_pos, camera_angle)

    if keys[pygame.K_c]:
        PIXELS_PER_RAY //= 5
        MAX_RECURSION_DEPTH *= 2
        cast_rays(camera_pos, camera_angle)
        PIXELS_PER_RAY *= 5
        MAX_RECURSION_DEPTH //= 2
