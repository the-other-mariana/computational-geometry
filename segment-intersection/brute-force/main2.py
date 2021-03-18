from algoritmo import AlgoritmoBarrido
from Punto import Punto
from Segmento import Segmento

def main():

	s1 = Segmento(Punto(10,10), Punto(0,0))
	s2 = Segmento(Punto(10,0), Punto(0,10))

	INPUT_FILE = '1.in'

	file1 = open(INPUT_FILE, 'r')
	flines = file1.readlines()
	N = 0
	offset = 1
	fast = True

	# support files with starting line with N or not
	try:
		N = int(flines[0])
		offset = 1
	except:
		N = len(flines)
		offset = 0

	R = []
	R_segs = []

	tot_seg = [] # total segments
	tot_pts = []
	iteration = 0
	isHorizontal = True
	yVal = 0

	for line in flines[offset:]:
		pts = line.split(' ')

		segmentName = iteration
		# if file contains segment name (store it) or not (segment id is num of iteration) at the end of line
		if "s" in pts[len(pts) - 1]:
			segmentName = pts[len(pts) - 1].rstrip("\n")
		else:
			segmentName = "s" + str(iteration)


		seg = []
		for i in range(0, len(pts) - 1, 2):
			x = float(pts[i]) if '.' in pts[i] else int(pts[i])
			y = float(pts[i + 1]) if '.' in pts[i + 1] else int(pts[i + 1])
			pt = Punto(x, y)
			tot_pts.append(pt)
			seg.append(pt)
		for i in range(len(seg)):
			if i == 0: yVal = seg[i].y
			if seg[i].y != yVal:
				isHorizontal = False
		if not isHorizontal:
			seg_sorted = sorted(seg, key=lambda p: p.y, reverse=True)
		else:
			seg_sorted = sorted(seg, key=lambda p: p.x, reverse=False)
		s = Segmento(seg_sorted[0], seg_sorted[1])
		tot_seg.append(s)
		iteration += 1

	#segmentos = [s1,s2]
	'''
	for s in segmentos:
	  print(s)
	'''

	barr = AlgoritmoBarrido(tot_seg)
	barr.barrer()
	print(barr.R)
	[print(p) for p in barr.R if isinstance(p, Punto)]

if __name__=="__main__":
	main()
