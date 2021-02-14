# Segment Intersection Algorithm
## Data Structures Needed

### 1. Binary Search Tree

Code: [tree.py](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/tree.py)

Test script: [test.py](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/test.py)

### 1.1 Simple BST

A binary search tree is a data structure that groups nodes. The first node inserted becomes the root, and then the next value inserted will be added in the left (if the value is smaller that the root/parent node) or in the right (if the value is smaller that the root/parent node) child node of the node that is a leaf (no children). <br />

Using the code, an example tree would be the following:
```python
>>> from tree import BST
>>> tree = BST()
>>> tree.insert(5)
>>> tree.insert(4)
>>> tree.insert(6)
>>> tree.insert(10)
>>> tree.insert(9)
>>> tree.insert(11)
>>> tree.printBST()
4
5
6
9
10
11
```
Which gives us the following tree: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/res/tree-insert-example.png?raw=true) <br />

If, for example, we delete the root node as below: <br />
```python
>>> tree.delete_value(5)
>>> tree.printBST()
4
6
9
10
11
```
Giving us the following tree now: <br/>
![image](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/res/tree-delete-example.png?raw=true) <br />

*Note: the printBST() function prints an inorder traversed tree, so if we see the values in order, our tree works fine.*

### 1.2 Balanced BST

Using this idea, if we simply create the following: <br />
```python
>>> from tree import BST
>>> tree2 = BST()
>>> tree2.insert(10)
>>> tree2.insert(8)
>>> tree2.insert(7)
>>> tree2.insert(6)
>>> tree2.insert(5)
>>> in_array = BST.inorder(tree2.root)
[5, 6, 7, 8, 10] # same output as printBST(), inorder
```
We have this tree: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/res/unbalanced.png?raw=true) <br />

Which, in theory is **unbalanced**: a balanced BST is one where their left and right subtree differ in height by at most 1. In the above tree, the left subtree has height is 4 and the right subtree has height 0. To balance it, we do the following: <br />

```python
>>> bTreeRoot = BST.getBalancedBST(in_array, 0, len(in_array) - 1)
>>> pre_array = BST.preorder(bTreeRoot)
[7, 5, 6, 8, 10] # preorder
```

And now we have a balanced BST.

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/res/balanced.png?raw=true) <br />

### 1.3 Point Binary Search Tree

Code: [ptree.py](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/ptree.py)

Test script: [ptree-test.py](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/ptree-test.py)

Now we changed the basic data structure to store Point objects instead of simple numbers. BST uses **comparisons** which we need to override so that the three stores left and right values following the rule below. <br />

----

## **(p1 < p2) ->  if p1.y > p2.y or if p1.y == p2.y and p1.x < p2.x**

----

Now if we test it as follows: <br />

```python
>>> from ptree import BST
>>> from glibrary import Point, Vector, Line
>>> ptree = BST()
>>> ptree.insert(Point(10, 5))
>>> ptree.insert(Point(10, 6))
>>> ptree.insert(Point(9, 3))
>>> in_array = BST.inorder(ptree.root)
>>> print(in_array)
[(10, 6), (10, 5), (9, 3)] # now 'sorted' order means bigger y's in front
```
Which gives us the tree below.<br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/res/ptree.png?raw=true) <br />

## Handy Links

[BST Basics](https://www.youtube.com/watch?v=Zaf8EOVa72I) <br />
[BST Balanced](https://www.youtube.com/watch?v=VCTP81Ij-EM) <br />
[BST to balanced](https://www.geeksforgeeks.org/convert-normal-bst-balanced-bst/)
