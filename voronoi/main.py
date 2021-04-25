from glibrary import Point, Line, Vector
import numpy as np
from matplotlib import pyplot as plt

f = 0

def paint(p, input):
    global f

    xs = [p.x for p in input]
    ys = [p.y for p in input]

    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()

    ax1.scatter(xs, ys, s=20, zorder=10, color='blue')

    # plot horizontal sweep line
    xlim = ax1.get_xlim()
    ax1.plot(list(xlim), [p.y, p.y], color="red")

    figure = plt.gcf()
    figure.set_size_inches(10, 8)
    plt.savefig("frames/anim_{0}.png".format(f), bbox_inches='tight', dpi=100)
    f += 1
    #plt.show()

def main():
    input = [Point(3, 3), Point(5, 8), Point(7, 1)]
    sorts = sorted(input, key=lambda p: p.y, reverse=True)
    print(sorts)
    for p in sorts:
        # PLOT
        paint(p, sorts)

if __name__ == "__main__":
    main()