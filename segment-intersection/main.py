from glibrary import Point, Vector, Line
from etree import *
from ttree import *
import matplotlib.pyplot as plt
from matplotlib import collections  as mc

INPUT_FILE = 'input/0.in'
fast = True

def paint(p):
	global R
	global ev
	global f
	global etree

	plt_segs = []
	in_array = Q.inorder(etree.root)
	q_xs = []
	q_ys = []
	for e in in_array:
		q_xs.append(e.point.x)
		q_ys.append(e.point.y)

	for i in range(len(tot_seg)):
		begin = tuple([tot_seg[i].start.x, tot_seg[i].start.y])
		end = tuple([tot_seg[i].end.x, tot_seg[i].end.y])
		plt_segs.append([begin, end])

	x = [e.point.x for e in ev]
	y = [e.point.y for e in ev]
	R_plot = [p for p in R if not (p in tot_pts)]

	xr = [p.x for p in R_plot]
	yr = [p.y for p in R_plot]

	fig = plt.figure()
	fig.add_subplot()
	ax1 = plt.gca()

	ax1.scatter(x, y, s=100, marker="x", linewidths=2)

	ax1.scatter(q_xs, q_ys, s=100, marker="o", color="green", zorder=10)
	ax1.scatter(xr, yr, s=100, marker="P", color="red", zorder=20)
	ax1.add_collection(mc.LineCollection(plt_segs, linewidths=2))

	# plot sweep line
	xlim = ax1.get_xlim()
	#print("lim:", xlim)
	ax1.plot(list(xlim), [p.y, p.y], color="red")


	plt.savefig("frames/anim_{0}.png".format(f),bbox_inches='tight')
	f +=1

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
		print("added event:", e)
		#R.append(hit)
	elif hit.y == p.y and hit.x < p.x and isThere == None:
		e = Event(hit)
		etree.insert(e)
		print("added event:", e)
		#R.append(hit)
	paint(p)
	paint(p)

def processEvent(p):
	global tot_seg
	global tLine
	global R
	global R_segs

	p = p.value.point
	paint(p)
	paint(p)
	U = [s for s in tot_seg if s.start == p]
	U2, C, L = tLine.findByPoint(p)
	if not fast:
		in_array = tLine.inorder(tLine.root)
		print("T line:", in_array)
		L = [s for s in in_array if s.end == p]
		C = []
		for s in in_array:
			if s.isInSegment(p) == 2:
				C.append(s)

	U = U
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
		R_segs.append([s.index for s in UCL])
		print("hi")
	for s in (L.union(C)):
		tLine.deleteValue(s, p)
		print("j")
	for s in (UC):
		tLine.insert(s, p)
	if len(UC) == 0:

		s_l = tLine.getLeftFromP(p, tLine.root)
		s_r = tLine.getRightFromP(p, tLine.root)
		print("########### new step neighbours:", s_l.value, s_r.value)
		findEvent(s_l.value, s_r.value, p)
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
		#s_left = tLine.getLeftNeighbour(s_prime, p)
		s_left = tLine.getPredecessor(tLine.root, s_prime, p)
		if s_left != None:
			print("left neighbour:", s_left.value)
			findEvent(s_left.value, s_prime, p)
		s_bprime = tot_seg[hits[len(hits) - 1][1]]
		#s_right = tLine.getRightNeighbour(s_bprime, p)
		s_right= tLine.getSuccessor(tLine.root, s_bprime, p)
		if s_right != None:
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
f = 0

for line in flines[1:]:
	pts = line.split(' ')
	segment = int("".join(filter(str.isdigit, pts[len(pts) - 1]))) - 1
	seg = []
	for i in range(0, len(pts) - 1, 2):
		x = float(pts[i]) if '.' in pts[i] else int(pts[i])
		y = float(pts[i + 1]) if '.' in pts[i + 1] else int(pts[i + 1])
		pt = Point(x, y)
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

first_p = etree.getFirst(etree.root).value.point
paint(Point(first_p.x, first_p.y))
paint(Point(first_p.x, first_p.y))

while not etree.isEmpty():
	p = etree.getFirst(etree.root)
	print("**pull:", p.value, "root:", etree.root.value)
	etree.deleteNode(p)
	processEvent(p)

print(etree.isEmpty()) # true
R = [p for p in R if not (p in tot_pts)]
print("Output", R, R_segs)

# PLOTTING
'''
plt_segs = []

for i in range(len(tot_seg)):
	begin = tuple([tot_seg[i].start.x, tot_seg[i].start.y])
	end = tuple([tot_seg[i].end.x, tot_seg[i].end.y])
	plt_segs.append([begin, end])

x = [e.point.x for e in ev]
y = [e.point.y for e in ev]
xr = [p.x for p in R]
yr = [p.y for p in R]


fig = plt.figure()
fig.add_subplot()
ax1 = plt.gca()


ax1.scatter(x,y, s=100, marker="o")
ax1.scatter(xr,yr, s=100, marker="P", color="red", zorder=10)
ax1.add_collection(mc.LineCollection(plt_segs, linewidths=2))

# plot sweep line
xlim = ax1.get_xlim()
print("lim:", xlim)
ax1.plot(list(xlim), [10, 10], color = "red")
#plt.savefig("test_{c}.png".format(c=cont),bbox_inches='tight')

for i in range(len(tot_seg)):
    mid = Point.midPoint(tot_seg[i].start, tot_seg[i].end)
    coord = tuple([mid.x, mid.y])
    coordt = tuple([mid.x + 2, mid.y])
    ax1.annotate("S{0}".format(i), xy=coord, xytext=coordt, size=10, arrowprops = dict(facecolor ='black',width=1,headwidth=4))

plt.show()
'''
