""" Implementation of a Binary Tree that stores Events as values """
from glibrary import Point, Vector, Line
eps = 10**-4

class Segment():
	def __init__(self, p1=Point(), p2=Point()):
		self.start = p1
        self.end = p2

	def __repr__(self):
		if self == None:
			return "Null Segment"
		return f"S[start:{self.p1} end:{self.p2}]"

	def __str__(self):
		if self == None:
			return "Null Event"
		return "E[start: {s} end: {e}]".format(s=self.p1, e=self.p2)
    def __eq__(self, other):
        return (self.start == other.start and self.end == other.end)

class Node:
	def __init__(self, value=Segment()):
		self.value = value # now a segment
		self.left_child = None
		self.right_child = None
		self.parent = None

class T:
	def __init__(self):
		self.root = None

	@staticmethod
    # returns whether s1 < s2
	def isLessThan(s1, s2, t1):
		t2 = Point(t1.x + 1, t1.y)
        tline = Line.points2Line(t1, t2)
        hit1 = tline.intersects(Line.points2Line(s1.start, s1.end))
        hit2 = tline.intersects(Line.points2Line(s2.start, s2.end))
        if hit1.x < hit2.x:
            return True
        else:
            return False


	def insert(self, value):
		if self.root == None:
			self.root = Node(value)
		else:
			self._insert(value, self.root)

	def _insert(self, value, curr_node):
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

	def search(self, segment):
		if self.root != None:
			return self._search(segment, self.root)
		else:
			return False

	def _search(self, segment, curr_node):
		if segment == curr_node.value:
			return True
		elif T.isLessThan(segment, curr_node.value) and curr_node.left_child != None:
			return self._search(segment, curr_node.left_child)
		elif not T.isLessThan(segment, curr_node.value) and curr_node.right_child != None:
			return self._search(segment, curr_node.right_child)
		return False

	def find(self, segment):
		if self.root != None:
			return self._find(segment, self.root)
		else:
			return None

	def _find(self, segment, curr_node):
		if segment == curr_node.value:
			return curr_node
		elif T.isLessThan(segment, curr_node.value) and curr_node.left_child != None:
			return self._find(segment, curr_node.left_child)
		elif not T.isLessThan(segment, curr_node.value) and curr_node.right_child != None:
			return self._find(segment, curr_node.right_child)

	def deleteValue(self, segment):
		return self.deleteNode(self.find(segment))

	def deleteNode(self, node):
		if node == None or self.find(node.value) == None:
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
			self.deleteNode(successor)

	def getFirstRightParent(self, node):
		if node.parent == None:
			return None
		while node.parent != None and node.parent.left_child != node:
			node = node.parent
		return node.parent

	def getLeftMostRightChild(self, node):
		# get left-most node from the right sub tree
		if node.right_child != None:
			node = node.right_child
		while node.left_child != None:
			node = node.left_child
		return node

	def getNextInorder(self, node):
		if node.right_child != None:
			return self.getLeftMostRightChild(node)
		else:
			return self.getFirstRightParent(node)

	def printT(self):
		if self.root != None:
			self._printT(self.root)

	def _printT(self, curr_node):
		# in order traversal printing: all numbers sorted
		if curr_node != None:
			self._printT(curr_node.left_child)
			print(curr_node.value)
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

	@staticmethod
	def preorder(root):
		a = []
		if root != None:
			T._preorder(root, a)
		return a

	def _preorder(curr_node, array):
		if curr_node != None:
			array.append(curr_node.value)
			T._preorder(curr_node.left_child, array)
			T._preorder(curr_node.right_child, array)

	@staticmethod
	def getBalancedT(array, start, end, parent=None):
		if start > end: return None
		mid = int((start + end) / 2)
		root = Node(array[mid])
		root.parent = parent
		root.left_child = T.getBalancedT(array, start, mid - 1, root)
		root.right_child = T.getBalancedT(array, mid + 1, end, root)

		return root
