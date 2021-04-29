from re import M
from constants import X_FOV
from vectors import Vector

class Material:
    def __init__(self, opacity, reflectivity, refraction, color):
        self.opacity = opacity
        self.reflectivity = reflectivity
        self.refraction = refraction
        self.color = color

    def get_opacity(self):
        return self.opacity

    def get_reflectivity(self):
        return self.reflectivity

    def get_refraction(self):
        return self.refraction

    def get_color(self):
        return self.color

class Line:
    def __init__(self, direction: Vector, pos: Vector):
        self.direction = direction
        self.pos = pos

    def get_pos(self):
        return self.pos

    def get_dir(self):
        return self.direction

    def get_point(self, increment):
        return (self.pos + (increment * self.direction)).get_coords()

class Object:
    def __init__(self, pos: Vector, material: Material):
        self.pos = pos
        self.material = material

    def get_material(self):
        '''Returns the material of the object'''
        return self.material

    def contains(self, point):
        '''Returns true if the given point is contained within the object, otherwise it returns false.'''
        pass

    def get_normal(self, point):
        '''Returns the normal vector of the object at the given point.'''
        pass

    def get_intersection(self, line: Line):
        '''
        Returns the t value of the closest intersection between a given line and the object.
        
        t is the smallest postive real number and r is a point on both the line and object
        for the line 'r = r_0 + tm', where r and r_0 are points on the line and m is a direction vector.
        '''
        pass


class Sphere(Object):
    def __init__(self, radius, pos: Vector, material: Material):
        super(Sphere, self).__init__(pos, material)
        self.radius = radius

    def contains(self, point):
        x,y,z = point

        return Vector(x,y,z).get_mag() <= self.radius

    def get_normal(self, point):
        x,y,z = point
        h,k,l = self.pos.get_coords()
        return Vector(x-h,y-k,z-l)

    def get_intersection(self, line: Line):
        x,y,z = line.get_pos().get_coords()
        a,b,c = line.get_dir().get_coords()
        h,k,l = self.pos.get_coords()
        r = self.radius

        t_vals = [(a*h - a*x + b*k - b*y + c*l - c*z - (-a**2*k**2 + 2*a**2*k*y - a**2*l**2 
        + 2*a**2*l*z + a**2*r**2 - a**2*y**2 - a**2*z**2 + 2*a*b*h*k - 2*a*b*h*y 
        - 2*a*b*k*x + 2*a*b*x*y + 2*a*c*h*l - 2*a*c*h*z - 2*a*c*l*x + 2*a*c*x*z 
        - b**2*h**2 + 2*b**2*h*x - b**2*l**2 + 2*b**2*l*z + b**2*r**2 - b**2*x**2 
        - b**2*z**2 + 2*b*c*k*l - 2*b*c*k*z - 2*b*c*l*y + 2*b*c*y*z - c**2*h**2 
        + 2*c**2*h*x - c**2*k**2 + 2*c**2*k*y + c**2*r**2 - c**2*x**2 - c**2*y**2)**0.5)/(a**2 + b**2 + c**2), 
        (a*h - a*x + b*k - b*y + c*l - c*z + (-a**2*k**2 + 2*a**2*k*y - a**2*l**2 
        + 2*a**2*l*z + a**2*r**2 - a**2*y**2 - a**2*z**2 + 2*a*b*h*k - 2*a*b*h*y 
        - 2*a*b*k*x + 2*a*b*x*y + 2*a*c*h*l - 2*a*c*h*z - 2*a*c*l*x + 2*a*c*x*z 
        - b**2*h**2 + 2*b**2*h*x - b**2*l**2 + 2*b**2*l*z + b**2*r**2 - b**2*x**2 
        - b**2*z**2 + 2*b*c*k*l - 2*b*c*k*z - 2*b*c*l*y + 2*b*c*y*z - c**2*h**2 + 2*c**2*h*x 
        - c**2*k**2 + 2*c**2*k*y + c**2*r**2 - c**2*x**2 - c**2*y**2)**0.5)/(a**2 + b**2 + c**2)]

        intersections = [t for t in t_vals if not type(t) is complex and t > 0]

        if len(intersections) == 0:
            return None
        else:
            return min(intersections)

        ''' sympy code for generating the expression to calculate the intersections of the line and sphere
        
        from sympy import symbols, Eq, solve, lambdify
        from sympy.utilities.lambdify import lambdastr

        x,y,z,t = symbols('x y z t')
        a,b,c = symbols('a b c')
        h,k,l,r = symbols('h k l r')

        lineX = x + a*t
        lineY = y + b*t
        lineZ = z + c*t

        eq_sphere = Eq((lineX - h)**2 + (lineY - k)**2 + (lineZ - l)**2, r**2)

        solve(eq_sphere, t)'''
                 
class Plane(Object):
    def __init__(self, dir1: Vector, dir2: Vector, pos: Vector, length, width, material: Material):
        super(Plane, self).__init__(pos, material)
        self.dir1 = dir1.normalize()
        self.dir2 = dir2.normalize()
        self.pos = pos
        self.length = length
        self.width = width
        self.material = material

    def get_normal(self, point):
        return self.dir1.cross(self.dir2)

    def get_translation(self):
        A,B,C = self.get_normal((0,0,0)).get_coords()
        x,y,z = self.pos.get_coords()

        return -(A*x + B*y + C*z)

    def contains(self, point):
        A,B,C = self.get_normal((0,0,0)).get_coords()
        D = self.get_translation()
        x,y,z = point

        if A*x + B*y + C*y + D == 0:
            return True
        else:
            return False

        

    def get_intersection(self, line):
        x,y,z = line.get_pos().get_coords()
        a,b,c = line.get_dir().get_coords()
        A,B,C = self.get_normal((0,0,0)).get_coords()
        D = self.get_translation()

        try:
            m = -(A*x + B*y + C*z + D) / (A*a + B*b + C*c)
        except:
            return None

        if type(m) is complex:
            return None

        point = Vector(*line.get_point(m))

        dir1 = self.dir1
        dir2 = self.dir2

        pos = self.pos

        dist_dir1 = (dir1.cross(point - pos)).get_mag() / dir1.get_mag()
        dist_dir2 = (dir2.cross(point - pos)).get_mag() / dir2.get_mag()

        '''a1, a2, a3 = self.dir1.get_coords()
        b1, b2, b3 = self.dir2.get_coords()

        s = (y*b1 - x*b2) / (a2*b1 - a1*b2)
        t = (x - s*a1) / b1'''

        if m > 0 and dist_dir1 <= self.width/2 and dist_dir2 <= self.length/2:
            return m
        else:
            return None

class RectangularPrism:
    def __init__(self, length, width, height, pos: Vector, material: Material):
        self.length = length
        self.width = width
        self.height = height
        self.pos = pos
        self.material = material

    def get_pos(self):
        return self.pos
    
    def get_material(self):
        return self.material

    def get_planes(self):

        x,y,z = self.pos.get_coords()

        top = Plane(Vector(0,0,1), Vector(1,0,0), Vector(x,y + self.height*0.5,z), self.width, self.length, self.material)
        bottom = Plane(Vector(1,0,0), Vector(0,0,1), Vector(x,y - self.height*0.5,z), self.length, self.width, self.material)
        front = Plane(Vector(1,0,0), Vector(0,1,0), Vector(x,y,z + self.length*0.5), self.height, self.width, self.material)
        back = Plane(Vector(0,1,0), Vector(1,0,0), Vector(x,y,z - self.length*0.5), self.width, self.height, self.material)
        left = Plane(Vector(0,0,1), Vector(0,1,0), Vector(x - 0.5*self.width,y,z), self.length, self.height, self.material)
        right = Plane(Vector(0,1,0), Vector(0,0,1), Vector(x + 0.5*self.width,y,z), self.height, self.width, self.material)

        return (top, bottom, front, back, left, right)

    def get_intersection(self, line):
        faces = self.get_planes()
        intersections = []

        for face in faces: 
            intersection = face.get_intersection(line)
            if intersection is not None:
                intersections.append((intersection, face))

        if not len(intersections) == 0:
            collision = intersections[0][0]

            for intersection in intersections:
                if (Vector(*intersection[0]) - line.get_pos()).get_mag() < (Vector(*collision) - line.get_pos()).get_mag():
                    collision = intersection[0]

            return collision
        else:
            return None

    def get_normal(self, point):
        faces = self.get_planes()

        for face in faces:
            if face.contains(point):
                return face.get_normal(point)

        return Vector(1,1,1)

        