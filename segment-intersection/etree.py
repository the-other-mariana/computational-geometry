""" Implementation of a Binary Tree that stores Events as values """
from glibrary import Point, Vector, Line
eps = 10**-4

class Event():
	def __init__(self, p=Point(), seg=0, pos=0):
		self.point = p
		self.seg = seg
		self.pos = pos

	def __repr__(self):
		if self == None:
			return "Null Event"
		return f"E[Point: ({self.point.x}, {self.point.y}) Seg: {self.seg} Pos: {self.pos}]"

	def __str__(self):
		if self == None:
			return "Null Event"
		return "E[Point: ({x}, {y}) Seg: {s} Pos: {i}]".format(x=self.point.x, y=self.point.y, s=self.seg, i=self.pos)

class Node:
	def __init__(self, value=Event()):
		self.value = value # now a event
		self.left_child = None
		self.right_child = None
		self.parent = None

class Q:
	def __init__(self):
		self.root = None

	@staticmethod
	def isLessThan(p1, p2):
		if p1.y > p2.y:
			return True
		if (abs(p1.y - p2.y) < eps) and (p1.x < p2.x):
			return True
		return False

	def insert(self, value):
		if self.root == None:
			self.root = Node(value)
		else:
			self._insert(value, self.root)

	def _insert(self, value, curr_node):
		if Q.isLessThan(value.point, curr_node.value.point):
			if curr_node.left_child == None:
				curr_node.left_child = Node(value)
				curr_node.left_child.parent = curr_node
			else:
				self._insert(value, curr_node.left_child)
		elif not Q.isLessThan(value.point, curr_node.value.point):
			if value.point ==  curr_node.value.point:
				r = 1
				#print("Value repeated:", value.point)
			if curr_node.right_child == None:
				curr_node.right_child = Node(value)
				curr_node.right_child.parent = curr_node
			else:
				self._insert(value, curr_node.right_child)


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

	def search(self, point):
		if self.root != None:
			return self._search(point, self.root)
		else:
			return False

	def _search(self, point, curr_node):
		if point == curr_node.value.point:
			return True
		elif Q.isLessThan(point, curr_node.value.point) and curr_node.left_child != None:
			return self._search(point, curr_node.left_child)
		elif not Q.isLessThan(point, curr_node.value.point) and curr_node.right_child != None:
			return self._search(point, curr_node.right_child)
		return False

	def find(self, point):
		if self.root != None:
			return self._find(point, self.root)
		else:
			return None

	def _find(self, point, curr_node):
		if point == curr_node.value.point:
			return curr_node
		elif Q.isLessThan(point, curr_node.value.point) and curr_node.left_child != None:
			return self._find(point, curr_node.left_child)
		elif not Q.isLessThan(point, curr_node.value.point) and curr_node.right_child != None:
			return self._find(point, curr_node.right_child)

	def deleteValue(self, point):
		return self.deleteNode(self.find(point))

	def deleteNode(self, node):
		if node == None or self.find(node.value.point) == None:
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

	def getFirst(self, node):
		if node.left_child != None:
			return self.getFirst(node.left_child)
		return node

	def printQ(self):
		if self.root != None:
			self._printQ(self.root)

	def _printQ(self, curr_node):
		# in order traversal printing: all numbers sorted
		if curr_node != None:
			self._printQ(curr_node.left_child)
			print(curr_node.value)
			self._printQ(curr_node.right_child)

	def isEmpty(self):
		if self.root == None:
			return True
		else:
			return False

	def getNext(self):
		n = []
		if self.root != None:
			Q._getNext(self.root, n)
		return n

	def _getNext(curr_node, n):
		if len(n) == 1:
			return
		if curr_node != None:
			Q._getNext(curr_node.left_child, n)
			n.append(curr_node.value)

	@staticmethod
	def inorder(root):
		a = []
		if root != None:
			Q._inorder(root, a)
		return a

	def _inorder(curr_node, array):
		if curr_node != None:
			Q._inorder(curr_node.left_child, array)
			array.append(curr_node.value)
			Q._inorder(curr_node.right_child, array)

	@staticmethod
	def preorder(root):
		a = []
		if root != None:
			Q._preorder(root, a)
		return a

	def _preorder(curr_node, array):
		if curr_node != None:
			array.append(curr_node.value)
			Q._preorder(curr_node.left_child, array)
			Q._preorder(curr_node.right_child, array)

	@staticmethod
	def getBalancedQ(array, start, end, parent=None):
		if start > end: return None
		mid = int((start + end) / 2)
		root = Node(array[mid])
		root.parent = parent
		root.left_child = Q.getBalancedQ(array, start, mid - 1, root)
		root.right_child = Q.getBalancedQ(array, mid + 1, end, root)

		return root
