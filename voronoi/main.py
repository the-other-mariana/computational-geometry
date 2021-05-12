from queue import Event, Q
from tline import Node, T
from glibrary import Point, Line, Vector, eps
from matplotlib import pyplot as plt

# main code that runs the voronoi algorithm

STEPS = 100
gap = 5 # limits
q = Q()
t = T()


def activateCircle(p, h):
    if p.pointer:
        # this is the leaf in t that will disappear when h reaches the circle event height
        g = p.pointer
        if g.parent.parent:
            grandpa = g.parent.parent
            subtree_root = grandpa.parent
            parent = g.parent

            t.delete_node(g, h)
            t.delete_node(grandpa, h)

            new_node = Node([parent.value[0], grandpa.value[1]])

            # update links
            subtree_root.left_child = new_node
            new_node.parent = subtree_root
            new_node.left_child = parent.left_child
            new_node.left_child.parent = new_node
            new_node.right_child = grandpa.right_child
            new_node.right_child.parent = new_node

            

def activatePlace(p, h):
    if not t.root:
        t.root = Node([p.value])
        return
    else:
        a = t.find(p, h)
        if a.pointer:
            circle_event = a.pointer
            q.delete(circle_event)
        n1, n2, n3 = t.insert(p, h)
        if n1:
            left = t.getLeft(n1)
            cc, cr = Point.getCircumCenterRadius(left, n1, n2)
            # new circle event in q points to n1 in t
            new_event1 = Event(Point(cc.x, cc.y - cr), cc, cr, n1)
            # n1 in t points to event in q
            n1.pointer = new_event1
            q.push(new_event1)
        if n3:
            right = t.getRight(n3)
            cc, cr, = Point.getCircumCenterRadius(n2, n3, right)
            # new circle event in q points to n3 in t
            new_event2 = Event(Point(cc.x, cc.y - cr), cc, cr, n3)
            # n3 in t points to event in q
            n3.pointer = new_event2
            q.push(new_event2)
        return


def main():

    input = [Point(14, 0), Point(10, 10), Point(-3, 15), Point(4, 1), Point(-5, 6), Point(7, 18)]
    xs = [p.x for p in input]
    ys = [p.y for p in input]

    # get axis min and max
    xMin, xMax = min(input, key=lambda p: p.x).x, max(input, key=lambda p: p.x).x
    yMin, yMax = min(input, key=lambda p: p.y).y, max(input, key=lambda p: p.y).y

    # for plot
    fig = plt.figure()
    fig.add_subplot()
    ax1 = plt.gca()

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
    next = q.show()

    while h > (ylim[0] - gap):
        h -= dh
        # print("-> h:", h)
        if abs(h - next.value.y) < dh and not q.isEmpty():
            next = q.show()
            p = q.pop()
            print("Pop Event:", p)
            if not p.center:
                activatePlace(p, h)
            else:
                activateCircle(p, h)


    plt.show()

if __name__ == "__main__":
    main()
