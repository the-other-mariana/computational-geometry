import matplotlib.pyplot as plt
import numpy as np
from glibrary import eps, Point, Line, Vector

file1 = open('3.in', 'r')
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

fig = plt.figure()
fig.add_axes()
ax1 = plt.gca()

ax1.plot(x,y)
ax1.scatter(hide_point.x,hide_point.y, s=100, marker="x", color='red')

#ax1.arrow(.1, 1, 0.3, -0.3, width=.015, head_width=0.05, head_length=0.05)
#ax1.annotate("l1", xy=(.1, 1), xytext=(.25, .9), size=12)
plt.show()
