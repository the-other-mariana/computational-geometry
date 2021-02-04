from glibrary import Point, Vector, Line, eps
import math

n = int(input())
pts = []
tuples = []
x = []
y = []
for i in range(n):
    row = str(input()).split()
    newPoint = Point(float(row[0]), float(row[1]))
    pts.append(newPoint)
    tuples.append(tuple([newPoint.x,newPoint.y]))
    x.append(newPoint.x)
    y.append(newPoint.y)

sorted_lex = sorted(tuples, key=lambda k: (k[0], k[1]))

L = []
U = []
ch_segs = []
x2 = []
y2 = []
x2 = [tup[0] for tup in sorted_lex]
y2 = [tup[1] for tup in sorted_lex]

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
print("Convex Hull points: ", CH)

pivot = CH[0]
pair = Point(0,0)
max_dist = 0
for i in range(1, len(CH)):
    if i == 1:
        max_dist = Point.distance(pivot, CH[i])
        pair = CH[i]
    if Point.distance(pivot, CH[i]) > max_dist:
        max_dist = Point.distance(pivot, CH[i])
        pair = CH[i]
dx = abs(pair.x - pivot.x)
dy = abs(pair.y - pivot.y)
c = math.sqrt(dx**2 + dy**2) # same as max_dist
print(str(round(c, 2)))
