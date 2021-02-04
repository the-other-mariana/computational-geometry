from glibrary import Point, Line, Vector, eps
import matplotlib.pyplot as plt
from matplotlib import collections  as mc


cont = 0
n = int(input())
pts = []
tuples = []
x = []
y = []
for i in range(n):
    row = str(input()).split()
    newPoint = Point(int(row[0]), int(row[1]))
    pts.append(newPoint)
    tuples.append(tuple([newPoint.x,newPoint.y]))
    x.append(newPoint.x)
    y.append(newPoint.y)

sorted_lex = sorted(tuples, key=lambda k: (k[0], k[1]))
print("sorted ", sorted_lex)

L = []
U = []
ch_segs = []
x2 = []
y2 = []
x2 = [tup[0] for tup in sorted_lex]
y2 = [tup[1] for tup in sorted_lex]

def paint(x2, y2, x, y, cont):
    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()
    ax1.scatter(x2,y2, s=100, marker="x")
    ax1.scatter(x,y, s=100, marker="o", color="red")
    ax1.plot(x,y, color="red")
    plt.savefig("test_{c}.png".format(c=cont),bbox_inches='tight')



for p in sorted_lex[:2]:
    U.append(Point(p[0], p[1]))
    xs = [p.x for p in U]
    ys = [p.y for p in U]
    cont += 1
    paint(x2, y2, xs, ys, cont)

print(U)

for i in range(2,n):
    U.append(Point(sorted_lex[i][0], sorted_lex[i][1]))
    xs = [p.x for p in U]
    ys = [p.y for p in U]
    cont += 1
    paint(x2, y2, xs, ys, cont)

    while len(U) > 2 and Vector.ccw(U[len(U) - 2], U[len(U) - 1], U[len(U) - 3]):
      del U[len(U) - 2]
      xs = [p.x for p in U]
      ys = [p.y for p in U]
      cont += 1
      paint(x2, y2, xs, ys, cont)

for p in reversed(sorted_lex[len(sorted_lex) - 2:]):
    L.append(Point(p[0], p[1]))
    xs = [p.x for p in (U + L)]
    ys = [p.y for p in (U + L)]
    cont += 1
    paint(x2, y2, xs, ys, cont)

print(L)

for i in range(n - 3, -1, -1):
    L.append(Point(sorted_lex[i][0], sorted_lex[i][1]))
    xs = [p.x for p in (U + L)]
    ys = [p.y for p in (U + L)]
    cont += 1
    paint(x2, y2, xs, ys, cont)
    while len(L) > 2 and Vector.ccw(L[len(L) - 2], L[len(L) - 1], L[len(L) - 3]):
        del L[len(L) - 2]
        xs = [p.x for p in (U + L)]
        ys = [p.y for p in (U + L)]
        cont += 1
        paint(x2, y2, xs, ys, cont)


del L[0]

del L[len(L) - 1]
CH = U + L
print("Convex Hull points: ", CH)
xs = [p.x for p in CH]
ys = [p.y for p in CH]
cont += 1
paint(x2, y2, xs, ys, cont)

for i in range(len(CH)):
    ch_segs.append([tuple([CH[i].x, CH[i].y]), tuple([CH[(i + 1) % len(CH)].x, CH[(i + 1) % len(CH)].y])])
    if i == len(CH) - 1:
        xs.append(CH[(i + 1) % len(CH)].x)
        ys.append(CH[(i + 1) % len(CH)].y)
        cont += 1
        paint(x2, y2, xs, ys, cont)

# PLOTTING
x = [p.x for p in CH]
y = [p.y for p in CH]
