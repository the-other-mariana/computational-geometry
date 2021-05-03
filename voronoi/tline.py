from glibrary import Line, Vector, Point, eps

class Node():
    def __init__(self, value, pointer=None):
        # internal: intersection of parabolas (L point, R point)
        # external: parabola (point)
        self.value = value
        # internal: pointer to its edge
        # external: pointer to its circle event where it will disappear, can be None
        self.pointer = pointer