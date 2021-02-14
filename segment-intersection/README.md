# Segment Intersection Algorithm
## Data Structures Needed

### 1. Binary Search Tree

Code: [tree.py](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/tree.py)

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

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/res/tree-example.png?raw=true) <br />

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
![image](https://github.com/the-other-mariana/computational-geometry/blob/master/segment-intersection/res/tree-deleted.png?raw=true) <br />

*Note: the printBST() function prints an inorder traversed tree, so if we see the values in order, our tree works fine.*

## Handy Links

[BST Basics](https://www.youtube.com/watch?v=Zaf8EOVa72I)
