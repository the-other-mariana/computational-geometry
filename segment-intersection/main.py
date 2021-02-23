from glibrary import Point, Vector, Line
from etree import *
from ttree import *
import matplotlib.pyplot as plt
from matplotlib import collections  as mc

def processEvent(p):
    global tot_seg
    global tLine
    global R
    global R_sets

    p = p.value.point
    U = [s for s in tot_seg if s.start == p]
    U2, C, L = tLine.findByPoint(p)
    U = U + U2
    print("U: {u}\nC:{c}\nL:{l}".format(u=U, c=C, l=L))
    # lists to sets
    U = set(U)
    C = set(C)
    L = set(L)
    UCL = (U.union(C)).union(L)
    print("UCL: {0}".format(UCL))
    if len(UCL) > 1:
        R.append(p)
    for s in (L.union(C)):
        tLine.deleteValue(s)
    for s in (U.union(C)):
        tLine.insert(s, p)
    #if len(U.union(C)) == 0:



file1 = open('input/0.in', 'r')
flines = file1.readlines()

N = int(flines[0])
R = []
R_segs = []

tot_seg = [] # total segments
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

'''
print("Events: {0}".format(len(ev)))
[print(e) for e in ev]
print("Segments: {0}".format(len(tot_seg)))
[print(s) for s in tot_seg]
'''

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

while not etree.isEmpty():
    p = etree.getFirst(etree.root)
    print("pull:", p.value, "root:", etree.root.value)
    etree.deleteNode(p)
    processEvent(p)

print(etree.isEmpty()) # true
print(R)

# PLOTTING
plt_segs = []
for i in range(len(tot_seg)):
    plt_segs.append([tuple([tot_seg[i].start.x, tot_seg[i].start.y]), tuple([tot_seg[(i + 1) % len(tot_seg)].end.x, tot_seg[(i + 1) % len(tot_seg)].end.y])])

x = [e.point.x for e in ev]
y = [e.point.y for e in ev]
xr = [p.x for p in R]
yr = [p.y for p in R]


fig = plt.figure()
fig.add_subplot()
ax1 = plt.gca()

ax1.scatter(x,y, s=100, marker="o")
ax1.scatter(xr,yr, s=100, marker="P", color="red")
ax1.add_collection(mc.LineCollection(plt_segs, linewidths=2))
plt.show()
