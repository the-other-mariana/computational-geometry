from glibrary import Point
import math
from matplotlib import pyplot as plt
import numpy as np

gap = 3
txt_offset = 0.1

fig = plt.figure()
fig.add_subplot()
ax1 = plt.gca()

input = [Point(-3, 15), Point(10, 10), Point(4, 1)]

xs = [p.x for p in input]
ys = [p.y for p in input]

cc, cr = Point.getCircumCenterRadius(input[0], input[1], input[2])
circle = plt.Circle((cc.x, cc.y), cr, color='black', fill=False)
low_point = Point(cc.x, cc.y - cr)

ax1.scatter(xs, ys, s=20, zorder=10, color='blue')
ax1.scatter([cc.x], [cc.y], s=20, zorder=10, color='blue', marker='x')
ax1.scatter([low_point.x], [low_point.y], s=20, zorder=10, color='red')
ax1.add_patch(circle)


xMin, xMax = min(input, key=lambda p: p.x).x, max(input, key=lambda p: p.x).x
yMin, yMax = min(input, key=lambda p: p.y).y, max(input, key=lambda p: p.y).y
plt.setp(ax1, xlim=(xMin - gap, xMax + gap), ylim=(yMin - gap, yMax + gap))

for i in range(len(input)):
    plt.annotate(chr(i+97),xy=(input[i].x + txt_offset, input[i].y + txt_offset))

plt.annotate('cc',xy=(cc.x + txt_offset, cc.y + txt_offset))
plt.annotate('circle event',xy=(low_point.x + txt_offset, low_point.y + txt_offset), color='r')
print("ce:", low_point)

plt.show()