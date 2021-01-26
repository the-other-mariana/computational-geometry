import matplotlib.pyplot as plt
import numpy as np

pointsNumber = int(input())
x = []
y = []
for point in pointsNumber:
    temp = p.split()
    x.append(int(temp[0]))
    y.append(int(temp[1]))

fig = plt.figure()
fig.add_axes()
ax1 = plt.gca()

ax1.plot(x, y)
ax1.scatter(x,y, s=100, marker="x")
ax1.fill_between(x,y,0)

ax1.arrow(0.1, 1, 0.3, -0.3, width=.015, head_width=0.05, head_length=0.05)
ax1.annotate("l1", xy=(.1, 1), xytext=(0.25,0.9), size=12)
