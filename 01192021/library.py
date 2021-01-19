from math import sin, cos, sqrt, pi

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

d = 1.4142
theta = 45
p1 = Point(1, 1)
p2 = Point(p1.x + d * cos(theta * pi / 180), p1.y + d * sin(theta * pi / 180)) # (1.9999, 1.9999)
p3 = Point(2, 2)

print(p2 == p3)
print(p2)
#print("({x}, {y})".format(x=p2.x, y=p2.y))
