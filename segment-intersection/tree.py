class Node:
    def __init__(self, value=None):
        self.value = value
        self.left_child = None
        self.right_child = None

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
            else:
                self._insert(value, curr_node.left_child)
        elif value > curr_node.value:
            if curr_node.right_child == None:
                curr_node.right_child = Node(value)
            else:
                self._insert(value, curr_node.right_child)
        else:
            print("Value repeated.")

    def printBST(self):
        if self.root != None:
            self._printBST(self.root)

    def _printBST(self, curr_node):
        # in order traversal printing: all numbers sorted
        if curr_node != None:
            self._printBST(curr_node.left_child)
            print(curr_node.value)
            self._printBST(curr_node.right_child)
