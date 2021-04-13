from glibrary import Point, Line, Vector

class Vertex:
    def __init__(self, vname="", pos=Point()):
        self.name = vname
        self.pos = pos
        self.incident = None # edge

    def __repr__(self):
        return f"V[name:{self.name}, pos:{self.pos}]"

    def __str__(self):
        return "V[name:{n}, pos:{p}]".format(n=self.name, p=self.pos)

    def __eq__(self, other):
        if other == None:
            return False
        return self.pos == other.pos and self.incident == other.incident

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

    def __eq__(self, other):
        if other == None:
            return False
        return self.origin == other.origin and self.mate == other.mate and self.face == other.face and self.next == other.next and self.prev == other.prev

class Face:
    def __init__(self, fname=""):
        self.name = fname
        self.internal = None # edge
        self.external = None # edge

    def __repr__(self):
        return f"F[name:{self.name}]"

    def __str__(self):
        return "F[name:{n}]".format(n=self.name)

    def __eq__(self, other):
        if other == None:
            return False
        return self.internal == other.internal and self.external == other.internal