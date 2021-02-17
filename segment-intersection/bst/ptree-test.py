from ptree import BST
from glibrary import Point, Vector, Line

ptree = BST()
ptree.insert(Point(10, 5))
ptree.insert(Point(10, 6))
ptree.insert(Point(9, 3))
in_array = BST.inorder(ptree.root)
print(in_array)
# balance p tree
bTreeRoot = BST.getBalancedBST(in_array, 0, len(in_array) - 1)
pre_array = BST.preorder(bTreeRoot)
print(pre_array)
myBalancedBST = BST()
myBalancedBST.root = bTreeRoot # now is saved as proper tree
print(myBalancedBST.root.value) # 10,5
print(myBalancedBST.root.left_child.value) # 10,6
print(myBalancedBST.root.right_child.value) # 9,3
