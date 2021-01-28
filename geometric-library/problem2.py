import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import numpy as np
from glibrary import eps, Point, Line, Vector

file1 = open('4.in', 'r')
flines = file1.readlines()
hide_point = Point(float(flines[0]), float(flines[1]))

n_stations = int(flines[2])
x = []
y = []

init_index = 3
for i in range(n_stations*2):
    if (init_index + i) % 2 == 1:
        x.append(float(flines[init_index + i]))
    else:
        y.append(float(flines[init_index + i]))

min_dist = 0
perpPoint = Point()
seg = []

fig = plt.figure()
fig.add_axes()
ax1 = plt.gca()

ax1.plot(x,y, color="green")
ax1.scatter(hide_point.x,hide_point.y, s=100, marker="P", color='red')

for i in range(len(x) - 1):
    p1 = Point(x[i], y[i])
    p2 = Point(x[i + 1], y[i + 1])
    ax1.scatter(p1.x,p1.y, s=100, marker="o", color="green")
    dist = Line.point2SegDist(p1, p2, hide_point)
    if i == 0:
        min_dist = dist
    if i == len(x) - 2:
        ax1.scatter(p2.x,p2.y, s=100, marker="o", color="green")
    if dist <= min_dist:
        min_dist = dist
        perpPoint = Line.perpPoint2Line(p1, p2, hide_point)


seg.append([tuple([hide_point.x, hide_point.y]), tuple([perpPoint.x, perpPoint.y])])
mid = Point.midPoint(hide_point, perpPoint)
coord = tuple([mid.x, mid.y])
coordt = tuple([mid.x + 1, mid.y + 1])
ax1.annotate("d={a:.2f}".format(a=min_dist), xy=coord, xytext=coordt, size=12, arrowprops = dict(facecolor ='black',width=1,headwidth=4))

ax1.scatter(perpPoint.x,perpPoint.y, s=100, marker="P", color='red')
ax1.add_collection(mc.LineCollection(seg, color='red', linewidths=2))

#ax1.arrow(.1, 1, 0.3, -0.3, width=.015, head_width=0.05, head_length=0.05)
#ax1.annotate("l1", xy=(.1, 1), xytext=(.25, .9), size=12)
plt.show()
