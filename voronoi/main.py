from glibrary import Point, Line, Vector, eps
import numpy as np
import math
from matplotlib import pyplot as plt

STEPS = 100
f = 0
gap = 10
xhits = []
yhits = []

def paint(input):
    global f

    xs = [p.x for p in input]
    ys = [p.y for p in input]

    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()

    ax1.scatter(xs, ys, s=20, zorder=10, color='blue')

    # set plot limits according to points
    xMin, xMax = min(input, key=lambda p: p.x).x, max(input, key=lambda p: p.x).x
    yMin, yMax = min(input, key=lambda p: p.y).y, max(input, key=lambda p: p.y).y
    plt.setp(ax1, xlim=(xMin - gap, xMax + gap), ylim=(yMin - gap, yMax + gap))

    # plot horizontal sweep line
    xlim = ax1.get_xlim()
    ylim = ax1.get_ylim()
    yRange = abs(ylim[1] - ylim[0])
    dy = yRange / (STEPS * 1.0)

    yValue = ylim[1] - (f * dy)
    ax1.plot(list(xlim), [yValue, yValue], color="red")

    yps = []
    xp = list(np.linspace(xlim[0], xlim[1], 100))
    for p in input:
        if yValue <= p.y:

            yp = []
            for x in xp:
                try:
                    y = ( (x - p.x)**2 + (p.y)**2 - (yValue)**2 ) / (2 * (p.y - yValue))
                    yp.append(y)

                except ZeroDivisionError:
                    y = math.inf
                    yp.append(y)
            yps.append(yp)
            ax1.plot(xp, yp, linewidth=2)

    global xhits
    global yhits

    for i in range(len(yps) - 1):
        idx = np.argwhere(np.diff(np.sign(np.array(yps[i]) - np.array(yps[i + 1])))).flatten()
        x = np.array(xp)
        y = np.array(yps[i])

        for k in range(len(y[idx])):
            xhits.append(x[idx][k])
            yhits.append(y[idx][k])

        #ax1.plot(x[idx], y[idx], 'ro')

    ax1.scatter(xhits, yhits, s=10, color='black', zorder=50)
    figure = plt.gcf()
    figure.set_size_inches(10, 8)
    plt.savefig("frames/anim_{0}.png".format(f), bbox_inches='tight', dpi=100)
    f += 1
    #plt.show()

def main():
    input = [Point(-5, 5), Point(7, 18), Point(18, 0)]
    sorts = sorted(input, key=lambda p: p.y, reverse=True)
    print(sorts)
    for i in range(STEPS):
        # PLOT
        paint(sorts)

if __name__ == "__main__":
    main()