from math import sin, cos, sqrt, pi, acos

eps = 10**-4

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

    @staticmethod
    def distance(p1, p2):
        return sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)

    @staticmethod
    def midPoint(p1, p2):
        return Point((p1.x + p2.x)/2.0, (p1.y + p2.y)/2.0)

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

    @staticmethod
    def points2Line(p1, p2):
        A = p2.y - p1.y
        B = p1.x - p2.x
        C = (p2.x * p1.y) - (p1.x*p2.y)
        return Line(A, B, C)

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
            if abs((self.b * num) - other.b) < eps and abs((self.c * num) - other.c) < eps:
                return True
            else:
                return False
        elif self.b != 0:
            num = other.b / self.b
            if abs((self.c * num) - other.c) < eps:
                return True
            else:
                return False

    @staticmethod
    def point2LineDist(a, b, p, option=True):
        if option == True:
            ap = Vector.toVector(a, p)
            ab = Vector.toVector(a, b)
            # perpendicular proyection of p over line
            u = (Vector.dot(ap, ab)) / Vector.squareNorm(ab)
            # point perpendicularly under p
            c = Vector.translate(a, ab.scale(u))
            return Point.distance(p, c)

        if option == False:
            line1 = Line.points2Line(a, b)
            nv = Vector(line1.a, line1.b)
            p2 = Vector.translate(p, nv)
            line2 = Line.points2Line(p, p2)
            intersection = line2.intersects(line1)
            return Point.distance(p, intersection)

    @staticmethod
    def point2SegDist(a, b, p):
        ap = Vector.toVector(a, p)
        ab = Vector.toVector(a, b)
        u = (Vector.dot(ap, ab)) / Vector.squareNorm(ab)
        # if point is closest to a but outside ab
        if u < 0:
            return Point.distance(p, a)
        # if point is inside ab
        if u >= 0 and u <= 1:
            c = Vector.translate(a, ab.scale(u))
            return Point.distance(p, c)
        # if point is closest to b but outside ab
        if u > 1:
            return Point.distance(p, b)
    @staticmethod
    def perpPoint2Seg(a, b, p):
        ap = Vector.toVector(a, p)
        ab = Vector.toVector(a, b)
        u = (Vector.dot(ap, ab)) / Vector.squareNorm(ab)
        # if point is closest to a but outside ab
        if u < 0:
            return a
        # if point is inside ab
        if u >= 0 and u <= 1:
            c = Vector.translate(a, ab.scale(u))
            return c
        # if point is closest to b but outside ab
        if u > 1:
            return b

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return "<{X}, {Y}>".format(X=self.x, Y=self.y)

    def scale(self, s):
        return Vector((s * self.x), (s * self.y))

    @staticmethod
    def translate(p, v):
        return Point((p.x + v.x), (p.y + v.y))

    @staticmethod
    def toVector(p1, p2):
        return Vector((p2.x - p1.x), (p2.y - p1.y))

    @staticmethod
    def dot(u, v):
        return ((u.x * v.x) + (u.y * v.y))

    @staticmethod
    def cross(a, b):
        # returns the length of cross product vector
        return ((a.x * b.y) - (a.y * b.x))

    @staticmethod
    def squareNorm(v):
        return ((v.x * v.x) + (v.y * v.y))

    @staticmethod
    def angle(a, o, b, deg=False):
        oa = Vector.toVector(o, a)
        ob = Vector.toVector(o, b)
        theta = acos(Vector.dot(oa, ob) / sqrt(Vector.squareNorm(oa) * Vector.squareNorm(ob)))
        f = 1.0
        if deg == True:
            f = (180.0 / pi)
        return theta * f

    @staticmethod
    def ccw(p, q, r):
        pq = Vector.toVector(p, q)
        pr = Vector.toVector(p, r)
        return (Vector.cross(pq, pr) > 0)

    @staticmethod
    def areCollinear(p, q, r):
        pq = Vector.toVector(p, q)
        pr = Vector.toVector(p, r)
        return (abs(Vector.cross(pq, pr)) < eps)

xs = []
ys = []
polygons = int(input())
for p in range(polygons):
  values = str(input())
  coords = values.split(" ")
  for i in range(len(coords)):
    if int(i) % 2 == 0:
      xs.append(coords[i])
    else:
      ys.append(coords[i])
n = len(xs)

#Creating tuples list of points
tuples = []
for point in range(len(xs)):
  tuples.append(tuple([int(xs[point]),int(ys[point])]))

#Sorting tuples lexicographic
sorted_lex = sorted(tuples, key=lambda k: (k[0], k[1]))

# Convex Hull starts
L = []
U = []

for p in sorted_lex[:2]:
    U.append(Point(p[0], p[1]))

for i in range(2,n):
    U.append(Point(sorted_lex[i][0], sorted_lex[i][1]))
    while len(U) > 2 and Vector.ccw(U[len(U) - 2], U[len(U) - 1], U[len(U) - 3]):
      del U[len(U) - 2]

for p in reversed(sorted_lex[len(sorted_lex) - 2:]):
    L.append(Point(p[0], p[1]))

for i in range(n - 3, -1, -1):
    L.append(Point(sorted_lex[i][0], sorted_lex[i][1]))
    while len(L) > 2 and Vector.ccw(L[len(L) - 2], L[len(L) - 1], L[len(L) - 3]):
        del L[len(L) - 2]

del L[0]
del L[len(L) - 1]
CH = U + L
# Convex Hull ends

#Area of a convex polygon using Gauss Determinant: https://www.universoformulas.com/matematicas/geometria/area-pentagono-irregular/
area = 0.0
for i in range(len(CH)-1,-1,-1):
  if i == 0:
    area += (CH[i].x * CH[len(CH)-1].y) - (CH[i].y * CH[len(CH)-1].x)
  else:
    area += (CH[i].x * CH[i-1].y) - (CH[i].y * CH[i-1].x)

area = area / 2
print("{:0.2f}".format(area))
