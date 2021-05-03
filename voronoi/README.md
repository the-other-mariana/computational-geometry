# Voronoi Diagram

The last implementation of this couse will be the Voronoi Diagram of a given set of points. The return value is an image with said diagram.

## 1. Data Structures Needed

### 1.1 Priority Queue (Q)

This will be a queue of Event objects, where each Event is basically a Node. The value of an Event is a Point object, where all events in the Priority Queue will be ordered their value's Y coordinate, where the biggest Y needs to be the first and if there's an equal Y, we take the one with smallest X value. <br />

To implement this, we will use `heapq` built-in structure from Python. We will call it Q. <br />

There are two types of Events: 

- **Point (Place) Events** and circle events. Point events are basically each one of the given points the algorithm must visit. This is an event where there will be an addition in T, which represents when a new parabola is found and its added to the beach line. This type of object will store the point as its value.

- **Circle Events** are the ones where three points form a circle, and the lowest point of this circle is the circle event. This is an event where there will be a deletion from T, which represents that its parabola disappears from the beach line. This type of object will store the lowest point of the circle (circun-radius substracted in the center's Y coordinate) formed by three consecutive points as its value. Additionally to the point it will store:

    - Its center. Depends on h.
    - Its radius. Depends on h.
    - A pointer to the leaf in T this event represents

### 1.2 Beach Line (T)

This will be the Sweep Line that will travel from top to bottom, and we will call it T. This will be implemented as a Binary Search Tree, where the three can have two types of nodes:

- **Internal Node** is any node that is not a leaf. This will contain a value that will be a tuple of points (Left point, R point) that will represent the intersection of two parabolas defined by the point and the sweep line Y level. It will also hold a pointer to its edge in the diagram.

- **External Node** is any node that is a leaf in the tree, which means it does not have any child. This node will store a value of just one point, representing the parabola defined by that point and the known sweep line Y level. It will also hold a pointer to its circle event where it will disappear from the sweep line.

As a side note, you can define a parabola from a point (x1, y1) and a sweep line Y level, called d, with the following parametric formula: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/formula.png?raw=true) <br />

where x are all the posible x's of the domain and y is the range of the parabola, which together (x, y) form every point of said parabola. <br />

This is how the tree will represent the Beach Line: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/T-structure.png?raw=true) <br />

which, by looking at the tree traversals' theory,

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/tree-traversals.png?raw=true) <br />

we can say that the Beach Line order can be achieved by an inorder traversal of the tree T.

To search in the tree T, we need the sweep line Y level. The beach line structure, no matter h, will **remain the same** unless an event happens, no matter h. 

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/h-level.png?raw=true) <br />

But, for example, if we want to search for x = 5 in the tree T, we can have the following situation, where the structure does not change but **where to look for** does change.

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/search-x5.png?raw=true) <br />

Therefore, whenever we are searching in the tree T and we find an **intersection node** with the tuple (s1, s2), we will need a function that returns the X value of the point of intersection between the two parabolas with focus on s1 and s2 and directrix at h, where the sent params are f(s1, s2, h). Depending on that returned x, you will know if to move to the left (x=5 is smaller than that x) or to the right (x=5 is bigger than that x) when you look for x = 5.

## 2. Algorithm


### Main Function

1. Add to Q all the given points
2. For every height h of the Beach Line:
3. Check if there is an event in Q at height h
4. If there is an event:
5. Remove the firt event of Q. Do a Q pop basically and call it p
6. If the event is a place event: <br />
    -> *ActivatePlace(p)*
7. Else: it is a circle event: <br />
    -> *ActivateCircle(p)*
8. *Draw(T)*.
9. End for.

### ActivatePlace

1. If T is empty, then: <br />
   -> Add p as root of T <br />
   -> return
2. Else: <br />
3. Search in T the parabola arc (leaf), we call it a, that corresponds to p.x
4. If a points to a circle event: <br />
   -> Delete the pointed event from Q
5. End if.
6. Replace a with the subtree, <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/subtree.png?raw=true) <br />

where a and p are places or points

7. Insert new circle events with the generated arcs: <br />

    1. CircleEvent(left_neighbour(1.), 1., 2.), this means to find where does this circle event happens (lowest point of the circle). If there is no left neighbour, there will be no circle event.
    2. CircleEvent(2., 3., right_neighbour(3.)), same with this step. If there is no right neighbour, there will be no circle event.

8. Update pointers between T and Q, because each new leaf will point to a new circle event. In the previous step, this means that 7.1, if there's a circle event, leaf 1 will point to it and the circle event will point to leaf 1. In the same way, if there's a circle event in step 7.2, leaf 3 will point to it and the circle event will point to leaf 3.

### ActivateCircle

1. Obtain the parabola segment that is in between, which will disappear from T. This refers to the parabola that will disappear with the circle event. The circle event contains this pointer that points to the leaf of T, that we will call g. In this example, g points to p1 which is exactly the segment that will disappear from T when the directrix reaches that circle event height. <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/parabola-inbetween.png?raw=true) <br />

2. Delete g from T. When you erase g from T, you will also delete its two intersection parents, <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/erase-from-T.png?raw=true) <br />

and substitute all these erased nodes with one intersection: (p2, p3) which represents the first element of the parent intersection and the last element of the grandparent intersection. <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/substitute-T.png?raw=true) <br />

At last, hang the other son of the father, in this case p2, as the other son of this substitute intersection. When you finish this deletion, you have: <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/erased.png?raw=true) <br />

where the two sided lines represent the four links of father-son that you need to update. Note that there will be no cases where there is no grandparent, because these pseudo-circle-events where deleted in the previous function.

3. Delete all the circle events that involve the g arc (tree leaf). This means to erase from Q all the circle events where their pointer points to this leaf g. For that, you need to only check the event pointer of the previous and next leaf of g arc in T before the deletion, that is, check the circle event pointers of p2 as prev and p3 as next.

4. Mark the center of the circle as a **vertex** of the Voronoi diagram.

5. Check that the new triplet of consecutive arcs that formed in T as we removed g, converge in one new circle event and add it to Q. If this new circle opens upwards, it will not generate a true circle event.  If the circle opens downwards, you have a new circle event. To know this just check if the center of this circle is higher than the directrix (no event) or not (new event). Check this also with the 'center' parabola being the left and right neighbours from the new leaf generated from the deletion.

6. Update links between T and Q accordingly. This means that this new circle event points to its center parabola arc in T and this arc in T points to this circle event in Q.

### Draw

This function mainly draws the beach line T. As we have seen before, the inorder traversal of T is the beach line from left to right, with an example order below. <br />

![image](https://github.com/the-other-mariana/computational-geometry/blob/master/voronoi/res/draw.png?raw=true) <br />

With the parabolas' equations you will calculate the x's of the intersections in T.

Do not draw the parabolas' segments cumulatively, but do so with their intersections, because they will paint the edges of the Voronoi diagram.