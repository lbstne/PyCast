class Vector: 
    def __init__(self, x, y, z):
        self.comp = (x, y, z) #the x, y and z components of the vector

    def __add__(self, other):
        ax, ay, az = self.comp
        bx, by, bz = other.comp

        return Vector(ax + bx, ay + by, az + bz)

    def __mul__(self, other: int): #scalar multiplication w/ vector
        x, y, z = self.comp

        return Vector(x * other, y * other, z * other)

    def __rmul__(self, other):
        return self * other

    def __sub__(self, other):
        return self.__add__(other * -1)

    def __str__(self) -> str: #returns a string in the form '(x, y, z)'
        x,y,z = self.comp

        return "(" + str(x) + ", " + str(y)+ ", " + str(z) + ")"

    def cross(self, vec): #vector product
        ax, ay, az = self.comp
        bx, by, bz = vec.comp

        rx = ay*bz - az*by
        ry = az*bx - ax*bz
        rz = ax*by - ay*bx

        return Vector(rx, ry, rz)

    def dot(self, vec): #scalar product
        ax, ay, az = self.comp
        bx, by, bz = vec.comp

        return ax*bx + ay*by + az*bz

    def get_coords(self):
        return self.comp

    def normalize(self):
        return (1/self.get_mag()) * self

    get_unit_vect = normalize
    
    def get_mag(self):
        x, y, z = self.comp

        return (x**2 + y**2 + z**2)**0.5

    