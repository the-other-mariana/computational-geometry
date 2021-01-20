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
        self.a = a * 1.0
        self.b = b * 1.0
        self.c = c * 1.0
        if b == 0:
            self.slope = 1000000.0
        else:
            self.slope = -1 * ((a * 1.0) / b)

    def __str__(self):
        return "{A}x + {B}y + {C} = 0".format(A=self.a, B=self.b, C=self.c)

    def isParallelTo(self, other):
        return (self.slope - other.slope) < eps

    def intersects(self, other):
        denom = (self.a * other.b) - (other.a * self.b)
        if denom == 0:
            return False
        else:
            x = ((other.c * self.b) - (self.c * other.b)) / denom
            y = ((self.a * other.c) - (other.a * self.c)) / ((other.a * self.b) - (self.a * other.b))
            return Point(x, y)

    def isEquivalent(self, other):
        if self.a != 0:
            num = other.a / self.a
            if ((self.b * num) == other.b) and ((self.c * num) == other.c):
                return True
        elif self.b != 0:
            num = other.b / self.b
            if ((self.c * num) == other.c):
                return True
        else:
            return False


d = 1.4142
theta = 45
p1 = Point(1, 1)
p2 = Point(p1.x + d * cos(theta * pi / 180), p1.y + d * sin(theta * pi / 180)) # (1.9999, 1.9999)
p3 = Point(2, 2)

# POINTS
print(p2 == p3)
print(p2)
print("Point distance:", distance(p1, p3)) # 1.4142
print("Point rotation:", p1.rotate(90))

# LINE FROM 2 POINTS
p1 = Point(3,0)
p2 = Point(3,1)
line1 = points2Line(p1, p2)
print("Line from 2 points:", line1)

# CHECK PARALLEL LINES
p3 = Point(4,1)
p4 = Point(4,3)
line2 = points2Line(p3, p4)
print("Is Paralel:", line1.isParallelTo(line2))

# CHECK INTERSECTION
line1 = points2Line(Point(0, 0), Point(1, 1))
line2 = points2Line(Point(1, 0), Point(1, 2))

line1 = points2Line(Point(15, 10), Point(49, 25))
line2 = points2Line(Point(29, 5), Point(32, 32))
print("Intersection:", line1.intersects(line2))

# CHECK EQUIVALENT
line1 = Line(1, 2, 3)
line2 = Line(2, 4, 6)
print("Equivalent:", line1.isEquivalent(line2))
print("Equivalent:", line2.isEquivalent(line1))
