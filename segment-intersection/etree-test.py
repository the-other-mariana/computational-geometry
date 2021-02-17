from glibrary import Point
from etree import *

etree = BST()
e1 = Event(Point(10, 5), 0, False)
etree.insert(e1)
e2 = Event(Point(10, 6), 0, True)
etree.insert(e2)
etree.insert(Event(Point(9, 3), 1, False))
etree.insert(Event(Point(14, 1), 1, True))
in_array = BST.inorder(etree.root)
print(in_array)
print(etree.root.value)
print(etree.root.left_child.value)
print(etree.root.right_child.value)
print(etree.root.right_child.right_child.value)
etree.deleteValue(Point(14, 1))
in_array = BST.inorder(etree.root)
print(in_array)
