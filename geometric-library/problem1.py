import matplotlib.pyplot as plt
from matplotlib import collections  as mc
import numpy as np
from glibrary import eps, Point, Line, Vector

file1 = open('1.in', 'r')
flines = file1.readlines()

pointsNumber = int(flines[0])
x = []
y = []
tuples = []
for point in range(pointsNumber):
  p = str(flines[point + 1])
  temp = p.split(" ")
  tuples.append(tuple([int(temp[0]),int(temp[1])]))

mountains = sorted(tuples, key=lambda tup: tup[0])

for i in mountains:
  x.append(i[0])
  y.append(i[1])

peaks_x = []
peaks_y = []
distances = []
sun_lows_x = []
sun_lows_y = []
sunny_segs = []
max_peak = tuple([0,0])

odd = 0 # odds are peaks if 1
if (len(x) > 1):
    if y[0] < y[1]:
        odd = 1

for i in range(odd,len(mountains), 2):
    curr_peak = mountains[i][1]
    max_peak = tuple([0,0])
    sun = True
    for j in range(i, len(mountains), 2):
        if (mountains[j][1] > curr_peak):
            sun = False
            break
    if sun == True:
        peaks_x.append(mountains[i][0])
        peaks_y.append(mountains[i][1])
        for k in range(i + 2, len(mountains), 2):
            if (mountains[k][1] > max_peak[1]):
                max_peak = mountains[k]
        other_point = Point(max_peak[0] + 1, max_peak[1])
        block_point = Point(max_peak[0], max_peak[1])
        sun_ray = Line.points2Line(block_point, other_point)

        peak_point = Point(mountains[i][0], mountains[i][1])
        low_point = Point(mountains[i + 1][0], mountains[i + 1][1])
        peak_slope = Line.points2Line(peak_point, low_point)

        hit_point = sun_ray.intersects(peak_slope)
        sunny_segs.append([tuple([hit_point.x, hit_point.y]), tuple([peak_point.x, peak_point.y])])
        sun_lows_x.append(hit_point.x)
        sun_lows_y.append(hit_point.y)

        distances.append([Point.distance(peak_point, low_point), peak_point, hit_point])


fig = plt.figure()
fig.add_axes()
ax1 = plt.gca()

ax1.plot(x,y)
ax1.fill_between(x,y,0, color="powderblue")
ax1.scatter(x,y, s=100, marker="o")
ax1.scatter(peaks_x,peaks_y, s=100, marker="P", color='red')
ax1.scatter(sun_lows_x,sun_lows_y, s=100, marker="P", color='red')

ax1.add_collection(mc.LineCollection(sunny_segs, color='red', linewidths=5))

for i in range(len(distances)):
    mid = Point.midPoint(distances[i][1], distances[i][2])
    coord = tuple([mid.x, mid.y])
    coordt = tuple([mid.x + 50, mid.y + 50])
    ax1.annotate("d={a:.2f}".format(a=distances[i][0]), xy=coord, xytext=coordt, size=10, arrowprops = dict(facecolor ='black',width=1,headwidth=4))

#ax1.arrow(.1, 1, 0.3, -0.3, width=.015, head_width=0.05, head_length=0.05)
#ax1.annotate("l1", xy=(.1, 1), xytext=(.25, .9), size=12)
plt.show()
