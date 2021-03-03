'''Code that implements an Edge Linked List from input files'''
from glibrary import Point, Line, Vector
import re

INPUT_VERTEX = 'input/01/layer01.ver'
INPUT_EDGE = 'input/01/layer01.ari'
INPUT_FACE = 'input/01/layer01.car'

class Vertex:
    def __init__(self, vname="", pos=Point()):
        self.name = vname
        self.pos = pos
        self.incidentFace = None # face

    def __repr__(self):
        return f"V[name:{self.name}, pos:{self.pos}, incident:{self.incidentFace}]"

    def __str__(self):
        return "V[name:{n}, pos:{p}, incident:{f}]".format(n=self.name, p=self.pos, f=self.incidentFace)

class Edge:
    def __init__(self, ename=""):
        self.name = ename
        self.origin = None # vertex
        self.mate = None # edge
        self.face = None # face
        self.next = None # edge
        self.prev = None # egde

    def __repr__(self):
        return f"E[name:{self.name}, origin:{self.origin}, mate:{self.mate}, face:{self.face}, next:{self.next}, prev:{self.prev}]"

    def __str__(self):
        return "E[name:{n}, origin:{o}, mate:{m}, face:{f}, next:{nx}, prev:{p}]]".format(n=self.name, o=self.origin, m=self.mate, f=self.face, nx=self.next, p=self.prev)

class Face:
    def __init__(self, fname=""):
        self.name = fname
        self.internal = None
        self.external = None

    def __repr__(self):
        return f"F[name:{self.name}, internal:{self.internal}, external:{self.external}]"

    def __str__(self):
        return "F[name:{n}, internal:{i}, external:{e}]".format(n=self.name, i=self.internal, e=self.external)

if __name__ == "__main__":
    vertFile = open(INPUT_VERTEX, 'r')
    vlines = vertFile.readlines()

    edgeFile = open(INPUT_EDGE, 'r')
    elines = edgeFile.readlines()

    faceFile = open(INPUT_FACE, 'r')
    flines = faceFile.readlines()

    objMap = {}
    verts = []
    edges = []
    faces = []

    # indexes 0 1 2 3 contain just headers
    for line in vlines[4:]:
        data = re.sub(' +', ' ', line).split()
        v = Vertex(data[0], Point(data[1], data[2]))
        verts.append(v)
        objMap[v.name] = v

    for line in elines[4:]:
        data = re.sub(' +', ' ', line).split()
        e = Edge(data[0])
        edges.append(e)
        objMap[e.name] = e

    for line in flines[4:]:
        data = re.sub(' +', ' ', line).split()
        f = Face(data[0])
        faces.append(f)
        objMap[f.name] = f

    print(verts, edges, faces)
    print(objMap)
