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
from structures import Vertex, Edge, Face
from tools import Tools as t

LAYERS = 2
INPUT_ID = '02'
TOT_PTS = []
TOT_SEGS = []


def analyzeFig(figs, reqEdge, hole=False):
    global TOT_PTS
    global TOT_SEGS

    edge = reqEdge
    started = False
    pts = []

    # get all the current figure's vertices
    while edge.name != reqEdge.name or not started:
        started = True
        v = edge.origin
        # print(v.name)
        pts.append([v.pos.x, v.pos.y])  # as list instead of Point for plot
        TOT_PTS.append(v.pos)
        edge = edge.next

    # get all the current figure's segments
    for i in range(len(pts) - 1):
        start = pts[i % len(pts)]
        end = pts[(i + 1) % len(pts)]
        s = Segmento(Point(start[0], start[1]), Point(end[0], end[1]))
        TOT_SEGS.append(s)

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

        # lines indexes 0 1 2 3 contain just headers
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
            vMap[name].incident = t.getMapValue(data[3], eMap)

        # fill edges
        for line in elines[4:]:
            data = re.sub(' +', ' ', line).split()
            name = data[0]

            eMap[name].origin = t.getMapValue(data[1], vMap)
            eMap[name].mate = t.getMapValue(data[2], eMap)
            eMap[name].face = t.getMapValue(data[3], fMap)
            eMap[name].next = t.getMapValue(data[4], eMap)
            eMap[name].prev = t.getMapValue(data[5], eMap)

        # fill faces
        for line in flines[4:]:
            data = re.sub(' +', ' ', line).split()
            name = data[0]
            fMap[name].internal = t.getMapValue(data[1], eMap) # []
            fMap[name].external = t.getMapValue(data[2], eMap)

    print(fMap.keys())
    figs = []
    pts = []

    for key in fMap.keys():
        # check externals, cannot have lists
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
    print("Sweep Line Output:", barr.R)
    newverts = [p for p in barr.R if not isinstance(p, set) and p not in TOT_PTS]
    info = []

    # put indexes of R where there is an intersection point
    for i in range(len(barr.R)):
        if not isinstance(barr.R[i], set) and barr.R[i] not in TOT_PTS:
            info.append(i)
            print(barr.R[i])

    [print("New vertex:",p) for p in newverts]

    print(vMap)
    print(eMap)
    print(fMap)
    print("info: ", info)

    neMap = {}
    verts = []

    noChanges = False
    if len(newverts) == 0:
        noChanges = True

    names = len(vMap.keys())
    for nv in newverts:
        name = 'p' + str(names + 1)
        vert = Vertex(name, nv)
        # update vertex map
        vMap[name] = Vertex(name, nv)
        names += 1
        verts.append(vert)

    # update edge map
    # for each new intersection point
    for j in range(len(info)):
        vert = verts[j]

        # list of segments in intersection response
        involved = list(barr.R[info[j] + 1])
        print("Intersection Processing ->", vert, "With Segments Involved:", involved)

        primes = []
        bprimes = []
        both = []

        # for each segment involved in the curr intersection point
        # update edge origins and primes.prev and bprimes.next
        for i in range(len(involved)):
            aux = []
            e, e_mate = t.getEdges(involved[i], eMap)
            print("Edges involved:", e, e_mate, involved[i])

            # divide e in two
            e_name = str(e.name)
            e_prime = Edge(e_name)
            e_prime.origin = e.origin
            # data from previous map
            neMap[e.prev.name] = e.prev
            neMap[e.prev.name].next = e_prime
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
            # data from previous map
            neMap[e.next.name] = e.next
            neMap[e.next.name].prev = e_bprime
            e_bprime.next = neMap[e.next.name] # from eMap
            e_bprime.face = None # will update later
            neMap[e_name] = e_bprime
            aux.append(e_bprime)
            # circular list
            bprimes.append(e_bprime)
            both.append(e_bprime)

            # divide e_mate in two
            em_name = str(e_mate.name)
            em_prime = Edge(em_name)
            em_prime.origin = e_mate.origin
            # data from previous map
            neMap[e_mate.prev.name] = e_mate.prev
            neMap[e_mate.prev.name].next = em_prime
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
            # data from previous map
            neMap[e_mate.next.name] = e_mate.next
            neMap[e_mate.next.name].prev = em_bprime
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

        # make primes and bprimes circular lists based on angles
        circp = []
        circbp = []
        for p in range(len(primes)):
            p1 = vert.pos
            # primes
            p2 = neMap[primes[p].name].origin.pos
            angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
            circp.append([angle, primes[p].name])
            print(f"{primes[p].name}: {p1} -> {p2}, angle: {angle}")
            # bprimes
            p2 = neMap[bprimes[p].next.name].origin.pos
            angle = math.atan2(p2.y - p1.y, p2.x - p1.x)
            circbp.append([angle, bprimes[p].name])
            print(f"{bprimes[p].name}: {p1} -> {p2}, angle: {angle}")

        # sort based on angle
        circp = sorted(circp, key=lambda p: p[0])
        circbp = sorted(circbp, key=lambda p: p[0])

        circ = []
        # make one list with prime bprime, prime bprime, ...
        for i in range(len(circp)):
            # append only names
            circ.append(circp[i][1])
            circ.append(circbp[i][1])

        circ.reverse()
        print("Circular list:", circ)
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
        vMap[k].incident = t.getIncident(vMap[k].pos, neMap)

    if not noChanges:
        # write vertex file
        content = ""
        content += "Vertex File\n"
        content += "#################################\n"
        content += "Name\tx\ty\tIncident\n"
        content += "#################################\n"
        for key, v in vMap.items():
            n = t.getValidName(v)
            xv = v.pos.x
            yv = v.pos.y
            inc = t.getValidName(v.incident)
            content += f"{n}\t{xv}\t{yv}\t{inc}\n"
        t.writeFile("ver", content, LAYERS)

    ''' '''
    # update face map
    visitedEdges = {}
    keys = neMap.keys()
    cycles = []
    ext_cycles = []
    int_cycles = []
    # array that will store the leftmost edge of each cycle at index 0
    extremes = []
    # init visited map (string, bool)
    for k in keys:
        visitedEdges[k] = False
    for k in keys:
        if visitedEdges[k]:
            continue
        cycle = []
        started = False
        edge = neMap[k]
        first = edge
        #print("cycle")
        while edge.name != first.name or not started:
            #print(edge)
            started = True
            cycle.append(edge)
            visitedEdges[edge.name] = True
            if edge.next == None:
                break
            edge = edge.next
        # leave the left-most vertex as first element of an aux array
        extreme = sorted(cycle, key=lambda edge: (edge.origin.pos.x), reverse=False)
        extreme = sorted(extreme, key=lambda edge: (edge.origin.pos.y), reverse=True)

        # use the left-most edge and its previous to do a cross product to determine type
        print("Extreme vertex:", extreme[0].origin, "Extreme Edge:", extreme[0], "Previous:", extreme[0].prev, "Next:", extreme[0].next, "For cycle:", cycle)
        a1 = extreme[0].origin.pos
        a2 = extreme[0].prev.origin.pos
        b1 = extreme[0].origin.pos
        b2 = extreme[0].next.origin.pos
        print(f"a: {a1} -> {a2} b: {b1} -> {b2}")

        a = Vector.toVector(a1, a2)
        b = Vector.toVector(b1, b2)

        # cycle's last element says its type: internal or external
        orientation = Vector.cross(a, b)
        print(f"{a} x {b} = {orientation}, a = {extreme[0].prev.name} b = {extreme[0].name}")
        if orientation >= 0:
            # angle between a and b is larger than 180: external cycle
            cycle.append("external")
            ext_cycles.append(cycle)
        if orientation < 0:
            # angle between a and b is smaller than 180: internal cycle
            cycle.append("internal")
            int_cycles.append(cycle)
        cycles.append(cycle)
        extremes.append(extreme[0]) # fetch its origin to get extreme vertex of ith cycle

    # internal cycles are always faces
    # external cycles may be united with others and form one face
    # we will represent the union graphs where cycles are vertices in a dict: keys are the vertices
    graph = {}
    for c in range(len(cycles)):
        if cycles[c][len(cycles[c]) - 1] == "external":
            # fill each key with an empty list that will be filled if that external cycle gets together with another
            graph[f"c{c}"] = []
    print("Graph:", graph)
    for c in range(len(cycles)):
        if cycles[c][len(cycles[c]) - 1] == "external":
            extEdge = extremes[c]
            horizontal = Line.points2Line(extEdge.origin.pos, Point(extEdge.origin.pos.x - 0.1, extEdge.origin.pos.y))
            # with the line, check every external cycle and each of its edges to see if there is an intersection
            for ec in ext_cycles:
                for edge in ec[:len(ec) - 1]:
                    tempLine = Line.points2Line(edge.origin.pos, edge.next.origin.pos)
                    hit = horizontal.intersects(tempLine)
                    # if the two lines intersect and the point is in left side of the extreme point of that cycle
                    if isinstance(hit, Point) and hit.x < extEdge.origin.pos.x:
                        # if hit point inside edge bounds
                        if hit.x >= edge.origin.pos.x and hit.x <= edge.next.origin.pos.x and hit.y >= edge.origin.pos.y and hit.y <= edge.next.origin.pos.y:
                            # connect it to the graph by appending the cycle index where that hitting edge is
                            idx = cycles.index(ext_cycles[ext_cycles.index(ec)])
                            print(f"Union -> Edge: {edge} in ext cycle: {ec} from ext cycles: {ext_cycles} at cycle index: {idx} from cycles array")
                            graph[f"c{c}"].append(f"c{idx}")

    print("Graph:", graph)
    efMap = {} # externals face map
    ifMap = {} # internals face map
    nfMap = {} # new face map
    f = 1
    # make sure non repeating cycle ids are in graph
    for cycleId, cList in graph.items():
        notRepeating = set(graph[cycleId])
        newList = list(notRepeating)
        graph[cycleId] = newList
        # if this cycle has a lits of cycles
        if len(newList) > 0:
            # check each of its cycles
            for c in newList:
                # if the graph value of these cycles has a list
                if len(graph[c]) > 0:
                    # append these and delete the cycle id
                    graph[cycleId] += graph[c]
                    idx = newList.index(c)
                    del graph[cycleId][idx]

    # make sure non repeating cycle ids are in graph
    # add external cycles graph result to faces map
    for cycleId, cList in graph.items():
        notRepeating = set(graph[cycleId])
        newList = list(notRepeating)
        graph[cycleId] = newList
        ifMap[f"f{f}"] = []
        ifMap[f"f{f}"].append(int(cycleId.replace("c", "")))
        for item in newList:
            ifMap[f"f{f}"].append(int(item.replace("c", "")))
        f += 1
    # add all internal cycles as faces
    for ic in int_cycles:
        efMap[f"f{f}"] = []
        efMap[f"f{f}"].append(cycles.index(ic))
        f += 1

    if not noChanges:
        # write face file
        content = ""
        content += "Face File\n"
        content += "#################################\n"
        content += "Name\tInternal\tExternal\n"
        content += "#################################\n"
        # fill external field
        for key, v in efMap.items():
            # cannot have lists
            idx = v[0] # cycle index
            firstEdge = cycles[idx][0] # first edge of a cycle
            n = firstEdge.name
            # new face map appending
            nfMap[key] = Face(key)
            nfMap[key].internal = None
            nfMap[key].external = firstEdge

            content += f"{key}\tNone\t{n}\n"
        # fill external field
        for key, v in ifMap.items():
            # can have lists
            n = ""
            # new face map appending
            nfMap[key] = Face(key)

            internals = 0
            if len(v) > 1:
                n += "["
                internals = []
                for item in range(len(v)):
                    idx = v[item] # cycle index
                    firstEdge = cycles[idx][0] # first edge of a cycle
                    if item < len(v) - 1:
                        n += firstEdge.name + ","
                    if item == len(v) - 1:
                        n += firstEdge.name + "]"
                    internals.append(firstEdge)
            else:
                idx = v[0]  # cycle index
                firstEdge = cycles[idx][0]  # first edge of a cycle
                n += firstEdge.name
                internals = firstEdge

            nfMap[key].internal = internals
            nfMap[key].external = None
            content += f"{key}\t{n}\tNone\n"
        t.writeFile("car", content, LAYERS)

    # now that nfMap is complete, update face field in Edges map
    for keyEdge, ne in neMap.items():
        faceKey = ""
        idxCycle = 0
        for c in cycles:
            cnames = [e.name for e in c[:-1]]
            if ne.name in cnames:
                idxCycle = cycles.index(c)
                break
        for keyFace, e_f in efMap.items():
            if idxCycle in efMap[keyFace]:
                faceKey = keyFace
                break
        for keyFace, i_f in ifMap.items():
            if idxCycle in ifMap[keyFace]:
                faceKey = keyFace
                break
        neMap[keyEdge].face = nfMap[faceKey]

    # write edge file
    if not noChanges:
        content = ""
        content += "Edge File\n"
        content += "#################################\n"
        content += "Name\tOrigin\tMate\tFace\tNext\tPrev\n"
        content += "#################################\n"
        for key, ne in neMap.items():
            n = t.getValidName(ne)
            o = t.getValidName(ne.origin)
            m = t.getValidName(ne.mate)
            fc = t.getValidName(ne.face)
            nx = t.getValidName(ne.next)
            pv = t.getValidName(ne.prev)
            content += f"{n}\t{o}\t{m}\t{fc}\t{nx}\t{pv}\n"
        t.writeFile("ari", content, LAYERS)

    print("Graph:", graph)
    print("Faces:", efMap, ifMap, nfMap)
    
    print("cycles", cycles)
    print("extremes", extremes)

    print(neMap)
    print(vMap)

    # PLOTTING
    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()

    figs = []
    pts = []
    colors = ['darkred', 'mediumblue', 'limegreen', 'deeppink', 'tomato', 'powderblue']
    markers = ['s', 'o', 'D', '>', 'X', '<']

    if noChanges:
        nfMap = fMap
        neMap = eMap

    for key in nfMap.keys():
        # check externals
        if nfMap[key].external != None:
            reqEdge = nfMap[key].external
            figs = analyzeFig(figs, reqEdge)
            # append at the end of a fig its label and type
            figs[-1].append(key)
            figs[-1].append("external")

        # check internals, list of figs inside
        if isinstance(nfMap[key].internal, list):
            internalEdges = nfMap[key].internal
            for i in range(len(internalEdges)):
                reqEdge = internalEdges[i]
                figs = analyzeFig(figs, reqEdge)
                # append at the end of a fig its label and type
                figs[-1].append(key)
                figs[-1].append("internal-list")

        # check internals, one fig inside
        if nfMap[key].internal != None and not isinstance(nfMap[key].internal, list):
            reqEdge = nfMap[key].internal
            figs = analyzeFig(figs, reqEdge, True)
            # append at the end of a fig its label and type
            figs[-1].append(key)
            figs[-1].append("internal-one")

    colorCont = 0
    listColor = False
    hatch = False
    for f in figs[:]:
        # all internal faces will be filled with a hatch pattern in the plot
        if f[-1] == "internal-one":
            hatch = True
        # if f is an internal face that is part of a list, keep the same color
        if f[-1] == "internal-list" and not listColor:
            listColor = True
            hatch = True
        if f[-1] != "internal-list" and listColor:
            listColor = False
            hatch = False
        fg = f[:-2]
        xp = [p[0] for p in fg]
        yp = [p[1] for p in fg]
        ax1.scatter(xp, yp, s=(50 * len(colors)) - 50 * colorCont, marker=markers[colorCont % len(colors)], zorder=5 * colorCont, color=colors[colorCont % len(colors)])
        p = Polygon(np.array(fg), facecolor=colors[colorCont % len(colors)], alpha=0.3, edgecolor=colors[colorCont % len(colors)], lw=(2 * len(colors)) - 1 * colorCont, label=f[-2])
        if hatch:
            p = Polygon(np.array(fg), facecolor='none', alpha=0.3, edgecolor=colors[colorCont % len(colors)], lw=4, label=f[-2])
            p.set_hatch('o')
        ax1.add_patch(p)
        if not listColor:
            colorCont += 1
    #plt.gca().axes.get_yaxis().set_visible(False)
    plt.legend(loc="lower center")
    plt.show()