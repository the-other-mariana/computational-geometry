from glibrary import Point, Vector, Line
from etree import *
from ttree import *

import matplotlib.pyplot as plt
from matplotlib import collections  as mc

file1 = open('input/0.in', 'r')
flines = file1.readlines()

N = int(flines[0])
R = []

tot_seg = []
ev = []
for line in flines[1:]:
    pts = line.split(' ')
    segment = int("".join(filter(str.isdigit, pts[len(pts) - 1])))
    seg = []
    for i in range(0, len(pts) - 1, 2):
        pt = Point(int(pts[i]), int(pts[i + 1]))
        seg.append(pt)
    seg_sorted = sorted(seg, key=lambda p: p.y, reverse=True)
    for i in range(len(seg_sorted)):
        e = Event(seg_sorted[i], segment, i)
        ev.append(e)
    s = Segment(seg_sorted[0], seg_sorted[1])
    tot_seg.append(s)

print("Events: {0}".format(len(ev)))
[print(e) for e in ev]
print("Segments: {0}".format(len(tot_seg)))
[print(s) for s in tot_seg]

# init event queue inserting all extremes of segments
etree = Q()
[etree.insert(e) for e in ev]
in_array = Q.inorder(etree.root)
print("root:", etree.root.value)
first = etree.getFirst(etree.root)
print("first:", first.value)
print(in_array)
# init sweep line as empty
tLine = T()

node = first
#p = first
#print("pull:", p.value, "root:", etree.root.value)
while not etree.isEmpty():
    #p = etree.getNextInorder(node)
    p = etree.getFirst(etree.root)
    if p == None: break
    print("pull:", p.value, "root:", etree.root.value)
    etree.deleteNode(p)
#print("root:", etree.root.value) # last is root
#etree.deleteNode(etree.root)
print(etree.isEmpty()) # true

# PLOTTING
plt_segs = []
for i in range(len(tot_seg)):
    plt_segs.append([tuple([tot_seg[i].start.x, tot_seg[i].start.y]), tuple([tot_seg[(i + 1) % len(tot_seg)].end.x, tot_seg[(i + 1) % len(tot_seg)].end.y])])

x = [e.point.x for e in ev]
y = [e.point.y for e in ev]

fig = plt.figure()
fig.add_subplot()
ax1 = plt.gca()

#ax1.scatter(x2,y2, s=100, marker="x")
ax1.scatter(x,y, s=100, marker="o")
ax1.add_collection(mc.LineCollection(plt_segs, linewidths=2))
plt.show()
