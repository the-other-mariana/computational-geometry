from glibrary import Point, Line, Vector, eps
import matplotlib.pyplot as plt

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

x2 = []
y2 = []
x2 = [tup[0] for tup in sorted_lex]
y2 = [tup[1] for tup in sorted_lex]

for p in sorted_lex[:2]:
    U.append(Point(p[0], p[1]))

print(U)

for i in range(2,n):
    U.append(Point(sorted_lex[i][0], sorted_lex[i][1]))
    while len(U) > 2 and Vector.ccw(U[len(U) - 2], U[len(U) - 1], U[len(U) - 3]):
      del U[len(U) - 2]

for p in reversed(sorted_lex[len(sorted_lex) - 2:]):
    L.append(Point(p[0], p[1]))

print(L)

for i in range(n - 3, 0, -1):
    L.append(Point(sorted_lex[i][0], sorted_lex[i][1]))
    while len(L) > 2 and Vector.ccw(L[len(L) - 2], L[len(L) - 1], L[len(L) - 3]):
        del L[len(L) - 2]

del L[0]
del L[len(L) - 1]
CH = U + L
print("Convex Hull points: ", CH)

# PLOTTING
x = [p.x for p in CH]
y = [p.y for p in CH]

fig = plt.figure()
fig.add_subplot()
ax1 = plt.gca()


ax1.scatter(x2,y2, s=100, marker="x")
ax1.scatter(x,y, s=100, marker="o", color="red")
plt.show()
