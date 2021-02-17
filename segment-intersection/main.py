from glibrary import Point, Vector, Line
from etree import *

file1 = open('input/0.in', 'r')
flines = file1.readlines()

N = int(flines[0])

ev = []
for line in flines[1:]:
    pts = line.split(' ')
    segment = int("".join(filter(str.isdigit, pts[len(pts) - 1])))
    for i in range(0, len(pts) - 1, 2):
        pt = Point(int(pts[i]), int(pts[i + 1]))
        e = Event(pt, segment, bool(i))
        ev.append(e)
[print(e) for e in ev]
print(len(ev))

# init event queue inserting all extremes of segments
etree = BST()
[etree.insert(e) for e in ev]
