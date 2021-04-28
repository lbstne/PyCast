
from sympy import symbols, Eq, solve, lambdify
from sympy.utilities.lambdify import lambdastr

x,y,z,t = symbols('x y z t')
a,b,c = symbols('a b c')
h,k,l,r = symbols('h k l r')

lineX = x + a*t
lineY = y + b*t
lineZ = z + c*t

eq_sphere = Eq((lineX - h)**2 + (lineY - k)**2 + (lineZ - l)**2, r**2)

print(solve(eq_sphere, t))