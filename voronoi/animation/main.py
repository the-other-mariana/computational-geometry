import numpy as np
import math
from matplotlib import pyplot as plt
from glibrary import Point, Line, Vector, eps
from celluloid import Camera

STEPS = 50
gap = 20
f = 0

xhits = []
yhits = []

fig = plt.figure()
camera = Camera(fig)

def paint(input):
    global f
    global fig

    xs = [p.x for p in input]
    ys = [p.y for p in input]

    fig.add_subplot()
    ax1 = plt.gca()

    ax1.scatter(xs, ys, s=20, zorder=10, color='blue')

    xMin, xMax = min(input, key=lambda p: p.x).x, max(input, key=lambda p: p.x).x
    yMin, yMax = min(input, key=lambda p: p.y).y, max(input, key=lambda p: p.y).y

    plt.setp(ax1, xlim=(xMin - gap, xMax + gap), ylim=(yMin - gap, yMax + gap))

    # plot sweep line
    xlim = ax1.get_xlim()
    ylim = ax1.get_ylim()

    yRange = abs(ylim[1] - ylim[0])
    dy = yRange / (STEPS * 1.0)

    yValue = ylim[1] - (f * dy)
    ax1.plot(list(xlim), [yValue, yValue], color="black")

    yps = []
    xp = list(np.linspace(xlim[0], xlim[1], 100))
    for p in input:
        if yValue <= p.y:
            yp = []
            for x in xp:
                try:
                    y = ((x - p.x)**2 + (p.y)**2 - (yValue)**2) / (2 * (p.y - yValue))
                    yp.append(y)
                except ZeroDivisionError:
                    y = math.inf
                    yp.append(y)
            yps.append(yp)
            ax1.plot(xp, yp, lw=2)
        else:
            break

    global xhits
    global yhits

    for i in range(len(yps)):
        comparator = yps[i]
        for j in range(i, len(yps)):
            idx = np.argwhere(np.diff(np.sign(np.array(comparator) - np.array(yps[j])))).flatten()
            x = np.array(xp)
            y = np.array(comparator)

            for k in range(len(y[idx])):
                xhits.append(x[idx][k])
                yhits.append(y[idx][k])

            #plt.plot(x[idx], f[idx], 'ro')
    ax1.scatter(xhits, yhits, s=20, color="red", zorder=100)

    figure = plt.gcf()
    figure.set_size_inches(10, 8)

    #plt.savefig("frames/anim_{0}.png".format(f), bbox_inches='tight', dpi=100)
    camera.snap()

    f += 1



def main():
    input = [Point(-5, 5), Point(7, 18), Point(18, 0)]
    input.sort()
    print(input)

    for i in range(STEPS):
        paint(input)
    animation = camera.animate()
    animation.save('animation.mp4')


if __name__ == "__main__":
    main()