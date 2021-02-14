from ptree import BST
from glibrary import Point, Vector, Line

ptree = BST()
ptree.insert(Point(10, 5))
ptree.insert(Point(10, 6))
ptree.insert(Point(9, 3))
in_array = BST.inorder(ptree.root)
print(in_array)
