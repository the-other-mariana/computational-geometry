import matplotlib.pyplot as plt
import numpy as np
from math import sin,pi,cos,radians,sqrt,acos

eps = 10**1
class Point:
  def _init_(self, x=0, y=0):
    self.x = x
    self.y = y

  def _eq_(self, other):
    return abs(self.x-other.x)<eps and abs(self.y-other.y)<eps

  def _repr_(self):
    return f"({self.x}, {self.y})"

  def distance(self, p):
    return sqrt((self.x-p.x)*2 + (self.y-p.y)*2)

  def rotate(self, theta):
    return Point(self.x * cos(radians(theta)) - self.y * sin(radians(theta)), self.x * sin(radians(theta)) + self.y * cos(radians(theta)))

  def pointToVector(self, point2):
    x = point2.x - self.x
    y = point2.y - self.y
    return Vector(x,y)

  def translate(self, vector):
    x = self.x + vector.x
    y = self.y + vector.y
    return Point(x,y)

  def distancePTL(self, pointA, pointB):
    a = Vector(pointA.x. pointA.y)
    ap = a.pointToVector(self)
    ab = a.pointToVector(pointB)
    v = ap.dot(ab) / ab.sqrNorm()
    s = ab.scale(v)
    c = pointA.translate(s)
    return self.distance(c)

  def distancePTS(self, pointA, pointB):
    a = Vector(pointA.x. pointA.y)
    ap = a.pointToVector(self)
    ab = a.pointToVector(pointB)
    v = ap.dot(ab) / ab.sqrNorm()
    if v < 0: return self.distance(pointA)
    if v >= 0 and v <= 1: return self.distancePTL(pointA,pointB)
    if v > 1: return self.distance(ponitB)

  def angle(self, pointA, pointB):
    oa = self.pointToVector(pointA)
    ob = self.pointToVector(pointB)
    return acos(oa.dot(ob)) / ao.sqrNorm() * ob.sqrNorm()

  def CCW(self, pointQ, pointR):
    pq = self.pointToVector(pointQ)
    pr = self.pointToVector(pointR)
    return pq.cross(pr) > 0

  def isColineal(self, pointQ, pointR):
    pq = self.pointToVector(pointQ)
    pr = self.pointToVector(pointR)
    return abs(pq.cross(pr)) < eps

class Line:
  def _init_(self, a=0, b=0, c=0):
    self.a = a
    self.b = b
    self.c = c

  def _repr_(self):
    return f"({self.a}, {self.b}, {self.c})"

  def pointsToLine(self,p1,p2):
    den = p2.x-p1.x
    if den == 0:
      y = 0
      m = p1.x
    else:
      m = (p2.y-p1.y)/(den)
      y = -1
    x = m
    ind = m*(-p1.x) + p1.y
    return Line(x,y,ind)

  def isParallel(self, line2):
    if self.a == line2.a: return True
    else: return False

  def isTheSame(self, line2):
    if self.a > line2.a:
      if (self.a/line2.a) == (self.b/line2.b) == (self.c/line2.c): return True
      else: return False
    else:
      if (line2.a/self.a) == (line2.b/self.b) == (line2.c/self.c): return True
      else: return False

  def intersect(self, line2):
    if self.isParallel(line2): return False
    else:
      x = (self.b*line2.c - line2.b*self.c) / (self.a*line2.b - line2.a*self.b)
      y = (line2.a*self-c - self.a*line2.c) / (self.a*line2.b - line2.s*self.b)
      return Point(x,y)

class Vector:
  def _init_(self, x=0, y=0):
    self.x = x
    self.y = y

  def scale(self, factor):
    self.x = self.x * factor
    self.y = self.y * factor

  def dot(self, vector2):
    return self.x * vector2.x + self.y * vector2.y

  def sqrNorm(self):
    return self.x*2 + self.y*2

  def cross(self, vector2):
    return self.x * vector2.y - vector2.x * self.y

#Defining points coordinates

pointsNumber = int(input())
pts = []
tuples = []
x = []
y = []
for i in range(pointsNumber):
    row = str(input()).split()
    newPoint = Point(int(row[0]), int(row[1]))
    pts.append(newPoint)
    tuples.append(tuple([newPoint.x,newPoint.y]))
    x.append(newPoint.x)
    y.append(newPoint.y)

#Creating tuples list of points
tuples = []
for point in range(pointsNumber):
  #p = str(input())
  #temp = p.split(" ")
  #x.append(int(temp[0]))
  #y.append(int(temp[1]))
  tuples.append(tuple([int(x[point]),int(y[point])]))

#Sorting tuples lexicographic
sorted_lex = sorted(tuples, key=lambda k: (k[0], k[1]))

print(tuples)
print(sorted_lex)

#Superior limit
L_sup = []
#Adding first two elements of lex sorted list
for t in sorted_lex[:2]:
  L_sup.append(Point(t[0], t[1]))

print(L_sup)
#L_sup[1].CCW(L_sup[2], L_sup[0])

#Checking if points are part of superior limit using convex hull algorythm
for p in range(2,len(sorted_lex)):
  #print(p)
  L_sup.append(Point(sorted_lex[p][0], sorted_lex[p][1]))
  i = len(L_sup) - 1
  if len(L_sup) > 2 and L_sup[i-1].CCW(L_sup[i], L_sup[i-2]):
    del L_sup[i-1]

# Inferior limit.
L_inf = []
#Adding last two elements of lex sorted list
for t in sorted_lex[:-3:-1]:
  L_inf.append(Point(t[0], t[1]))

print(L_inf)

#Checking if points are part of inferior limit using convex hull algorythm
for p in range(len(sorted_lex)-3,-1,-1):
  #print(p)
  L_inf.append(Point(sorted_lex[p][0], sorted_lex[p][1]))
  i = len(L_inf) - 1
  if len(L_inf) > 2 and L_inf[i-1].CCW(L_inf[i], L_inf[i-2]):
    del L_inf[i-1]

print(L_sup)
print(L_inf)

#Deleting first and last element of inferior limit to prevent duplicates
#del L_inf[len(L_inf)-1]
del L_inf[0]

#Merging two superior and iferior limit
L = L_sup + L_inf
print(L)

#Ploting points
x2=[]
y2=[]
for i in L:
  x2.append(i.x)
  y2.append(i.y)

fig = plt.figure()
fig.add_axes()
ax1 = plt.gca()

ax1.plot(x2,y2)
ax1.scatter(x,y, s=100, marker="o", color="red")
ax1.scatter(x2,y2, s=100, marker="x")
#ax1.fill_between(x2,y2,0, color="powderblue")

#ax1.arrow(.1, 1, 0.3, -0.3, width=.015, head_width=0.05, head_length=0.05)
#ax1.annotate("l1", xy=(.1, 1), xytext=(.25, .9), size=12)
