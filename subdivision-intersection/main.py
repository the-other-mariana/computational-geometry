'''Code that implements an Edge Linked List (map) from input files'''
from glibrary import Point, Line, Vector
from segint.Segmento import Segmento
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Polygon
from matplotlib.patches import PathPatch
import math
import re

from segint.algoritmo import AlgoritmoBarrido

LAYERS = 2
INPUT_ID = '01'
TOT_PTS = []
TOT_SEGS = []

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

class Item:
    def __init__(self, name=""):
        self.name = name
        self.prev = None
        self.next = None

def getEdges(s, eMap):
    for key, value in eMap.items():
        if value.origin.pos == s.puntos[0]:
            return value, value.mate
    return None, None

def getIncident(p, eMap):
    for key, value in eMap.items():
        if value.origin.pos == p:
            return value
    return None


def getMapValue(data, objMap):
    if "[" in data:
        data = data[1:(len(data) - 1)].split(',')
        return [objMap[d] for d in data]
    elif data.rstrip("\n") != 'None':
        return objMap[data]
    else:
        return None

def analyzeFig(figs, reqEdge):
    global TOT_PTS
    global TOT_SEGS

    edge = reqEdge
    started = False
    pts = []
    fig_segs = []
    # get all the current figure's vertices
    while edge.name != reqEdge.name or not started:
        started = True
        v = edge.origin
        print(v.name)
        pts.append([v.pos.x, v.pos.y]) # as list instead of Point for plot
        TOT_PTS.append(v.pos)
        edge = edge.next

    for i in range(len(pts) - 1):
        start = pts[i % len(pts)]
        end = pts[(i + 1) % len(pts)]
        s = Segmento(Point(start[0], start[1]), Point(end[0], end[1]))
        #fig_segs.append(s)
        TOT_SEGS.append(s)

    #TOT_SEGS.append(fig_segs)
    figs.append(pts)
    return figs

if __name__ == "__main__":

    vMap = {}
    eMap = {}
    fMap = {}

    for i in range(LAYERS):

        INPUT_VERTEX = f'input/{INPUT_ID}/layer0{i+1}.ver'
        INPUT_EDGE = f'input/{INPUT_ID}/layer0{i+1}.ari'
        INPUT_FACE = f'input/{INPUT_ID}/layer0{i+1}.car'

        vertFile = open(INPUT_VERTEX, 'r')
        vlines = vertFile.readlines()

        edgeFile = open(INPUT_EDGE, 'r')
        elines = edgeFile.readlines()

        faceFile = open(INPUT_FACE, 'r')
        flines = faceFile.readlines()

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

    print(fMap.keys())
    figs = []
    pts = []

    for key in fMap.keys():
        # check externals
        if fMap[key].external != None:
            reqEdge = fMap[key].external
            figs = analyzeFig(figs, reqEdge)

        # check internals, list of figs inside
        if isinstance(fMap[key].internal, list):
            internalEdges = fMap[key].internal
            for i in range(len(internalEdges)):
                reqEdge = internalEdges[i]
                figs = analyzeFig(figs, reqEdge)

        # check internals, one fig inside
        if fMap[key].internal != None and not isinstance(fMap[key].internal, list):
            reqEdge = fMap[key].internal
            figs = analyzeFig(figs, reqEdge)

    print("Points:",TOT_PTS)
    print("Segments:",TOT_SEGS)

    # CALL SEGMENT INTERSECTION ALGORITHM
    barr = AlgoritmoBarrido(TOT_SEGS)
    barr.barrer()
    print("Output", barr.R, type(barr.R[0]))
    newverts = [p for p in barr.R if not isinstance(p, set)]
    info = []

    # put indexes of R where there is a point
    for i in range(len(barr.R)):
        if not isinstance(barr.R[i], set):
            info.append(i)

    [print("New vertex:",p) for p in newverts]

    print(vMap)
    print(eMap)
    print(fMap)

    neMap = {}

    names = len(vMap.keys())
    for nv in newverts:
        name = 'p' + str(names + 1)
        vert = Vertex(name, nv)
        # update vertex map
        vMap[name] = Vertex(name, nv)
        names += 1

        # update edge map
        # for each new intersection point
        for j in range(len(info)):
            # list of segments in intersection response
            involved = list(barr.R[info[j] + 1])

            primes = []
            bprimes = []
            both = []

            # for each segment involved in the curr intersection point
            # update edge origins and primes.prev and bprimes.next
            for i in range(len(involved)):
                aux = []
                e, e_mate = getEdges(involved[i], eMap)

                # divide e in two
                e_name = str(e.name + "p")
                e_prime = Edge(e_name)
                e_prime.origin = e.origin
                neMap[e.prev.name] = e.prev
                e_prime.prev = neMap[e.prev.name] # from eMap
                e_prime.face = None # will update later
                neMap[e_name] = e_prime
                aux.append(e_prime)
                # circular list
                primes.append(e_prime)
                both.append(e_prime)

                e_name = str(e.name + "pp")
                e_bprime = Edge(e_name)
                e_bprime.origin = vert
                neMap[e.next.name] = e.next
                e_bprime.next = neMap[e.next.name] # from eMap
                e_bprime.face = None # will update later
                neMap[e_name] = e_bprime
                aux.append(e_bprime)
                # circular list
                bprimes.append(e_bprime)
                both.append(e_bprime)

                # divide e_mate in two
                em_name = str(e_mate.name + "p")
                em_prime = Edge(em_name)
                em_prime.origin = e_mate.origin
                neMap[e_mate.prev.name] = e_mate.prev
                em_prime.prev = neMap[e_mate.prev.name] # from eMap
                em_prime.face = None
                neMap[em_name] = em_prime
                aux.append(em_prime)
                # circular list
                primes.append(em_prime)
                both.append(em_prime)

                em_name = str(e_mate.name + "pp")
                em_bprime = Edge(em_name)
                em_bprime.origin = vert
                neMap[e_mate.next.name] = e_mate.next
                em_bprime.next = neMap[e_mate.next.name] # from eMap
                em_bprime.face = None
                neMap[em_name] = em_bprime
                aux.append(em_bprime)
                # circular list
                bprimes.append(em_bprime)
                both.append(em_bprime)

                # update edge mates
                for i in range(len(aux)):
                    neMap[aux[i].name].mate = neMap[aux[len(aux) - 1 - i].name]
                #neMap[aux[t].name].next = neMap[aux[(t + 1) % len(aux)].name]
                #neMap[aux[t].name].prev = neMap[aux[(t - 1)].name]

            # make primes circular lists based on angles
            circp = []
            circbp = []
            for p in range(len(primes)):
                p1 = vert.pos
                # primes
                p2 = neMap[primes[p].name].origin.pos
                angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
                circp.append([angle, primes[p].name])
                # bprimes
                p2 = neMap[bprimes[p].next.name].origin.pos
                angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
                circbp.append([angle, bprimes[p].name])

            # sort based on angle
            circp = sorted(circp, key=lambda p: p[0])
            circbp = sorted(circbp, key=lambda p: p[0])
            circ = []
            # make one list with prime bprime prime bprime ...
            for i in range(len(circp)):
                circ.append(circp[i][1])
                circ.append(circbp[i][1])

            # primes are even and need next
            # bprimes are odd and need prev
            for i in range(len(both)):
                name = both[i].name
                if i % 2 == 0:
                    # primes
                    neMap[name].next = neMap[circ[(circ.index(name) + 1) % len(circ)]]
                if i % 2 == 1:
                    # bprimes
                    neMap[name].prev = neMap[circ[circ.index(name) - 1]]

        # update vertex file (incident edge)
        keys = vMap.keys()
        for k in keys:
            vMap[k].incident = getIncident(vMap[k].pos, eMap)


    print(neMap)
    print(vMap)

    # PLOTTING
    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()

    for f in figs:
        xp = [p[0] for p in f]
        yp = [p[1] for p in f]
        ax1.scatter(xp, yp,s=100, marker="o", zorder=10, color='black')
        p = Polygon(np.array(f), facecolor = 'powderblue')
        ax1.add_patch(p)
        path = p.get_path()
        patch = PathPatch(path, facecolor='powderblue', lw=2)
        ax1.add_patch(patch)

    plt.show()