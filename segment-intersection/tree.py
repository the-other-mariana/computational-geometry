eps = 10**-4

class Node:
    def __init__(self, value=None):
        self.value = value
        self.left_child = None
        self.right_child = None
        self.parent = None

class BST:
    def __init__(self):
        self.root = None

    def insert(self, value):
        if self.root == None:
            self.root = Node(value)
        else:
            self._insert(value, self.root)

    def _insert(self, value, curr_node):
        if value < curr_node.value:
            if curr_node.left_child == None:
                curr_node.left_child = Node(value)
                curr_node.left_child.parent = curr_node
            else:
                self._insert(value, curr_node.left_child)
        elif value > curr_node.value:
            if curr_node.right_child == None:
                curr_node.right_child = Node(value)
                curr_node.right_child.parent = curr_node
            else:
                self._insert(value, curr_node.right_child)
        else:
            print("Value repeated.")

    def height(self):
        if self.root != None:
            return self._height(self.root, 0)
        else:
            return 0

    def _height(self, curr_node, curr_height):
        if curr_node == None: return curr_height
        left_height = self._height(curr_node.left_child, curr_height + 1)
        right_height = self._height(curr_node.right_child, curr_height + 1)
        return max(left_height, right_height)

    def search(self, value):
        if self.root != None:
            return self._search(value, self.root)
        else:
            return False

    def _search(self, value, curr_node):
        if abs(value - curr_node.value) < eps:
            return True
        elif value < curr_node.value and curr_node.left_child != None:
            return self._search(value, curr_node.left_child)
        elif value > curr_node.value and curr_node.right_child != None:
            return self._search(value, curr_node.right_child)
        return False

    def find(self, value):
        if self.root != None:
            return self._find(value, self.root)
        else:
            return None
    def _find(self, value, curr_node):
        if abs(value - curr_node.value) < eps:
            return curr_node
        elif value < curr_node.value and curr_node.left_child != None:
            return self._find(value, curr_node.left_child)
        elif value > curr_node.value and curr_node.right_child != None:
            return self._find(value, curr_node.right_child)

    def delete_value(self, value):
        return self.delete_node(self.find(value))

    def delete_node(self, node):
        def min_value_node(n):
            current = n
            while current.left_child != None:
                current = current.left_child
            return current

        def num_children(n):
            num_children = 0
            if n.left_child != None: num_children += 1
            if n.right_child != None: num_children += 1
            return num_children

        # get the parent of the node to be deleted
        node_parent = node.parent
        # get the number of children of the node to be deleted
        node_children = num_children(node)

        # case 1: (node has no children)
        if node_children == 0:
            if node_parent.left_child == node:
                node_parent.left_child = None
            else:
                node_parent.right_child = None
        # case 2: (node has a single child)
        if node_children == 1:
            if node.left_child != None:
                child = node.left_child
            else:
                child = node.right_child

            # replace the node to be deleted with its child
            if node_parent.left_child == node:
                node_parent.left_child = child
            else:
                node_parent.right_child = child
            child.parent = node_parent

        # case 3: (node has 2 children)
        if node_children == 2:
            # get the inorder successor of the deleted node
            successor = min_value_node(node.right_child)
            # copy this successor value to the node to be deleted
            node.value = successor
            # delete the successor now that value is copied
            self.delete_node(successor)


    def printBST(self):
        if self.root != None:
            self._printBST(self.root)

    def _printBST(self, curr_node):
        # in order traversal printing: all numbers sorted
        if curr_node != None:
            self._printBST(curr_node.left_child)
            print(curr_node.value)
            self._printBST(curr_node.right_child)
