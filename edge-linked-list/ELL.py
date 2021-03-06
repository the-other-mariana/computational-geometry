'''Code that implements an Edge Linked List from input files'''
from glibrary import Point, Line, Vector
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
import re

INPUT_VERTEX = 'input/03/layer01.ver'
INPUT_EDGE = 'input/03/layer01.ari'
INPUT_FACE = 'input/03/layer01.car'

class Vertex:
    def __init__(self, vname="", pos=Point()):
        self.name = vname
        self.pos = pos
        self.incident = None # edge

    def __repr__(self):
        return f"V[name:{self.name}, pos:{self.pos}]"

    def __str__(self):
        return "V[name:{n}, pos:{p}]".format(n=self.name, p=self.pos)

class Edge:
    def __init__(self, ename=""):
        self.name = ename
        self.origin = None # vertex
        self.mate = None # edge
        self.face = None # face
        self.next = None # edge
        self.prev = None # egde

    def __repr__(self):
        return f"E[name:{self.name}]"

    def __str__(self):
        return "E[name:{n}]".format(n=self.name)

class Face:
    def __init__(self, fname=""):
        self.name = fname
        self.internal = None # edge
        self.external = None # edge

    def __repr__(self):
        return f"F[name:{self.name}]"

    def __str__(self):
        return "F[name:{n}]".format(n=self.name)



def getMapValue(data, objMap):
    if "[" in data:
        data = data[1:(len(data) - 1)].split(',')
        return [objMap[d] for d in data]
    elif data.rstrip("\n") != 'None':
        return objMap[data]
    else:
        return None

def analyzeFig(figs, reqEdge):
    edge = reqEdge
    started = False
    pts = []
    while edge.name != reqEdge.name or not started:
        started = True
        v = edge.origin
        print(v.name)
        pts.append([v.pos.x, v.pos.y])
        edge = edge.next
    print(pts)
    figs.append(pts)
    return figs

if __name__ == "__main__":

    vertFile = open(INPUT_VERTEX, 'r')
    vlines = vertFile.readlines()

    edgeFile = open(INPUT_EDGE, 'r')
    elines = edgeFile.readlines()

    faceFile = open(INPUT_FACE, 'r')
    flines = faceFile.readlines()

    vMap = {}
    eMap = {}
    fMap = {}
    verts = []
    edges = []
    faces = []

    # indexes 0 1 2 3 contain just headers
    # vertex reading
    for line in vlines[4:]:
        data = re.sub(' +', ' ', line).split()
        x = float(data[1]) if '.' in data[1] else int(data[1])
        y = float(data[2]) if '.' in data[2] else int(data[2])
        v = Vertex(data[0], Point(x, y))
        vMap[v.name] = v
    # edges reading
    for line in elines[4:]:
        data = re.sub(' +', ' ', line).split()
        e = Edge(data[0])
        eMap[e.name] = e
    # faces reading
    for line in flines[4:]:
        data = re.sub(' +', ' ', line).split()
        f = Face(data[0])
        fMap[f.name] = f

    # after none init in map, go back and fill
    # fill vertices
    for line in vlines[4:]:
        data = re.sub(' +', ' ', line).split()
        name = data[0]
        vMap[name].incident = getMapValue(data[3], eMap)

    # fill edges
    for line in elines[4:]:
        data = re.sub(' +', ' ', line).split()
        name = data[0]

        eMap[name].origin = getMapValue(data[1], vMap)
        eMap[name].mate = getMapValue(data[2], eMap)
        eMap[name].face = getMapValue(data[3], fMap)
        eMap[name].next = getMapValue(data[4], eMap)
        eMap[name].prev = getMapValue(data[5], eMap)

    # fill faces
    for line in flines[4:]:
        data = re.sub(' +', ' ', line).split()
        name = data[0]
        fMap[name].internal = getMapValue(data[1], eMap) # []
        fMap[name].external = getMapValue(data[2], eMap)

    print("Enter face:")
    inputFace = str(input()) # read external
    figs = []
    pts = []

    # check externals
    if fMap[inputFace].external != None:
        reqEdge = fMap[inputFace].external
        figs = analyzeFig(figs, reqEdge)

    # check internals, list of figs inside
    elif isinstance(fMap[inputFace].internal, list):
        internalEdges = fMap[inputFace].internal
        for i in range(len(internalEdges)):
            reqEdge = internalEdges[i]
            figs = analyzeFig(figs, reqEdge)

    # check internals, one fig inside
    elif fMap[inputFace].internal != None and not isinstance(fMap[inputFace].internal, list):
        reqEdge = fMap[inputFace].internal
        figs = analyzeFig(figs, reqEdge)

    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()

    for f in figs:
        xp = [p[0] for p in f]
        yp = [p[1] for p in f]
        ax1.scatter(xp, yp,s=100, marker="o", zorder=10)
        p = Polygon(np.array(f), facecolor = 'powderblue')
        ax1.add_patch(p)

    plt.show()
    #printMap(objMap)
    #verts = [objMap[key] for key in objMap.keys() if "p" in key]
    #edges = [objMap[key] for key in objMap.keys() if "s" in key]
    #faces = [objMap[key] for key in objMap.keys() if "f" in key]
    #print(verts, edges, faces)


