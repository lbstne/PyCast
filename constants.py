from math import pi
from vectors import Vector


FRAMERATE = 60
WIDTH = 1000
HEIGHT = 1000

PIXELS_PER_RAY = 15

LIGHT = Vector(1,1,-1.5).normalize()
LIGHT_TEMP = (1,1,0.9)

SHADOW_BRIGHTNESS = 0.2
SHADOW_TEMP = (0.8,0.9,1)

BKGD_COLOR = (30,30,100)

Y_FOV = pi*0.5 #90 deg.
X_FOV = pi*0.5 #90 deg.

MAX_RECURSION_DEPTH = 6