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
    if data.rstrip("\n") != 'None': return objMap[data]
    else: return None

def printMap(objMap):
    for key in objMap.keys():
        obj = objMap[key]
        if "p" in obj.name: # vertex
            print(key, 'incident:', obj.incident)
        if "s" in obj.name: # edge
            print(key, 'origin:', obj.origin, 'mate:', obj.mate, 'face:', obj.face, 'next:', obj.next, 'prev:', obj.prev)
        if "f" in obj.name: # face
            print(key, 'internal:', obj.internal, 'external:', obj.external)

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
        objMap[v.name] = v

    for line in elines[4:]:
        data = re.sub(' +', ' ', line).split()
        e = Edge(data[0])
        objMap[e.name] = e

    for line in flines[4:]:
        data = re.sub(' +', ' ', line).split()
        f = Face(data[0])
        objMap[f.name] = f

    # after none init in map, go back and fill
    # fill vertices
    for line in vlines[4:]:
        data = re.sub(' +', ' ', line).split()
        name = data[0]
        objMap[name].incident = getMapValue(data[3], objMap)

    # fill edges
    for line in elines[4:]:
        data = re.sub(' +', ' ', line).split()
        name = data[0]

        objMap[name].origin = getMapValue(data[1], objMap)
        objMap[name].mate = getMapValue(data[2], objMap)
        objMap[name].face = getMapValue(data[3], objMap)
        objMap[name].next = getMapValue(data[4], objMap)
        objMap[name].prev = getMapValue(data[5], objMap)

    # fill faces
    for line in flines[4:]:
        data = re.sub(' +', ' ', line).split()
        name = data[0]
        objMap[name].internal = getMapValue(data[1], objMap)
        objMap[name].external = getMapValue(data[2], objMap)

    printMap(objMap)
    verts = [objMap[key] for key in objMap.keys() if "p" in key]
    edges = [objMap[key] for key in objMap.keys() if "s" in key]
    faces = [objMap[key] for key in objMap.keys() if "f" in key]
    print(verts, edges, faces)


