""" Implementation of a Binary Tree that stores internal/external nodes as values """
from glibrary import Line, Vector, Point, eps
import math

class Node():
    def __init__(self, value, pointer=None):
        # internal: intersection of parabolas (L point, R point)
        # external: parabola (point)
        self.value = value
        # internal: pointer to its edge
        # external: pointer to its circle event where it will disappear, can be None
        self.pointer = pointer

        self.left_child = None
        self.right_child = None
        self.parent = None

class T():
    def __init__(self):
        self.root = None

    @staticmethod
    def getParabolaCoeff(f, d):
        a = 1.0 / (2 * (f.y - d))
        b = (-1 * 2 * f.x) / (2 *(f.y - d))
        c = ((f.x * f.x) + (f.y * f.y) - (d * d)) / (2 * (f.y - d))
        return a, b, c

    @staticmethod
    def findIntersect(a1, b1, c1, a2, b2, c2):
        a = a1 - a2
        b = b1 - b2
        c = c1 - c2

        inner_calc = b ** 2 - 4 * a * c

        # Check if `inner_cal` is negative. If so, there are no real solutions.
        # Thus, return the empty set.
        if inner_calc < 0:
            return set()

        square = math.sqrt(inner_calc)
        double_a = 2 * a
        answers = [(-b + square) / double_a, (-b - square) / double_a]

        # Using `set()` removes any possible duplicates.
        return set(answers)

    @staticmethod
    def isLessThan(xVal, inode, h):
        p1 = inode[0]
        p2 = inode[1]
        a1, b1, c1 = T.getParabolaCoeff(p1, h)
        a2, b2, c2 = T.getParabolaCoeff(p2, h)
        xResult = T.findIntersect(a1, b2, c1, a2, b2, c2)
        xResult = list(xResult)
        x = min(xResult)
        if xVal <= x:
            return True
        return False
    '''
    @staticmethod
    def isLessThan(p1, p2):
        if p1.y > p2.y:
            return True
        if (abs(p1.y - p2.y) < eps) and (p1.x < p2.x):
            return True
        return False
    '''

    def insert(self, p, h):
        if self.root == None:
            self.root = Node([p.value])
        else:
            self._insert(p, self.root, h)

    def _insert(self, p, curr_node, h):
        '''
        if T.isLessThan(value, curr_node.value):
            if curr_node.left_child == None:
                curr_node.left_child = Node(value)
                curr_node.left_child.parent = curr_node
            else:
                self._insert(value, curr_node.left_child)
        elif not T.isLessThan(value, curr_node.value):
            if curr_node.right_child == None:
                curr_node.right_child = Node(value)
                curr_node.right_child.parent = curr_node
            else:
                self._insert(value, curr_node.right_child)
        else:
            print("Value repeated.")
        '''
        # if you found a leaf (only one value)
        if len(curr_node.value) == 1:
            a = curr_node
            # replace node with subtree
            curr_node = Node([a.value, p.value])

            curr_node.left_child = Node([a.value])
            curr_node.left_child.parent = curr_node
            curr_node.right_child = Node([p.value, a.value])
            curr_node.right_child.parent = curr_node

            curr_node.right_child.left_child = Node([p.value])
            curr_node.right_child.left_child.parent = curr_node.right_child
            curr_node.right_child.right_child = Node([a.value])
            curr_node.right_child.right_child.parent = curr_node.right_child

        # else it must be a 2 value node, keep searching
        elif T.isLessThan(p.value.x, curr_node, h) and curr_node.left_child != None:
            self._find(p, curr_node.left_child, h)
        elif not T.isLessThan(p.value.x, curr_node, h) and curr_node.right_child != None:
            self._find(p.value.x, curr_node.right_child, h)

    def find(self, p, h):
        if self.root != None:
            return self._find(p.value.x, self.root, h)
        else:
            return None

    def _find(self, x, curr_node, h):
        if curr_node == None:
            return None
        # if you found a leaf (only one value)
        if len(curr_node.value) == 1:
            return curr_node
        # else it must be a 2 value node
        elif T.isLessThan(x, curr_node, h) and curr_node.left_child != None:
            return self._find(x, curr_node.left_child, h)
        elif not T.isLessThan(x, curr_node, h) and curr_node.right_child != None:
            return self._find(x, curr_node.right_child, h)

    def delete_value(self, p, h):
        return self.delete_node(self.find(p, h))

    def delete_node(self, node, p):
        if node == None or self.find(node.value, p) == None:
            print("Node is not found to delete")
            return None

        # returns the node with min value in tree rooted at input node
        def min_value_node(n):
            current = n
            while current.left_child != None:
                current = current.left_child
            return current

        # returns the number of children for the given node
        def num_children(n):
            num_children = 0
            if n.left_child != None: num_children += 1
            if n.right_child != None: num_children += 1
            return num_children

        node_parent = node.parent
        # get the number of children of the node to be deleted
        node_children = num_children(node)

        # CASE 1 (node has no children)
        if node_children == 0:
            if node_parent != None:
                if node_parent.left_child == node:
                    node_parent.left_child = None
                else:
                    node_parent.right_child = None
            else:
                self.root = None

        # CASE 2 (node has a single child)
        if node_children == 1:
            if node.left_child != None:
                child = node.left_child
            else:
                child = node.right_child
            if node_parent != None:
                # replace the node to be deleted with its child
                if node_parent.left_child == node:
                    node_parent.left_child = child
                else:
                    node_parent.right_child = child
            else:
                self.root = child

            # correct the parent pointer in node
            child.parent = node_parent

        # CASE 3 (node has two children)
        if node_children == 2:
            # get the inorder successor of the deleted node
            successor = min_value_node(node.right_child)
            node.value = successor.value
            # delete the inorder successor now that value is saved
            self.delete_node(successor)