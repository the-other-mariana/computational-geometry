from glibrary import Point, Vector, Line
from etree import *

# returns if p1 is superior point of p1p2
def isStart(p1, p2):
    if p1.y > p2.y:
        return True
    elif p2.y > p1.y:
        return False
    elif p1.y == p2.y:
        if p1.x < p2.x:
            return True
        else:
            return False

file1 = open('input/0.in', 'r')
flines = file1.readlines()

N = int(flines[0])

tot_seg = []
ev = []
for line in flines[1:]:
    pts = line.split(' ')
    segment = int("".join(filter(str.isdigit, pts[len(pts) - 1])))
    seg = []
    for i in range(0, len(pts) - 1, 2):
        pt = Point(int(pts[i]), int(pts[i + 1]))
        seg.append(pt)
        #e = Event(pt, segment, bool(i))
        #ev.append(e)
    seg_sorted = sorted(seg, key=lambda x: x.y, reverse=True)
    for i in range(len(seg_sorted)):
        e = Event(seg_sorted[i], segment, i)
        ev.append(e)
    tot_seg.append(seg)
[print(e) for e in ev]
print(len(ev))

# init event queue inserting all extremes of segments
etree = BST()
[etree.insert(e) for e in ev]
#in_array = BST.inorder(etree.root)
#print(in_array)
