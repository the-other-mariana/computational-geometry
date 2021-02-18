from glibrary import Point
from etree import *

etree = Q()
e1 = Event(Point(10, 5), 0, 0)
etree.insert(e1)
e2 = Event(Point(10, 6), 0, 1)
etree.insert(e2)
etree.insert(Event(Point(9, 3), 1, 0))
etree.insert(Event(Point(14, 1), 1, 1))
in_array = Q.inorder(etree.root)
print(in_array)
print(etree.root.value)
print(etree.root.left_child.value)
print(etree.root.right_child.value)
print(etree.root.right_child.right_child.value)
#etree.deleteValue(Point(14, 1))
#etree.deleteValue(Point(10, 5))
'''
etree.deleteNode(etree.root)
in_array = Q.inorder(etree.root)
print(in_array, etree.root.value)
'''
#node = etree.find(Point(10,6))
#print(node.value)
node = etree.find(Point(10, 5))
next = etree.getNextInorder(node)
print("next: ", next.value)
