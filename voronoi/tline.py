""" Implementation of a Binary Search Tree that stores internal/external nodes as values """
from glibrary import Line, Vector, Point, eps
import math

class Node():
    def __init__(self, value, pointer=None):
        # internal: intersection of parabolas [L point, R point]
        # external: parabola [point]
        self.value = value
        # external: pointer to its circle event where it will disappear, can be None # ask teacher
        self.pointer = pointer
        self.left_child = None
        self.right_child = None
        self.parent = None

    def __eq__(self, other):
        if not other:
            return False
        for i in range(len(self.value)):
            if self.value[i] != other.value[i]:
                return False
        return True

    def __repr__(self):
        return f"N[value:{self.value} pointer:{self.pointer}]"

    def __str__(self):
        return "N[value:{v} pointer:{p}]".format(v=self.value, p=self.pointer)

    def isLeaf(self):
        if not self: return False
        return self.right_child == None and self.left_child == None

    def isRoot(self):
        return self.parent == None

    def isRightChild(self):
        if not self.parent: return False
        if self.parent.right_child == self:
            return True
        else:
            return False

    def isLeftChild(self):
        if not self.parent: return False
        if self.parent.left_child == self:
            return True
        else:
            return False

class T():
    def __init__(self):
        self.root = None

    @staticmethod
    def getParabolaCoeff(f, d):
        a = 1.0 / (2 * (f.y - d))
        b = (-1.0 * 2 * f.x) / (2 * (f.y - d))
        c = ((f.x * f.x) + (f.y * f.y) - (d * d)) / (2.0 * (f.y - d))
        return a, b, c

    @staticmethod
    def findIntersect(a1, b1, c1, a2, b2, c2, f1, f2):
        a = a1 - a2
        b = b1 - b2
        c = c1 - c2

        inner_calc = b ** 2 - 4 * a * c

        # Check if `inner_cal` is negative. If so, there are no real solutions.
        # Thus, return the empty list.
        if inner_calc < 0:
            return None

        square = math.sqrt(inner_calc)
        double_a = 2 * a
        answers = [(-b - square) / double_a, (-b + square) / double_a]

        if f1.x <= f2.x:
            # points ordered from left to right, which means hit point from f1,f2 is the first element
            return answers[1]

        return answers[0]

    @staticmethod
    def isLessThan(xVal, inode, h):
        p1 = inode.value[0]
        p2 = inode.value[1]
        a1, b1, c1 = T.getParabolaCoeff(p1, h)
        a2, b2, c2 = T.getParabolaCoeff(p2, h)
        xHit = T.findIntersect(a1, b2, c1, a2, b2, c2, p1, p2)
        if xHit:
            if xVal <= xHit:
                return True
            return False
        else:
            return False

    def insert(self, p, h):
        if self.root == None:
            self.root = Node([p.value])
            return [None, self.root, None]
        else:
            return self._insert(p, self.root, None, h)

    def _insert(self, p, curr_node, parent, h):
        # if you found a leaf (only one value)
        if len(curr_node.value) == 1:
            a = curr_node
            # replace node with subtree
            # curr_node = Node([a.value[0], p.value])
            curr_node.value = [a.value[0], p.value]
            curr_node.parent = parent

            curr_node.left_child = Node([a.value[0]]) # ext
            curr_node.left_child.parent = curr_node
            curr_node.right_child = Node([p.value, a.value[0]])
            curr_node.right_child.parent = curr_node

            curr_node.right_child.left_child = Node([p.value]) # ext
            curr_node.right_child.left_child.parent = curr_node.right_child
            curr_node.right_child.right_child = Node([a.value[0]]) # ext
            curr_node.right_child.right_child.parent = curr_node.right_child

            print([curr_node.left_child, curr_node.right_child.left_child, curr_node.right_child.right_child])
            return [curr_node.left_child, curr_node.right_child.left_child, curr_node.right_child.right_child]

        # else it must be a 2 value node, keep searching
        elif T.isLessThan(p.value.x, curr_node, h) and curr_node.left_child != None:
            return self._insert(p, curr_node.left_child, curr_node, h)
        elif not T.isLessThan(p.value.x, curr_node, h) and curr_node.right_child != None:
            return self._insert(p, curr_node.right_child, curr_node, h)

    def getLeft(self, node):
        if node.isRoot():
            return None
        elif node.parent.isRoot() and node.isLeftChild():
            return None
        else:
            if node.parent.right_child == node and node.parent.left_child and node.parent.left_child.isLeaf():
                node = node.parent.left_child
                while node.right_child:
                    node = node.right_child
                if node.isLeaf():
                    return node
                else:
                    while node.right_child or node.left_child:
                        if node.right_child:
                            node = node.right_child
                            continue
                        if node.left_child:
                            node.left_child
                            continue
                    return node
            if node.parent.left_child == node or not node.parent.left_child:
                node = node.parent
                if node.isRoot(): return None
                while node.parent.left_child:
                    if node.parent and node.parent.left_child == node:
                        node = node.parent
                    if node.parent and node.parent.left_child and node.parent.left_child != node:
                        node = node.parent
                        break
                    if node.isRoot():
                        return None
                node = node.left_child
                while node.right_child:
                    node = node.right_child
                if node.isLeaf():
                    return node
                else:
                    while node.left_child:
                        node = node.left_child
                    return node

    def getRight(self, node):
        if node.isRoot():
            return None
        elif node.parent.isRoot() and node.isRightChild():
            return None
        else:
            if node.parent.left_child == node and node.parent.right_child:
                node = node.parent.right_child
                while node.left_child:
                    node = node.left_child
                if node.isLeaf():
                    return node
                else:
                    while node.right_child or node.left_child:
                        if node.left_child:
                            node = node.left_child
                            continue
                        if node.right_child:
                            node.right_child
                            continue
                    return node
            if node.parent.right_child == node or not node.parent.right_child:
                node = node.parent
                if node.isRoot(): return None
                while node.parent.right_child:
                    if node.parent and node.parent.right_child == node:
                        node = node.parent
                    if node.parent and node.parent.right_child and node.parent.right_child != node:
                        node = node.parent
                        break
                    if node.isRoot():
                        return None
                node = node.right_child
                while node.left_child:
                    node = node.left_child
                if node.isLeaf():
                    return node
                else:
                    while node.right_child:
                        node = node.right_child
                    return node

    def getRightSubtree(self, node):
        while node.parent and node.parent.right_child == node:
            node = node.parent
        node = node.parent.right_child
        if not node.isLeaf():
            return node
        return None

    def getLeftSubtree(self, node):
        while node.parent and node.parent.left_child == node:
            node = node.parent
        node = node.parent.left_child
        if not node.isLeaf():
            return node
        return None

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
        elif T.isLessThan(x, curr_node, h) and curr_node.left_child:
            return self._find(x, curr_node.left_child, h)
        elif not T.isLessThan(x, curr_node, h) and curr_node.right_child:
            return self._find(x, curr_node.right_child, h)

    def delete_value(self, p, h):
        return self.delete_node(self.find(p, h), h)

    def delete_node(self, node, h):

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
            self.delete_node(successor, h)

    def printT(self):
        if self.root != None:
            self._printT(self.root)

    def _printT(self, curr_node):
        # in order traversal printing: all numbers sorted
        if curr_node != None:
            self._printT(curr_node.left_child)
            print(curr_node)
            self._printT(curr_node.right_child)

    @staticmethod
    def inorder(root):
        a = []
        if root != None:
            T._inorder(root, a)
        return a

    def _inorder(curr_node, array):
        if curr_node != None:
            T._inorder(curr_node.left_child, array)
            array.append(curr_node.value)
            T._inorder(curr_node.right_child, array)