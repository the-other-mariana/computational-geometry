from queue import Event, Q
from tline import Node, T
from glibrary import Point, Line, Vector, eps
from matplotlib import pyplot as plt

# main code that runs the voronoi algorithm

STEPS = 100
gap = 5

def main():
    q = Q()
    t = T()
    input = [Point(14, 0), Point(10, 10), Point(-3, 15), Point(4, 1), Point(-5, 6), Point(7, 18)]
    xs = [p.x for p in input]
    ys = [p.y for p in input]

    # get axis min and max
    xMin, xMax = min(input, key=lambda p: p.x).x, max(input, key=lambda p: p.x).x
    yMin, yMax = min(input, key=lambda p: p.y).y, max(input, key=lambda p: p.y).y

    # for plot
    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()

    ax1.scatter(xs, ys, s=30, zorder=10, color='tab:blue')
    plt.setp(ax1, xlim=(xMin - gap, xMax + gap), ylim=(yMin - gap, yMax + gap))

    for p in input:
        e = Event(p)
        q.push(e)

    xlim = ax1.get_xlim()
    ylim = ax1.get_ylim()

    height = abs((ylim[1] + gap) - (ylim[0] - gap))
    dh = (height * 1.0) / STEPS
    h = ylim[1] + gap
    next = q.show()

    while h > (ylim[0] - gap):
        h -= dh
        print("-> h:", h)
        if abs(h - next.value.y) < dh and not q.isEmpty():
            next = q.show()
            popped = q.pop()
            print("Pop:", popped)

    plt.show()

if __name__ == "__main__":
    main()
