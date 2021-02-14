from tree import BST
tree = BST()
tree.insert(5)
tree.insert(4)
tree.insert(6)
tree.insert(10)
tree.insert(9)
tree.insert(11)

#tree.find(5)
tree.delete_value(5)
tree.printBST()
in_array = BST.inorder(tree.root)
print(in_array)

tree2 = BST()
tree2.insert(10)
tree2.insert(8)
tree2.insert(7)
tree2.insert(6)
tree2.insert(5)

in_array = BST.inorder(tree2.root)
print(in_array)
bTreeRoot = BST.getBalancedBST(in_array, 0, len(in_array) - 1)
pre_array = BST.preorder(bTreeRoot)
print(pre_array)
print(bTreeRoot.value) # 7
myBalancedBST = BST()
myBalancedBST.root = bTreeRoot # now is saved as proper tree
