from glibrary import Point, Line, Vector
import numpy as np
from matplotlib import pyplot as plt

def main():
    input = [Point(3, 3), Point(5, 8), Point(7, 1)]
    xs = [p.x for p in input]
    ys = [p.y for p in input]

    # PLOT
    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()

    ax1.scatter(xs, ys, s=20, zorder=10, color='red')
    plt.show()

if __name__ == "__main__":
    main()