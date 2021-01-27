import matplotlib.pyplot as plt
import numpy as np

pointsNumber = int(input())
x = []
y = []
tuples = []
for point in range(pointsNumber):
  p = str(input())
  temp = p.split(" ")
  #x.append(int(temp[0]))
  #y.append(int(temp[1]))
  tuples.append(tuple([int(temp[0]),int(temp[1])]))

sorted_by_first = sorted(tuples, key=lambda tup: tup[0])

for i in sorted_by_first:
  x.append(i[0])
  y.append(i[1])

fig = plt.figure()
fig.add_axes()
ax1 = plt.gca()

ax1.plot(x,y)
ax1.fill_between(x,y,0, color="powderblue")
ax1.scatter(x,y, s=100, marker="o")


ax1.arrow(.1, 1, 0.3, -0.3, width=.015, head_width=0.05, head_length=0.05)
ax1.annotate("l1", xy=(.1, 1), xytext=(.25, .9), size=12)
plt.show()
