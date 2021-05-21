from glibrary import Point
import math
from matplotlib import pyplot as plt
import numpy as np

gap = 20

def getParabolaCoeff(f, d):
    a = 1.0 / (2 * (f.y - d))
    b = (-1.0 * 2 * f.x) / (2 * (f.y - d))
    c = ((f.x * f.x) + (f.y * f.y) - (d * d)) / (2.0 * (f.y - d))
    return a, b, c

def findIntersect(a1, b1, c1, a2, b2, c2):
    a = a1 - a2
    b = b1 - b2
    c = c1 - c2

    inner_calc = b ** 2 - 4 * a * c

    # Check if `inner_cal` is negative. If so, there are no real solutions.
    # Thus, return the empty list.
    if inner_calc < 0:
        return []

    square = math.sqrt(inner_calc)
    double_a = 2 * a
    answers = [(-b - square) / double_a, (-b + square) / double_a]

    return answers

fig = plt.figure()
fig.add_subplot()
ax1 = plt.gca()

yValue = -0.2
input1 = [Point(-3, 15), Point(10, 10), Point(4,1), Point(-3,15), Point(14,0), Point(-3,15)]
xs = [p.x for p in input1]
ys = [p.y for p in input1]

ax1.scatter(xs, ys, s=20, zorder=10, color='blue')
xMin, xMax = min(input1, key=lambda p: p.x).x, max(input1, key=lambda p: p.x).x
yMin, yMax = min(input1, key=lambda p: p.y).y, max(input1, key=lambda p: p.y).y
plt.setp(ax1, xlim=(xMin - gap, xMax + gap), ylim=(yMin - gap, yMax + gap))

# plot sweep line
xlim = ax1.get_xlim()
ylim = ax1.get_ylim()
ax1.plot(list(xlim), [yValue, yValue], color="black")
xp = list(np.linspace(xlim[0], xlim[1], 100))
yps = []
for p in input1:
    yp = []
    for x in xp:
        try:
            y = ((x - p.x) ** 2 + (p.y) ** 2 - (yValue) ** 2) / (2 * (p.y - yValue))
            yp.append(y)
        except ZeroDivisionError:
            y = math.inf
            yp.append(y)
    ax1.plot(xp, yp, lw=2)
    yps.append(yp)

a1, b1, c1 = getParabolaCoeff(input1[0], yValue)
a2, b2, c2 = getParabolaCoeff(input1[1], yValue)

xhits = findIntersect(a1, b1, c1, a2, b2, c2)
yhits = [a1*x*x + b1*x + c1 for x in xhits]

ax1.scatter(xhits, yhits, s=20, zorder=10, color='red')
print(xhits)
print(yhits)

bl = []
curr_hit = 0
curr_p = 0
by = []
for x in xp:
    xComp = 0
    if curr_hit >= len(xhits):
        xComp = 10000000
    else:
        xComp = xhits[curr_hit]
    if x > xComp:
        curr_hit += 1
        curr_p += 1
    y = 0
    try:
        y = ((x - input1[curr_p % len(yps)].x) ** 2 + (input1[curr_p % len(yps)].y) ** 2 - (yValue) ** 2) / (2 * (input1[curr_p % len(yps)].y - yValue))
    except ZeroDivisionError:
        y = math.inf
    by.append(y)
ax1.plot(xp, by, lw=2, color="cyan")


plt.show()