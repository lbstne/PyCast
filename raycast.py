import pygame
from constants import *
from objects import Line, Material, Plane, Sphere
from vectors import Vector
from math import pi, sin, cos, asin
from random import uniform

def get_dir_vect(yaw, pitch): #yaw is left-right angle, pitch is angle from horizontal
    x = sin(yaw) * cos(pitch)
    y = sin(pitch)
    z = cos(yaw) * cos(pitch)

    return Vector(x, y, z).normalize()

def get_yaw_pitch(point):
    x,y,z = point

    pitch = asin(y)
    yaw = x/cos(pitch)

    return(yaw, pitch)

def get_color(point, object):
    material = object.get_material()
    material_color = material.get_color()

    brightness = object.get_normal(point).normalize().dot(LIGHT) * 255

    red = max(min(brightness * LIGHT_TEMP[0] * material_color[0], 255), 0)
    green = max(min(brightness * LIGHT_TEMP[1] * material_color[1], 255), 0)
    blue = max(min(brightness * LIGHT_TEMP[2] * material_color[2], 255), 0)

    return (red,green,blue)

def get_nearest_intersection(objects, line: Line, caster):
    intersections = []

    for object in objects:
        intersection = object.get_intersection(line)

        if intersection is not None and object is not caster:
            intersections.append((intersection, object))

    if len(intersections) == 0:
        return None

    intersection = sorted(intersections)[0]

    return intersection

def cast_ray(direction, pos, objects, caster, depth):
    ray = Line(direction, pos)

    intersection = get_nearest_intersection(objects, ray, caster)

    if intersection is None:
        return BKGD_COLOR

    collision = ray.get_point(intersection[0])
    object = intersection[1]

    material = object.get_material()
    material_color = material.get_color()

    brightness = object.get_normal(collision).normalize().dot(LIGHT) * 255
    shadow_ray = Line(LIGHT, Vector(*collision))

    obstruction = get_nearest_intersection(objects, shadow_ray, object)

    if not obstruction is None:
        brightness = 0

    if depth >= MAX_RECURSION_DEPTH:
        return (max(min(brightness * LIGHT_TEMP[0] * material_color[0], 255), 0), max(min(brightness * LIGHT_TEMP[1] * material_color[1], 255), 0), max(min(brightness * LIGHT_TEMP[2] * material_color[2], 255), 0))

    color = (brightness * LIGHT_TEMP[0] * material_color[0], brightness * LIGHT_TEMP[1] * material_color[1], brightness * LIGHT_TEMP[2] * material_color[2])

    roughness = material.get_roughness()
    
    reflect_dir = direction - 2*(object.get_normal(collision).normalize().dot(direction))*object.get_normal(collision).normalize()

    yaw, pitch = get_yaw_pitch(reflect_dir.get_coords())

    yaw += uniform(-pi*0.5, pi*0.5)*roughness
    pitch += uniform(-pi*0.5, pi*0.5)*roughness

    reflect_dir = get_dir_vect(yaw, pitch)

    if not material.get_reflectivity() == 0:
        reflect_color = cast_ray(reflect_dir, Vector(*collision), objects, object, depth + 1) 
    else:
        reflect_color = (0,0,0)

    red = max(min(reflect_color[0]*material.get_reflectivity()*material_color[0] + color[0]*(1 - material.get_reflectivity()), 255), 0)
    green = max(min(reflect_color[1]*material.get_reflectivity()*material_color[1] + color[1]*(1 - material.get_reflectivity()), 255), 0)
    blue = max(min(reflect_color[2]*material.get_reflectivity()*material_color[2] + color[2]*(1 - material.get_reflectivity()), 255), 0)

    return (red, green, blue)


def cast_rays(start_pos, start_angle, objects, width_res, height_res, pixels_per_ray, window):
    start_yaw = start_angle[0]
    start_pitch = start_angle[1]

    for y in range(height_res):  
        pitch = Y_FOV/2 - y * (Y_FOV / (height_res- 1)) + start_pitch

        for x in range(width_res):
            yaw = X_FOV/2 - x * (X_FOV / (width_res - 1)) + start_yaw

            pos = start_pos
            direction = get_dir_vect(yaw, pitch)

            color = cast_ray(direction, pos, objects, None, 1)

            x_pos = x*pixels_per_ray
            y_pos = y*pixels_per_ray

            pygame.draw.rect(window, color, ((x_pos, y_pos), (pixels_per_ray, pixels_per_ray)))