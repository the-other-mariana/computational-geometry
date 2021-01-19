from math import sin, cos, sqrt, pi

eps = 10**-4

def distance(p1, p2):
    return sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

def points2Line(p1, p2):
    A = p2.y - p1.y
    B = p1.x - p2.x
    C = (p2.x * p1.y) - (p1.x*p2.y)
    return Line(A, B, C)

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return (abs(self.x - other.x) < eps) and (abs(self.y - other.y) < eps)

    def __repr__(self):
        return f"({self.x}, {self.y})"

    def __str__(self):
        return "({x}, {y})".format(x=self.x, y=self.y)

    def rotate(self, deg):
        return Point(self.x * cos(deg * pi/180) - self.y * sin(deg * pi/180), self.x * sin(deg * pi/180) + self.y * cos(deg * pi/180))

class Line:
    def __init__(self, a=0, b=0, c=0):
        self.a = a
        self.b = b
        self.c = c

    def __str__(self):
        return "{A}x + {B}y + {C} = 0".format(A=self.a, B=self.b, C=self.c)

d = 1.4142
theta = 45
p1 = Point(1, 1)
p2 = Point(p1.x + d * cos(theta * pi / 180), p1.y + d * sin(theta * pi / 180)) # (1.9999, 1.9999)
p3 = Point(2, 2)

# POINTS
print(p2 == p3)
print(p2)
print(distance(p1, p3)) # 1.4142
print(p1.rotate(90))

# LINES
p1 = Point(0,0)
p2 = Point(1,1)
print(points2Line(p1, p2))
