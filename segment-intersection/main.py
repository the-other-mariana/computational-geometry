from glibrary import Point, Vector, Line
from etree import *
from ttree import *
import matplotlib.pyplot as plt
from matplotlib import collections  as mc

INPUT_FILE = 'input/test.in'

def findEvent(s_left, s_right, p):
	global etree
	global R
	sl_line = Line.points2Line(s_left.start, s_left.end)
	sr_line = Line.points2Line(s_right.start, s_right.end)
	print(sl_line)
	print(sr_line)
	hit = sl_line.intersects(sr_line)

	# case: sr and sl are same segment, they never intersect
	if not hit: return
	if s_left.isInSegment(hit) == -1: return
	if s_right.isInSegment(hit) == -1: return

	isThere = etree.find(hit)
	if hit.y < p.y and isThere == None:
		e = Event(hit)
		etree.insert(e)
		#R.append(hit)
	elif hit.y == p.y and hit.x < p.x and isThere == None:
		e = Event(hit)
		etree.insert(e)
		#R.append(hit)

def processEvent(p):
	global tot_seg
	global tLine
	global R
	global R_sets

	p = p.value.point
	U = [s for s in tot_seg if s.start == p]
	U2, C, L = tLine.findByPoint(p)
	U = U + U2
	print("U:{u}\nC:{c}\nL:{l}".format(u=U, c=C, l=L))
	# lists to sets
	U = set(U)
	C = set(C)
	L = set(L)
	UCL = (U.union(C)).union(L)
	UC = U.union(C)
	print("UCL: {0}".format(UCL))
	if len(UCL) > 1:
		R.append(p)
		print("hi")
	for s in (L.union(C)):
		tLine.deleteValue(s, p)
	for s in (UC):
		tLine.insert(s, p)
	if len(UC) == 0:
		print("new step")
		s_left = tLine.getLeftFromP(p, tLine.root)
		s_right = tLine.getRightFromP(p, tLine.root)
		findEvent(s_left.value, s_right.value, p)
	else:
		uc = list(UC)
		hits = []
		# UC in T
		for s in uc:
			t2 = Point(p.x + 1, p.y)
			tempLine = Line.points2Line(p, t2)
			hit = tempLine.intersects(Line.points2Line(s.start, s.end))
			hits.append([hit, s.index])

		# UC in T (ordered horizontally)
		hits = sorted(hits, key=lambda p: p[0].x, reverse=False)

		s_prime = tot_seg[hits[0][1]]
		s_left = tLine.getLeftNeighbour(s_prime, p)
		print("left neighbour:", s_left.value)
		findEvent(s_left.value, s_prime, p)
		s_bprime = tot_seg[hits[len(hits) - 1][1]]
		s_right = tLine.getRightNeighbour(s_bprime, p)
		print("right neighbour:", s_right.value)
		findEvent(s_bprime, s_right.value, p)


file1 = open(INPUT_FILE, 'r')
flines = file1.readlines()

N = int(flines[0])
R = []
R_segs = []

tot_seg = [] # total segments
tot_pts = []
ev = []

for line in flines[1:]:
	pts = line.split(' ')
	segment = int("".join(filter(str.isdigit, pts[len(pts) - 1]))) - 1
	seg = []
	for i in range(0, len(pts) - 1, 2):
		pt = Point(int(pts[i]), int(pts[i + 1]))
		tot_pts.append(pt)
		seg.append(pt)
	seg_sorted = sorted(seg, key=lambda p: p.y, reverse=True)
	for i in range(len(seg_sorted)):
		e = Event(seg_sorted[i], segment, i)
		ev.append(e)
	s = Segment(seg_sorted[0], seg_sorted[1], segment)
	tot_seg.append(s)

print("------------------")
print("Events: {0}".format(len(ev)))
[print(e) for e in ev]
print("Segments: {0}".format(len(tot_seg)))
[print(s) for s in tot_seg]
print("------------------")


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
	print("**pull:", p.value, "root:", etree.root.value)
	etree.deleteNode(p)
	processEvent(p)

print(etree.isEmpty()) # true
print("Output", R)

# PLOTTING
plt_segs = []
for i in range(len(tot_seg)):
	begin = tuple([tot_seg[i].start.x, tot_seg[i].start.y])
	end = tuple([tot_seg[i].end.x, tot_seg[i].end.y])
	plt_segs.append([begin, end])

x = [e.point.x for e in ev]
y = [e.point.y for e in ev]
xr = [p.x for p in R if not (p in tot_pts)]
yr = [p.y for p in R if not (p in tot_pts)]


fig = plt.figure()
fig.add_subplot()
ax1 = plt.gca()

ax1.scatter(x,y, s=100, marker="o")
ax1.scatter(xr,yr, s=100, marker="P", color="red", zorder=10)
ax1.add_collection(mc.LineCollection(plt_segs, linewidths=2))

'''
for i in range(len(tot_seg)):
    mid = Point.midPoint(tot_seg[i].start, tot_seg[i].end)
    coord = tuple([mid.x, mid.y])
    coordt = tuple([mid.x + 10, mid.y])
    ax1.annotate("S{0}".format(i), xy=coord, xytext=coordt, size=10, arrowprops = dict(facecolor ='black',width=1,headwidth=4))
'''
plt.show()
