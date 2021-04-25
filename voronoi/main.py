from glibrary import Point, Line, Vector
import numpy as np
import math
from matplotlib import pyplot as plt

STEPS = 50
f = 0

def paint(input):
    global f

    xs = [p.x for p in input]
    ys = [p.y for p in input]

    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()

    ax1.scatter(xs, ys, s=20, zorder=10, color='blue')

    # plot horizontal sweep line
    plt.setp(ax1, xlim=(2.5, 8), ylim=(0, 10))
    xlim = ax1.get_xlim()
    ylim = ax1.get_ylim()
    yRange = abs(ylim[1] - ylim[0])
    dy = yRange / (STEPS * 1.0)

    yValue = ylim[1] - (f * dy)
    ax1.plot(list(xlim), [yValue, yValue], color="red")


    for p in input:
        if yValue <= p.y:
            xp = list(np.linspace(xlim[0], xlim[1], STEPS))
            yp = []
            for x in xp:
                try:
                    y = ( (x - p.x)**2 + (p.y)**2 - (yValue)**2 ) / (2 * (p.y - yValue))
                    yp.append(y)
                except ZeroDivisionError:
                    yp.append(math.inf)

            ax1.plot(xp, yp, linewidth=2)


    figure = plt.gcf()
    figure.set_size_inches(10, 8)
    plt.savefig("frames/anim_{0}.png".format(f), bbox_inches='tight', dpi=100)
    f += 1
    #plt.show()

def main():
    input = [Point(3, 3), Point(5, 8), Point(7, 1)]
    sorts = sorted(input, key=lambda p: p.y, reverse=True)
    print(sorts)
    for i in range(STEPS):
        # PLOT
        paint(sorts)

if __name__ == "__main__":
    main()