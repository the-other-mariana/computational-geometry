from glibrary import eps, Point, Line, Vector
from math import sin, cos, pi 

# TESTS
d = 1.4142
theta = 45
p1 = Point(1, 1)
p2 = Point(p1.x + d * cos(theta * pi / 180), p1.y + d * sin(theta * pi / 180)) # (1.9999, 1.9999)
p3 = Point(2, 2)

# POINTS
print(p2 == p3)
print(p2)
print("Point distance:", Point.distance(p1, p3)) # 1.4142
print("Point rotation:", p1.rotate(90))

# LINE FROM 2 POINTS
p1 = Point(2,2)
p2 = Point(2,4)
line1 = Line.points2Line(p1, p2)
print("Line from 2 points:", line1)

# CHECK PARALLEL LINES
p3 = Point(4,1)
p4 = Point(4,3)
line2 = Line.points2Line(p3, p4)
print("Is Paralel:", line1.isParallelTo(line2))

# CHECK INTERSECTION
line1 = Line.points2Line(Point(0, 0), Point(1, 1))
line2 = Line.points2Line(Point(1, 0), Point(1, 2))

line1 = Line.points2Line(Point(15, 10), Point(49, 25))
line2 = Line.points2Line(Point(29, 5), Point(32, 32))
print("Intersection:", line1.intersects(line2))

# CHECK EQUIVALENT
line1 = Line(1, 2, 3)
line2 = Line(2, 4, 6)
print("Equivalent:", line1.isEquivalent(line2))
print("Equivalent:", line2.isEquivalent(line1))

# CHECK VECTOR FROM POINTS
p1 = Point(2, 3)
p2 = Point(10, 7)
print("Points to Vector:", Vector.toVector(p1, p2))

# CHECK DISTANCE FROM POINT TO LINE
p = Point(2, 3)
a = Point(0, 1.0/4.0)
b = Point(-1.0/3.0, 0)
print("Distance point to line:", Line.point2LineDist(a, b, p, True))
