""" Implementation of a Binary Tree that stores Segments as values """
from glibrary import Point, Vector, Line
eps = 10**-4

class Segment():
	def __init__(self, p1=Point(), p2=Point(), index=0):
		self.start = p1
		self.end = p2
		self.index = index

	def __repr__(self):
		return f"S[start:{self.start} end:{self.end} idx:{self.index}]"

	def __str__(self):
		return "S[start:{s} end:{e} index:{i}]".format(s=self.start, e=self.end, i=self.index)

	def __eq__(self, other):
		if not isinstance(other, type(self)): return NotImplemented
		return (self.start == other.start and self.end == other.end)

	def __hash__(self):
		return hash((self.start, self.end, self.index))


	def inBounds(self, p):
		tempsX = [self.start, self.end]
		tempsX = sorted(tempsX, key=lambda p: p.x, reverse=False)
		tempsY = [self.start, self.end]
		tempsY = sorted(tempsY, key=lambda p: p.y, reverse=False)
		# temps[0] = temp start

		if p.x <= tempsX[1].x and p.x >= tempsX[0].x and p.y <= tempsY[1].y and p.y >= tempsY[0].y:
			return True
		return False

	def isInSegment(self, p):
		if p == self.start: return 0
		if p == self.end: return 1

		sline = Line.points2Line(self.start, self.end)
		result = (sline.a * p.x) + (sline.b * p.y) + sline.c
		if abs(result) < eps:
			if self.inBounds(p):
				# point in middle of segment
				return 2
			else:
				# point in segment line but not in segment
				return -1
		else:
			return -1


class Node:
	def __init__(self, value=Segment(), hit=Point()):
		self.value = value # now a segment
		self.hit = hit # hit with T
		self.left_child = None
		self.right_child = None
		self.parent = None

	def __repr__(self):
		return f"N[start:{self.value}]"

	def __str__(self):
		return "N[start:{s}]".format(s=self.value)

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

	@staticmethod
	def getSegmentHit(s, p):
		t2 = Point(p.x + 1, p.y)
		tline = Line.points2Line(p, t2)
		hit = tline.intersects(Line.points2Line(s.start, s.end))
		return hit

	def findByPoint(self, p):
		U = []
		C = []
		L = []
		if self.root != None:
			self._findByPoint(p, U, C, L, self.root)
		return U, C, L

	def _findByPoint(self, p, U, C, L, curr_node):
		if curr_node != None:
			# if p in segment (0,1,2), node to solution and recursive on its subtree
			# if p not in subtree (-1), node not to sol and keep checking on the
			# side of the segment it was
			where = curr_node.value.isInSegment(p)
			if where == 0:
				# p = start case
				#U.append(curr_node.value)
				if curr_node.right_child != None:
					self._findByPoint(p, U, C, L, curr_node.right_child)
				if curr_node.left_child != None:
					self._findByPoint(p, U, C, L, curr_node.left_child)
			elif where == 1:
				# p = end case
				L.append(curr_node.value)
				if curr_node.right_child != None:
					self._findByPoint(p, U, C, L, curr_node.right_child)
				if curr_node.left_child != None:
					self._findByPoint(p, U, C, L, curr_node.left_child)
			elif where == 2:
				# p is in middle case
				C.append(curr_node.value)
				if curr_node.right_child != None:
					self._findByPoint(p, U, C, L, curr_node.right_child)
				if curr_node.left_child != None:
					self._findByPoint(p, U, C, L, curr_node.left_child)
			elif where == -1:
				# send recursion to the x side it is and node not to sol
				# 1. find out on which side of seg s point p is (horizontally)
				tempsX = [curr_node.value.start, curr_node.value.end]
				tempsX = sorted(tempsX, key=lambda p: p.x, reverse=False)
				start2end = Vector.toVector(tempsX[0], tempsX[1])
				start2p = Vector.toVector(tempsX[0], p)
				u = (Vector.dot(start2p, start2end)) / Vector.squareNorm(start2end)
				# 2. send recursion to the side subtree where p is
				if u < 0:
					# p is closest to start but outside seg (left tree)
					if curr_node.left_child != None:
						self._findByPoint(p, U, C, L, curr_node.left_child)
					else:
						self._findByPoint(p, U, C, L, curr_node.right_child)
				if u > 1:
					# p is closest to end but outside seg (right tree)
					if curr_node.right_child != None:
						self._findByPoint(p, U, C, L, curr_node.right_child)
					else:
						self._findByPoint(p, U, C, L, curr_node.left_child)
				if u > 0.0 and u < 1.0:
					if curr_node.right_child != None:
						self._findByPoint(p, U, C, L, curr_node.right_child)
					if curr_node.left_child != None:
						self._findByPoint(p, U, C, L, curr_node.left_child)


	def getLeftFromP(self, p, curr_node):
		while curr_node.right_child != None or curr_node.left_child != None:

			if p.x < curr_node.hit.x and curr_node.left_child != None:
				curr_node = curr_node.left_child
				continue
			if p.x >= curr_node.hit.x and curr_node.right_child != None:
				curr_node = curr_node.right_child
				continue
			if curr_node.left_child == None or curr_node.right_child == None:
				break
		return curr_node

	def getRightFromP(self, p, curr_node):
		answer = None
		while curr_node.right_child != None or curr_node.left_child != None:
			if p.x < curr_node.hit.x and curr_node.left_child != None:
				curr_node = curr_node.left_child
				answer = curr_node
				continue
			if p.x >= curr_node.hit.x and curr_node.right_child != None:
				curr_node = curr_node.right_child
				continue
			if curr_node.left_child == None or curr_node.right_child == None:
				break
		if answer != None: return answer
		else: return curr_node

	def insert(self, value, t1):
		if self.root == None:
			hit = T.getSegmentHit(value, t1)
			self.root = Node(value, hit)
		else:
			self._insert(value, self.root, t1)

	def _insert(self, value, curr_node, t1):
		if T.isLessThan(value, curr_node.value, t1):
			if curr_node.left_child == None:
				hit = T.getSegmentHit(value, t1)
				curr_node.left_child = Node(value, hit)
				curr_node.left_child.parent = curr_node
			else:
				self._insert(value, curr_node.left_child, t1)
		elif not T.isLessThan(value, curr_node.value, t1):
			if curr_node.right_child == None:
				hit = T.getSegmentHit(value, t1)
				curr_node.right_child = Node(value, hit)
				curr_node.right_child.parent = curr_node
			else:
				self._insert(value, curr_node.right_child, t1)
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

	def search(self, segment, t1):
		if self.root != None:
			return self._search(segment, self.root, t1)
		else:
			return False

	def _search(self, segment, curr_node, t1):
		if segment == curr_node.value:
			return True
		elif T.isLessThan(segment, curr_node.value, t1) and curr_node.left_child != None:
			return self._search(segment, curr_node.left_child, t1)
		elif not T.isLessThan(segment, curr_node.value, t1) and curr_node.right_child != None:
			return self._search(segment, curr_node.right_child, t1)
		return False

	def find(self, segment, t1):
		if self.root != None:
			return self._find(segment, self.root, t1)
		else:
			return None

	def _find(self, segment, curr_node, t1):
		if segment == curr_node.value:
			return curr_node
		elif T.isLessThan(segment, curr_node.value, t1) and curr_node.left_child != None:
			return self._find(segment, curr_node.left_child, t1)
		elif not T.isLessThan(segment, curr_node.value, t1) and curr_node.right_child != None:
			return self._find(segment, curr_node.right_child, t1)

	def deleteValue(self, segment, t1):
		return self.deleteNode(self.find(segment, t1), t1)

	def deleteNode(self, node, t1):
		if node == None or self.find(node.value, t1) == None:
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
			self.deleteNode(successor, t1)

	def findMax(self, node):
		while node.right_child != None:
			node = node.right_child
		return node

	# iterative function to find predecessor
	def getPredecessor(self, root, s, p):
		sNode = self.find(s, p)
		predecessor = None

		if (root == None):
			return None
		while (True):
			# if key is less than root  traverse the left tree
			if (sNode.hit.x < root.hit.x):
				root = root.left_child
			# if key is greater than root  traverse the right tree
			elif (sNode.hit.x > root.hit.x):
				# set the predecessor to root
				predecessor = root
				root = root.right_child
			# if any node has the same value as key,the predecessor is the max value
			# or rightmost value of its left subtree
			else:
				if root.left_child != None:
					predecessor = self.findMax(root.left_child)
				break
			if root == None:
				return None
		return predecessor

	def findMin(self, node):
		while node.left_child != None:
			node = node.left_child
		return node

	def getSuccessor(self, root, s, p):
		sNode = self.find(s, p)
		successor = None
		# Base condition
		if root == None:
			return None
		while (True):
			# if key is less than root  traverse the left  subtree
			if (sNode.hit.x < root.hit.x):
				# the current node(root) is set to the successor
				successor = root
				root = root.left_child
			# if key is greater than root  traverse the right subtree
			elif (sNode.hit.x > root.hit.x):
				root = root.right_child
			# if any node has the same data  value as key , the successor is the min value
			# or leftmost value of its right subtree

			else:
				if (root.right_child):
					successor = self.findMin(root.right_child)
				break
			if (root == None):
				return None
		return successor

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
