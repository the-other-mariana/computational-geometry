from pqueue import Event, Q
from tline import Node, T
from glibrary import Point, Line, Vector, eps
from matplotlib import pyplot as plt

# main code that runs the voronoi algorithm

STEPS = 100
gap = 5 # limits
q = Q()
t = T()
voronoi = []

fig = plt.figure()
fig.add_subplot()
ax1 = plt.gca()

def plotEdges(tree, h, hits):
    for n in tree:
        if len(n) > 1:
            a1, b1, c1 = T.getParabolaCoeff(n[0], h)
            a2, b2, c2 = T.getParabolaCoeff(n[1], h)
            hitx = T.findIntersect(a1, b1, c1, a2, b2, c2, n[0], n[1])
            if hitx:
                hits.append([hitx, a1 * hitx * hitx + b1 * hitx + c1])
    return hits


def checkCircleEvent(l, c, r, h):
    cc, cr = Point.getCircumCenterRadius(l.value[0], c.value[0], r.value[0])
    if cc.y <= h:
        # new circle event
        low_point = Point(cc.x, cc.y - cr)
        e = Event(low_point, cc, cr, c)
        c.pointer = e
        return e
    else:
        return None

def activateCircle(p, h):
    global t
    global q
    global voronoi
    if p.pointer:
        # this is the leaf in t that will disappear when h reaches the circle event height
        g = p.pointer
        if g.parent.parent:
            grandpa = g.parent.parent
            subtree_root = grandpa.parent
            parent = g.parent

            first = parent.value[0]
            sec = grandpa.value[1]
            if first == sec:
                first, sec = grandpa.value[0], parent.value[1]
            new_node = Node([first, sec])

            bro = t.getLeft(g)
            subtree = t.getRightSubtree(g)
            if g.isRightChild():
                bro = t.getRight(g)
                subtree = t.getLeftSubtree(g)
            t.delete_node(g, h)
            isLeft = True
            if grandpa.isRightChild():
                isLeft = False
            t.delete_node(grandpa, h)

            # update links
            if isLeft:
                subtree_root.left_child = new_node
            else:
                subtree_root.right_child = new_node

            new_node.parent = subtree_root
            new_node.left_child = bro
            if new_node.left_child:
                new_node.left_child.parent = new_node
            # new_node.right_child = grandpa.right_child # bug here, get root of right subtree
            # new_node.right_child = right_subtree
            if subtree:
                subtree.value[1] = new_node.value[0]
                if subtree.right_child:
                    subtree.right_child.value[0] = subtree.value[1]

                new_node.right_child = subtree
                if new_node.right_child:
                    new_node.right_child.parent = new_node

            prev, next = None, None
            if new_node.left_child:
                prev = new_node.left_child
            if new_node.right_child and new_node.right_child.left_child:
                next = new_node.right_child.left_child

            if prev and prev.pointer == g:
                q.delete(prev)
            if next and next.pointer == g:
                q.delete(next)
            # q.delete(p)
            # mark the center of the circle as a vertex of the voronoi
            voronoi.append(p.center)

            ncenter = new_node.left_child
            if not ncenter.isLeaf():
                ncenter = new_node.right_child
            nleft = t.getLeft(ncenter)
            nright = t.getRight(ncenter)
            if nleft and ncenter and nright:
                e = checkCircleEvent(nleft, ncenter, nright, h)
                if e:
                    q.push(e)
                leftleft = t.getLeft(nleft)
                if leftleft:
                    # e = checkCircleEvent(leftleft, nleft, nright, h)
                    e = checkCircleEvent(leftleft, nleft, ncenter, h)
                    if e:
                        q.push(e)
                rightright = t.getRight(nright)
                if rightright:
                    # e = checkCircleEvent(nleft, nright, rightright, h)
                    e = checkCircleEvent(ncenter, nright, rightright, h)
                    if e:
                        q.push(e)

def activatePlace(p, h):
    global t
    global q
    if not t.root:
        t.root = Node([p.value])
        return
    else:
        a = t.find(p, h)
        if a.pointer:
            circle_event = a.pointer
            q.delete(circle_event)
        nodes = t.insert(p, h)
        print(nodes)

        n1 = nodes[0]
        n2 = nodes[1]
        n3 = nodes[2]
        if n1:
            left = t.getLeft(n1)
            if left:
                cc, cr = Point.getCircumCenterRadius(left.value[0], n1.value[0], n2.value[0])
                # new circle event in q points to n1 in t
                new_event1 = Event(Point(cc.x, cc.y - cr), cc, cr, n1)
                # n1 in t points to event in q
                n1.pointer = new_event1
                q.push(new_event1)
        if n3:
            right = t.getRight(n3)
            if right:
                cc, cr, = Point.getCircumCenterRadius(n2.value[0], n3.value[0], right.value[0])
                # new circle event in q points to n3 in t
                new_event2 = Event(Point(cc.x, cc.y - cr), cc, cr, n3)
                # n3 in t points to event in q
                n3.pointer = new_event2
                q.push(new_event2)
        return


def main():
    global t
    global q
    global ax1

    #input = [Point(14, 0), Point(10, 10), Point(-3, 15), Point(4, 1), Point(-5, 6), Point(7, 18)]
    #input = [Point(10, 10), Point(-3, 15), Point(4, 1)]
    input = [Point(14, 0), Point(10, 10), Point(-3, 15), Point(4, 1)]
    #input = [Point(14, 0), Point(10, 10), Point(-3, 15), Point(4, 1), Point(20, 7)]
    #input = [Point(14, 0), Point(10, 10), Point(-3, 15), Point(4, 1), Point(-5, 6)]
    xs = [p.x for p in input]
    ys = [p.y for p in input]

    # get axis min and max
    xMin, xMax = min(input, key=lambda p: p.x).x, max(input, key=lambda p: p.x).x
    yMin, yMax = min(input, key=lambda p: p.y).y, max(input, key=lambda p: p.y).y

    # for plot
    ax1.scatter(xs, ys, s=30, zorder=10, color='tab:blue')
    plt.setp(ax1, xlim=(xMin - gap, xMax + gap), ylim=(yMin - gap, yMax + gap))

    for p in input:
        e = Event(p)
        q.push(e)

    xlim = ax1.get_xlim()
    ylim = ax1.get_ylim()

    height = abs((ylim[1] + gap) - (ylim[0] - gap))
    dh = (height * 1.0) / STEPS
    h = ylim[1] + gap
    #next = q.show()
    hits = []

    while h > (ylim[0] - gap):
        # print("-> h:", h)
        if not q.isEmpty():
            next = q.show()
        if abs(h - next.value.y) < dh and not q.isEmpty():
            p = q.pop()

            # print("Pop Event:", p, "height:", h, "dh:", dh, "next:", next)
            if not p.center:
                activatePlace(p, h)
            else:
                activateCircle(p, h)

        tree = T.inorder(t.root)
        # print(tree)
        hits = plotEdges(tree, h, hits)

        h -= dh

    print(q.isEmpty())
    print(len(q.data))
    #p = q.pop()
    voronoi_x = [p.x for p in voronoi]
    voronoi_y = [p.y for p in voronoi]
    print(voronoi)
    ax1.scatter(voronoi_x, voronoi_y, s=30, zorder=10, color='red')
    for hit in hits:
        ax1.scatter([hit[0]], [hit[1]], s=5, zorder=5, color='black')

    plt.show()

if __name__ == "__main__":
    main()